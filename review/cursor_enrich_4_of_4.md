# PermiePortal — Enrichment Batch 4 of 4

## YOUR TASK
You are Cursor Agent in Agent mode. Your job is to:
1. Open each YAML file listed under "Plants to Enrich" below
2. Replace every `NEEDS_DATA` field with accurate botanical data
3. Follow the standards exactly as written
4. Run the validation commands in "When Done"
5. Delete this file when done

Do NOT ask clarifying questions. Start editing immediately.

> **Agent mode only.** ONE session at a time.
> This batch: 11 plants. Total remaining: 71 plants + 243 pest fields.

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

- `src/seeds/plants/turmeric-ginger-data.yml` (11 fields)
- `src/seeds/plants/turnip-data.yml` (11 fields)
- `src/seeds/plants/velvet-bean-data.yml` (11 fields)
- `src/seeds/plants/water-mimosa-data.yml` (11 fields)
- `src/seeds/plants/watermelon-data.yml` (11 fields)
- `src/seeds/plants/wheat-data.yml` (11 fields)
- `src/seeds/plants/white-clover-data.yml` (11 fields)
- `src/seeds/plants/winter-rye-data.yml` (11 fields)
- `src/seeds/plants/winter-savory-data.yml` (11 fields)
- `src/seeds/plants/winter-squash-data.yml` (11 fields)
- `src/seeds/plants/zucchini-data.yml` (11 fields)

## Pests to Enrich (0 files, 243 fields)

Use `src/seeds/pests/aphids-data.yml` as the gold standard reference.

**Voice:** Lifecycle-aware, actionable, accessible. No generic slop.

**Required fields for each pest:**
- description: 2-3 sentences, what it is and first sign of damage
- characteristics: what to look for, how to confirm identity
- symptoms: 2-5 tags from: holes-in-leaves, yellowing-leaves, wilting,
  sticky-residue, white-powder, leaf-spots, curling-leaves, webbing,
  chewed-stems, stem-damage, root-damage, fruit-damage, black-coating,
  distorted-growth, tunneling, galls, dropping-leaves, silvery-streaking,
  brown-edges, die-back, sooty-deposits, slime-trails, skeletonized-leaves,
  bark-damage, crown-damage
- control_methods: biological_controls, preventive_methods,
  cultural_practices, mechanical_physical, organic_sprays
  Each section min 4 sentences. Use ' -- ' not em dashes.
- natural_enemies: real predators/parasitoids only

**Files to enrich:**

---

## When Done

```bash
python3 validate.py --since 2h
python3 validate.py --fix --since 2h
./sync.sh --check
./sync.sh
rm review/cursor_enrich_4_of_4.md
```

Zero warnings required before the next batch.

✅ Final batch — commit:
```bash
git add -A && git commit -m 'enrichment complete'
```
