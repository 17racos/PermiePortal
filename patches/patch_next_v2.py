#!/usr/bin/env python3
from pathlib import Path

f = Path("src/pages/guild-checker.astro")
text = f.read_text()

# Find exact boundaries using unique anchors
start = text.find("NEXT_FOUNDATIONAL_ROLES = [")
end   = text.find("// ── Render ──────", start)

if start < 0 or end < 0:
    print(f"❌ Anchors not found: start={start}, end={end}")
    exit(1)

old_block = text[start:end]
print(f"Found block: {len(old_block)} chars, starts with: {repr(old_block[:80])}")
print(f"Ends with: {repr(old_block[-80:])}")

NEW_BLOCK = """// Role weights: high-value missing roles score much higher
const ROLE_WEIGHTS = {
  'Ground Cover':        { missing: 2.0, weak: 1.0 },
  'Pollinator':          { missing: 2.0, weak: 1.0 },
  'Pest Management':     { missing: 2.0, weak: 1.0 },
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

    let roleScore = 0;
    let onlyStrongRoles = true;
    const roleReasons = [];
    for (const fn of fns) {
      const w = ROLE_WEIGHTS[fn];
      if (!w) continue;
      if (missingRoles.includes(fn)) {
        roleScore += w.missing;
        roleReasons.push('Fills missing ' + fn + ' role');
        onlyStrongRoles = false;
      } else if (weakRoles.includes(fn)) {
        roleScore += w.weak;
        roleReasons.push('Supports ' + fn + ' role');
        onlyStrongRoles = false;
      }
    }

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
      familyReasons.push('Introduces new family (' + family + ')');
    } else if (family && family === dominantFamily) {
      familyScore = -1;
    }

    if (roleScore === 0 && familyScore <= 0 && sharedPestCount > 2) continue;

    const score = (roleScore * 2.5) + (familyScore * 1.5) + pestBonus
                  - (sharedPestCount * 0.5) + diminishingPenalty;

    if (score <= 0 && roleReasons.length === 0 && familyReasons.length === 0) continue;

    const pestReasons = [];
    if (sharedPestCount === 0 && pests.size > 0) pestReasons.push('No shared pest pressure');
    else if (sharedPestCount <= 2 && pests.size > 0) pestReasons.push('Low shared pest overlap');

    const reasons = [...roleReasons, ...familyReasons, ...pestReasons].slice(0, 3);
    if (reasons.length === 0) continue;

    candidates.push({
      slug: p.slug, name: p.common_name, family: family || '',
      reasons, score: Math.round(score * 10) / 10,
    });
  }

  candidates.sort((a, b) => b.score - a.score || a.name.localeCompare(b.name));

  // Family diversity filter: max 2 per family in final results
  const familySeen = {};
  const filtered = [];
  for (const c of candidates) {
    const fam = c.family || '__none__';
    familySeen[fam] = (familySeen[fam] || 0) + 1;
    if (familySeen[fam] <= 2) filtered.push(c);
    if (filtered.length >= limit) break;
  }
  return filtered;
}

"""

text = text[:start] + NEW_BLOCK + text[end:]
f.write_text(text)
print("✅ getNextBestPlants() upgraded in guild-checker.astro")
