#!/usr/bin/env python3
"""
patch_final_polish.py
=====================
Refactors scorePlant() into a transparent 2-stage sub-score system.
Updates getNextBestPlants() to use identical evaluation logic.

Sub-scores:
  gapScore          fills missing foundational role
  diversityScore    adds new family
  structureScore    adds missing layer
  goalScore         aligns with goal targetRoles + food_role
  riskScore         low shared pest overlap
  redundancyPenalty duplicates saturated roles
  nichePenalty      specialty / support-heavy in production guild
"""
from pathlib import Path
import re

f = Path("src/pages/guild-checker.astro")
text = f.read_text()
changes = 0

# ── 1. Replace scorePlant() ────────────────────────────────────────────────────
score_start = text.find("// ── Scoring function")
score_end   = text.find("  // ── Helper: pick best plant", score_start)

if score_start < 0 or score_end < 0:
    print("❌ 1: scorePlant boundaries not found")
else:
    NEW_SCORE = """// ── Scoring weights (tune here to adjust relative importance) ────────────────
  const W = {
    gap:        3.0,   // filling a missing foundational role is highest priority
    diversity:  1.5,   // new family reduces shared vulnerability
    structure:  1.2,   // missing layer adds vertical diversity
    goal:       2.5,   // goal alignment drives identity of the guild
    risk:       1.0,   // pest separation is a moderate positive
    redundancy: 1.5,   // stacking covered roles wastes a slot
    niche:      2.0,   // low-fit plants should lose decisively
  };

  // ── scorePlant: 2-stage evaluation ────────────────────────────────────────
  // Stage 1 (eligibility) is handled by callers via continue/filter.
  // Stage 2 (scoring) produces a named sub-score breakdown.
  function scorePlant(p, currentSlugs) {
    const fns    = p.plant_function || [];
    const family = plantToFamily[p.slug] || null;
    const pests  = plantToPests[p.slug] || new Set();

    // ── Build guild state snapshot ────────────────────────────────────────
    const existingFamilies = new Set(currentSlugs.map(s => plantToFamily[s]).filter(Boolean));
    const guildLayers      = new Set(currentSlugs.map(s => inferLayer(plantBySlug[s] || {})));
    const roleCounts       = {};
    const guildPests       = new Set();
    for (const s of currentSlugs) {
      const pp = plantBySlug[s];
      if (!pp) continue;
      for (const fn of (pp.plant_function || [])) roleCounts[fn] = (roleCounts[fn] || 0) + 1;
      for (const pest of (plantToPests[s] || new Set())) guildPests.add(pest);
    }

    // ── gapScore: reward filling a missing foundational role ──────────────
    const FOUNDATIONAL = ['Nitrogen Fixer','Pollinator','Pest Management',
                          'Ground Cover','Mulcher','Dynamic Accumulator'];
    let gapScore = 0;
    for (const fn of fns) {
      if (FOUNDATIONAL.includes(fn) && !roleCounts[fn])      gapScore += 1.0;
      else if (FOUNDATIONAL.includes(fn) && roleCounts[fn] === 1) gapScore += 0.4;
    }

    // ── diversityScore: reward adding a new plant family ─────────────────
    const famCount = currentSlugs.filter(s => plantToFamily[s] === family).length;
    let diversityScore = 0;
    if (family && !existingFamilies.has(family)) diversityScore =  1.0;
    else if (famCount === 1)                      diversityScore = -0.3;
    else if (famCount >= 2)                       diversityScore = -1.0;

    // ── structureScore: reward adding a missing growth layer ──────────────
    const myLayer = inferLayer(p);
    const STRUCT  = ['canopy','shrub','ground','vine','root'];
    let structureScore = 0;
    if (STRUCT.includes(myLayer) && !guildLayers.has(myLayer)) {
      structureScore = 1.0;
    } else if (guildLayers.has(myLayer)) {
      const lc = currentSlugs.filter(s => inferLayer(plantBySlug[s]||{}) === myLayer).length;
      structureScore = Math.max(-1.0, lc * -0.3);
    }

    // ── goalScore: reward alignment with selected goal ────────────────────
    let goalScore = 0;
    for (const fn of fns) {
      if (profile.targetRoles.includes(fn))
        goalScore += (goalKey === 'food_production' && fn === 'Edible') ? 1.5 : 1.0;
      if (profile.avoidOverweight.includes(fn) && !profile.targetRoles.includes(fn))
        goalScore -= 0.5;
    }
    if (goalKey === 'food_production') {
      if (p.food_role === 'anchor')       goalScore += 2.0;
      else if (p.food_role === 'support') goalScore += 0.5;
    }

    // ── riskScore: reward low shared pest overlap ─────────────────────────
    let sharedPests = 0;
    for (const pest of pests) { if (guildPests.has(pest)) sharedPests++; }
    const riskScore = Math.max(-1.0, 1.0 - sharedPests * 0.35);

    // ── redundancyPenalty: penalise stacking already-covered roles ────────
    const SUPP_ROLES = new Set(['Ground Cover','Mulcher','Dynamic Accumulator','Erosion Control']);
    let redundancyPenalty = 0;
    for (const fn of fns) {
      const rc = roleCounts[fn] || 0;
      if (rc >= 3)                          redundancyPenalty += 0.5;
      else if (rc >= 2 && SUPP_ROLES.has(fn)) redundancyPenalty += 0.3;
    }
    if (goalKey === 'low_maintenance') {
      const SAT = ['Ground Cover','Pollinator','Pest Management'];
      for (const fn of fns) {
        if (SAT.includes(fn) && (roleCounts[fn]||0) >= 2 &&
            family && existingFamilies.has(family)) redundancyPenalty += 0.5;
      }
    }

    // ── nichePenalty: penalise low-fit plants in production guilds ────────
    let nichePenalty = 0;
    if (goalKey === 'food_production') {
      const FP_SUPP = ['Ground Cover','Mulcher','Dynamic Accumulator','Erosion Control','Pest Management'];
      const supportCount = FP_SUPP.filter(r => fns.includes(r)).length;
      if (fns.includes('Edible')) {
        if (supportCount >= 3)      nichePenalty += 1.5;
        else if (supportCount >= 2) nichePenalty += 0.75;
        else if (supportCount <= 1) nichePenalty -= 0.5; // clean edible bonus
      }
      if (FOOD_PRODUCTION_EXCLUDE.includes(p.slug)) nichePenalty += 3.0;
      if (p.food_role === 'specialty') nichePenalty += 1.5;
    }

    // ── Final weighted score ──────────────────────────────────────────────
    return (
      gapScore        * W.gap        +
      diversityScore  * W.diversity  +
      structureScore  * W.structure  +
      goalScore       * W.goal       +
      riskScore       * W.risk       -
      redundancyPenalty * W.redundancy -
      nichePenalty    * W.niche
    );
  }

"""
    text = text[:score_start] + NEW_SCORE + text[score_end:]
    changes += 1
    print("✅ 1: scorePlant() replaced with 2-stage sub-score system")

# ── 2. Update getNextBestPlants scoring to use same sub-score logic ────────────
# Find the parallel scoring block in getNextBestPlants
fn_start = text.find("function getNextBestPlants")
role_score_idx = text.find("    let roleScore", fn_start)
if role_score_idx < 0:
    role_score_idx = text.find("    // ── Score", fn_start)

# Find where explanations start (end of scoring block)
expl_idx = text.find("    // ── Context-aware explanation builder", fn_start)
if expl_idx < 0:
    expl_idx = text.find("    const pestReasons", fn_start)

if role_score_idx > 0 and expl_idx > 0 and role_score_idx < expl_idx:
    old_scoring_block = text[role_score_idx:expl_idx]
    new_scoring_block = """    // ── Sub-score evaluation (mirrors scorePlant logic for consistency) ────
    // Gap: fills missing foundational role
    const FOUND_ROLES = ['Nitrogen Fixer','Pollinator','Pest Management',
                          'Ground Cover','Mulcher','Dynamic Accumulator'];
    const curRoleCounts = {};
    for (const s of currentSlugs) {
      for (const fn of (plantBySlug[s]?.plant_function || []))
        curRoleCounts[fn] = (curRoleCounts[fn] || 0) + 1;
    }
    let gapScore = 0;
    let hasMissing = false;
    for (const fn of fns) {
      if (FOUND_ROLES.includes(fn) && !curRoleCounts[fn])     { gapScore += 3.0; hasMissing = true; }
      else if (FOUND_ROLES.includes(fn) && curRoleCounts[fn] === 1) { gapScore += 1.2; }
    }

    // Diversity: new family
    const existFamilies = new Set(currentSlugs.map(s => plantToFamily[s]).filter(Boolean));
    const famRepeat = currentSlugs.filter(s => plantToFamily[s] === family).length;
    let diversityScore = family && !existFamilies.has(family) ? 2.25
                       : famRepeat >= 2 ? -1.5 : famRepeat === 1 ? -0.45 : 0;
    const hasNewFamily = family && !existFamilies.has(family);

    // Structure: missing layer
    const existLayers = new Set(currentSlugs.map(s => inferLayer(plantBySlug[s] || {})));
    const myLayer = inferLayer(p);
    const STRUCT_LAYERS = ['canopy','shrub','ground','vine','root'];
    let structureScore = 0;
    if (STRUCT_LAYERS.includes(myLayer) && !existLayers.has(myLayer)) structureScore = 1.2;
    else if (existLayers.has(myLayer)) {
      const lc = currentSlugs.filter(s => inferLayer(plantBySlug[s]||{}) === myLayer).length;
      structureScore = Math.max(-1.2, lc * -0.3);
    }

    // Risk: shared pest overlap
    const guildPestSet = new Set();
    for (const s of currentSlugs) {
      for (const pest of (plantToPests[s] || new Set())) guildPestSet.add(pest);
    }
    let sharedPestCount = 0;
    for (const pest of pests) { if (guildPestSet.has(pest)) sharedPestCount++; }
    const riskScore = Math.max(-1.0, 1.0 - sharedPestCount * 0.35);

    // Redundancy penalty
    let redundancyPenalty = 0;
    const SUPP_S = new Set(['Ground Cover','Mulcher','Dynamic Accumulator','Erosion Control']);
    for (const fn of fns) {
      const rc = curRoleCounts[fn] || 0;
      if (rc >= 3) redundancyPenalty += 0.75;
      else if (rc >= 2 && SUPP_S.has(fn)) redundancyPenalty += 0.45;
    }

    // Diminishing returns across candidates already queued
    const diminishingPenalty = candidates.filter(c =>
      (hasMissing && c._hasMissing) || (hasNewFamily && c._hasNewFamily)
    ).length * 0.5;

    const score = gapScore + diversityScore + structureScore + riskScore
                - redundancyPenalty - diminishingPenalty;

"""
    text = text[:role_score_idx] + new_scoring_block + text[expl_idx:]
    changes += 1
    print("✅ 2: getNextBestPlants scoring updated to match sub-score system")
else:
    print(f"❌ 2: scoring block not found in getNextBestPlants (role_score={role_score_idx}, expl={expl_idx})")

# ── 3. Update signature comment ───────────────────────────────────────────────
old_comment = "// ── Next Best Plant scorer (inlined from src/lib/nextPlant.js) ──────────────"
new_comment  = "// ── Next Best Plant scorer — uses same sub-score logic as generator ──────────"
if old_comment in text:
    text = text.replace(old_comment, new_comment)
    changes += 1
    print("✅ 3: comment updated")

f.write_text(text)
print(f"\n{changes} patches applied")
