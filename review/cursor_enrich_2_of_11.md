# PermiePortal — Enrichment Batch 2 of 11

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

- `src/seeds/plants/black-elderberry-data.yml` (11 fields)
- `src/seeds/plants/blue-elderberry-data.yml` (11 fields)
- `src/seeds/plants/blue-grama-data.yml` (11 fields)
- `src/seeds/plants/blue-palmetto-data.yml` (11 fields)
- `src/seeds/plants/blue-tongue-data.yml` (11 fields)
- `src/seeds/plants/blue-wild-indigo-data.yml` (11 fields)
- `src/seeds/plants/breadnut-tree-data.yml` (11 fields)
- `src/seeds/plants/broadleaf-stonecrop-data.yml` (11 fields)
- `src/seeds/plants/broomsedge-bluestem-data.yml` (11 fields)
- `src/seeds/plants/brush-cherry-data.yml` (11 fields)
- `src/seeds/plants/buffalo-plum-data.yml` (11 fields)
- `src/seeds/plants/cabbage-palm-data.yml` (11 fields)
- `src/seeds/plants/canadian-wild-ginger-data.yml` (11 fields)
- `src/seeds/plants/cannonball-tree-data.yml` (11 fields)
- `src/seeds/plants/carambola-tree-data.yml` (11 fields)
- `src/seeds/plants/carolina-rose-data.yml` (11 fields)
- `src/seeds/plants/cempedak-data.yml` (11 fields)
- `src/seeds/plants/chinaberry-data.yml` (11 fields)
- `src/seeds/plants/chokeberry-data.yml` (11 fields)
- `src/seeds/plants/clasping-coneflower-data.yml` (11 fields)
---

## When Done

```bash
python3 validate.py --since 2h
python3 validate.py --fix --since 2h
./sync.sh --check
./sync.sh
rm review/cursor_enrich_2_of_11.md
```

Zero warnings required before the next batch.

Next: `cursor_enrich_3_of_11.md`
