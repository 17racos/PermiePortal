# PermiePortal — Enrichment Batch 1 of 1

> **Agent mode only.** ONE session at a time.
> This batch: 0 plants. Total remaining: 0 plants + 723 pest fields.

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


## Pests to Enrich (48 files, 723 fields)

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
- `src/seeds/pests/ambrosia-beetles-data.yml` (10 fields)
- `src/seeds/pests/armored-scale-data.yml` (10 fields)
- `src/seeds/pests/bacterial-wilt-data.yml` (10 fields)
- `src/seeds/pests/bark-beetles-data.yml` (10 fields)
- `src/seeds/pests/billbugs-data.yml` (10 fields)
- `src/seeds/pests/black-scale-data.yml` (10 fields)
- `src/seeds/pests/brown-soft-scale-data.yml` (10 fields)
- `src/seeds/pests/bulb-mites-data.yml` (10 fields)
- `src/seeds/pests/calcium-deficiency-data.yml` (10 fields)
- `src/seeds/pests/chafer-grubs-data.yml` (10 fields)
- `src/seeds/pests/chinch-bugs-data.yml` (10 fields)
- `src/seeds/pests/cottony-cushion-scale-data.yml` (10 fields)
- `src/seeds/pests/crane-fly-larvae-data.yml` (10 fields)
- `src/seeds/pests/cuban-tree-frog-data.yml` (10 fields)
- `src/seeds/pests/cutworm-larvae-data.yml` (10 fields)
- `src/seeds/pests/florida-wax-scale-data.yml` (10 fields)
- `src/seeds/pests/fungus-gnat-larvae-data.yml` (10 fields)
- `src/seeds/pests/gall-wasps-data.yml` (10 fields)
- `src/seeds/pests/glass-snails-data.yml` (10 fields)
- `src/seeds/pests/green-iguana-data.yml` (10 fields)
- `src/seeds/pests/iron-deficiency-data.yml` (10 fields)
- `src/seeds/pests/jumping-worms-data.yml` (10 fields)
- `src/seeds/pests/june-beetle-grubs-data.yml` (10 fields)
- `src/seeds/pests/lace-bugs-data.yml` (10 fields)
- `src/seeds/pests/leaf-footed-bugs-data.yml` (10 fields)
- `src/seeds/pests/leaf-scorch-data.yml` (10 fields)
- `src/seeds/pests/leatherleaf-slug-data.yml` (10 fields)
- `src/seeds/pests/magnesium-deficiency-data.yml` (10 fields)
- `src/seeds/pests/mole-crickets-data.yml` (10 fields)
- `src/seeds/pests/nitrogen-deficiency-data.yml` (10 fields)
- `src/seeds/pests/nutrient-burn-data.yml` (10 fields)
- `src/seeds/pests/oleander-scale-data.yml` (10 fields)
- `src/seeds/pests/overwatering-root-rot-data.yml` (10 fields)
- `src/seeds/pests/planthoppers-data.yml` (10 fields)
- `src/seeds/pests/potassium-deficiency-data.yml` (10 fields)
- `src/seeds/pests/root-aphids-data.yml` (10 fields)
- `src/seeds/pests/root-feeding-grubs-data.yml` (10 fields)
- `src/seeds/pests/russet-mites-data.yml` (10 fields)
- `src/seeds/pests/shot-hole-borers-data.yml` (10 fields)
- `src/seeds/pests/sod-webworms-data.yml` (10 fields)
- `src/seeds/pests/soft-scale-data.yml` (10 fields)
- `src/seeds/pests/southern-chinch-bug-data.yml` (10 fields)
- `src/seeds/pests/sunscald-data.yml` (10 fields)
- `src/seeds/pests/tea-scale-data.yml` (10 fields)
- `src/seeds/pests/treehoppers-data.yml` (10 fields)
- `src/seeds/pests/twig-borers-data.yml` (10 fields)
- `src/seeds/pests/white-grubs-data.yml` (10 fields)
- `src/seeds/pests/white-peach-scale-data.yml` (10 fields)

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
