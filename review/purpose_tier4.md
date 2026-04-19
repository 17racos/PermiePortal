# PermiePortal — Purpose Quality Pass Tier 4

## YOUR TASK
You are Cursor Agent in Agent mode. Rewrite the `purpose:` field for the 25 plants
listed below to match the gold standard quality from Tiers 1-3.

Do NOT ask questions. Start immediately.

---

## Gold Standard — Read These First
Before writing anything, read these four files:
- `src/seeds/plants/moringa-data.yml`
- `src/seeds/plants/elderberry-data.yml`
- `src/seeds/plants/black_locust-data.yml`
- `src/seeds/plants/dandelion-data.yml`

---

## Voice Rules — CRITICAL
Write like a field practitioner. Every sentence must contain a fact about THIS
plant specifically. Plain, specific, earned. No generic ecological abstractions.

DO NOT use these phrases under any circumstances:
- "stacks calories and culinary diversity"
- "keeps informed-adult herbal capacity on-site"
- "feeds insect and bird guilds so edges read as habitat"
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

- `src/seeds/plants/ashwagandha-data.yml`
- `src/seeds/plants/valerian-data.yml`
- `src/seeds/plants/skullcap-data.yml`
- `src/seeds/plants/motherwort-data.yml`
- `src/seeds/plants/blue-vervain-data.yml`
- `src/seeds/plants/wild-bergamot-data.yml`
- `src/seeds/plants/feverfew-data.yml`
- `src/seeds/plants/mugwort-data.yml`
- `src/seeds/plants/wormwood-data.yml`
- `src/seeds/plants/rue-data.yml`
- `src/seeds/plants/hyssop-officinalis-data.yml`
- `src/seeds/plants/agrimony-data.yml`
- `src/seeds/plants/boneset-data.yml`
- `src/seeds/plants/goldenseal-data.yml`
- `src/seeds/plants/echinacea-data.yml`
- `src/seeds/plants/st-johns-mint-data.yml`
- `src/seeds/plants/spearmint-data.yml` (if exists, skip if not)
- `src/seeds/plants/mint-data.yml`
- `src/seeds/plants/vietnamese-coriander-data.yml`
- `src/seeds/plants/cuban-oregano-data.yml`
- `src/seeds/plants/root-beer-plant-data.yml`
- `src/seeds/plants/pineapple-sage-data.yml`
- `src/seeds/plants/lemon-verbena-data.yml`
- `src/seeds/plants/lemon-thyme-data.yml`
- `src/seeds/plants/society-garlic-data.yml`

---

## When ALL Files Are Done

```bash
python3 validate.py --since 2h
python3 validate.py --fix --since 2h
./sync.sh --check
./sync.sh
git add -A
git commit -m "Purpose quality pass tier 4 -- medicinal herbs and aromatics"
git push origin v2
rm review/purpose_tier4.md
```

Zero warnings required before committing.
