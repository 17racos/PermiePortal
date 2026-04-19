# PermiePortal — Purpose Quality Pass Tier 1

## YOUR TASK
You are Cursor Agent in Agent mode. Rewrite the `purpose:` field for the 20 plants
listed below. These are the highest-value plants on the site and need hand-quality prose.

Do NOT ask questions. Start immediately.

---

## Gold Standard — Read These First
Before writing anything, read these three files completely:
- `src/seeds/plants/moringa-data.yml` — the gold standard
- `src/seeds/plants/okra-data.yml` — second reference

---

## Voice Rules — CRITICAL

Write like a field practitioner explaining to another gardener what this plant
actually does in a system. Plain, specific, earned.

GOOD:
  Edible: Leaves harvest within 60 days and regrow aggressively after hard pruning -- one of the most productive cut-and-come-again plants in a subtropical food forest.

BAD (do not write like this):
  Edible: Elderberry in the edible role draws on field reality -- stacks calories and culinary diversity into guilds and annual rotations without leaning on imported fertility theater.

The bad example is template language. It says nothing specific about the plant.
Every sentence must contain a fact about THIS plant specifically.

DO NOT use these phrases under any circumstances:
- "stacks calories and culinary diversity"
- "keeps informed-adult herbal capacity on-site"
- "feeds insect and bird guilds so edges read as habitat"
- "moves minerals from deep or marginal horizons"
- "turns fast leaf/stem turnover into mulch"
- "draws on field reality"
- "stays grounded in what growers actually report"
- any phrase ending in "without leaning on imported fertility theater"

---

## Format
Each function on its own line, no bullet points, no dashes:

  purpose: |-
    Edible: [specific description of what part, how used, when harvested]
    Medicinal: [specific use, what part, what compound or traditional use]
    Pollinator: [what insects, what flowers, when, why it matters in system]

Use ' -- ' (space dash dash space) not em dashes (—).
Minimum 3 functions. Most should have 5-8.
Only include functions that genuinely apply to this plant.

---

## Functions to Consider for Each Plant
- Edible (what part, how used, harvest timing)
- Medicinal (what use, what part, any cautions)
- Nitrogen Fixer (if legume or documented root associations)
- Dynamic Accumulator (what minerals, how released into system)
- Mulcher / Chop-and-Drop (biomass rate, breakdown speed)
- Animal Fodder (what animals, what parts, protein content if known)
- Pollinator (what insects, what flowers, when)
- Wildlife Attractor (birds, mammals, specific species if known)
- Windbreaker (height, density)
- Erosion Control (root system specifics)
- Shade Provider (canopy density, what grows beneath)
- Pest Repellent (what pests, what compound)
- Water Purification (if documented)
- Plant Growth Stimulant (if documented)
- Ornamental (specific aesthetic value)
- Fiber / Dye (if applicable)

---

## Plants to Rewrite (20 files)

- `src/seeds/plants/elderberry-data.yml`
- `src/seeds/plants/comfrey-data.yml`
- `src/seeds/plants/tithonia-data.yml`
- `src/seeds/plants/banana-data.yml`
- `src/seeds/plants/pigeon_pea-data.yml`
- `src/seeds/plants/lemongrass-data.yml`
- `src/seeds/plants/turmeric-data.yml`
- `src/seeds/plants/sweet_potato-data.yml`
- `src/seeds/plants/passionflower-data.yml`
- `src/seeds/plants/fig-data.yml`
- `src/seeds/plants/ginger-data.yml`
- `src/seeds/plants/garlic-data.yml`
- `src/seeds/plants/tomato-data.yml`
- `src/seeds/plants/basil-data.yml`
- `src/seeds/plants/chamomile-data.yml`
- `src/seeds/plants/lavender-data.yml`
- `src/seeds/plants/rosemary-data.yml`
- `src/seeds/plants/echinacea-data.yml`
- `src/seeds/plants/lemon-balm-data.yml`
- `src/seeds/plants/yarrow-data.yml`

---

## When ALL 20 Files Are Done

```bash
python3 validate.py --since 2h
python3 validate.py --fix --since 2h
./sync.sh --check
./sync.sh
git add -A
git commit -m "Purpose quality pass tier 1 -- 20 high value plants hand-written to gold standard"
git push origin v2
rm review/purpose_tier1.md
```

Zero warnings required before committing.
