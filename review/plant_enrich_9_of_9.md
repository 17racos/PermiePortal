# Plant Enrichment — Batch 9 of 9

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

## Files to Enrich (14 files, 140 total NEEDS_DATA fields)

- `src/seeds/plants/tickseed-sunflower-data.yml` (10 fields)
- `src/seeds/plants/tuberous-nasturtium-data.yml` (10 fields)
- `src/seeds/plants/turkish-rocket-data.yml` (10 fields)
- `src/seeds/plants/twinflower-data.yml` (10 fields)
- `src/seeds/plants/verbena-bonariensis-data.yml` (10 fields)
- `src/seeds/plants/walking-onion-data.yml` (10 fields)
- `src/seeds/plants/wax-myrtle-data.yml` (10 fields)
- `src/seeds/plants/wild-mustard-greens-data.yml` (10 fields)
- `src/seeds/plants/wild-olive-data.yml` (10 fields)
- `src/seeds/plants/wild-sweet-potato-data.yml` (10 fields)
- `src/seeds/plants/yam-daisy-data.yml` (10 fields)
- `src/seeds/plants/yellow-sweet-clover-data.yml` (10 fields)
- `src/seeds/plants/yellowhorn-tree-data.yml` (10 fields)
- `src/seeds/plants/yerba-santa-data.yml` (10 fields)

---

## When Done

```bash
./sync.sh --check
```
Fix any pest name warnings, then:
```bash
./sync.sh
```

✅ All batches complete!
