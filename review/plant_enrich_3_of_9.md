# Plant Enrichment — Batch 3 of 9

> **Agent mode only.** Sequential — complete this batch before starting the next.

---

## Reference
Use `src/seeds/plants/moringa-data.yml` as the quality standard.

## Geographic Context
**Florida and Puerto Rico (zones 8b–13)**
- Do NOT write "North Florida" — write "Florida and Puerto Rico" or "subtropical/tropical"
- Puerto Rico: year-round tropical, dry season Dec–Apr, wet season May–Nov
- Florida: humid subtropical to tropical zones 8b–11

## Standards — every field must meet these:

**description** (min 400 chars) must include:
1. What the plant is, origin, appearance, mature size
2. ☀️💧 Sun and Water Requirements
3. ✂️ Propagation (2+ methods with timing)
4. 🌾 Harvest / Best Use Timing

**purpose** — explain HOW each plant_function works in a permaculture system

**companions** — min 3 specific species with reason WHY they companion

**plant_function** — min 3 values from:
Edible, Medicinal, Nitrogen Fixer, Dynamic Accumulator, Mulcher,
Pollinator, Wildlife Attractor, Erosion Control, Animal Fodder,
Windbreaker, Border Plant, Pest Management, Ground Cover,
Shade Provider, Water Retention, Fiber, Biomass, Aquatic, Ornamental

**pests** — must exactly match names in `src/seeds/pests/pests-data.yml`
Run: `grep -i "pest name" src/seeds/pests/pests-data.yml` to confirm before adding
Use empty list `pests: []` if genuinely pest-free

**avoid** — list antagonistic PLANTS not growing conditions
"None documented" is acceptable if genuinely true

---

## Files to Enrich (15 files, 150 total NEEDS_DATA fields)

- `src/seeds/plants/ceylon-gooseberry-tree-data.yml` (10 fields)
- `src/seeds/plants/chiltepin-pepper-data.yml` (10 fields)
- `src/seeds/plants/chiltepin-pepper-tree-data.yml` (10 fields)
- `src/seeds/plants/cistus-data.yml` (10 fields)
- `src/seeds/plants/claytonea-perfoliata-data.yml` (10 fields)
- `src/seeds/plants/coastal-rosemary-data.yml` (10 fields)
- `src/seeds/plants/coffee-senna-data.yml` (10 fields)
- `src/seeds/plants/coralberry-data.yml` (10 fields)
- `src/seeds/plants/coreopsis-data.yml` (10 fields)
- `src/seeds/plants/corsican-stonecrop-data.yml` (10 fields)
- `src/seeds/plants/costmary-data.yml` (10 fields)
- `src/seeds/plants/creeping-phlox-data.yml` (10 fields)
- `src/seeds/plants/creeping-raspberry-data.yml` (10 fields)
- `src/seeds/plants/crown-vetch-data.yml` (10 fields)
- `src/seeds/plants/desert-date-data.yml` (10 fields)

---

## When Done

```bash
./sync.sh --check
```
Fix any pest name warnings, then:
```bash
./sync.sh
```

Then open `plant_enrich_4_of_9.md`
