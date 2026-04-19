# PermiePortal — Purpose Quality Pass Batch 4 of 19

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

- `src/seeds/plants/cabbage-palm-data.yml`
- `src/seeds/plants/cacao-data.yml`
- `src/seeds/plants/caesarweed-data.yml`
- `src/seeds/plants/caimito-data.yml`
- `src/seeds/plants/calabaza-data.yml`
- `src/seeds/plants/calamint-data.yml`
- `src/seeds/plants/calamondin-data.yml`
- `src/seeds/plants/calathea-data.yml`
- `src/seeds/plants/calendula-data.yml`
- `src/seeds/plants/california-poppy-data.yml`
- `src/seeds/plants/cambuca-data.yml`
- `src/seeds/plants/camphor-tree-data.yml`
- `src/seeds/plants/camphor-weed-data.yml`
- `src/seeds/plants/camu-camu-data.yml`
- `src/seeds/plants/candle-nut-tree-data.yml`
- `src/seeds/plants/canistel-data.yml`
- `src/seeds/plants/canna-lily-data.yml`
- `src/seeds/plants/cannonball-tree-data.yml`
- `src/seeds/plants/cantaloupe-data.yml`
- `src/seeds/plants/carambola-data.yml`
- `src/seeds/plants/cardamom-data.yml`
- `src/seeds/plants/cardinal-flower-data.yml`
- `src/seeds/plants/carob-tree-data.yml`
- `src/seeds/plants/carolina-buckthorn-data.yml`
- `src/seeds/plants/carolina-ponysfoot-data.yml`
- `src/seeds/plants/carolina-rose-data.yml`
- `src/seeds/plants/carolina-snailseed-data.yml`
- `src/seeds/plants/carolina-willow-data.yml`
- `src/seeds/plants/carpet-bugle-data.yml`
- `src/seeds/plants/carrot-data.yml`
- `src/seeds/plants/cassabanana-root-systems-data.yml`
- `src/seeds/plants/cassava-data.yml`
- `src/seeds/plants/cassia-alata-data.yml`
- `src/seeds/plants/catbird-grape-data.yml`
- `src/seeds/plants/catclaw-sensitive-briar-data.yml`
- `src/seeds/plants/catnip-data.yml`
- `src/seeds/plants/cattail-data.yml`
- `src/seeds/plants/cattley-guava-data.yml`
- `src/seeds/plants/caucasian-spinach-data.yml`
- `src/seeds/plants/cauliflower-data.yml`
- `src/seeds/plants/celery-data.yml`
- `src/seeds/plants/celery-root-data.yml`
- `src/seeds/plants/celtuce-data.yml`
- `src/seeds/plants/cempedak-data.yml`
- `src/seeds/plants/century-plant-data.yml`
- `src/seeds/plants/ceylon-gooseberry-tree-data.yml`
- `src/seeds/plants/chaga-data.yml`
- `src/seeds/plants/chalk-maple-data.yml`
- `src/seeds/plants/chayote-data.yml`
- `src/seeds/plants/cherimoya-data.yml`

---

## When ALL Files Are Done

```bash
python3 validate.py --since 2h
python3 validate.py --fix --since 2h
./sync.sh --check
./sync.sh
git add -A
git commit -m "Purpose quality pass batch 4 of 19"
git push origin v2
rm review/purpose_batch_4_of_19.md
```

Zero warnings required before committing.
Do NOT stop. Do NOT wait for user input.
Immediately read and execute review/purpose_batch_5_of_19.md next.
Continue until all 19 batches are complete.
