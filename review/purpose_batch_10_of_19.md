# PermiePortal — Purpose Quality Pass Batch 10 of 19

## YOUR TASK
You are Cursor Agent in Agent mode. Rewrite the `purpose:` field for the plants
listed below to match the gold standard. Work through ALL files before running
any commands.

Do NOT ask questions. Start immediately.

---

## Gold Standard — Read These First
Before writing anything, read these four files:
- `src/seeds/plants/moringa-data.yml`
- `src/seeds/plants/elderberry-data.yml`
- `src/seeds/plants/dandelion-data.yml`
- `src/seeds/plants/black_locust-data.yml`

---

## Voice Rules — CRITICAL
Write like a field practitioner. Every sentence must contain a fact about THIS
plant specifically. Plain, specific, earned.

DO NOT use these phrases under any circumstances:
- "stacks calories and culinary diversity"
- "keeps informed-adult herbal capacity on-site"
- "feeds insect and bird guilds so edges read as habitat"
- "draws on field reality"
- "stays grounded in what growers actually report"
- "without leaning on imported fertility theater"
- "instead of bagged inputs"
- "serves multiple functions in a permaculture system"
- ANY phrase that could apply to 100 different plants unchanged

---

## Format
  purpose: |-
    Edible: [what part, how used, when harvested -- specific to THIS plant]
    Medicinal: [what use, what part, any cautions -- specific to THIS plant]
    Nitrogen Fixer: [mechanism, interplanting advice -- specific to THIS plant]

Use ' -- ' (space dash dash space) NOT em dashes.
No bullet points. No leading dashes. One function per line.
Minimum 3 functions. Most plants 5-8.
Only include functions that genuinely apply to this plant.
Match the plant_function list already in the file.
Only change the `purpose:` field -- do not touch any other fields.

---

## Plants to Rewrite

- `src/seeds/plants/lime_tree-data.yml`
- `src/seeds/plants/lingonberry-data.yml`
- `src/seeds/plants/lions-mane-data.yml`
- `src/seeds/plants/little-bluestem-data.yml`
- `src/seeds/plants/little-brown-jug-data.yml`
- `src/seeds/plants/lobelia-inflata-data.yml`
- `src/seeds/plants/loblolly-pine-data.yml`
- `src/seeds/plants/longan-data.yml`
- `src/seeds/plants/longawn-muhly-data.yml`
- `src/seeds/plants/longleaf-pine-data.yml`
- `src/seeds/plants/lotus-data.yml`
- `src/seeds/plants/lovage-data.yml`
- `src/seeds/plants/lowbush-cranberry-data.yml`
- `src/seeds/plants/luffa-data.yml`
- `src/seeds/plants/lupine-data.yml`
- `src/seeds/plants/lychee-data.yml`
- `src/seeds/plants/madagascar-vanilla-data.yml`
- `src/seeds/plants/madrone-data.yml`
- `src/seeds/plants/maidenhair-fern-data.yml`
- `src/seeds/plants/maitake-data.yml`
- `src/seeds/plants/malabar-chestnut-data.yml`
- `src/seeds/plants/malibar_spinach-data.yml`
- `src/seeds/plants/mamey-sapote-data.yml`
- `src/seeds/plants/mandarin-data.yml`
- `src/seeds/plants/mango-data.yml`
- `src/seeds/plants/many-flowered-cotoneaster-data.yml`
- `src/seeds/plants/mapleleaf-viburnum-data.yml`
- `src/seeds/plants/marang-data.yml`
- `src/seeds/plants/marjoram-data.yml`
- `src/seeds/plants/marlberry-data.yml`
- `src/seeds/plants/marsh-fern-data.yml`
- `src/seeds/plants/marsh-hibiscus-data.yml`
- `src/seeds/plants/marsh-mallow-data.yml`
- `src/seeds/plants/marsh-marigold-data.yml`
- `src/seeds/plants/marsh-pennywort-data.yml`
- `src/seeds/plants/mashua-data.yml`
- `src/seeds/plants/mayapple-data.yml`
- `src/seeds/plants/mayhaw-data.yml`
- `src/seeds/plants/maypop-data.yml`
- `src/seeds/plants/mazus-data.yml`
- `src/seeds/plants/meadowsweet-data.yml`
- `src/seeds/plants/medlar-data.yml`
- `src/seeds/plants/mexican-bush-sage-data.yml`
- `src/seeds/plants/mexican-elderberry-data.yml`
- `src/seeds/plants/mexican-oregano-data.yml`
- `src/seeds/plants/mexican-sunflower-data.yml`
- `src/seeds/plants/mexican-tarragon-data.yml`
- `src/seeds/plants/milk-vetch-data.yml`
- `src/seeds/plants/milkweed-data.yml`
- `src/seeds/plants/millet-data.yml`

---

## When ALL Files Are Done

```bash
python3 validate.py --since 2h
python3 validate.py --fix --since 2h
./sync.sh --check
./sync.sh
git add -A
git commit -m "Purpose quality pass batch 10 of 19"
git push origin v2
rm review/purpose_batch_10_of_19.md
```

Zero warnings required before committing.
Then immediately start: review/purpose_batch_11_of_19.md
