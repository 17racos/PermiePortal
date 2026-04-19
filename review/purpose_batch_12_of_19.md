# PermiePortal — Purpose Quality Pass Batch 12 of 19

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

- `src/seeds/plants/papaya-data.yml`
- `src/seeds/plants/papyrus-data.yml`
- `src/seeds/plants/parsley-data.yml`
- `src/seeds/plants/parsley-hawthorn-data.yml`
- `src/seeds/plants/parsnip-data.yml`
- `src/seeds/plants/partridge-acacia-data.yml`
- `src/seeds/plants/partridge-cassia-data.yml`
- `src/seeds/plants/partridge-pea-data.yml`
- `src/seeds/plants/partridgeberry-data.yml`
- `src/seeds/plants/pea-data.yml`
- `src/seeds/plants/peach-palm-data.yml`
- `src/seeds/plants/peach-tree-data.yml`
- `src/seeds/plants/peanut-butter-fruit-tree-data.yml`
- `src/seeds/plants/peanut-tree-data.yml`
- `src/seeds/plants/pear-hawthorn-data.yml`
- `src/seeds/plants/pear_tree-data.yml`
- `src/seeds/plants/pecan-tree-data.yml`
- `src/seeds/plants/pennyroyal-data.yml`
- `src/seeds/plants/pepino-melon-data.yml`
- `src/seeds/plants/peppervine-data.yml`
- `src/seeds/plants/perennial-basil-data.yml`
- `src/seeds/plants/perennial-leek-data.yml`
- `src/seeds/plants/perilla-data.yml`
- `src/seeds/plants/persian-lilac-data.yml`
- `src/seeds/plants/persian-lime-data.yml`
- `src/seeds/plants/phacelia-data.yml`
- `src/seeds/plants/pickerelweed-data.yml`
- `src/seeds/plants/piedmont-purslane-data.yml`
- `src/seeds/plants/pigeonwood-data.yml`
- `src/seeds/plants/pignut-hickory-data.yml`
- `src/seeds/plants/pinaepple-pear-data.yml`
- `src/seeds/plants/pindo-palm-data.yml`
- `src/seeds/plants/pineappe_sage-data.yml`
- `src/seeds/plants/pineland-croton-data.yml`
- `src/seeds/plants/pineland-heather-data.yml`
- `src/seeds/plants/piper-data.yml`
- `src/seeds/plants/pitcher-plant-data.yml`
- `src/seeds/plants/pitomba-data.yml`
- `src/seeds/plants/plains-wild-indigo-data.yml`
- `src/seeds/plants/pollinator-support-data.yml`
- `src/seeds/plants/pomegranate_tree-data.yml`
- `src/seeds/plants/pomelo-data.yml`
- `src/seeds/plants/pond-apple-data.yml`
- `src/seeds/plants/pond-cypress-data.yml`
- `src/seeds/plants/pond-pine-data.yml`
- `src/seeds/plants/ponytail-palm-data.yml`
- `src/seeds/plants/possum-grape-data.yml`
- `src/seeds/plants/possumhaw-viburnum-data.yml`
- `src/seeds/plants/potato-data.yml`
- `src/seeds/plants/potato_mint-data.yml`

---

## When ALL Files Are Done

```bash
python3 validate.py --since 2h
python3 validate.py --fix --since 2h
./sync.sh --check
./sync.sh
git add -A
git commit -m "Purpose quality pass batch 12 of 19"
git push origin v2
rm review/purpose_batch_12_of_19.md
```

Zero warnings required before committing.
Do NOT stop. Do NOT wait for user input.
Immediately read and execute review/purpose_batch_13_of_19.md next.
Continue until all 19 batches are complete.
