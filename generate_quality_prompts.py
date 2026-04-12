#!/usr/bin/env python3
"""
PermiePortal — Quality Enrichment Prompt Generator
====================================================
Generates Cursor Agent prompts for plants below quality threshold.
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

for f in REVIEW.glob("quality_enrichment_*.md"):
    f.unlink()

if not needs_work:
    print("✅ All plants meet quality threshold — nothing to generate")
    exit(0)

CHUNK = 12
chunks = [needs_work[i:i+CHUNK] for i in range(0, len(needs_work), CHUNK)]

HEADER = """\
# Plant Quality Enrichment — Batch {i} of {total}

> **Agent mode only.** ONE session at a time.
> Improve existing entries only — do NOT create new files.

---

## Reference Standard

Open `src/seeds/plants/moringa-data.yml` — every plant should reach this quality level.

---

## Geographic Context

**Audience: All of the Americas — zones 3–13**
- Do NOT write 'North Florida', 'South Florida', or any single state/region framing
- Use universal climate language: 'temperate', 'subtropical', 'tropical'
- Use 'wet season / dry season' not 'spring / fall' where relevant
- Trust the zone: field to communicate range — don't repeat it unless adding context
- Where regional context adds value: "common throughout the Caribbean and Gulf Coast"
- Temperatures: Fahrenheit with Celsius in parentheses — 32°F (0°C)
- Spanish version planned — write descriptions that translate cleanly, avoid idioms

---

## Quality Standards

### description (minimum 400 characters, all four sections required)

```
[Plant name] is a [growth form] native to [origin]. [Appearance, mature size].
[Why it matters in a permaculture or food system context].

☀️💧 Sun and Water Requirements:
- Sun: [full sun / partial shade / shade tolerant]
- Water: [drought tolerant / moderate / moisture-loving]
- Soil: [preferences and tolerances]

✂️ Propagation:
- [Method 1 with timing]
- [Method 2 with timing]

🌾 Harvest / Best Use Timing:
- [When and how to harvest, or when the plant delivers its primary value]
```

### purpose
Explain HOW each plant_function works in a permaculture system — not just a list.
Example: "Nitrogen Fixer: Root nodules host Rhizobium bacteria that fix atmospheric
N₂ into plant-available nitrates, feeding neighboring plants via root exudates."

### companions (minimum 3 specific species)
- Actual species names — NOT categories like 'nitrogen-fixing plants', 'legumes',
  'fruit trees', 'herbs', 'ground covers', or 'tropical plants'
- Include WHY: what functional benefit the pairing provides

### cautions
- Antagonistic plants OR specific growing condition warnings — both valid
- PermieBro voice encouraged: be specific and direct
- 'None documented' acceptable if genuinely true

### plant_function (minimum 3, exact values only)
Edible, Medicinal, Nitrogen Fixer, Dynamic Accumulator, Mulcher,
Pollinator, Wildlife Attractor, Erosion Control, Animal Fodder,
Windbreaker, Border Plant, Pest Management, Ground Cover, Shade Provider,
Water Retention, Fiber, Biomass, Aquatic, Ornamental, Dye Plant

### pests
- ONLY names verbatim from `src/seeds/pests/pests-data.yml`
- grep to confirm before adding: `grep -i "name" src/seeds/pests/pests-data.yml`
- Minimum 2 for cultivated plants — pests: [] for specialist plants only
- NEVER: None, None documented, NEEDS_DATA, or animals without pest profiles

---

## Mandatory Workflow After Each Batch

```bash
python3 validate.py --since 2h
python3 validate.py --fix --since 2h
./sync.sh --check
./sync.sh
rm review/{filename}
```

Zero warnings required before moving to the next batch.

---

## Plants to Improve ({count} plants)

"""

FOOTER = """\

---

## When Done

```bash
python3 validate.py --since 2h
python3 validate.py --fix --since 2h
./sync.sh --check
./sync.sh
rm review/{filename}
```

{next_batch}
"""

for i, chunk in enumerate(chunks, 1):
    filename = f"quality_enrichment_{i}_of_{len(chunks)}.md"
    path = REVIEW / filename

    lines = [HEADER.format(i=i, total=len(chunks), count=len(chunk), filename=filename)]

    for p in chunk:
        slug = p['slug']
        dlen = len(p.get('description', ''))
        clen = len(p.get('companions', []))
        flen = len(p.get('plant_function', []))

        issues = []
        if dlen < 400:
            issues.append(f"description only {dlen} chars — needs full structured entry")
        if clen < 3:
            issues.append(f"only {clen} companions — needs 3+ specific named species")
        if flen < 3:
            issues.append(f"only {flen} functions — needs 3+ permaculture roles")

        lines.append(f"### {p['common_name']}\n")
        lines.append(f"File: `src/seeds/plants/{slug}-data.yml`\n\n")
        lines.append("Issues:\n")
        for issue in issues:
            lines.append(f"- {issue}\n")
        lines.append("\n")

    if i < len(chunks):
        next_batch = f"Then open `quality_enrichment_{i+1}_of_{len(chunks)}.md`"
    else:
        next_batch = "✅ Final batch — commit when complete:\n```bash\ngit add -A && git commit -m 'quality enrichment complete'\n```"

    lines.append(FOOTER.format(filename=filename, next_batch=next_batch))
    path.write_text(''.join(lines))

print(f"✅ Generated {len(chunks)} quality enrichment prompts in review/")
print(f"   {len(needs_work)} plants to improve, {CHUNK} per Agent session")
print()
for i in range(1, len(chunks) + 1):
    chunk = needs_work[(i-1)*CHUNK:i*CHUNK]
    print(f"  quality_enrichment_{i}_of_{len(chunks)}.md — {len(chunk)} plants")
print()
print("Start: open review/quality_enrichment_1_of_N.md in Cursor Agent")
print("Run sequentially — one session per file, validate between each")
