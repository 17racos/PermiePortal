#!/usr/bin/env python3
"""
patch_family_page.py
====================
Upgrades src/pages/plants/family/[family].astro to use families.json
as primary data source for pest_pressure and trait_profile.
Does NOT redesign the page — only wires in the graph data.
"""
from pathlib import Path

f = Path("src/pages/plants/family/[family].astro")
text = f.read_text()

# ── PATCH 1: Add families.json import ────────────────────────────────────────
OLD_IMPORT = "import plantsData from '../../../data/plants.json';\nimport pestsData from '../../../data/pests.json';"
NEW_IMPORT = "import plantsData from '../../../data/plants.json';\nimport pestsData from '../../../data/pests.json';\nimport familiesRaw from '../../../data/families.json';"

if OLD_IMPORT in text:
    text = text.replace(OLD_IMPORT, NEW_IMPORT)
    print("✅ Patch 1: families.json import added")
else:
    print("❌ Patch 1: import anchor not found")

# ── PATCH 2: Resolve family node from families.json in getStaticPaths ────────
# Add family node to props
OLD_PATHS = """  return Object.entries(familyMap).map(([slug, plants]) => ({
    params: { family: slug },
    props: { plants, familyName: plants[0].family }
  }));"""

NEW_PATHS = """  const familyNodes = Array.isArray(familiesRaw) ? familiesRaw : (familiesRaw.families || []);
  const familyNodeMap: Record<string, any> = {};
  for (const node of familyNodes) {
    familyNodeMap[node.slug] = node;
  }
  return Object.entries(familyMap).map(([slug, plants]) => ({
    params: { family: slug },
    props: {
      plants,
      familyName: plants[0].family,
      familyNode: familyNodeMap[slug] || null,
    }
  }));"""

if OLD_PATHS in text:
    text = text.replace(OLD_PATHS, NEW_PATHS)
    print("✅ Patch 2: familyNode added to props")
else:
    print("❌ Patch 2: getStaticPaths anchor not found")

# ── PATCH 3: Destructure familyNode from props ────────────────────────────────
OLD_PROPS = "const { plants, familyName } = Astro.props;"
NEW_PROPS = "const { plants, familyName, familyNode } = Astro.props;"

if OLD_PROPS in text:
    text = text.replace(OLD_PROPS, NEW_PROPS)
    print("✅ Patch 3: familyNode destructured from props")
else:
    print("❌ Patch 3: props destructure not found")

# ── PATCH 4: Replace manual pest aggregation with graph data ─────────────────
OLD_PEST_BLOCK = """// Build pest pressure for this family
// Count how many family plants each pest affects
const pestCounts: Record<string, number> = {};
for (const plant of plants) {
  for (const pestName of (plant.pests || [])) {
    pestCounts[pestName] = (pestCounts[pestName] || 0) + 1;
  }
}

// Build pest lookup for slug/scientific_name
const pestLookup: Record<string, any> = {};
for (const pest of pestsData) {
  pestLookup[pest.name] = pest;
}

// Pests affecting at least 20% of family — sorted by coverage
const minCount = Math.max(2, Math.floor(plants.length * 0.2));
const familyPests = Object.entries(pestCounts)
  .filter(([, count]) => count >= minCount)
  .sort((a, b) => b[1] - a[1])
  .slice(0, 15)
  .map(([name, count]) => ({
    name,
    count,
    slug: pestLookup[name]?.slug || name.toLowerCase().replace(/\\s+/g, '-'),
    scientific_name: pestLookup[name]?.scientific_name || '',
    pct: Math.round((count / plants.length) * 100),
  }));"""

NEW_PEST_BLOCK = """// Build pest lookup for slug/scientific_name
const pestLookup: Record<string, any> = {};
for (const pest of pestsData) {
  pestLookup[pest.name] = pest;
}

// Use graph-derived pest pressure from families.json when available
// Falls back to manual aggregation for families not in graph
const graphPestPressure = familyNode?.pest_pressure || null;
const graphTopPests = graphPestPressure?.top_pests || [];

// Build familyPests from graph top_pests (already aggregated + sorted)
// Fall back to manual count if no graph data
const familyPests = (() => {
  if (graphTopPests.length > 0) {
    return graphTopPests
      .filter((p: any) => p.count >= Math.max(2, Math.floor(plants.length * 0.1)))
      .slice(0, 15)
      .map((p: any) => ({
        name: p.name,
        count: p.count,
        slug: pestLookup[p.name]?.slug || p.name.toLowerCase().replace(/\\s+/g, '-'),
        scientific_name: pestLookup[p.name]?.scientific_name || '',
        pct: Math.round((p.count / plants.length) * 100),
      }));
  }
  // Fallback: manual aggregation
  const pestCounts: Record<string, number> = {};
  for (const plant of plants) {
    for (const pestName of (plant.pests || [])) {
      pestCounts[pestName] = (pestCounts[pestName] || 0) + 1;
    }
  }
  const minCount = Math.max(2, Math.floor(plants.length * 0.2));
  return Object.entries(pestCounts)
    .filter(([, count]) => count >= minCount)
    .sort((a, b) => b[1] - a[1])
    .slice(0, 15)
    .map(([name, count]) => ({
      name,
      count: count as number,
      slug: pestLookup[name]?.slug || name.toLowerCase().replace(/\\s+/g, '-'),
      scientific_name: pestLookup[name]?.scientific_name || '',
      pct: Math.round(((count as number) / plants.length) * 100),
    }));
})();

// Graph-derived trait profile
const traitProfile = familyNode?.trait_profile || null;"""

if OLD_PEST_BLOCK in text:
    text = text.replace(OLD_PEST_BLOCK, NEW_PEST_BLOCK)
    print("✅ Patch 4: pest aggregation replaced with graph data")
else:
    print("❌ Patch 4: pest block anchor not found")

# ── PATCH 5: Add trait profile section to stats panel ────────────────────────
OLD_STATS = """    {topLayers.slice(0,3).map(([layer, count]) => (
      <div class="stat-row">
        <div class="stat-label">{layer}</div>
        <div class="stat-value">{count} plants</div>
      </div>
    ))}"""

NEW_STATS = """    {topLayers.slice(0,3).map(([layer, count]) => (
      <div class="stat-row">
        <div class="stat-label">{layer}</div>
        <div class="stat-value">{count} plants</div>
      </div>
    ))}
    {graphPestPressure && (
      <div class="stat-row">
        <div class="stat-label">Avg Pests / Plant</div>
        <div class="stat-value">{graphPestPressure.avg_pests_per_plant}</div>
      </div>
    )}
    {traitProfile && traitProfile.perennial_ratio > 0 && (
      <div class="stat-row">
        <div class="stat-label">Perennial Ratio</div>
        <div class="stat-value">{Math.round(traitProfile.perennial_ratio * 100)}%</div>
      </div>
    )}
    {traitProfile && traitProfile.nitrogen_fixers > 0 && (
      <div class="stat-row">
        <div class="stat-label">Nitrogen Fixers</div>
        <div class="stat-value">{traitProfile.nitrogen_fixers}</div>
      </div>
    )}"""

if OLD_STATS in text:
    text = text.replace(OLD_STATS, NEW_STATS)
    print("✅ Patch 5: graph stats added to stats panel")
else:
    print("❌ Patch 5: stats panel anchor not found")

f.write_text(text)
print("\nDone — run: npm run dev, then visit /plants/family/fabaceae")
