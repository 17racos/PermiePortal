# PermiePortal — Enrichment Batch 2 of 2

> **Agent mode only.** ONE session at a time.
> This batch: 3 plants. Total remaining: 23 plants + 243 pest fields.

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

- `src/seeds/plants/vietnamese-mint-data.yml` (11 fields)
- `src/seeds/plants/water-hickory-data.yml` (11 fields)
- `src/seeds/plants/wild-rice-data.yml` (11 fields)

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
rm review/cursor_enrich_2_of_2.md
```

Zero warnings required before the next batch.

✅ Final batch — commit:
```bash
git add -A && git commit -m 'enrichment complete'
```
