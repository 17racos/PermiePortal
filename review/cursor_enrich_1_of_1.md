# PermiePortal — Enrichment Batch 1 of 1

> **Agent mode only.** ONE session at a time.
> This batch: 18 plants. Total remaining: 18 plants + 0 pest fields.

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

- `src/seeds/plants/bald-cypress-data.yml` (11 fields)
- `src/seeds/plants/blue-palmetto-data.yml` (11 fields)
- `src/seeds/plants/cabbage-palm-data.yml` (11 fields)
- `src/seeds/plants/coconut-palm-data.yml` (11 fields)
- `src/seeds/plants/coontie-palm-data.yml` (11 fields)
- `src/seeds/plants/dwarf-palmetto-data.yml` (11 fields)
- `src/seeds/plants/florida-thatch-palm-data.yml` (11 fields)
- `src/seeds/plants/key-thatch-palm-data.yml` (11 fields)
- `src/seeds/plants/loblolly-pine-data.yml` (11 fields)
- `src/seeds/plants/longleaf-pine-data.yml` (11 fields)
- `src/seeds/plants/pond-pine-data.yml` (11 fields)
- `src/seeds/plants/ribbon-palm-data.yml` (11 fields)
- `src/seeds/plants/royal-palm-data.yml` (11 fields)
- `src/seeds/plants/sago-palm-data.yml` (11 fields)
- `src/seeds/plants/sand-pine-data.yml` (11 fields)
- `src/seeds/plants/scrub-palmetto-data.yml` (11 fields)
- `src/seeds/plants/slash-pine-data.yml` (11 fields)
- `src/seeds/plants/spruce-pine-data.yml` (11 fields)
---

## When Done

```bash
python3 validate.py --since 2h
python3 validate.py --fix --since 2h
./sync.sh --check
./sync.sh
rm review/cursor_enrich_1_of_1.md
```

Zero warnings required before the next batch.

✅ Final batch — commit:
```bash
git add -A && git commit -m 'enrichment complete'
```
