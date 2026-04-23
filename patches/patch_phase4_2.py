#!/usr/bin/env python3
"""
patch_phase4_2.py
=================
Phase 4.2 — Goal Personality Tuning:
1. Food Production: support-heavy edible penalty (too many support roles = -1.0)
2. Low Maintenance: de-stacking logic (saturated roles penalized)
3. Dominant role messages refined to advisory tone
"""
from pathlib import Path

f = Path("src/pages/guild-checker.astro")
text = f.read_text()

OLD_SCORE = """  // ── Scoring function ───────────────────────────────────────────────────────
  function scorePlant(p, currentSlugs) {
    const fns    = p.plant_function || [];
    const family = plantToFamily[p.slug] || null;
    const pests  = plantToPests[p.slug] || new Set();
    // Goal role bonus — stronger Food Production Edible bias
    let goalBonus = 0;
    for (const fn of fns) {
      if (profile.targetRoles.includes(fn)) {
        // Extra boost for primary goal role in food_production
        goalBonus += (goalKey === 'food_production' && fn === 'Edible') ? 2.5 : 1.5;
      }
      if (profile.avoidOverweight.length > 0 &&
          profile.avoidOverweight.includes(fn) &&
          !profile.targetRoles.includes(fn)) {
        goalBonus -= goalKey === 'food_production' ? 1.5 : 0.5;
      }
    }
    // Support role soft cap — penalize if already 3+ of same support role
    const roleCounts = {};
    for (const s of currentSlugs) {
      const pp = plantBySlug[s];
      if (!pp) continue;
      for (const fn of (pp.plant_function || [])) {
        if (SUPPORT_ROLES.includes(fn)) roleCounts[fn] = (roleCounts[fn] || 0) + 1;
      }
    }
    for (const fn of fns) {
      if (SUPPORT_ROLES.includes(fn) && (roleCounts[fn] || 0) >= 3) goalBonus -= 1.0;
    }
    // Family diversity bonus — stronger penalty for repeated family in low_maintenance
    const existingFamilies = new Set(currentSlugs.map(s => plantToFamily[s]).filter(Boolean));
    const famRepeatCount = currentSlugs.filter(s => plantToFamily[s] === family).length;
    const familyBonus = (family && !existingFamilies.has(family))
      ? 1.0
      : (goalKey === 'low_maintenance' && famRepeatCount >= 1 ? -1.5 : 0);
    // Pest overlap penalty — reduced for food_production
    const guildPests = new Set();
    for (const s of currentSlugs) {
      for (const pest of (plantToPests[s] || new Set())) guildPests.add(pest);
    }
    let sharedPests = 0;
    for (const pest of pests) { if (guildPests.has(pest)) sharedPests++; }
    const basePestPenalty = sharedPests * 0.3;
    const pestPenalty = goalKey === 'food_production'
      ? basePestPenalty * 0.7
      : basePestPenalty;
    return goalBonus + familyBonus - pestPenalty;
  }"""

NEW_SCORE = """  // ── Scoring function ───────────────────────────────────────────────────────
  function scorePlant(p, currentSlugs) {
    const fns    = p.plant_function || [];
    const family = plantToFamily[p.slug] || null;
    const pests  = plantToPests[p.slug] || new Set();

    // ── Goal role bonus ──────────────────────────────────────────────────────
    let goalBonus = 0;
    for (const fn of fns) {
      if (profile.targetRoles.includes(fn)) {
        goalBonus += (goalKey === 'food_production' && fn === 'Edible') ? 2.5 : 1.5;
      }
      if (profile.avoidOverweight.length > 0 &&
          profile.avoidOverweight.includes(fn) &&
          !profile.targetRoles.includes(fn)) {
        goalBonus -= goalKey === 'food_production' ? 1.5 : 0.5;
      }
    }

    // ── Food Production: penalize support-heavy edibles ──────────────────────
    // Prevents support-edibles (e.g. chamomile, chia) from outranking productive crops
    if (goalKey === 'food_production' && fns.includes('Edible')) {
      const supportCount = fns.filter(fn =>
        ['Ground Cover','Mulcher','Dynamic Accumulator','Erosion Control','Pest Management'].includes(fn)
      ).length;
      if (supportCount >= 3) goalBonus -= 1.0;
    }

    // ── Support role soft cap — penalize if already 3+ of same support role ──
    const roleCounts = {};
    for (const s of currentSlugs) {
      const pp = plantBySlug[s];
      if (!pp) continue;
      for (const fn of (pp.plant_function || [])) {
        if (SUPPORT_ROLES.includes(fn)) roleCounts[fn] = (roleCounts[fn] || 0) + 1;
      }
    }
    for (const fn of fns) {
      if (SUPPORT_ROLES.includes(fn) && (roleCounts[fn] || 0) >= 3) goalBonus -= 1.0;
    }

    // ── Low Maintenance: de-stacking — reduce reinforcement of saturated roles ─
    if (goalKey === 'low_maintenance') {
      const SATURATE_ROLES = ['Ground Cover', 'Pollinator', 'Pest Management'];
      const saturatedRoles = SATURATE_ROLES.filter(r => (roleCounts[r] || 0) >= 2);
      if (saturatedRoles.length > 0) {
        const onlySaturates = fns.every(fn =>
          saturatedRoles.includes(fn) || !profile.targetRoles.includes(fn)
        );
        const addsNewFamily = family && !new Set(currentSlugs.map(s => plantToFamily[s]).filter(Boolean)).has(family);
        if (onlySaturates && !addsNewFamily) goalBonus -= 1.25;
      }
    }

    // ── Family diversity bonus ────────────────────────────────────────────────
    const existingFamilies = new Set(currentSlugs.map(s => plantToFamily[s]).filter(Boolean));
    const famRepeatCount = currentSlugs.filter(s => plantToFamily[s] === family).length;
    const familyBonus = (family && !existingFamilies.has(family))
      ? 1.0
      : (goalKey === 'low_maintenance' && famRepeatCount >= 1 ? -1.5 : 0);

    // ── Pest overlap penalty — reduced for food_production ────────────────────
    const guildPests = new Set();
    for (const s of currentSlugs) {
      for (const pest of (plantToPests[s] || new Set())) guildPests.add(pest);
    }
    let sharedPests = 0;
    for (const pest of pests) { if (guildPests.has(pest)) sharedPests++; }
    const basePestPenalty = sharedPests * 0.3;
    const pestPenalty = goalKey === 'food_production'
      ? basePestPenalty * 0.7
      : basePestPenalty;

    return goalBonus + familyBonus - pestPenalty;
  }"""

if OLD_SCORE in text:
    text = text.replace(OLD_SCORE, NEW_SCORE)
    print("✅ 1: scoring function updated with goal personality")
else:
    print("❌ 1: scoring function not found")

# ── 2. Refine dominant role messages to advisory tone ────────────────────────
OLD_DOM = """const dominantMsgs = {
    'Nitrogen Fixer':  'Nitrogen-fixing support is very strong — next additions should complement with productive or support roles.',
    'Ground Cover':    'Ground cover is well saturated — consider adding height and structural diversity to complement it.',
    'Pollinator':      'Pollinator support is very strong — consider adding structural or risk-reduction diversity next.',
    'Mulcher':         'Mulch production is strong — consider adding complementary roles to bal"""

# Find and replace the full dominantMsgs block
start = text.find("const dominantMsgs = {")
end   = text.find("};", start) + 2
old_block = text[start:end]

new_block = """const dominantMsgs = {
    'Nitrogen Fixer':  'Nitrogen fixation is already well covered — future additions can focus on productivity, pest management, or structural diversity.',
    'Ground Cover':    'Ground cover is well established — future additions can bring height, yield, or structural variety.',
    'Pollinator':      'Pollinator support is strong — future additions can broaden structure or introduce productive layers.',
    'Mulcher':         'Biomass production is well covered — consider adding yield or pest management layers to complement it.',
    'Pest Management': 'Pest disruption is already strong — future additions can focus on productivity or structural diversity.',
  };"""

if start > 0 and end > start:
    text = text[:start] + new_block + text[end:]
    print("✅ 2: dominant role messages refined to advisory tone")
else:
    print("❌ 2: dominantMsgs block not found")

f.write_text(text)
