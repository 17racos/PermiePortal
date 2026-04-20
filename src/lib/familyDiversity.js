/**
 * src/lib/familyDiversity.js
 * ==========================
 * analyzeDiversity(plantSlugs, relationships) — deterministic family diversity checker.
 *
 * Uses ONLY plant_family edges from relationships.json.
 * No re-scanning plants.json for family strings.
 */

/**
 * Analyze family diversity of a set of plants.
 *
 * @param {string[]} plantSlugs
 * @param {object[]} relationships - relationships array (plant_family edges used)
 * @returns {{
 *   total_plants: number,
 *   unique_families: number,
 *   dominant_family: string|null,
 *   dominant_family_count: number,
 *   diversity_score: number,
 *   warning: string|null
 * }}
 */
export function analyzeDiversity(plantSlugs, relationships) {
  const slugs = [...new Set(plantSlugs.map(s => s.trim()).filter(Boolean))];
  const n = slugs.length;

  if (n === 0) {
    return {
      total_plants:          0,
      unique_families:       0,
      dominant_family:       null,
      dominant_family_count: 0,
      diversity_score:       0,
      warning:               "No plants provided.",
    };
  }

  // ── Build plant → family index from edges ────────────────────────────────
  const plantToFamily = {};
  for (const r of relationships) {
    if (r.type === "plant_family") {
      plantToFamily[r.source_slug] = r.target_slug;
    }
  }

  // ── Count families ───────────────────────────────────────────────────────
  const familyCounts = {};
  for (const s of slugs) {
    const fam = plantToFamily[s];
    if (fam) {
      familyCounts[fam] = (familyCounts[fam] || 0) + 1;
    }
  }

  const uniqueFamilies = Object.keys(familyCounts).length;

  // Dominant family (deterministic: sort by count desc, then name asc)
  const sorted = Object.entries(familyCounts)
    .sort((a, b) => b[1] - a[1] || a[0].localeCompare(b[0]));

  const dominantFamily      = sorted[0]?.[0] || null;
  const dominantFamilyCount = sorted[0]?.[1] || 0;
  const dominantRatio       = dominantFamilyCount / n;

  // diversity_score: unique_families / total_plants, capped at 1
  const diversityScore = Math.min(1, Math.round((uniqueFamilies / n) * 1000) / 1000);

  // ── Warning ──────────────────────────────────────────────────────────────
  let warning = null;

  if (dominantRatio > 0.5) {
    warning = `${dominantFamily} makes up ${Math.round(dominantRatio * 100)}% of plants — consider diversifying families.`;
  } else if (uniqueFamilies < 3) {
    warning = `Only ${uniqueFamilies} unique family/families — aim for 3 or more for ecological resilience.`;
  }

  return {
    total_plants:          n,
    unique_families:       uniqueFamilies,
    dominant_family:       dominantFamily,
    dominant_family_count: dominantFamilyCount,
    diversity_score:       diversityScore,
    warning,
  };
}
