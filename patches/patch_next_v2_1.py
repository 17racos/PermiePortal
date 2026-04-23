#!/usr/bin/env python3
"""
patch_next_v2_1.py
==================
Signal quality improvements to getNextBestPlants():
1. Reduce Pest Management weight
2. Stricter meaningful contribution gate
3. Better pest reason text
4. Role reason priority (missing only, max 1 weak)
5. Better tie-break sort
6. Improved UX language
Updates BOTH guild-checker.astro and src/lib/nextPlant.js
"""
from pathlib import Path

CHANGES = 0

NEW_FN = '''ROLE_WEIGHTS = {
  'Ground Cover':        { missing: 2.0, weak: 1.0 },
  'Pollinator':          { missing: 2.0, weak: 1.0 },
  'Pest Management':     { missing: 1.5, weak: 0.75 },
  'Mulcher':             { missing: 1.5, weak: 0.75 },
  'Nitrogen Fixer':      { missing: 0.5, weak: 0.25 },
};
const NEXT_FOUNDATIONAL_ROLES = Object.keys(ROLE_WEIGHTS);

function getNextBestPlants(currentSlugs, limit = 5) {
  const guildSet = new Set(currentSlugs);
  const n = currentSlugs.length;
  if (n === 0) return [];

  const guildFamilies = new Set(currentSlugs.map(s => plantToFamily[s]).filter(Boolean));
  const familyCounts = {};
  for (const s of currentSlugs) {
    const f = plantToFamily[s];
    if (f) familyCounts[f] = (familyCounts[f] || 0) + 1;
  }
  const dominantFamily = Object.entries(familyCounts).sort((a,b) => b[1]-a[1])[0]?.[0] || null;

  const guildFnCounts = {};
  for (const role of NEXT_FOUNDATIONAL_ROLES) guildFnCounts[role] = 0;
  for (const slug of currentSlugs) {
    const p = plantBySlug[slug];
    if (!p) continue;
    for (const fn of (p.plant_function || [])) {
      if (guildFnCounts.hasOwnProperty(fn)) guildFnCounts[fn]++;
    }
  }
  const missingRoles = NEXT_FOUNDATIONAL_ROLES.filter(r => guildFnCounts[r] === 0);
  const weakRoles    = NEXT_FOUNDATIONAL_ROLES.filter(r => guildFnCounts[r] === 1);
  const strongRoles  = NEXT_FOUNDATIONAL_ROLES.filter(r => guildFnCounts[r] >= 2);

  const guildPests = new Set();
  for (const slug of currentSlugs) {
    for (const pest of (plantToPests[slug] || new Set())) guildPests.add(pest);
  }

  const candidates = [];
  for (const p of plantIndex) {
    if (guildSet.has(p.slug)) continue;
    const fns    = p.plant_function || [];
    const family = plantToFamily[p.slug] || null;
    const pests  = plantToPests[p.slug] || new Set();

    // Role scoring — missing roles only show their reason; weak roles max 1
    let roleScore = 0;
    let onlyStrongRoles = true;
    const missingReasons = [];
    const weakReasons    = [];
    for (const fn of fns) {
      const w = ROLE_WEIGHTS[fn];
      if (!w) continue;
      if (missingRoles.includes(fn)) {
        roleScore += w.missing;
        missingReasons.push('Adds missing ' + fn + ' function');
        onlyStrongRoles = false;
      } else if (weakRoles.includes(fn)) {
        roleScore += w.weak;
        weakReasons.push('Reinforces ' + fn + ' function');
        onlyStrongRoles = false;
      }
    }
    // If fills missing roles, skip weak role reasons entirely
    // Otherwise show max 1 weak role reason
    const roleReasons = missingReasons.length > 0
      ? missingReasons
      : weakReasons.slice(0, 1);

    const diminishingPenalty = (roleScore === 0 && onlyStrongRoles &&
      fns.some(fn => strongRoles.includes(fn))) ? -1 : 0;

    let sharedPestCount = 0;
    for (const pest of pests) { if (guildPests.has(pest)) sharedPestCount++; }
    const pestBonus = sharedPestCount === 0 && pests.size > 0 ? 1.0
                    : sharedPestCount <= 2 && pests.size > 0  ? 0.5 : 0;

    let familyScore = 0;
    const familyReasons = [];
    if (family && !guildFamilies.has(family)) {
      familyScore = 1.5;
      familyReasons.push('Adds new family diversity (' + family + ')');
    } else if (family && family === dominantFamily) {
      familyScore = -1;
    }

    // Meaningful contribution gate: skip weak candidates
    if (roleScore < 1.0 && familyScore <= 0 && pestBonus <= 0.5) continue;

    const score = (roleScore * 2.5) + (familyScore * 1.5) + pestBonus
                  - (sharedPestCount * 0.5) + diminishingPenalty;

    if (score <= 0 && roleReasons.length === 0 && familyReasons.length === 0) continue;

    // Pest reason — only if overlap is clean
    const pestReasons = [];
    if (sharedPestCount === 0 && pests.size > 0)
      pestReasons.push('No shared pest pressure \u2014 clean addition');
    else if (sharedPestCount <= 2 && pests.size > 0)
      pestReasons.push('Low shared pest overlap \u2014 minimal risk');
    // sharedPestCount > 2: no pest reason

    const reasons = [...roleReasons, ...familyReasons, ...pestReasons].slice(0, 3);
    if (reasons.length === 0) continue;

    // Tie-break metadata for sort
    const hasMissing   = missingReasons.length > 0;
    const hasNewFamily = familyScore > 0;

    candidates.push({
      slug: p.slug, name: p.common_name, family: family || '',
      reasons, score: Math.round(score * 10) / 10,
      _hasMissing: hasMissing, _hasNewFamily: hasNewFamily,
      _sharedPests: sharedPestCount,
    });
  }

  // Sort: score desc, then missing role > new family > lower pest overlap > name
  candidates.sort((a, b) => {
    if (b.score !== a.score) return b.score - a.score;
    if (b._hasMissing !== a._hasMissing) return b._hasMissing ? 1 : -1;
    if (b._hasNewFamily !== a._hasNewFamily) return b._hasNewFamily ? 1 : -1;
    if (a._sharedPests !== b._sharedPests) return a._sharedPests - b._sharedPests;
    return a.name.localeCompare(b.name);
  });

  // Family diversity filter: max 2 per family in final results
  const familySeen = {};
  const filtered = [];
  for (const c of candidates) {
    const fam = c.family || '__none__';
    familySeen[fam] = (familySeen[fam] || 0) + 1;
    if (familySeen[fam] <= 2) filtered.push(c);
    if (filtered.length >= limit) break;
  }

  // Strip internal sort metadata before returning
  return filtered.map(({ _hasMissing, _hasNewFamily, _sharedPests, ...rest }) => rest);
}

'''

# ── Patch guild-checker.astro ─────────────────────────────────────────────────
fc = Path("src/pages/guild-checker.astro")
text = fc.read_text()

start = text.find("ROLE_WEIGHTS = {")
end   = text.find("// ── Render ──────", start)

if start < 0 or end < 0:
    print(f"❌ Anchors not found in guild-checker.astro (start={start}, end={end})")
else:
    text = text[:start] + NEW_FN + text[end:]
    fc.write_text(text)
    CHANGES += 1
    print("✅ guild-checker.astro updated")

# ── Patch src/lib/nextPlant.js ────────────────────────────────────────────────
lib = Path("src/lib/nextPlant.js")
lib_content = lib.read_text() if lib.exists() else ""

LIB_NEW = '''/**
 * src/lib/nextPlant.js
 * ====================
 * getNextBestPlants() — Next Best Plant suggestion engine v2.1
 *
 * NOTE: Logic is also inlined in guild-checker.astro (define:vars scripts
 * cannot import ES modules). Keep both in sync when changing logic.
 *
 * Scoring formula:
 *   score = (roleScore * 2.5) + (familyScore * 1.5) + pestBonus
 *           - (sharedPestCount * 0.5) + diminishingPenalty
 *
 * Filters:
 *   - meaningful contribution gate (roleScore < 1.0 AND familyScore <= 0 AND pestBonus <= 0.5 → skip)
 *   - family diversity cap (max 2 per family in results)
 */

const ROLE_WEIGHTS = {
  'Ground Cover':        { missing: 2.0, weak: 1.0 },
  'Pollinator':          { missing: 2.0, weak: 1.0 },
  'Pest Management':     { missing: 1.5, weak: 0.75 },
  'Mulcher':             { missing: 1.5, weak: 0.75 },
  'Nitrogen Fixer':      { missing: 0.5, weak: 0.25 },
};
const FOUNDATIONAL_ROLES = Object.keys(ROLE_WEIGHTS);

export function getNextBestPlants(
  currentGuildSlugs,
  plantIndex,
  plantToFamily,
  plantToPests,
  limit = 5
) {
  const guildSet = new Set(currentGuildSlugs);
  const n = currentGuildSlugs.length;
  if (n === 0) return [];

  const guildFamilies = new Set(currentGuildSlugs.map(s => plantToFamily[s]).filter(Boolean));
  const familyCounts = {};
  for (const s of currentGuildSlugs) {
    const f = plantToFamily[s];
    if (f) familyCounts[f] = (familyCounts[f] || 0) + 1;
  }
  const dominantFamily = Object.entries(familyCounts).sort((a,b) => b[1]-a[1])[0]?.[0] || null;

  const guildFnCounts = {};
  for (const role of FOUNDATIONAL_ROLES) guildFnCounts[role] = 0;
  for (const slug of currentGuildSlugs) {
    const p = plantIndex.find(x => x.slug === slug);
    if (!p) continue;
    for (const fn of (p.plant_function || [])) {
      if (guildFnCounts.hasOwnProperty(fn)) guildFnCounts[fn]++;
    }
  }
  const missingRoles = FOUNDATIONAL_ROLES.filter(r => guildFnCounts[r] === 0);
  const weakRoles    = FOUNDATIONAL_ROLES.filter(r => guildFnCounts[r] === 1);
  const strongRoles  = FOUNDATIONAL_ROLES.filter(r => guildFnCounts[r] >= 2);

  const guildPests = new Set();
  for (const slug of currentGuildSlugs) {
    for (const pest of (plantToPests[slug] || new Set())) guildPests.add(pest);
  }

  const candidates = [];
  for (const p of plantIndex) {
    if (guildSet.has(p.slug)) continue;
    const fns    = p.plant_function || [];
    const family = plantToFamily[p.slug] || null;
    const pests  = plantToPests[p.slug] || new Set();

    let roleScore = 0;
    let onlyStrongRoles = true;
    const missingReasons = [];
    const weakReasons    = [];
    for (const fn of fns) {
      const w = ROLE_WEIGHTS[fn];
      if (!w) continue;
      if (missingRoles.includes(fn)) {
        roleScore += w.missing;
        missingReasons.push('Adds missing ' + fn + ' function');
        onlyStrongRoles = false;
      } else if (weakRoles.includes(fn)) {
        roleScore += w.weak;
        weakReasons.push('Reinforces ' + fn + ' function');
        onlyStrongRoles = false;
      }
    }
    const roleReasons = missingReasons.length > 0
      ? missingReasons
      : weakReasons.slice(0, 1);

    const diminishingPenalty = (roleScore === 0 && onlyStrongRoles &&
      fns.some(fn => strongRoles.includes(fn))) ? -1 : 0;

    let sharedPestCount = 0;
    for (const pest of pests) { if (guildPests.has(pest)) sharedPestCount++; }
    const pestBonus = sharedPestCount === 0 && pests.size > 0 ? 1.0
                    : sharedPestCount <= 2 && pests.size > 0  ? 0.5 : 0;

    let familyScore = 0;
    const familyReasons = [];
    if (family && !guildFamilies.has(family)) {
      familyScore = 1.5;
      familyReasons.push('Adds new family diversity (' + family + ')');
    } else if (family && family === dominantFamily) {
      familyScore = -1;
    }

    if (roleScore < 1.0 && familyScore <= 0 && pestBonus <= 0.5) continue;

    const score = (roleScore * 2.5) + (familyScore * 1.5) + pestBonus
                  - (sharedPestCount * 0.5) + diminishingPenalty;

    if (score <= 0 && roleReasons.length === 0 && familyReasons.length === 0) continue;

    const pestReasons = [];
    if (sharedPestCount === 0 && pests.size > 0)
      pestReasons.push('No shared pest pressure \u2014 clean addition');
    else if (sharedPestCount <= 2 && pests.size > 0)
      pestReasons.push('Low shared pest overlap \u2014 minimal risk');

    const reasons = [...roleReasons, ...familyReasons, ...pestReasons].slice(0, 3);
    if (reasons.length === 0) continue;

    const hasMissing   = missingReasons.length > 0;
    const hasNewFamily = familyScore > 0;

    candidates.push({
      slug: p.slug, name: p.common_name, family: family || '',
      reasons, score: Math.round(score * 10) / 10,
      _hasMissing: hasMissing, _hasNewFamily: hasNewFamily,
      _sharedPests: sharedPestCount,
    });
  }

  candidates.sort((a, b) => {
    if (b.score !== a.score) return b.score - a.score;
    if (b._hasMissing !== a._hasMissing) return b._hasMissing ? 1 : -1;
    if (b._hasNewFamily !== a._hasNewFamily) return b._hasNewFamily ? 1 : -1;
    if (a._sharedPests !== b._sharedPests) return a._sharedPests - b._sharedPests;
    return a.name.localeCompare(b.name);
  });

  const familySeen = {};
  const filtered = [];
  for (const c of candidates) {
    const fam = c.family || '__none__';
    familySeen[fam] = (familySeen[fam] || 0) + 1;
    if (familySeen[fam] <= 2) filtered.push(c);
    if (filtered.length >= limit) break;
  }

  return filtered.map(({ _hasMissing, _hasNewFamily, _sharedPests, ...rest }) => rest);
}
'''

lib.write_text(LIB_NEW)
CHANGES += 1
print("✅ src/lib/nextPlant.js updated")

print(f"\n{CHANGES} files updated")
