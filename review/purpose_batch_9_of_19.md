# PermiePortal — Purpose Quality Pass Batch 9 of 19

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

- `src/seeds/plants/illawarra-plum-data.yml`
- `src/seeds/plants/illinois-bundleflower-data.yml`
- `src/seeds/plants/imbe-data.yml`
- `src/seeds/plants/indian-cucumber-root-data.yml`
- `src/seeds/plants/indiangrass-data.yml`
- `src/seeds/plants/indigofera-tinctoria-data.yml`
- `src/seeds/plants/inkberry-data.yml`
- `src/seeds/plants/italian-oregano-data.yml`
- `src/seeds/plants/ivy-gourd-data.yml`
- `src/seeds/plants/jaboticaba-data.yml`
- `src/seeds/plants/jackbean-data.yml`
- `src/seeds/plants/jackfruit-data.yml`
- `src/seeds/plants/jambolan-data.yml`
- `src/seeds/plants/jatoba-data.yml`
- `src/seeds/plants/jelly-palm-data.yml`
- `src/seeds/plants/jerusalem-artichoke-data.yml`
- `src/seeds/plants/jewel-of-opar-data.yml`
- `src/seeds/plants/jicama-data.yml`
- `src/seeds/plants/joe-pye-weed-data.yml`
- `src/seeds/plants/jojoba-data.yml`
- `src/seeds/plants/jostaberry-data.yml`
- `src/seeds/plants/jucara-palm-data.yml`
- `src/seeds/plants/june-plum-data.yml`
- `src/seeds/plants/jute-data.yml`
- `src/seeds/plants/kaffir-lime-data.yml`
- `src/seeds/plants/kale-data.yml`
- `src/seeds/plants/kangkong-data.yml`
- `src/seeds/plants/kapok-tree-data.yml`
- `src/seeds/plants/kava-data.yml`
- `src/seeds/plants/kedondong-data.yml`
- `src/seeds/plants/kenaf-data.yml`
- `src/seeds/plants/key-lime-data.yml`
- `src/seeds/plants/key-thatch-palm-data.yml`
- `src/seeds/plants/kiwi-data.yml`
- `src/seeds/plants/konjac-data.yml`
- `src/seeds/plants/kratom-data.yml`
- `src/seeds/plants/kwai-muk-data.yml`
- `src/seeds/plants/lanceleaf-coreopsis-data.yml`
- `src/seeds/plants/lantana-data.yml`
- `src/seeds/plants/lead-plant-data.yml`
- `src/seeds/plants/leaf-of-life-data.yml`
- `src/seeds/plants/leatherleaf-fern-data.yml`
- `src/seeds/plants/leavenworths-tickseed-data.yml`
- `src/seeds/plants/leek-data.yml`
- `src/seeds/plants/lemon-basil-data.yml`
- `src/seeds/plants/lemon-beebalm-data.yml`
- `src/seeds/plants/lemon-eucalyptus-data.yml`
- `src/seeds/plants/leren-data.yml`
- `src/seeds/plants/lettuce-data.yml`
- `src/seeds/plants/leucaena-data.yml`

---

## When ALL Files Are Done

```bash
python3 validate.py --since 2h
python3 validate.py --fix --since 2h
./sync.sh --check
./sync.sh
git add -A
git commit -m "Purpose quality pass batch 9 of 19"
git push origin v2
rm review/purpose_batch_9_of_19.md
```

Zero warnings required before committing.
Then immediately start: review/purpose_batch_10_of_19.md
