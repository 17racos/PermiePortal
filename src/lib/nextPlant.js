/**
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
      pestReasons.push('No shared pest pressure — clean addition');
    else if (sharedPestCount <= 2 && pests.size > 0)
      pestReasons.push('Low shared pest overlap — minimal risk');

    const hasMissing   = missingReasons.length > 0;
    const hasNewFamily = familyScore > 0;

    // Build context-aware explanations (explicit params, no hidden scope)
    const explanations = [];
    if (hasMissing) {
      const role = missingReasons[0]?.replace('Adds missing ','').replace(' function','') || '';
      const roleMap = {
        'Ground Cover':    'Adds Ground Cover, protecting exposed soil and reducing moisture loss between your existing plants.',
        'Pollinator':      'Adds Pollinator support, attracting beneficial insects that improve fruit and seed set across your guild.',
        'Pest Management': 'Adds Pest Management, helping confuse and deter insects that currently have no disruption in your guild.',
        'Mulcher':         'Adds a Mulcher, generating biomass that feeds soil biology and reduces bare-ground evaporation.',
        'Nitrogen Fixer':  'Adds a Nitrogen Fixer, feeding soil nitrogen through root nodules to support neighboring plants.',
      };
      explanations.push(roleMap[role] || `Fills a missing ${role} role in your guild.`);
    }
    if (hasNewFamily && explanations.length < 2 && family) {
      const famLabel = family.charAt(0).toUpperCase() + family.slice(1);
      if (dominantFamily) {
        const domLabel = dominantFamily.charAt(0).toUpperCase() + dominantFamily.slice(1);
        explanations.push(`Introduces ${famLabel}, which breaks the shared pest vulnerability of your ${domLabel}-heavy guild.`);
      } else {
        explanations.push(`Introduces ${famLabel}, adding new family diversity that reduces cross-species pest transfer.`);
      }
    }
    if (explanations.length < 2 && sharedPestCount === 0 && pests.size > 0) {
      // Build pestOccurrence for top-pest sorting
      const pestOcc = {};
      for (const slug of currentGuildSlugs) {
        for (const pest of (plantToPests[slug] || new Set())) {
          pestOcc[pest] = (pestOcc[pest] || 0) + 1;
        }
      }
      const topPests = Array.from(guildPests)
        .sort((a, b) => (pestOcc[b] || 0) - (pestOcc[a] || 0))
        .slice(0, 2);
      if (topPests.length > 0) {
        explanations.push(`Shares no pests with your guild, reducing the risk of ${topPests.join(' and ')} spreading between plants.`);
      } else {
        explanations.push('Shares no pest pressure with your current guild — a clean addition.');
      }
    } else if (explanations.length === 0 && sharedPestCount <= 2 && pests.size > 0) {
      explanations.push('Low pest overlap with your guild — minimal risk of amplifying existing pest pressure.');
    }
    if (explanations.length === 0) continue;
    if (!hasMissing && !hasNewFamily && sharedPestCount > 2) continue;

    candidates.push({
      slug: p.slug, name: p.common_name, family: family || '',
      explanations, score: Math.round(score * 10) / 10,
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

  // Balanced guild check — structural completeness
  const familyDiversity = guildFamilies.size / n;
  const dominantFamilyRatio = n > 0 ? (Object.values(familyCounts).sort((a,b)=>b-a)[0]||0)/n : 0;
  const pestOccurrence2 = {};
  for (const slug of currentGuildSlugs) {
    for (const pest of (plantToPests[slug] || new Set())) {
      pestOccurrence2[pest] = (pestOccurrence2[pest] || 0) + 1;
    }
  }
  const totalGuildPests  = Object.keys(pestOccurrence2).length;
  const sharedGuildPests = Object.values(pestOccurrence2).filter(c => c > 1).length;
  const pestOverlap      = totalGuildPests > 0 ? sharedGuildPests / totalGuildPests : 0;

  if (
    missingRoles.length === 0 &&
    familyDiversity >= 0.75 &&
    pestOverlap <= 0.3 &&
    dominantFamilyRatio <= 0.5
  ) {
    return [];
  }

  // Improvement threshold: 70%
  const topScore = candidates[0]?.score || 0;
  const threshold = topScore * 0.7;
  const aboveThreshold = candidates.filter(c => c.score >= threshold);

  // Intent tagging
  const tagged = aboveThreshold.map(c => ({
    ...c,
    intent: c._hasMissing   ? 'fills_gap'
          : c._hasNewFamily ? 'adds_diversity'
          :                   'reduces_risk',
  }));

  const familySeen = {};
  const filtered = [];
  for (const c of tagged) {
    const fam = c.family || '__none__';
    familySeen[fam] = (familySeen[fam] || 0) + 1;
    if (familySeen[fam] <= 2) filtered.push(c);
    if (filtered.length >= limit) break;
  }

  return filtered.map(({ _hasMissing, _hasNewFamily, _sharedPests, ...rest }) => rest);
}
