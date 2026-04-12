# PermiePortal — Enrichment Batch 5 of 11

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

- `src/seeds/plants/highbush-cranberry-data.yml` (11 fields)
- `src/seeds/plants/hog-plum-data.yml` (11 fields)
- `src/seeds/plants/hortulan-plum-data.yml` (11 fields)
- `src/seeds/plants/indian-mulberry-data.yml` (11 fields)
- `src/seeds/plants/indiangrass-data.yml` (11 fields)
- `src/seeds/plants/jakfruit-data.yml` (11 fields)
- `src/seeds/plants/java-apple-data.yml` (11 fields)
- `src/seeds/plants/june-plum-data.yml` (11 fields)
- `src/seeds/plants/kedondong-data.yml` (11 fields)
- `src/seeds/plants/ketapang-data.yml` (11 fields)
- `src/seeds/plants/key-thatch-palm-data.yml` (11 fields)
- `src/seeds/plants/leavenworths-tickseed-data.yml` (11 fields)
- `src/seeds/plants/lemon-beebalm-data.yml` (11 fields)
- `src/seeds/plants/lilly-pilly-data.yml` (11 fields)
- `src/seeds/plants/lingonberry-data.yml` (11 fields)
- `src/seeds/plants/little-bluestem-data.yml` (11 fields)
- `src/seeds/plants/little-brown-jug-data.yml` (11 fields)
- `src/seeds/plants/loblolly-pine-data.yml` (11 fields)
- `src/seeds/plants/longawn-muhly-data.yml` (11 fields)
- `src/seeds/plants/longleaf-pine-data.yml` (11 fields)
---

## When Done

```bash
python3 validate.py --since 2h
python3 validate.py --fix --since 2h
./sync.sh --check
./sync.sh
rm review/cursor_enrich_5_of_11.md
```

Zero warnings required before the next batch.

Next: `cursor_enrich_6_of_11.md`
