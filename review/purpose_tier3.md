# PermiePortal — Purpose Quality Pass Tier 3

## YOUR TASK
You are Cursor Agent in Agent mode. Rewrite the `purpose:` field for the 25 plants
listed below to match the gold standard quality from Tiers 1 and 2.

Do NOT ask questions. Start immediately.

---

## Gold Standard — Read These First
Before writing anything, read these four files:
- `src/seeds/plants/moringa-data.yml`
- `src/seeds/plants/elderberry-data.yml`
- `src/seeds/plants/loquat-data.yml`
- `src/seeds/plants/sunshine-mimosa-data.yml`

---

## Voice Rules — CRITICAL

Write like a field practitioner. Every sentence must contain a fact about THIS
plant specifically. Plain, specific, earned.

DO NOT use these phrases:
- "stacks calories and culinary diversity"
- "keeps informed-adult herbal capacity on-site"
- "feeds insect and bird guilds so edges read as habitat"
- "moves minerals from deep or marginal horizons"
- "draws on field reality"
- "stays grounded in what growers actually report"
- any phrase ending in "without leaning on imported fertility theater"
- any phrase ending in "instead of bagged inputs"

---

## Format
  purpose: |-
    Edible: [specific -- what part, how used, when harvested]
    Medicinal: [specific -- what use, what part, any cautions]

Use ' -- ' not em dashes. No bullet points. No dashes at line start.
Minimum 3 functions. Most should have 5-8.
Only include functions that genuinely apply to this plant.

---

## Plants to Rewrite (25 files)

- `src/seeds/plants/elderflower-data.yml`
- `src/seeds/plants/pawpaw-data.yml`
- `src/seeds/plants/persimmon_tree-data.yml`
- `src/seeds/plants/blueberry-data.yml`
- `src/seeds/plants/raspberry-data.yml`
- `src/seeds/plants/strawberry-data.yml`
- `src/seeds/plants/blackberry-data.yml` (if exists, skip if not)
- `src/seeds/plants/passionflower-data.yml`
- `src/seeds/plants/black_locust-data.yml`
- `src/seeds/plants/honey-locust-data.yml`
- `src/seeds/plants/siberian_pea_shrub-data.yml`
- `src/seeds/plants/alfalfa-data.yml`
- `src/seeds/plants/red-clover-data.yml`
- `src/seeds/plants/white-clover-data.yml`
- `src/seeds/plants/crimson-clover-data.yml`
- `src/seeds/plants/dutch_clover-data.yml`
- `src/seeds/plants/hairy-vetch-data.yml`
- `src/seeds/plants/daikon-radish-data.yml`
- `src/seeds/plants/buckwheat-data.yml`
- `src/seeds/plants/sunflower-data.yml`
- `src/seeds/plants/stinging-nettle-data.yml`
- `src/seeds/plants/dandelion-data.yml`
- `src/seeds/plants/plantain-data.yml` (if exists, skip if not)
- `src/seeds/plants/broadleaf-plantain-data.yml`
- `src/seeds/plants/chicory-data.yml`

---

## When ALL Files Are Done

```bash
python3 validate.py --since 2h
python3 validate.py --fix --since 2h
./sync.sh --check
./sync.sh
git add -A
git commit -m "Purpose quality pass tier 3 -- fruit trees, nitrogen fixers, cover crops"
git push origin v2
rm review/purpose_tier3.md
```

Zero warnings required before committing.
