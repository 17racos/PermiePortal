#!/usr/bin/env python3
"""
patch_phase4_2.py — Function-Stack Scoring Refactor
====================================================
Adds calcFunctionStackScore() as an outer-scope helper,
then updates scorePlant() and getNextBestPlants() scoring
to prioritize multi-function plants over single-gap fillers.

All replacements are exact string matches — no position surgery.
"""
from pathlib import Path

f = Path("src/pages/guild-checker.astro")
text = f.read_text()
changes = 0

def patch(old, new, label):
    global text, changes
    if old in text:
        text = text.replace(old, new, 1)
        changes += 1
        print(f"✅ {label}")
    else:
        print(f"❌ {label}")

# ── 1. Insert role constants + helper before SUPPORT_ROLES ───────────────────
patch(
    "// Support roles subject to soft cap\nconst SUPPORT_ROLES =",
    """// ── Ecological role sets for function-stack scoring ─────────────────────────
const ECOLOGICAL_ROLES_VALUED = [
  'Nitrogen Fixer','Pollinator','Pest Management',
  'Ground Cover','Mulcher','Dynamic Accumulator',
  'Edible','Fiber','Fuel','Medicinal',
  'Windbreaker','Shade Provider','Erosion Control',
  'Wildlife Attractor','Water Purification',
];

// calcFunctionStackScore: primary ranking driver
// 1 fn→1.0, 2→1.7, 3→2.2, 4→2.6, 5+→3.0 (capped, diminishing returns)
function calcFunctionStackScore(fns) {
  let score = 0, count = 0;
  for (const fn of (fns || [])) {
    if (ECOLOGICAL_ROLES_VALUED.includes(fn)) {
      score += 1.0 * Math.pow(0.7, count++);
    }
  }
  return Math.min(3.0, score);
}

// Support roles subject to soft cap
const SUPPORT_ROLES =""",
    "1: role constants + calcFunctionStackScore added"
)

# ── 2. Replace scorePlant body ────────────────────────────────────────────────
OLD_SCORE = """  // ── Scoring function ───────────────────────────────────────────────────────
  //
  // Sub-scores (each named and independently adjustable):
  //   gapScore        → reward filling a missing foundational role
  //   diversityScore  → reward adding a new family
  //   structureScore  → reward adding a missing layer
  //   goalScore       → reward goal alignment (targetRoles + food_role)
  //   riskScore       → reward low shared pest overlap
  //   redundancyPenalty → penalise duplicating saturated roles
  //   nichePenalty    → penalise low-fit plants in production guilds
  //
  // Weights: tune these to adjust relative importance
  const W = {
    gap:        3.0,   // filling a role gap matters a lot
    diversity:  1.5,   // new family is valuable but not dominant
    structure:  1.2,   // layer diversity is a mild positive
    goal:       2.5,   // goal alignment is strong signal
    risk:       1.0,   // pest risk reduction is moderate
    redundancy: 1.5,   // stacking already-covered roles is a drag
    niche:      2.0,   // low-fit plants should lose decisively
  };

  function scorePlant(p, currentSlugs) {"""

NEW_SCORE = """  // ── scorePlant: function-stack-first evaluation ─────────────────────────────
  // PRIMARY: how many useful things does this plant do? (calcFunctionStackScore)
  // SECONDARY: bonuses for gap-filling, family diversity, layer, goal fit
  // PENALTIES: shallow redundancy, pest overlap, niche/low-fit plants
  function scorePlant(p, currentSlugs) {"""

patch(OLD_SCORE, NEW_SCORE, "2a: scorePlant header replaced")

# Replace the body — find the W.gap scoring block and replace with new logic
OLD_SCORE_BODY = """    // ── gapScore: reward filling a missing foundational role ─────────────────
    // Foundational roles are the backbone of any healthy guild
    const FOUNDATIONAL = ['Nitrogen Fixer','Pollinator','Pest Management',
                          'Ground Cover','Mulcher','Dynamic Accumulator'];
    let gapScore = 0;
    for (const fn of fns) {
      if (FOUNDATIONAL.includes(fn) && !roleCounts[fn]) gapScore += 1.0;
      // Partial credit for under-represented roles (only 1 present)
      else if (FOUNDATIONAL.includes(fn) && roleCounts[fn] === 1) gapScore += 0.4;
    }

    // ── diversityScore: reward adding a new plant family ─────────────────────
    // Family diversity reduces shared vulnerability
    const famCount = currentSlugs.filter(s => plantToFamily[s] === family).length;
    let diversityScore = 0;
    if (family && !existingFamilies.has(family)) diversityScore = 1.0;
    else if (famCount === 1) diversityScore = -0.3; // mild repeat penalty
    else if (famCount >= 2)  diversityScore = -1.0; // strong repeat penalty

    // ── structureScore: reward adding a missing growth layer ─────────────────
    const myLayer = inferLayer(p);
    const STRUCTURAL_LAYERS = ['canopy', 'shrub', 'ground', 'vine', 'root'];
    let structureScore = 0;
    if (STRUCTURAL_LAYERS.includes(myLayer) && !guildLayers.has(myLayer)) {
      structureScore = 1.0; // fills a missing structural layer
    } else if (guildLayers.has(myLayer)) {
      // Soft penalty for stacking same layer (capped at -1.0)
      const layerCount = currentSlugs.filter(s =>
        inferLayer(plantBySlug[s] || {}) === myLayer
      ).length;
      structureScore = Math.max(-1.0, layerCount * -0.3);
    }

    // ── goalScore: reward alignment with selected goal ────────────────────────
    // Combines targetRole matching + food_role signal
    let goalScore = 0;
    for (const fn of fns) {
      if (profile.targetRoles.includes(fn)) {
        // Primary goal role — weighted by goal importance
        goalScore += (goalKey === 'food_production' && fn === 'Edible') ? 1.5 : 1.0;
      }
    }
    // food_role bias for food_production
    if (goalKey === 'food_production') {
      if (p.food_role === 'anchor')       goalScore += 2.0;
      else if (p.food_role === 'support') goalScore += 0.5;
      // specialty handled in nichePenalty
    }
    // Penalise avoidOverweight roles
    for (const fn of fns) {
      if (profile.avoidOverweight.includes(fn) && !profile.targetRoles.includes(fn)) {
        goalScore -= 0.5;
      }
    }

    // ── riskScore: reward low shared pest overlap ─────────────────────────────
    // Fewer shared pests = better isolation = lower system pressure
    let sharedPests = 0;
    for (const pest of pests) { if (guildPests.has(pest)) sharedPests++; }
    // riskScore: 1.0 if no overlap, decreasing to -1.0 for heavy overlap
    const riskScore = Math.max(-1.0, 1.0 - sharedPests * 0.35);

    // ── redundancyPenalty: penalise stacking already-covered roles ────────────
    // Prevents guilds that over-invest in one function at cost of diversity
    const SUPPORT_ROLES_SET = new Set([
      'Ground Cover','Mulcher','Dynamic Accumulator','Erosion Control'
    ]);
    let redundancyPenalty = 0;
    for (const fn of fns) {
      const count = roleCounts[fn] || 0;
      if (count >= 3) redundancyPenalty += 0.5; // hard saturation
      else if (count >= 2 && SUPPORT_ROLES_SET.has(fn)) redundancyPenalty += 0.3;
    }
    // Low Maintenance special: more aggressive de-stacking
    if (goalKey === 'low_maintenance') {
      const SATURATE = ['Ground Cover','Pollinator','Pest Management'];
      for (const fn of fns) {
        if (SATURATE.includes(fn) && (roleCounts[fn] || 0) >= 2 &&
            family && existingFamilies.has(family)) {
          redundancyPenalty += 0.5;
        }
      }
    }

    // ── nichePenalty: penalise low-fit plants ─────────────────────────────────
    let nichePenalty = 0;
    if (goalKey === 'food_production') {
      // Support-heavy edibles behave more like support than food
      const FP_SUPPORT = ['Ground Cover','Mulcher','Dynamic Accumulator',
                          'Erosion Control','Pest Management'];
      const supportCount = FP_SUPPORT.filter(r => fns.includes(r)).length;
      if (fns.includes('Edible')) {
        if (supportCount >= 3)       nichePenalty += 1.5;
        else if (supportCount >= 2)  nichePenalty += 0.75;
        // Clean edible bonus — offset niche if very clean
        else if (supportCount <= 1)  nichePenalty -= 0.5; // negative penalty = bonus
      }
      // Exclusion list
      if (FOOD_PRODUCTION_EXCLUDE.includes(p.slug)) nichePenalty += 3.0;
      // Specialty in food guild
      if (p.food_role === 'specialty') nichePenalty += 1.5;
    }

    // ── Final score ───────────────────────────────────────────────────────────
    const total = (
      gapScore        * W.gap        +
      diversityScore  * W.diversity  +
      structureScore  * W.structure  +
      goalScore       * W.goal       +
      riskScore       * W.risk       -
      redundancyPenalty * W.redundancy -
      nichePenalty    * W.niche
    );

    return total;
  }"""

NEW_SCORE_BODY = """    // ── functionStackScore (PRIMARY) ─────────────────────────────────────────
    const functionStackScore = calcFunctionStackScore(fns);

    // ── missingRoleBonus (bonus, not gate) ────────────────────────────────────
    const FOUND_ROLES_SP = ['Nitrogen Fixer','Pollinator','Pest Management',
                            'Ground Cover','Mulcher','Dynamic Accumulator'];
    let missingRoleBonus = 0;
    for (const fn of fns) {
      if (FOUND_ROLES_SP.includes(fn) && !roleCounts[fn])      missingRoleBonus += 1.0;
      else if (FOUND_ROLES_SP.includes(fn) && roleCounts[fn] === 1) missingRoleBonus += 0.4;
    }

    // ── diversityBonus ────────────────────────────────────────────────────────
    const famCount = currentSlugs.filter(s => plantToFamily[s] === family).length;
    let diversityBonus = 0;
    if (family && !existingFamilies.has(family)) diversityBonus =  1.2;
    else if (famCount === 1)                      diversityBonus = -0.3;
    else if (famCount >= 2)                       diversityBonus = -1.2;

    // ── structureBonus ────────────────────────────────────────────────────────
    const myLayer = inferLayer(p);
    const STRUCT_SP = ['canopy','shrub','ground','vine','root'];
    let structureBonus = 0;
    if (STRUCT_SP.includes(myLayer) && !guildLayers.has(myLayer)) {
      structureBonus = 1.0;
    } else if (guildLayers.has(myLayer)) {
      const lc = currentSlugs.filter(s => inferLayer(plantBySlug[s]||{}) === myLayer).length;
      structureBonus = Math.max(-0.8, lc * -0.25);
    }

    // ── goalBonus ─────────────────────────────────────────────────────────────
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

    // ── riskPenalty ───────────────────────────────────────────────────────────
    let sharedPests = 0;
    for (const pest of pests) { if (guildPests.has(pest)) sharedPests++; }
    const riskPenalty = Math.min(2.0, sharedPests * 0.3);

    // ── redundancyPenalty: shallow redundancy only ────────────────────────────
    const famAlreadyIn   = existingFamilies.has(family);
    const layerAlreadyIn = guildLayers.has(myLayer);
    const saturatedFns   = fns.filter(fn => (roleCounts[fn] || 0) >= 3).length;
    let redundancyPenalty = 0;
    if (famAlreadyIn && layerAlreadyIn && saturatedFns >= 2) redundancyPenalty = 1.5;
    else if (famAlreadyIn && saturatedFns >= 3)              redundancyPenalty = 1.0;
    else if (saturatedFns >= 3)                              redundancyPenalty = 0.5;
    if (goalKey === 'low_maintenance') {
      const SAT_LM = ['Ground Cover','Pollinator','Pest Management'];
      for (const fn of fns) {
        if (SAT_LM.includes(fn) && (roleCounts[fn]||0) >= 2 && famAlreadyIn)
          redundancyPenalty += 0.4;
      }
    }

    // ── nichePenalty ──────────────────────────────────────────────────────────
    let nichePenalty = 0;
    if (goalKey === 'food_production') {
      const FP_SUPP = ['Ground Cover','Mulcher','Dynamic Accumulator',
                       'Erosion Control','Pest Management'];
      const supportCount = FP_SUPP.filter(r => fns.includes(r)).length;
      if (fns.includes('Edible')) {
        if (supportCount >= 3)      nichePenalty += 1.2;
        else if (supportCount >= 2) nichePenalty += 0.6;
        else if (supportCount <= 1) nichePenalty -= 0.4;
      }
      if (FOOD_PRODUCTION_EXCLUDE.includes(p.slug)) nichePenalty += 3.0;
      if (p.food_role === 'specialty') nichePenalty += 1.2;
    }

    return functionStackScore + missingRoleBonus + diversityBonus + structureBonus
         + goalBonus - riskPenalty - redundancyPenalty - nichePenalty;
  }"""

patch(OLD_SCORE_BODY, NEW_SCORE_BODY, "2b: scorePlant body replaced")

# ── 3. Replace getNextBestPlants scoring block ────────────────────────────────
OLD_GNB = """    // Zone fit (already filtered above, but need var for badge/explanation)
    const zoneFit = getZoneFit(p, userZone);

    // ── Sub-score evaluation (mirrors scorePlant logic for consistency) ────
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
                       : famRepeat >= 2 ? -1.5
                       : famRepeat === 1 ? -0.45 : 0;
    const hasNewFamily = family && !existFamilies.has(family);

    // Structure: missing layer
    const existLayers = new Set(currentSlugs.map(s => inferLayer(plantBySlug[s] || {})));
    const myLayer = inferLayer(p);
    const STRUCT_LAYERS = ['canopy','shrub','ground','vine','root'];
    let structureScore = 0;
    if (STRUCT_LAYERS.includes(myLayer) && !existLayers.has(myLayer)) structureScore = 1.2;
    else if (existLayers.has(myLayer)) {
      const lc = existSlugs.filter(s => inferLayer(plantBySlug[s]||{}) === myLayer).length;
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
    const SUPP = new Set(['Ground Cover','Mulcher','Dynamic Accumulator','Erosion Control']);
    for (const fn of fns) {
      const rc = curRoleCounts[fn] || 0;
      if (rc >= 3) redundancyPenalty += 0.75;
      else if (rc >= 2 && SUPP.has(fn)) redundancyPenalty += 0.45;
    }

    // Diminishing returns: don't stack same intent
    const diminishingPenalty = candidates.filter(c =>
      (hasMissing  && c._hasMissing)  ||
      (hasNewFamily && c._hasNewFamily)
    ).length * 0.5;

    const score = gapScore + diversityScore + structureScore + riskScore
                - redundancyPenalty - diminishingPenalty;"""

NEW_GNB = """    // Zone fit (already filtered above, but need var for badge/explanation)
    const zoneFit = getZoneFit(p, userZone);

    // ── Function-stack-first scoring ──────────────────────────────────────
    const fnStackScore = calcFunctionStackScore(fns);

    // Missing role bonus (secondary — bonus not gate)
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

    // Diversity bonus: new family
    const existFamilies = new Set(currentSlugs.map(s => plantToFamily[s]).filter(Boolean));
    const famRepeat = currentSlugs.filter(s => plantToFamily[s] === family).length;
    let diversityBonus = family && !existFamilies.has(family) ? 1.8
                       : famRepeat >= 2 ? -1.2 : famRepeat === 1 ? -0.35 : 0;
    const hasNewFamily = family && !existFamilies.has(family);

    // Structure bonus: missing layer
    const existLayers = new Set(currentSlugs.map(s => inferLayer(plantBySlug[s] || {})));
    const myLayer = inferLayer(p);
    const STRUCT_LAYERS = ['canopy','shrub','ground','vine','root'];
    let structureBonus = 0;
    if (STRUCT_LAYERS.includes(myLayer) && !existLayers.has(myLayer)) structureBonus = 1.0;
    else if (existLayers.has(myLayer)) {
      const lc = currentSlugs.filter(s => inferLayer(plantBySlug[s]||{}) === myLayer).length;
      structureBonus = Math.max(-0.8, lc * -0.25);
    }

    // Risk penalty: shared pest overlap
    const guildPestSet = new Set();
    for (const s of currentSlugs) {
      for (const pest of (plantToPests[s] || new Set())) guildPestSet.add(pest);
    }
    let sharedPestCount = 0;
    for (const pest of pests) { if (guildPestSet.has(pest)) sharedPestCount++; }
    const riskPenalty = Math.min(2.0, sharedPestCount * 0.3);

    // Redundancy penalty: shallow redundancy only
    const famAlreadyIn2 = existFamilies.has(family);
    const layerAlreadyIn2 = existLayers.has(myLayer);
    const saturatedFns2 = fns.filter(fn => (curRoleCounts[fn] || 0) >= 3).length;
    let redundancyPenalty = 0;
    if (famAlreadyIn2 && layerAlreadyIn2 && saturatedFns2 >= 2) redundancyPenalty = 1.5;
    else if (famAlreadyIn2 && saturatedFns2 >= 3)               redundancyPenalty = 1.0;
    else if (saturatedFns2 >= 3)                                redundancyPenalty = 0.5;

    // Diminishing returns across already-queued candidates
    const diminishingPenalty = candidates.filter(c =>
      (hasMissing && c._hasMissing) || (hasNewFamily && c._hasNewFamily)
    ).length * 0.4;

    const score = fnStackScore + missingRoleBonus + diversityBonus
                + structureBonus - riskPenalty - redundancyPenalty - diminishingPenalty;"""

patch(OLD_GNB, NEW_GNB, "3: getNextBestPlants scoring updated")

f.write_text(text)
print(f"\n{changes} patches applied")
