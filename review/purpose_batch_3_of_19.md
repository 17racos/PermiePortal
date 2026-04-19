# PermiePortal — Purpose Quality Pass Batch 3 of 19

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

- `src/seeds/plants/blackcurrant-data.yml`
- `src/seeds/plants/bladder-senna-data.yml`
- `src/seeds/plants/bladderwort-data.yml`
- `src/seeds/plants/blanket-flower-data.yml`
- `src/seeds/plants/blood-orange-data.yml`
- `src/seeds/plants/bloodroot-data.yml`
- `src/seeds/plants/blue-agave-data.yml`
- `src/seeds/plants/blue-cohosh-data.yml`
- `src/seeds/plants/blue-elderberry-data.yml`
- `src/seeds/plants/blue-flag-iris-data.yml`
- `src/seeds/plants/blue-flax-data.yml`
- `src/seeds/plants/blue-grama-data.yml`
- `src/seeds/plants/blue-mistflower-data.yml`
- `src/seeds/plants/blue-porterweed-data.yml`
- `src/seeds/plants/blue-sage-data.yml`
- `src/seeds/plants/blue-star-creeper-data.yml`
- `src/seeds/plants/blue-tongue-data.yml`
- `src/seeds/plants/blue-woodruff-data.yml`
- `src/seeds/plants/bluejack-oak-data.yml`
- `src/seeds/plants/bog-bean-data.yml`
- `src/seeds/plants/bok-choy-data.yml`
- `src/seeds/plants/borage-officinalis-data.yml`
- `src/seeds/plants/bottle-gourd-data.yml`
- `src/seeds/plants/bottlebrush-data.yml`
- `src/seeds/plants/bracken-fern-data.yml`
- `src/seeds/plants/brazilian-spinach-data.yml`
- `src/seeds/plants/breadfruit-data.yml`
- `src/seeds/plants/breadnut-tree-data.yml`
- `src/seeds/plants/broadleaf-stonecrop-data.yml`
- `src/seeds/plants/broccoli-data.yml`
- `src/seeds/plants/broom-data.yml`
- `src/seeds/plants/broomsedge-bluestem-data.yml`
- `src/seeds/plants/brush-cherry-data.yml`
- `src/seeds/plants/brussels-sprouts-data.yml`
- `src/seeds/plants/buck-plantain-data.yml`
- `src/seeds/plants/buddha-hand-data.yml`
- `src/seeds/plants/buffalo-bur-data.yml`
- `src/seeds/plants/buffalo-gourd-data.yml`
- `src/seeds/plants/buffalo-grass-data.yml`
- `src/seeds/plants/buffalo-plum-data.yml`
- `src/seeds/plants/bullbine-data.yml`
- `src/seeds/plants/burdock-data.yml`
- `src/seeds/plants/buriti-palm-data.yml`
- `src/seeds/plants/bush-chinquapin-data.yml`
- `src/seeds/plants/butterfly-cassia-data.yml`
- `src/seeds/plants/butterfly-ginger-data.yml`
- `src/seeds/plants/butterfly-pea-data.yml`
- `src/seeds/plants/butterwort-data.yml`
- `src/seeds/plants/buttonbush-data.yml`
- `src/seeds/plants/cabbage-data.yml`

---

## When ALL Files Are Done

```bash
python3 validate.py --since 2h
python3 validate.py --fix --since 2h
./sync.sh --check
./sync.sh
git add -A
git commit -m "Purpose quality pass batch 3 of 19"
git push origin v2
rm review/purpose_batch_3_of_19.md
```

Zero warnings required before committing.
Do NOT stop. Do NOT wait for user input.
Immediately read and execute review/purpose_batch_4_of_19.md next.
Continue until all 19 batches are complete.
