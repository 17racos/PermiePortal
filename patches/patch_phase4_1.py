#!/usr/bin/env python3
"""
patch_phase4_1.py
=================
Phase 4.1 — Goal Fidelity Refinement:
1. anchorRoles added to GOAL_PROFILES
2. generateGoalGuild() fills anchors first, then runs iterative generation
3. Stronger Food Production Edible bias (+2.0)
4. Reduced pest penalty for food_production (0.7x)
5. Soft cap on support-role dominance (3+ appearances = -1.0)
"""
from pathlib import Path

f = Path("src/pages/guild-checker.astro")
text = f.read_text()

OLD = """// ── Goal profiles ────────────────────────────────────────────────────────────
const GOAL_PROFILES = {
  food_production: {
    label: 'Food Production',
    description: 'Prioritizes edible species with soil support and structural resilience.',
    targetRoles: ['Edible', 'Ground Cover', 'Nitrogen Fixer', 'Mulcher'],
    avoidOverweight: ['Ornamental'],
    preferredGuildSize: 6,
  },
  low_maintenance: {
    label: 'Low Maintenance',
    description: 'Self-sustaining ground cover, mulch, and pest deterrence with minimal input.',
    targetRoles: ['Ground Cover', 'Mulcher', 'Pest Management', 'Pollinator'],
    avoidOverweight: ['Edible'],
    preferredGuildSize: 5,
  },
  pest_resistant: {
    label: 'Pest Resistant',
    description: 'Strong pest disruption, pollinator support, and family diversity to reduce shared pressure.',
    targetRoles: ['Pest Management', 'Pollinator', 'Ground Cover'],
    avoidOverweight: [],
    preferredGuildSize: 6,
  },
  pollinator_support: {
    label: 'Pollinator Support',
    description: 'Dense pollinator habitat with pest deterrence and ground-level coverage.',
    targetRoles: ['Pollinator', 'Pest Management', 'Ground Cover'],
    avoidOverweight: [],
    preferredGuildSize: 5,
  },
  soil_building: {
    label: 'Soil Building',
    description: 'Deep soil improvement through nitrogen fixation, dynamic accumulation, and biomass production.',
    targetRoles: ['Nitrogen Fixer', 'Mulcher', 'Dynamic Accumulator', 'Ground Cover'],
    avoidOverweight: [],
    preferredGuildSize: 6,
  },
};

function generateGoalGuild(goalKey) {
  const profile = GOAL_PROFILES[goalKey];
  if (!profile) return [];

  const generated = [];
  const guildSet  = new Set();
  const famSeen   = {};

  // Score a candidate against the current growing guild + goal profile
  function scorePlant(p, currentSlugs) {
    const fns    = p.plant_function || [];
    const family = plantToFamily[p.slug] || null;
    const pests  = plantToPests[p.slug] || new Set();

    // Goal role bonus
    let goalBonus = 0;
    for (const fn of fns) {
      if (profile.targetRoles.includes(fn)) goalBonus += 1.5;
      if (profile.avoidOverweight.length > 0 &&
          profile.avoidOverweight.includes(fn) &&
          !profile.targetRoles.includes(fn)) goalBonus -= 0.5;
    }

    // Family diversity bonus
    const existingFamilies = new Set(currentSlugs.map(s => plantToFamily[s]).filter(Boolean));
    const familyBonus = (family && !existingFamilies.has(family)) ? 1.0 : 0;

    // Pest overlap penalty
    const guildPests = new Set();
    for (const s of currentSlugs) {
      for (const pest of (plantToPests[s] || new Set())) guildPests.add(pest);
    }
    let sharedPests = 0;
    for (const pest of pests) { if (guildPests.has(pest)) sharedPests++; }
    const pestPenalty = sharedPests * 0.3;

    return goalBonus + familyBonus - pestPenalty;
  }

  // Build guild iteratively
  for (let i = 0; i < profile.preferredGuildSize; i++) {
    let bestSlug  = null;
    let bestScore = -Infinity;

    for (const p of plantIndex) {
      if (guildSet.has(p.slug)) continue;
      if (!p.plant_function || p.plant_function.length === 0) continue;

      // Max 2 per family in generated guild
      const fam = plantToFamily[p.slug] || '__none__';
      if ((famSeen[fam] || 0) >= 2) continue;

      const score = scorePlant(p, generated);
      if (score <= 0 && i > 0) continue; // first plant always gets added

      if (score > bestScore ||
          (score === bestScore && bestSlug && p.slug < bestSlug)) {
        bestScore = score;
        bestSlug  = p.slug;
      }
    }

    if (bestSlug) {
      generated.push(bestSlug);
      guildSet.add(bestSlug);
      const fam = plantToFamily[bestSlug] || '__none__';
      famSeen[fam] = (famSeen[fam] || 0) + 1;
    } else {
      break; // no more good candidates
    }
  }

  return generated;
}"""

NEW = """// ── Goal profiles ────────────────────────────────────────────────────────────
const GOAL_PROFILES = {
  food_production: {
    label: 'Food Production',
    description: 'Prioritizes edible species with soil support and structural resilience.',
    targetRoles: ['Edible', 'Ground Cover', 'Nitrogen Fixer', 'Mulcher'],
    avoidOverweight: ['Ornamental'],
    preferredGuildSize: 6,
    anchorRoles: { 'Edible': 3, 'Nitrogen Fixer': 1 },
  },
  low_maintenance: {
    label: 'Low Maintenance',
    description: 'Self-sustaining ground cover, mulch, and pest deterrence with minimal input.',
    targetRoles: ['Ground Cover', 'Mulcher', 'Pest Management', 'Pollinator'],
    avoidOverweight: ['Edible'],
    preferredGuildSize: 5,
    anchorRoles: { 'Ground Cover': 1, 'Mulcher': 1, 'Pest Management': 1 },
  },
  pest_resistant: {
    label: 'Pest Resistant',
    description: 'Strong pest disruption, pollinator support, and family diversity to reduce shared pressure.',
    targetRoles: ['Pest Management', 'Pollinator', 'Ground Cover'],
    avoidOverweight: [],
    preferredGuildSize: 6,
    anchorRoles: { 'Pest Management': 2, 'Pollinator': 1, 'Ground Cover': 1 },
  },
  pollinator_support: {
    label: 'Pollinator Support',
    description: 'Dense pollinator habitat with pest deterrence and ground-level coverage.',
    targetRoles: ['Pollinator', 'Pest Management', 'Ground Cover'],
    avoidOverweight: [],
    preferredGuildSize: 5,
    anchorRoles: { 'Pollinator': 2, 'Pest Management': 1 },
  },
  soil_building: {
    label: 'Soil Building',
    description: 'Deep soil improvement through nitrogen fixation, dynamic accumulation, and biomass production.',
    targetRoles: ['Nitrogen Fixer', 'Mulcher', 'Dynamic Accumulator', 'Ground Cover'],
    avoidOverweight: [],
    preferredGuildSize: 6,
    anchorRoles: { 'Nitrogen Fixer': 2, 'Mulcher': 1, 'Dynamic Accumulator': 1 },
  },
};

// Support roles subject to soft cap
const SUPPORT_ROLES = ['Mulcher', 'Ground Cover', 'Dynamic Accumulator', 'Erosion Control'];

function generateGoalGuild(goalKey) {
  const profile = GOAL_PROFILES[goalKey];
  if (!profile) return [];

  const generated = [];
  const guildSet  = new Set();
  const famSeen   = {};

  // ── Scoring function ───────────────────────────────────────────────────────
  function scorePlant(p, currentSlugs) {
    const fns    = p.plant_function || [];
    const family = plantToFamily[p.slug] || null;
    const pests  = plantToPests[p.slug] || new Set();

    // Goal role bonus — stronger Food Production Edible bias
    let goalBonus = 0;
    for (const fn of fns) {
      if (profile.targetRoles.includes(fn)) {
        // Extra boost for primary goal role in food_production
        goalBonus += (goalKey === 'food_production' && fn === 'Edible') ? 2.0 : 1.5;
      }
      if (profile.avoidOverweight.length > 0 &&
          profile.avoidOverweight.includes(fn) &&
          !profile.targetRoles.includes(fn)) goalBonus -= 0.5;
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

    // Family diversity bonus
    const existingFamilies = new Set(currentSlugs.map(s => plantToFamily[s]).filter(Boolean));
    const familyBonus = (family && !existingFamilies.has(family)) ? 1.0 : 0;

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
  }

  // ── Helper: pick best plant for a required role ───────────────────────────
  function pickBestForRole(requiredRole) {
    let bestSlug  = null;
    let bestScore = -Infinity;

    for (const p of plantIndex) {
      if (guildSet.has(p.slug)) continue;
      if (!p.plant_function || p.plant_function.length === 0) continue;
      if (!p.plant_function.includes(requiredRole)) continue;

      const fam = plantToFamily[p.slug] || '__none__';
      if ((famSeen[fam] || 0) >= 2) continue;

      const score = scorePlant(p, generated);
      if (score > bestScore ||
          (score === bestScore && bestSlug && p.slug < bestSlug)) {
        bestScore = score;
        bestSlug  = p.slug;
      }
    }
    return bestSlug;
  }

  function addToGuild(slug) {
    generated.push(slug);
    guildSet.add(slug);
    const fam = plantToFamily[slug] || '__none__';
    famSeen[fam] = (famSeen[fam] || 0) + 1;
  }

  // ── Phase 1: Fill anchor roles first ─────────────────────────────────────
  if (profile.anchorRoles) {
    for (const [role, count] of Object.entries(profile.anchorRoles)) {
      let filled = 0;
      while (filled < count && generated.length < profile.preferredGuildSize) {
        const slug = pickBestForRole(role);
        if (!slug) break;
        addToGuild(slug);
        filled++;
      }
    }
  }

  // ── Phase 2: Iterative generation to fill remaining slots ─────────────────
  while (generated.length < profile.preferredGuildSize) {
    let bestSlug  = null;
    let bestScore = -Infinity;

    for (const p of plantIndex) {
      if (guildSet.has(p.slug)) continue;
      if (!p.plant_function || p.plant_function.length === 0) continue;

      const fam = plantToFamily[p.slug] || '__none__';
      if ((famSeen[fam] || 0) >= 2) continue;

      const score = scorePlant(p, generated);
      if (score <= 0) continue;

      if (score > bestScore ||
          (score === bestScore && bestSlug && p.slug < bestSlug)) {
        bestScore = score;
        bestSlug  = p.slug;
      }
    }

    if (bestSlug) addToGuild(bestSlug);
    else break;
  }

  return generated;
}"""

if OLD in text:
    text = text.replace(OLD, NEW)
    f.write_text(text)
    print("✅ Phase 4.1: GOAL_PROFILES + generateGoalGuild() replaced")
else:
    print("❌ Pattern not found")
