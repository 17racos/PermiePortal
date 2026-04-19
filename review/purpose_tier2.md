# PermiePortal — Purpose Quality Pass Tier 2

## YOUR TASK
You are Cursor Agent in Agent mode. Rewrite the `purpose:` field for the 25 plants
listed below to match the gold standard quality from Tier 1.

Do NOT ask questions. Start immediately.

---

## Gold Standard — Read These First
Before writing anything, read these files completely:
- `src/seeds/plants/moringa-data.yml`
- `src/seeds/plants/elderberry-data.yml`
- `src/seeds/plants/comfrey-data.yml`
- `src/seeds/plants/tithonia-data.yml`

---

## Voice Rules — CRITICAL

Write like a field practitioner explaining to another gardener what this plant
actually does in a system. Plain, specific, earned. Every sentence must contain
a fact about THIS plant specifically.

DO NOT use these phrases under any circumstances:
- "stacks calories and culinary diversity"
- "keeps informed-adult herbal capacity on-site"
- "feeds insect and bird guilds so edges read as habitat"
- "moves minerals from deep or marginal horizons"
- "turns fast leaf/stem turnover into mulch"
- "draws on field reality"
- "stays grounded in what growers actually report"
- any phrase ending in "without leaning on imported fertility theater"
- any phrase ending in "instead of bagged inputs"

---

## Format
Each function on its own line, no bullet points, no dashes:

  purpose: |-
    Edible: [specific description of what part, how used, when harvested]
    Medicinal: [specific use, what part, what compound or traditional use]

Use ' -- ' (space dash dash space) not em dashes.
Minimum 3 functions. Most should have 5-8.
Only include functions that genuinely apply to this plant.

---

## Plants to Rewrite (25 files)

- `src/seeds/plants/moringa-data.yml` — DO NOT TOUCH, gold standard reference only
- `src/seeds/plants/loquat-data.yml`
- `src/seeds/plants/mulberry_tree-data.yml`
- `src/seeds/plants/pinapple_guava-data.yml`
- `src/seeds/plants/goji-berry-data.yml`
- `src/seeds/plants/katuk-data.yml`
- `src/seeds/plants/longevity_spinach-data.yml`
- `src/seeds/plants/okinawa_spinach-data.yml`
- `src/seeds/plants/cranberry_hibiscus-data.yml`
- `src/seeds/plants/roselle-data.yml`
- `src/seeds/plants/sunshine-mimosa-data.yml`
- `src/seeds/plants/florida-betony-data.yml`
- `src/seeds/plants/beautyberry-data.yml`
- `src/seeds/plants/firebush-data.yml`
- `src/seeds/plants/coral-honeysuckle-data.yml`
- `src/seeds/plants/muscadine-grape-data.yml`
- `src/seeds/plants/perennial_peanut-data.yml`
- `src/seeds/plants/society-garlic-data.yml`
- `src/seeds/plants/lemon_tree-data.yml`
- `src/seeds/plants/kumquat-data.yml`
- `src/seeds/plants/marigold-data.yml`
- `src/seeds/plants/nasturtium-data.yml`
- `src/seeds/plants/borage-data.yml`
- `src/seeds/plants/dill-data.yml`
- `src/seeds/plants/fennel-data.yml`

---

## When ALL 25 Files Are Done

```bash
python3 validate.py --since 2h
python3 validate.py --fix --since 2h
./sync.sh --check
./sync.sh
git add -A
git commit -m "Purpose quality pass tier 2 -- 25 Florida and companion plants"
git push origin v2
rm review/purpose_tier2.md
```

Zero warnings required before committing.
