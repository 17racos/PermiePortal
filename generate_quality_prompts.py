#!/usr/bin/env python3
"""
Generate quality enrichment prompts for the 35 plants needing real improvement.
Run from project root: python3 generate_quality_prompts.py
"""

import json
from pathlib import Path

plants = json.load(open('src/data/plants.json'))

SPECIALIST = {
    'Air Potato', 'Singapore Daisy', 'Water Hyacinth', 'Fennel',
    'Venus Flytrap', 'Bladderwort', 'Nepenthes', 'Pitcher Plant',
    'Chaga Host', 'Turkey Tail Host', 'Reishi Host', 'Cordyceps Host',
    'Stinging Tree', 'Kratom', 'Duckweed', 'Floating Heart',
    'Water Lettuce', 'Milkweed'
}

thin = [
    p for p in plants
    if len(p.get('description', '')) < 400
    or len(p.get('companions', [])) < 3
    or len(p.get('plant_function', [])) < 3
]

needs_work = sorted(
    [p for p in thin if p['common_name'] not in SPECIALIST],
    key=lambda x: x['common_name']
)

REVIEW = Path("review")
REVIEW.mkdir(exist_ok=True)

# Clean up old quality prompts
for f in REVIEW.glob("quality_enrichment_*.md"):
    f.unlink()

CHUNK = 12  # smaller chunks = better Agent quality
chunks = [needs_work[i:i+CHUNK] for i in range(0, len(needs_work), CHUNK)]

HEADER = """# Plant Quality Enrichment — Batch {i} of {total}

> **Agent mode only.** Improve existing entries to match Moringa quality.
> Do NOT create new files. Only edit the listed YAML files.

---

## Reference Standard

Open `src/seeds/plants/moringa-data.yml` — this is the quality bar.
Every plant you improve should reach this level of detail.

## Geographic Context

**Florida and Puerto Rico (zones 8b–13)**
- Do NOT say "North Florida" — say "Florida and Puerto Rico" or "subtropical/tropical"
- Puerto Rico: year-round tropical, dry season Dec–Apr, wet season May–Nov
- Florida: humid subtropical, brief cool winters in zones 8b–9, fully tropical in 10–11
- Many plants thrive year-round in PR that go dormant in FL — note both where relevant

## Quality Standards

### description (minimum 400 characters, structured):
```
[Plant name] is a [growth habit] native to [origin]. [Appearance, mature size].
[Ecological role / traditional use / why it matters].

☀️💧 Sun and Water Requirements:
- [Sun preference]
- [Water needs, drought/flood tolerance]
- [Soil preferences]

✂️ Propagation:
- [Method 1 with timing]
- [Method 2 with timing]
- [Method 3 if applicable]

🌾 Harvest / Best Use Timing:
- [When and how to harvest or use]
```

### purpose (explain HOW each function works):
Not just a list — explain the permaculture role. Example:
- Nitrogen Fixer: Root nodules host Rhizobium bacteria that convert atmospheric N₂ into plant-available nitrates, feeding neighboring plants via root exudates and leaf drop.

### companions (minimum 3 specific species):
- Use actual species names, not categories like "nitrogen-fixing plants"
- Include WHY they companion (e.g., "Moringa — provides dappled shade in dry season")

### plant_function (minimum 3):
Valid values (use exact spelling):
Edible, Medicinal, Nitrogen Fixer, Dynamic Accumulator, Mulcher,
Pollinator, Wildlife Attractor, Erosion Control, Animal Fodder,
Windbreaker, Border Plant, Pest Management, Ground Cover, Shade Provider,
Water Retention, Fiber, Dye Plant, Biomass, Aquatic, Ornamental

### pests:
- Must exactly match names in `src/seeds/pests/pests-data.yml`
- Grep to confirm before adding
- Minimum 2 for any cultivated plant

---

## Plants to Improve

"""

FOOTER = """
---

## When Done

```bash
./sync.sh --check
```

Fix any warnings about pest names, then:

```bash
./sync.sh
```

{next_batch}
"""

for i, chunk in enumerate(chunks, 1):
    path = REVIEW / f"quality_enrichment_{i}_of_{len(chunks)}.md"
    
    lines = [HEADER.format(i=i, total=len(chunks))]
    
    for p in chunk:
        slug = p['slug']
        dlen = len(p.get('description', ''))
        clen = len(p.get('companions', []))
        flen = len(p.get('plant_function', []))
        
        issues = []
        if dlen < 400:
            issues.append(f"description only {dlen} chars — needs full structured entry")
        if clen < 3:
            issues.append(f"only {clen} companions — needs 3+ specific species")
        if flen < 3:
            issues.append(f"only {flen} functions — needs 3+ permaculture roles")
        
        lines.append(f"### {p['common_name']}\n")
        lines.append(f"File: `src/seeds/plants/{slug}-data.yml`\n\n")
        lines.append("Issues:\n")
        for issue in issues:
            lines.append(f"- {issue}\n")
        lines.append("\n")
    
    if i < len(chunks):
        next_batch = f"Then open `quality_enrichment_{i+1}_of_{len(chunks)}.md` for the next batch."
    else:
        next_batch = "✅ All batches complete! Run `./sync.sh` to rebuild the full database."
    
    lines.append(FOOTER.format(next_batch=next_batch))
    path.write_text(''.join(lines))

print(f"✅ Generated {len(chunks)} quality enrichment prompts in review/")
print(f"   {len(needs_work)} plants to improve across {len(chunks)} Agent sessions")
print(f"   Chunk size: {CHUNK} plants per session")
print()
print("Files written:")
for i in range(1, len(chunks)+1):
    chunk = needs_work[(i-1)*CHUNK:i*CHUNK]
    print(f"  quality_enrichment_{i}_of_{len(chunks)}.md — {len(chunk)} plants")
print()
print("Run Agent sessions sequentially:")
print("  1. Open review/quality_enrichment_1_of_N.md in Cursor Agent")
print("  2. Let it complete")
print("  3. Run ./sync.sh --check")
print("  4. Move to next batch")
