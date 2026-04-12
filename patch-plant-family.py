#!/usr/bin/env python3
"""Add family display to plant slug page."""
from pathlib import Path

f = Path("src/pages/plants/[slug].astro")
content = f.read_text()

# Add family tag CSS after .tag.layer
old_css = "  .tag.layer { background: rgba(122,59,30,0.3); border-color: rgba(196,85,26,0.4); color: var(--straw); }"
new_css = """  .tag.layer { background: rgba(122,59,30,0.3); border-color: rgba(196,85,26,0.4); color: var(--straw); }
  .tag.family { background: rgba(28,24,18,0.8); border-color: rgba(212,168,67,0.3); color: var(--straw); text-decoration: none; }
  .tag.family:hover { border-color: var(--straw); color: var(--paper); }"""

# Add family slug computation to frontmatter
old_front = "const imagePath = plant.picture ? `/assets/plants/${plant.picture}` : null;"
new_front = """const imagePath = plant.picture ? `/assets/plants/${plant.picture}` : null;
const familySlug = plant.family ? plant.family.toLowerCase().replace(/[^a-z0-9]+/g, '-') : null;"""

# Add family tag in the tags section
old_tags = """    <div class="plant-tags">
      {(plant.layers || []).map((l: string) => <span class="tag layer">{l}</span>)}
      {(plant.plant_function || []).map((fn: string) => <span class="tag">{fn}</span>)}
    </div>"""
new_tags = """    <div class="plant-tags">
      {(plant.layers || []).map((l: string) => <span class="tag layer">{l}</span>)}
      {plant.family && familySlug && (
        <a href={`/plants/family/${familySlug}`} class="tag family">{plant.family}</a>
      )}
      {(plant.plant_function || []).map((fn: string) => <span class="tag">{fn}</span>)}
    </div>"""

fixes = 0
for old, new in [(old_css, new_css), (old_front, new_front), (old_tags, new_tags)]:
    if old in content:
        content = content.replace(old, new)
        fixes += 1
    else:
        print(f"⚠️  Not found: {old[:50]}")

if fixes > 0:
    f.write_text(content)
    print(f"✅ Plant slug page updated ({fixes}/3 fixes applied)")
