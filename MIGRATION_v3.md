# PermiePortal Converter v3 — Migration Guide

## What Changed

### Removed
- `practitioner_notes` — deprecated. Field is ignored if present in YAML.
  Converter emits a warning for every file that still contains it.
  Migrate any content worth keeping into `field_observations`.

### Added to JSON output (new fields on plant records)
- `zone_min` / `zone_max` — parsed from `zone` string. YAML unchanged.
- `companions_unresolved` — quarantined companion strings that failed slug validation.
- `data_quality_score` — float 0.0–1.0, computed by converter, never hand-set.
- `data_quality_dimensions` — dict of boolean checks that compose the score.
- `companions` — now outputs `[{slug, name}]` structured list (was flat string list).

### Changed in relationships.json
Every relationship record now includes:
```json
{
  "id":          "moringa__aphids__plant_pest",
  "type":        "plant_pest",
  "source_slug": "moringa",
  "source_type": "plant",
  "target_slug": "aphids",
  "target_type": "pest",
  "severity":    null,
  "regional":    [],
  "evidence":    "seed_data",
  "plant_slug":  "moringa",
  "plant_name":  "Moringa",
  "pest_slug":   "aphids",
  "pest_name":   "Aphids"
}
```
Legacy fields (`plant_slug`, `plant_name`, `pest_slug`, `pest_name`) are retained.
Existing Astro templates will not break.

---

## Migration Steps

### Step 1 — Deploy new converter
```bash
cp convert_permie_data.py convert_permie_data.py.bak
# copy v3 file into place
./sync.sh --check 2>&1 | head -60
```
Expected output on first run: many warnings about unresolved companions and
purpose formatting. This is correct — the warnings are surfacing real problems.

### Step 2 — Review companions_unresolved
After running `./sync.sh`, check the exports/plants.json for quarantined companions:
```bash
python3 -c "
import json
plants = json.load(open('exports/plants.json'))
has_unresolved = [(p['common_name'], p['companions_unresolved'])
                  for p in plants if p.get('companions_unresolved')]
for name, unres in sorted(has_unresolved, key=lambda x: len(x[1]), reverse=True)[:20]:
    print(f'{name}: {unres}')
print(f'---')
print(f'Total plants with unresolved companions: {len(has_unresolved)}')
"
```

For each unresolved companion, you have three options:
1. Find the correct plant slug and update the YAML to `{slug: x, name: X}` format
2. Leave in `companions_unresolved` — it stays quarantined, visible in data, not linked
3. Remove it from the YAML if it's genuinely a category name (e.g. "Legume Tree")

### Step 3 — Review purpose warnings
```bash
./sync.sh --check 2>&1 | grep "PURPOSE"
```
Fix categories:
- `PURPOSE DUPLICATE` — remove duplicate function lines from YAML purpose block
- `PURPOSE FORMAT` — add ` -- mechanism` to lines missing the separator
- `PURPOSE MISSING` — add purpose line for each plant_function entry that lacks one
- `PURPOSE ORPHAN` — either add to plant_function or remove from purpose

### Step 4 — Review data quality scores
```bash
python3 -c "
import json
plants = json.load(open('exports/plants.json'))
low = [(p['common_name'], p['data_quality_score'], p['data_quality_dimensions'])
       for p in plants if p['data_quality_score'] < 0.5]
low.sort(key=lambda x: x[1])
for name, score, dims in low[:20]:
    failing = [k for k, v in dims.items() if not v and k != 'has_field_observations']
    print(f'{score:.2f}  {name}: {failing}')
print(f'---')
print(f'Plants below 0.5: {len(low)}')
"
```

### Step 5 — Remove practitioner_notes from YAML seeds
Once you've confirmed no content worth keeping was lost:
```bash
# Find all YAML files with practitioner_notes
grep -rl "practitioner_notes" src/seeds/plants/ | wc -l

# Preview what's in them
grep -A2 "practitioner_notes" src/seeds/plants/*.yml | head -40

# Remove the field (after verifying content above)
# Run this only when confident:
python3 -c "
import re
from pathlib import Path
seeds = Path('src/seeds/plants')
count = 0
for f in seeds.glob('*.yml'):
    text = f.read_text()
    if 'practitioner_notes' in text:
        # Remove field and its value (handles multi-line values too)
        cleaned = re.sub(r'\n  practitioner_notes:.*?(?=\n  [a-z]|\Z)', '', text, flags=re.DOTALL)
        f.write_text(cleaned)
        count += 1
print(f'Cleaned {count} files')
"
```

---

## YAML Companion Format — Migration

### Old format (still accepted during migration)
```yaml
companions:
  - Banana
  - Papaya
  - Legume Tree
```

### New format (target)
```yaml
companions:
  - slug: banana
    name: Banana
  - slug: papaya
    name: Papaya
companions_unresolved:
  - "Legume Tree"
```

The converter handles both formats. String-list companions are auto-resolved
if the slugified string matches a known plant. If not, they go to
`companions_unresolved` with a warning.

**Migration priority:** Update companions in YAML as you review each plant.
Do not do a bulk automated conversion — each entry needs human verification.

---

## Data Quality Dimensions Reference

| Dimension | Check | Weight |
|---|---|---|
| `description_length` | description >= 400 chars | equal |
| `description_clean` | no emoji headers, no baked-in bullets | equal |
| `purpose_present` | purpose field >= 50 chars | equal |
| `purpose_format` | all lines match `Name: desc -- mechanism` | equal |
| `purpose_aligned` | purpose ↔ plant_function fully bidirectional | equal |
| `functions_count` | >= 3 plant_function entries | equal |
| `functions_valid` | all values in VALID_FUNCTIONS canonical set | equal |
| `companions_present` | >= 2 resolved companions | equal |
| `pests_present` | >= 1 pest reference | equal |
| `scientific_name` | non-empty, not NEEDS_DATA | equal |
| `zone_present` | zone parses to zone_min/zone_max | equal |
| `no_needs_data` | zero NEEDS_DATA tokens in record | equal |
| `has_field_observations` | **tracked, not penalized** | bonus signal |

Score = sum(passing checks) / 12

---

## Relationship Schema — Future Extension

To add plant↔plant companion relationships later:
```json
{
  "id":          "moringa__banana__plant_companion",
  "type":        "plant_companion",
  "source_slug": "moringa",
  "source_type": "plant",
  "target_slug": "banana",
  "target_type": "plant",
  "severity":    null,
  "regional":    [],
  "evidence":    "seed_data"
}
```

No schema change required. The `type` field already discriminates.
Astro templates filter by `type` to separate pest relationships from companion relationships.

---

## VALID_FUNCTIONS Canonical Set

These are the only valid values for `plant_function`.
Any other value generates a warning.

```
Edible, Medicinal, Nitrogen Fixer, Dynamic Accumulator, Mulcher,
Pollinator, Wildlife Attractor, Erosion Control, Animal Fodder,
Windbreaker, Border Plant, Pest Management, Ground Cover,
Shade Provider, Water Retention, Fiber, Biomass, Aquatic,
Ornamental, Water Purification, Plant Growth Stimulant
```

To add a new function: update `VALID_FUNCTIONS` in `convert_permie_data.py`.
Do not add ad-hoc values to YAML without updating this set first.
