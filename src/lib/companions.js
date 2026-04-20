/**
 * src/lib/companions.js
 * NOTE: Not currently rendered on plant profile pages.
 * Intended for future Guild Builder integration — suggest next plants,
 * swaps, and diversity improvements based on guild composition.
 * =====================
 * suggestCompanions(targetPlantSlug, plants, relationships) — data-driven companion finder.
 *
 * Logic: find plants with MINIMAL shared pests and DIFFERENT families.
 * No folklore. No hardcoded rules. Pure exclusion logic from graph data.
 */

/**
 * Suggest companion plants for a target plant.
 *
 * @param {string} targetPlantSlug
 * @param {object[]} plants - plants array from plants.json
 * @param {object[]} relationships - relationships array
 * @returns {{
 *   target_slug: string,
 *   target_family: string|null,
 *   suggestions: {
 *     slug: string,
 *     common_name: string,
 *     family: string,
 *     shared_pest_count: number,
 *     same_family: boolean,
 *     score: number
 *   }[]
 * }}
 */
export function suggestCompanions(targetPlantSlug, plants, relationships) {
  // ── Build indexes ──────────────────────────────────────────────────────────
  const plantBySlug   = {};
  for (const p of plants) {
    plantBySlug[p.slug] = p;
  }

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

  const targetPests  = plantToPests[targetPlantSlug] || new Set();
  const targetFamily = plantToFamily[targetPlantSlug] || null;

  // ── Score every other plant ─────────────────────────────────────────────────
  const candidates = [];

  for (const p of plants) {
    if (p.slug === targetPlantSlug) continue;
    if (!plantBySlug[p.slug]) continue;

    const candidatePests  = plantToPests[p.slug] || new Set();
    const candidateFamily = plantToFamily[p.slug] || null;

    // Count shared pests
    let sharedPestCount = 0;
    for (const pest of targetPests) {
      if (candidatePests.has(pest)) sharedPestCount++;
    }

    const sameFamilyPenalty = (candidateFamily && candidateFamily === targetFamily) ? 1 : 0;

    // Score: lower = better companion
    // Penalise shared pests heavily, penalise same family lightly
    const score = sharedPestCount * 10 + sameFamilyPenalty * 3;

    candidates.push({
      slug:              p.slug,
      common_name:       p.common_name,
      family:            candidateFamily || "",
      shared_pest_count: sharedPestCount,
      same_family:       sameFamilyPenalty === 1,
      score,
    });
  }

  // ── Sort: lowest score first, then alphabetical for determinism ─────────────
  candidates.sort((a, b) => a.score - b.score || a.common_name.localeCompare(b.common_name));

  return {
    target_slug:   targetPlantSlug,
    target_family: targetFamily,
    suggestions:   candidates.slice(0, 5),
  };
}
