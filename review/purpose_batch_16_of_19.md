# PermiePortal — Purpose Quality Pass Batch 16 of 19

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

- `src/seeds/plants/stokes-aster-data.yml`
- `src/seeds/plants/strawberry-guava-data.yml`
- `src/seeds/plants/strawberry-tree-data.yml`
- `src/seeds/plants/subterranean-clover-data.yml`
- `src/seeds/plants/sugar-apple-data.yml`
- `src/seeds/plants/sugar-hackberry-data.yml`
- `src/seeds/plants/summer-savory-data.yml`
- `src/seeds/plants/sun-hemp-data.yml`
- `src/seeds/plants/sundew-data.yml`
- `src/seeds/plants/sunn-hemp-data.yml`
- `src/seeds/plants/sunrose-data.yml`
- `src/seeds/plants/surinam-cherry-data.yml`
- `src/seeds/plants/swamp-bay-data.yml`
- `src/seeds/plants/swamp-dogwood-data.yml`
- `src/seeds/plants/swamp-milkweed-data.yml`
- `src/seeds/plants/swamp-rose-data.yml`
- `src/seeds/plants/swamp-sunflower-data.yml`
- `src/seeds/plants/sweet-alyssum-data.yml`
- `src/seeds/plants/sweet-black-eyed-susan-data.yml`
- `src/seeds/plants/sweet-cicely-data.yml`
- `src/seeds/plants/sweet-coltsfoot-data.yml`
- `src/seeds/plants/sweet-corn-data.yml`
- `src/seeds/plants/sweet-crabapple-data.yml`
- `src/seeds/plants/sweet-flag-data.yml`
- `src/seeds/plants/sweet-gale-data.yml`
- `src/seeds/plants/sweet-granadilla-data.yml`
- `src/seeds/plants/sweet-woodruff-data.yml`
- `src/seeds/plants/sweetbay-magnolia-data.yml`
- `src/seeds/plants/sweetgrass-data.yml`
- `src/seeds/plants/swiss-chard-data.yml`
- `src/seeds/plants/switchgrass-data.yml`
- `src/seeds/plants/syzygium-smithii-data.yml`
- `src/seeds/plants/tagasaste-data.yml`
- `src/seeds/plants/tamarisk-data.yml`
- `src/seeds/plants/tangelo-data.yml`
- `src/seeds/plants/tangerine-data.yml`
- `src/seeds/plants/tannia-data.yml`
- `src/seeds/plants/tansy-data.yml`
- `src/seeds/plants/taragon-data.yml`
- `src/seeds/plants/taro-data.yml`
- `src/seeds/plants/tea-olive-data.yml`
- `src/seeds/plants/tea-tree-data.yml`
- `src/seeds/plants/tephrosia-vogelii-data.yml`
- `src/seeds/plants/texas-olive-data.yml`
- `src/seeds/plants/texas-persimmon-data.yml`
- `src/seeds/plants/thai-basil-data.yml`
- `src/seeds/plants/thin-leaved-coneflower-data.yml`
- `src/seeds/plants/thorny-buffaloberry-data.yml`
- `src/seeds/plants/thyme-data.yml`
- `src/seeds/plants/tick-trefoil-data.yml`

---

## When ALL Files Are Done

```bash
python3 validate.py --since 2h
python3 validate.py --fix --since 2h
./sync.sh --check
./sync.sh
git add -A
git commit -m "Purpose quality pass batch 16 of 19"
git push origin v2
rm review/purpose_batch_16_of_19.md
```

Zero warnings required before committing.
Then immediately start: review/purpose_batch_17_of_19.md
