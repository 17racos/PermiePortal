#!/usr/bin/env python3
"""
patch_phase4.py  (reused name — function-stack scoring refactor)
================================================================
Refactors both scorePlant() and getNextBestPlants() scoring to
prioritize function stacking over missing-role gap-filling.

New score shape:
  totalScore =
    functionStackScore   ← PRIMARY: how much ecological work does this plant do?
    + missingRoleBonus   ← SECONDARY: bonus if it fills a gap, not a gate
    + diversityBonus     ← reward new family
    + structureBonus     ← reward missing layer
    + goalBonus          ← goal alignment + food_role signal
    - redundancyPenalty  ← shallow redundancy (same family/layer/role profile)
    - riskPenalty        ← shared pest overlap
    - nichePenalty       ← low-fit plants in specific goal contexts
"""
from pathlib import Path

f = Path("src/pages/guild-checker.astro")
text = f.read_text()
changes = 0

# ── 1. Replace scorePlant weights + scoring body ─────────────────────────────
score_start = text.find("// ── Scoring weights")
score_end   = text.find("  // ── Helper: pick best plant", score_start)

if score_start < 0 or score_end < 0:
    print("❌ 1: scorePlant boundaries not found")
else:
    NEW_SCORE = """// ── Ecological role definitions ──────────────────────────────────────────────
  const FOUNDATIONAL_ROLES = ['Nitrogen Fixer','Pollinator','Pest Management',
                               'Ground Cover','Mulcher','Dynamic Accumulator'];
  const PRODUCTIVE_ROLES   = ['Edible','Fiber','Fuel','Medicinal'];
  const STRUCTURAL_ROLES   = ['Windbreaker','Shade Provider','Erosion Control',
                               'Wildlife Attractor','Water Purification'];
  const ALL_VALUED_ROLES   = [...FOUNDATIONAL_ROLES, ...PRODUCTIVE_ROLES,
                               ...STRUCTURAL_ROLES];

  // ── functionStackScore helper ─────────────────────────────────────────────
  // Core idea: reward plants that do many useful things, not just one.
  // Uses diminishing returns so multi-function plants win, but not absurdly.
  function calcFunctionStackScore(fns) {
    let count = 0;
    for (const fn of fns) {
      if (ALL_VALUED_ROLES.includes(fn)) count++;
    }
    // Diminishing returns: each additional function worth less
    // 1 fn → 1.0,  2 → 1.8,  3 → 2.4,  4 → 2.8,  5+ → 3.0 (capped)
    if (count === 0) return 0;
    let score = 0;
    for (let i = 0; i < count; i++) score += 1.0 * Math.pow(0.7, i);
    return Math.min(3.0, score);
  }

  // ── scorePlant: function-stack-first evaluation ───────────────────────────
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

    // ── functionStackScore (PRIMARY) ─────────────────────────────────────
    // How much ecological work does this plant do?
    // Multi-function plants score higher with diminishing returns.
    const functionStackScore = calcFunctionStackScore(fns);

    // ── missingRoleBonus (SECONDARY — bonus not gate) ────────────────────
    // Extra credit for filling a foundational gap, but single-role plants
    // still need to compete against high-stack plants on total value.
    let missingRoleBonus = 0;
    for (const fn of fns) {
      if (FOUNDATIONAL_ROLES.includes(fn) && !roleCounts[fn])      missingRoleBonus += 1.0;
      else if (FOUNDATIONAL_ROLES.includes(fn) && roleCounts[fn] === 1) missingRoleBonus += 0.4;
    }

    // ── diversityBonus: reward adding a new plant family ─────────────────
    const famCount = currentSlugs.filter(s => plantToFamily[s] === family).length;
    let diversityBonus = 0;
    if (family && !existingFamilies.has(family)) diversityBonus =  1.2;
    else if (famCount === 1)                      diversityBonus = -0.3;
    else if (famCount >= 2)                       diversityBonus = -1.2;

    // ── structureBonus: reward adding a missing growth layer ─────────────
    const myLayer = inferLayer(p);
    const STRUCT  = ['canopy','shrub','ground','vine','root'];
    let structureBonus = 0;
    if (STRUCT.includes(myLayer) && !guildLayers.has(myLayer)) {
      structureBonus = 1.0;
    } else if (guildLayers.has(myLayer)) {
      const lc = currentSlugs.filter(s => inferLayer(plantBySlug[s]||{}) === myLayer).length;
      structureBonus = Math.max(-0.8, lc * -0.25);
    }

    // ── goalBonus: reward alignment with selected goal ────────────────────
    let goalBonus = 0;
    for (const fn of fns) {
      if (profile.targetRoles.includes(fn))
        goalBonus += (goalKey === 'food_production' && fn === 'Edible') ? 1.2 : 0.8;
      if (profile.avoidOverweight.includes(fn) && !profile.targetRoles.includes(fn))
        goalBonus -= 0.4;
    }
    if (goalKey === 'food_production') {
      if (p.food_role === 'anchor')       goalBonus += 1.5;
      else if (p.food_role === 'support') goalBonus += 0.4;
    }

    // ── riskPenalty: penalise shared pest overlap ─────────────────────────
    let sharedPests = 0;
    for (const pest of pests) { if (guildPests.has(pest)) sharedPests++; }
    const riskPenalty = Math.min(2.0, sharedPests * 0.3);

    // ── redundancyPenalty: penalise SHALLOW redundancy only ───────────────
    // Penalise same family + same dominant role (not just same role).
    // Intentional multi-function overlap is allowed.
    let redundancyPenalty = 0;
    const famAlreadyIn = existingFamilies.has(family);
    const myLayer2 = inferLayer(p);
    const layerAlreadyIn = guildLayers.has(myLayer2);
    // Count how many of my functions are already well covered (3+)
    const saturatedFns = fns.filter(fn => (roleCounts[fn] || 0) >= 3).length;
    if (famAlreadyIn && layerAlreadyIn && saturatedFns >= 2) redundancyPenalty += 1.5;
    else if (famAlreadyIn && saturatedFns >= 3)              redundancyPenalty += 1.0;
    else if (saturatedFns >= 3)                              redundancyPenalty += 0.5;
    // Low Maintenance: stronger de-stacking of already-maxed roles
    if (goalKey === 'low_maintenance') {
      const SAT = ['Ground Cover','Pollinator','Pest Management'];
      for (const fn of fns) {
        if (SAT.includes(fn) && (roleCounts[fn]||0) >= 2 && famAlreadyIn)
          redundancyPenalty += 0.4;
      }
    }

    // ── nichePenalty: penalise low-fit plants ────────────────────────────
    let nichePenalty = 0;
    if (goalKey === 'food_production') {
      const FP_SUPP = ['Ground Cover','Mulcher','Dynamic Accumulator',
                       'Erosion Control','Pest Management'];
      const supportCount = FP_SUPP.filter(r => fns.includes(r)).length;
      if (fns.includes('Edible')) {
        if (supportCount >= 3)      nichePenalty += 1.2;
        else if (supportCount >= 2) nichePenalty += 0.6;
        else if (supportCount <= 1) nichePenalty -= 0.4; // clean edible gets bonus
      }
      if (FOOD_PRODUCTION_EXCLUDE.includes(p.slug)) nichePenalty += 3.0;
      if (p.food_role === 'specialty') nichePenalty += 1.2;
    }

    // ── Final score ───────────────────────────────────────────────────────
    // functionStackScore drives ranking; bonuses and penalties refine it.
    return functionStackScore
         + missingRoleBonus
         + diversityBonus
         + structureBonus
         + goalBonus
         - riskPenalty
         - redundancyPenalty
         - nichePenalty;
  }

"""
    text = text[:score_start] + NEW_SCORE + text[score_end:]
    changes += 1
    print("✅ 1: scorePlant() refactored to function-stack-first")

# ── 2. Replace getNextBestPlants scoring block ────────────────────────────────
fn_start    = text.find("function getNextBestPlants")
score_start = text.find("    // Zone fit", fn_start)
score_end   = text.find("    // hasMissing and hasNewFamily", fn_start)

if score_start < 0 or score_end < 0:
    print(f"❌ 2: getNextBestPlants scoring boundaries not found (start={score_start} end={score_end})")
else:
    NEW_GNB_SCORE = """    // Zone fit (already filtered above, but need var for badge/explanation)
    const zoneFit = getZoneFit(p, userZone);

    // ── Function stack score (PRIMARY) ────────────────────────────────────
    // Multi-function plants rank higher; diminishing returns prevent dominance
    const fnStackScore = calcFunctionStackScore(fns);

    // ── Missing role bonus (SECONDARY — bonus not gate) ───────────────────
    const FOUND_ROLES = ['Nitrogen Fixer','Pollinator','Pest Management',
                          'Ground Cover','Mulcher','Dynamic Accumulator'];
    const curRoleCounts = {};
    for (const s of currentSlugs) {
      for (const fn of (plantBySlug[s]?.plant_function || []))
        curRoleCounts[fn] = (curRoleCounts[fn] || 0) + 1;
    }
    let missingRoleBonus = 0;
    let hasMissing = false;
    for (const fn of fns) {
      if (FOUND_ROLES.includes(fn) && !curRoleCounts[fn])     { missingRoleBonus += 1.5; hasMissing = true; }
      else if (FOUND_ROLES.includes(fn) && curRoleCounts[fn] === 1) { missingRoleBonus += 0.6; }
    }

    // ── Diversity bonus: new family ───────────────────────────────────────
    const existFamilies = new Set(currentSlugs.map(s => plantToFamily[s]).filter(Boolean));
    const famRepeat = currentSlugs.filter(s => plantToFamily[s] === family).length;
    let diversityBonus = family && !existFamilies.has(family) ? 1.8
                       : famRepeat >= 2 ? -1.2 : famRepeat === 1 ? -0.35 : 0;
    const hasNewFamily = family && !existFamilies.has(family);

    // ── Structure bonus: missing layer ────────────────────────────────────
    const existLayers = new Set(currentSlugs.map(s => inferLayer(plantBySlug[s] || {})));
    const myLayer = inferLayer(p);
    const STRUCT_LAYERS = ['canopy','shrub','ground','vine','root'];
    let structureBonus = 0;
    if (STRUCT_LAYERS.includes(myLayer) && !existLayers.has(myLayer)) structureBonus = 1.0;
    else if (existLayers.has(myLayer)) {
      const lc = currentSlugs.filter(s => inferLayer(plantBySlug[s]||{}) === myLayer).length;
      structureBonus = Math.max(-0.8, lc * -0.25);
    }

    // ── Risk penalty: shared pest overlap ────────────────────────────────
    const guildPestSet = new Set();
    for (const s of currentSlugs) {
      for (const pest of (plantToPests[s] || new Set())) guildPestSet.add(pest);
    }
    let sharedPestCount = 0;
    for (const pest of pests) { if (guildPestSet.has(pest)) sharedPestCount++; }
    const riskPenalty = Math.min(2.0, sharedPestCount * 0.3);

    // ── Redundancy penalty: shallow redundancy only ───────────────────────
    const famAlreadyIn = existFamilies.has(family);
    const layerAlreadyIn = existLayers.has(myLayer);
    const saturatedFns = fns.filter(fn => (curRoleCounts[fn] || 0) >= 3).length;
    let redundancyPenalty = 0;
    if (famAlreadyIn && layerAlreadyIn && saturatedFns >= 2) redundancyPenalty = 1.5;
    else if (famAlreadyIn && saturatedFns >= 3)              redundancyPenalty = 1.0;
    else if (saturatedFns >= 3)                              redundancyPenalty = 0.5;

    // ── Diminishing returns across already-queued candidates ─────────────
    const diminishingPenalty = candidates.filter(c =>
      (hasMissing && c._hasMissing) || (hasNewFamily && c._hasNewFamily)
    ).length * 0.4;

    const score = fnStackScore + missingRoleBonus + diversityBonus
                + structureBonus - riskPenalty - redundancyPenalty - diminishingPenalty;

"""
    text = text[:score_start] + NEW_GNB_SCORE + text[score_end:]
    changes += 1
    print("✅ 2: getNextBestPlants scoring refactored to function-stack-first")

f.write_text(text)
print(f"\n{changes} patches applied")
