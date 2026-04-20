#!/usr/bin/env python3
"""
patch_pest_family_index.py
==========================
Adds "Family Exposure" section to src/pages/pests/[slug].astro
using pest_family_index from families.json.

Shows: which plant families are most affected by this pest,
sorted by exposure ratio (affected / family_total).
"""
from pathlib import Path

f = Path("src/pages/pests/[slug].astro")
text = f.read_text()

# ── PATCH 1: Add families.json import ────────────────────────────────────────
OLD_IMPORT = "import pestsData from '../../data/pests.json';"
NEW_IMPORT = ("import pestsData from '../../data/pests.json';\n"
              "import familiesRaw from '../../data/families.json';")

if OLD_IMPORT in text and "familiesRaw" not in text:
    text = text.replace(OLD_IMPORT, NEW_IMPORT)
    print("✅ Patch 1: families.json import added")
else:
    print("⏭️  Patch 1: already applied or anchor not found")

# ── PATCH 2: Resolve pest_family_index entry in frontmatter ──────────────────
# Insert after const { pest } = Astro.props;
OLD_PROPS = "const { pest } = Astro.props;"
NEW_PROPS = """const { pest } = Astro.props;

// Resolve family exposure data for this pest from pest_family_index
const pestFamilyIndex = familiesRaw.pest_family_index || {};
const familyExposure = pestFamilyIndex[pest.name] || null;

// Build family canonical name lookup
const familyNodes = familiesRaw.families || [];
const familyBySlug: Record<string, string> = {};
for (const f of familyNodes) {
  familyBySlug[f.slug] = f.canonical_name;
}"""

if OLD_PROPS in text and "pestFamilyIndex" not in text:
    text = text.replace(OLD_PROPS, NEW_PROPS)
    print("✅ Patch 2: pest_family_index resolution added")
else:
    print("⏭️  Patch 2: already applied or anchor not found")

# ── PATCH 3: Add Family Exposure section before the closing </div> ─────────
# Insert after the affected_plants section
OLD_ANCHOR = """</div>
<footer class="footer">
  <div class="footer-logo">PermiePortal</div>
  <div class="footer-copy">© {new Date().getFullYear()} PermiePortal</div>
</footer>"""

NEW_ANCHOR = """</div>

  {familyExposure && familyExposure.families && familyExposure.families.length > 0 && (
    <div class="section">
      <p class="section-label">Family Risk Profile</p>
      <h2 class="section-title">Plant Families Affected</h2>
      <p style="font-size:0.9rem; color:var(--ash); margin-bottom:1.5rem; font-style:italic;">
        {familyExposure.total_plants_affected} plants affected across {familyExposure.families.length} families.
        Exposure = affected plants / total family plants in database.
      </p>
      <div class="family-exposure-grid">
        {familyExposure.families
          .sort((a: any, b: any) => b.exposure - a.exposure)
          .slice(0, 12)
          .map((fam: any) => (
            <a href={`/plants/family/${fam.family_slug}`} class="family-exposure-card">
              <div class="family-exposure-header">
                <div class="family-exposure-name">
                  {familyBySlug[fam.family_slug] || fam.family_slug}
                </div>
                <div class="family-exposure-pct">
                  {Math.round(fam.exposure * 100)}%
                </div>
              </div>
              <div class="family-exposure-count">{fam.plant_count} plants</div>
              <div class="family-exposure-bar">
                <div class="family-exposure-fill"
                     style={`width:${Math.min(100, Math.round(fam.exposure * 100))}%`}>
                </div>
              </div>
            </a>
          ))
        }
      </div>
    </div>
  )}

<footer class="footer">
  <div class="footer-logo">PermiePortal</div>
  <div class="footer-copy">© {new Date().getFullYear()} PermiePortal</div>
</footer>"""

if OLD_ANCHOR in text and "family-exposure-grid" not in text:
    text = text.replace(OLD_ANCHOR, NEW_ANCHOR)
    print("✅ Patch 3: family exposure section added")
else:
    print("⏭️  Patch 3: already applied or anchor not found")

# ── PATCH 4: Add CSS for family exposure cards ───────────────────────────────
OLD_CSS_ANCHOR = "  .footer { padding: 2rem 4rem;"
NEW_CSS = """  .family-exposure-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(220px, 1fr)); gap: 0.6rem; }
  .family-exposure-card { display: block; text-decoration: none; padding: 0.9rem 1.1rem; background: var(--bark); border: 1px solid rgba(212,168,67,0.15); transition: all 0.2s; }
  .family-exposure-card:hover { border-color: rgba(212,168,67,0.4); background: rgba(42,61,31,0.15); }
  .family-exposure-header { display: flex; justify-content: space-between; align-items: baseline; margin-bottom: 0.25rem; }
  .family-exposure-name { font-family: 'Space Mono', monospace; font-size: 0.72rem; color: var(--paper); letter-spacing: 0.04em; }
  .family-exposure-pct { font-family: 'Bebas Neue', sans-serif; font-size: 1.1rem; color: var(--straw); }
  .family-exposure-count { font-size: 0.72rem; color: var(--ash); margin-bottom: 0.5rem; }
  .family-exposure-bar { height: 2px; background: rgba(212,168,67,0.15); border-radius: 1px; }
  .family-exposure-fill { height: 100%; background: var(--straw); border-radius: 1px; }
  .footer { padding: 2rem 4rem;"""

if OLD_CSS_ANCHOR in text and "family-exposure-grid" not in text:
    text = text.replace(OLD_CSS_ANCHOR, NEW_CSS)
    print("✅ Patch 4: CSS added for family exposure cards")
else:
    print("⏭️  Patch 4: already applied or anchor not found")

f.write_text(text)
print("\nDone — run: npm run build 2>&1 | grep -E 'error|Error|built' | tail -5")
