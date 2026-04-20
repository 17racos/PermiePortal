/**
 * src/lib/guildRisk.js
 * ====================
 * scoreGuild(plantSlugs, relationships) — deterministic guild risk scorer.
 *
 * Uses ONLY:
 *   - relationships (plant_family + plant_pest edges)
 *
 * No ML. No heuristics. Pure aggregation math.
 */

/**
 * Score a guild of plants for ecological risk.
 *
 * @param {string[]} plantSlugs - list of plant slug strings
 * @param {object[]} relationships - full relationships array (plant_family + plant_pest edges)
 * @returns {{
 *   score: number,
 *   breakdown: {
 *     family_diversity: number,
 *     pest_overlap: number,
 *     dominant_family_ratio: number
 *   },
 *   risk_level: "low"|"medium"|"high",
 *   dominant_families: string[],
 *   shared_pests: {name: string, count: number}[],
 *   warnings: string[],
 *   suggestions: string[]
 * }}
 */
export function scoreGuild(plantSlugs, relationships) {
  // Dedup input
  const slugs = [...new Set(plantSlugs.map(s => s.trim()).filter(Boolean))];
  const n = slugs.length;

  if (n === 0) {
    return {
      score: 0,
      breakdown: { family_diversity: 0, pest_overlap: 0, dominant_family_ratio: 0 },
      risk_level: "low",
      dominant_families: [],
      shared_pests: [],
      warnings: ["No valid plant slugs provided."],
      suggestions: ["Add at least 3 plants to assess guild risk."],
    };
  }

  // ── Build indexes from edges (read-only) ────────────────────────────────────
  const plantToFamily = {};
  const plantToPests  = {};

  for (const r of relationships) {
    if (r.type === "plant_family") {
      plantToFamily[r.source_slug] = r.target_slug;
    } else if (r.type === "plant_pest") {
      if (!plantToPests[r.source_slug]) plantToPests[r.source_slug] = new Set();
      plantToPests[r.source_slug].add(r.pest_name);
    }
  }

  // ── Resolve families ────────────────────────────────────────────────────────
  const guildFamilies = slugs
    .filter(s => plantToFamily[s])
    .map(s => plantToFamily[s]);

  const familyCounts = {};
  for (const f of guildFamilies) {
    familyCounts[f] = (familyCounts[f] || 0) + 1;
  }

  const uniqueFamilies = Object.keys(familyCounts).length;
  const familyDiversity = uniqueFamilies / n;

  const sortedFamilies = Object.entries(familyCounts)
    .sort((a, b) => b[1] - a[1]);
  const dominantFamilies = sortedFamilies.map(([f]) => f);

  const topCount = sortedFamilies[0]?.[1] || 0;
  const dominantFamilyRatio = topCount / n;

  // ── Gather pests ────────────────────────────────────────────────────────────
  const pestOccurrence = {};
  for (const s of slugs) {
    for (const pest of (plantToPests[s] || new Set())) {
      pestOccurrence[pest] = (pestOccurrence[pest] || 0) + 1;
    }
  }

  const allPestNames  = Object.keys(pestOccurrence);
  const totalPests    = allPestNames.length;
  const sharedPests   = allPestNames
    .filter(p => pestOccurrence[p] > 1)
    .sort((a, b) => pestOccurrence[b] - pestOccurrence[a])
    .map(p => ({ name: p, count: pestOccurrence[p] }));

  // ── Pest overlap score = shared pests / total pests ─────────────────────────
  const pestOverlap   = totalPests > 0 ? sharedPests.length / totalPests : 0;

  // ── Risk score 0–100 with size normalization ────────────────────────────────
  const sizeFactor    = Math.min(1.0, n / 5);
  const rawScore      = (
    (1 - familyDiversity) * 0.4 +
    pestOverlap          * 0.4 +
    dominantFamilyRatio  * 0.2
  ) * sizeFactor;

  const score         = Math.round(rawScore * 100);
  const riskLevel     = score < 25 ? "low" : score < 55 ? "medium" : "high";

  // ── Warnings ────────────────────────────────────────────────────────────────
  const warnings = [];
  const topFamily = sortedFamilies[0]?.[0];

  if (n >= 3 && dominantFamilyRatio > 0.6) {
    warnings.push(
      `Family dominance: ${topFamily} makes up ${Math.round(dominantFamilyRatio * 100)}% of guild.`
    );
  }
  if (totalPests > 0 && pestOverlap > 0.5) {
    warnings.push(
      `High shared pest load: ${sharedPests.length} of ${totalPests} pests affect multiple guild members.`
    );
  }

  const unresolved = slugs.filter(s => !plantToFamily[s]);
  if (unresolved.length > 0) {
    warnings.push(`Slugs not found in family edges: ${unresolved.join(", ")}.`);
  }

  // ── Suggestions ─────────────────────────────────────────────────────────────
  const suggestions = [];

  if (n >= 3 && dominantFamilyRatio > 0.6) {
    suggestions.push(
      `Reduce ${topFamily} representation — replace one plant with a different family.`
    );
  }
  if (totalPests > 0 && pestOverlap > 0.5) {
    suggestions.push(
      "Introduce Lamiaceae or Asteraceae plants to disrupt shared pest pressure."
    );
  }
  if (familyDiversity < 0.5) {
    suggestions.push(
      `Only ${uniqueFamilies} family across ${n} plants — aim for 3–4 distinct families.`
    );
  }
  if (suggestions.length === 0) {
    suggestions.push("Guild composition looks ecologically balanced.");
  }

  return {
    score,
    breakdown: {
      family_diversity:      Math.round(familyDiversity * 1000) / 1000,
      pest_overlap:          Math.round(pestOverlap * 1000) / 1000,
      dominant_family_ratio: Math.round(dominantFamilyRatio * 1000) / 1000,
    },
    risk_level:       riskLevel,
    dominant_families: dominantFamilies,
    shared_pests:     sharedPests,
    warnings,
    suggestions,
  };
}
