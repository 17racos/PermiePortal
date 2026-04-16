# PermiePortal — Enrichment Batch 1 of 3

> **Agent mode only.** ONE session at a time.
> This batch: 20 plants. Total remaining: 51 plants + 243 pest fields.

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

- `src/seeds/plants/currant-data.yml` (10 fields)
- `src/seeds/plants/curry-plant-data.yml` (10 fields)
- `src/seeds/plants/daikon-radish-data.yml` (10 fields)
- `src/seeds/plants/dragon-fruit-data.yml` (10 fields)
- `src/seeds/plants/eggplant-data.yml` (10 fields)
- `src/seeds/plants/feverfew-data.yml` (10 fields)
- `src/seeds/plants/florida-betony-data.yml` (10 fields)
- `src/seeds/plants/hairy-vetch-data.yml` (10 fields)
- `src/seeds/plants/hawthorn-data.yml` (10 fields)
- `src/seeds/plants/hummingbird-sage-data.yml` (10 fields)
- `src/seeds/plants/jackbean-data.yml` (10 fields)
- `src/seeds/plants/kiwi-data.yml` (10 fields)
- `src/seeds/plants/leek-data.yml` (10 fields)
- `src/seeds/plants/lemon-thyme-data.yml` (10 fields)
- `src/seeds/plants/lettuce-data.yml` (10 fields)
- `src/seeds/plants/mandarin-data.yml` (10 fields)
- `src/seeds/plants/medlar-data.yml` (10 fields)
- `src/seeds/plants/mexican-sunflower-data.yml` (10 fields)
- `src/seeds/plants/mustard-greens-data.yml` (10 fields)
- `src/seeds/plants/oat-data.yml` (10 fields)
---

## When Done

```bash
python3 validate.py --since 2h
python3 validate.py --fix --since 2h
./sync.sh --check
./sync.sh
rm review/cursor_enrich_1_of_3.md
```

Zero warnings required before the next batch.

Next: `cursor_enrich_2_of_3.md`
