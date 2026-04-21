/**
 * src/lib/nextPlant.js
 * ====================
 * getNextBestPlants(currentGuildSlugs, plantIndex, plantToFamily, plantToPests, limit)
 *
 * Suggests the best plants to add to an existing guild based on:
 * - Filling missing foundational roles
 * - Strengthening weak roles
 * - Minimizing shared pest overlap
 * - Introducing new family diversity
 *
 * NOTE: This logic is also inlined in guild-checker.astro since define:vars
 * scripts cannot import ES modules. Keep both in sync when changing logic.
 *
 * Uses ONLY:
 *   - plants.json (via plantIndex)
 *   - relationships.json (via plantToFamily + plantToPests indexes)
 *
 * No ML. No hardcoded suggestions. Pure deterministic scoring.
 */

const FOUNDATIONAL_ROLES = [
  'Nitrogen Fixer',
  'Ground Cover',
  'Pollinator',
  'Pest Management',
  'Mulcher',
];

/**
 * @param {string[]} currentGuildSlugs
 * @param {object[]} plantIndex        - slim plant array with slug, common_name, family, plant_function
 * @param {object}   plantToFamily     - { slug: familySlug }
 * @param {object}   plantToPests      - { slug: Set<pestName> }
 * @param {number}   limit             - max suggestions to return (default 5)
 * @returns {{ slug, name, family, reasons, score }[]}
 */
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

  // ── Build guild context ────────────────────────────────────────────────────
  const guildFamilies = new Set(
    currentGuildSlugs.map(s => plantToFamily[s]).filter(Boolean)
  );

  // Dominant family (most represented)
  const familyCounts = {};
  for (const s of currentGuildSlugs) {
    const f = plantToFamily[s];
    if (f) familyCounts[f] = (familyCounts[f] || 0) + 1;
  }
  const dominantFamily = Object.entries(familyCounts)
    .sort((a, b) => b[1] - a[1])[0]?.[0] || null;

  // Guild function counts
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

  // Guild pest set (union of all guild plant pests)
  const guildPests = new Set();
  for (const slug of currentGuildSlugs) {
    for (const pest of (plantToPests[slug] || new Set())) {
      guildPests.add(pest);
    }
  }

  // ── Score every candidate ──────────────────────────────────────────────────
  const candidates = [];

  for (const p of plantIndex) {
    if (guildSet.has(p.slug)) continue;

    const fns    = p.plant_function || [];
    const family = plantToFamily[p.slug] || null;
    const pests  = plantToPests[p.slug] || new Set();

    // Role score
    let roleScore = 0;
    const roleReasons = [];
    for (const fn of fns) {
      if (missingRoles.includes(fn)) {
        roleScore += 2;
        roleReasons.push(`Adds ${fn} — a missing foundational role`);
      } else if (weakRoles.includes(fn)) {
        roleScore += 1;
        roleReasons.push(`Strengthens ${fn} support`);
      }
    }

    // Pest overlap score (fewer shared pests = better)
    let sharedPestCount = 0;
    for (const pest of pests) {
      if (guildPests.has(pest)) sharedPestCount++;
    }

    // Family score
    let familyScore = 0;
    const familyReasons = [];
    if (family && !guildFamilies.has(family)) {
      familyScore = 1;
      familyReasons.push(`Introduces ${family} — a new family`);
    } else if (family && family === dominantFamily) {
      familyScore = -1;
    }

    // Pest reason
    const pestReasons = [];
    if (sharedPestCount === 0 && pests.size > 0) {
      pestReasons.push('No shared pests with current guild');
    } else if (sharedPestCount <= 2 && pests.size > 0) {
      pestReasons.push('Low shared pest overlap');
    }

    // Combined score
    const score = (roleScore * 2) + (familyScore * 1) - (sharedPestCount * 0.5);

    // Only include plants with positive contribution
    if (score <= 0 && roleReasons.length === 0) continue;

    // Build reasons (cap at 3)
    const reasons = [...roleReasons, ...familyReasons, ...pestReasons].slice(0, 3);
    if (reasons.length === 0) continue;

    candidates.push({
      slug:   p.slug,
      name:   p.common_name,
      family: family || '',
      reasons,
      score:  Math.round(score * 10) / 10,
    });
  }

  // Sort by score descending, then alphabetically for determinism
  candidates.sort((a, b) => b.score - a.score || a.name.localeCompare(b.name));

  return candidates.slice(0, limit);
}
