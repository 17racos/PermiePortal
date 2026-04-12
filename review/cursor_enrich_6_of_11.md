# PermiePortal — Enrichment Batch 6 of 11

> **Agent mode only.** ONE session at a time.
> This batch: 20 plants. Total remaining: 211 plants + 0 pest fields.

---

## Reference

Use `src/seeds/plants/moringa-data.yml` as the quality standard.

---

## Geographic Context

**Audience: All of the Americas — zones 3–13**
- Do NOT write 'North Florida' or any single state/region framing
- Use universal climate language: 'temperate', 'subtropical', 'tropical'
- Use 'wet season / dry season' not 'spring / fall' where relevant
- Temperatures: Fahrenheit with Celsius in parentheses — 32°F (0°C)

---

## Standards

**description** (min 400 chars):
1. What the plant is, origin, appearance, mature size
2. ☀️💧 Sun and Water Requirements
3. ✂️ Propagation (2+ methods with timing)
4. 🌾 Harvest / Best Use Timing

**purpose** — explain HOW each function works in a permaculture system

**companions** — min 3 specific species with reason WHY
NOT categories like 'nitrogen-fixing plants' or 'legumes'

**cautions** — antagonistic plants OR growing condition warnings (both valid)
'None documented' acceptable if genuinely true

**plant_function** — min 3 from:
Edible, Medicinal, Nitrogen Fixer, Dynamic Accumulator, Mulcher,
Pollinator, Wildlife Attractor, Erosion Control, Animal Fodder,
Windbreaker, Border Plant, Pest Management, Ground Cover,
Shade Provider, Water Retention, Fiber, Biomass, Aquatic, Ornamental

**pests** — ONLY names verbatim from `src/seeds/pests/pests-data.yml`
grep to confirm before adding. Min 2 cultivated plants. [] for specialists.
NEVER: None, NEEDS_DATA, or animals without pest profiles

---

## Plants to Enrich

- `src/seeds/plants/lowbush-cranberry-data.yml` (11 fields)
- `src/seeds/plants/malay-apple-data.yml` (11 fields)
- `src/seeds/plants/many-flowered-cotoneaster-data.yml` (11 fields)
- `src/seeds/plants/marang-fruit-data.yml` (11 fields)
- `src/seeds/plants/marsh-blazingstar-data.yml` (11 fields)
- `src/seeds/plants/mexican-elderberry-data.yml` (11 fields)
- `src/seeds/plants/monkey-fruit-data.yml` (11 fields)
- `src/seeds/plants/morinda-citrifolia-data.yml` (11 fields)
- `src/seeds/plants/mountain-apple-data.yml` (11 fields)
- `src/seeds/plants/munson-plum-data.yml` (11 fields)
- `src/seeds/plants/neem-tree-data.yml` (11 fields)
- `src/seeds/plants/nelumbo-lutea-data.yml` (11 fields)
- `src/seeds/plants/noni-fruit-data.yml` (11 fields)
- `src/seeds/plants/ohio-spiderwort-data.yml` (11 fields)
- `src/seeds/plants/orange-coneflower-data.yml` (11 fields)
- `src/seeds/plants/otaheite-apple-data.yml` (11 fields)
- `src/seeds/plants/pale-purple-coneflower-data.yml` (11 fields)
- `src/seeds/plants/panama-candle-tree-data.yml` (11 fields)
- `src/seeds/plants/parsley-hawthorn-data.yml` (11 fields)
- `src/seeds/plants/pasture-rose-data.yml` (11 fields)
---

## When Done

```bash
python3 validate.py --since 2h
python3 validate.py --fix --since 2h
./sync.sh --check
./sync.sh
rm review/cursor_enrich_6_of_11.md
```

Zero warnings required before the next batch.

Next: `cursor_enrich_7_of_11.md`
