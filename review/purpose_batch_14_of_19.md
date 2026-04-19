# PermiePortal — Purpose Quality Pass Batch 14 of 19

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

- `src/seeds/plants/rumberry-data.yml`
- `src/seeds/plants/running-serviceberry-data.yml`
- `src/seeds/plants/russet-buffaloberry-data.yml`
- `src/seeds/plants/russian-olive-data.yml`
- `src/seeds/plants/rusty-blackhaw-data.yml`
- `src/seeds/plants/sage-data.yml`
- `src/seeds/plants/sago-palm-data.yml`
- `src/seeds/plants/salal-data.yml`
- `src/seeds/plants/saltbush-data.yml`
- `src/seeds/plants/saltgrass-data.yml`
- `src/seeds/plants/saltmarsh-aster-data.yml`
- `src/seeds/plants/saltmeadow-cordgrass-data.yml`
- `src/seeds/plants/saltwort-data.yml`
- `src/seeds/plants/samphire-data.yml`
- `src/seeds/plants/sand-blackberry-data.yml`
- `src/seeds/plants/sand-bluestem-data.yml`
- `src/seeds/plants/sand-cherry-data.yml`
- `src/seeds/plants/sand-cordgrass-data.yml`
- `src/seeds/plants/sand-grama-data.yml`
- `src/seeds/plants/sand-grape-data.yml`
- `src/seeds/plants/sand-live-oak-data.yml`
- `src/seeds/plants/sand-lovegrass-data.yml`
- `src/seeds/plants/sand-pine-data.yml`
- `src/seeds/plants/sapodilla-data.yml`
- `src/seeds/plants/saskatoon-berry-data.yml`
- `src/seeds/plants/saskatoon-data.yml`
- `src/seeds/plants/sassafras-data.yml`
- `src/seeds/plants/savory-data.yml`
- `src/seeds/plants/saw_palmetto-data.yml`
- `src/seeds/plants/scarlet-eggplant-data.yml`
- `src/seeds/plants/scorpion-weed-data.yml`
- `src/seeds/plants/scorzonera-data.yml`
- `src/seeds/plants/screw-pine-data.yml`
- `src/seeds/plants/scrub-cherry-data.yml`
- `src/seeds/plants/scrub-hickory-data.yml`
- `src/seeds/plants/scrub-palmetto-data.yml`
- `src/seeds/plants/sea-buckthorn-data.yml`
- `src/seeds/plants/sea-kale-data.yml`
- `src/seeds/plants/sea-lavender-data.yml`
- `src/seeds/plants/sea-oxeye-daisy-data.yml`
- `src/seeds/plants/sea-plantain-data.yml`
- `src/seeds/plants/sea-purslane-data.yml`
- `src/seeds/plants/sea-rocket-data.yml`
- `src/seeds/plants/seagrape-data.yml`
- `src/seeds/plants/sedium-data.yml`
- `src/seeds/plants/seminole-pumpkin-data.yml`
- `src/seeds/plants/sensitive-briar-data.yml`
- `src/seeds/plants/sensitive-plant-data.yml`
- `src/seeds/plants/serviceberry-data.yml`
- `src/seeds/plants/sesbania-data.yml`

---

## When ALL Files Are Done

```bash
python3 validate.py --since 2h
python3 validate.py --fix --since 2h
./sync.sh --check
./sync.sh
git add -A
git commit -m "Purpose quality pass batch 14 of 19"
git push origin v2
rm review/purpose_batch_14_of_19.md
```

Zero warnings required before committing.
Do NOT stop. Do NOT wait for user input.
Immediately read and execute review/purpose_batch_15_of_19.md next.
Continue until all 19 batches are complete.
