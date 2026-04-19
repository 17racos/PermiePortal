# PermiePortal — Purpose Quality Pass Batch 1 of 19

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

- `src/seeds/plants/abiu-data.yml`
- `src/seeds/plants/acacia-data.yml`
- `src/seeds/plants/acai-palm-data.yml`
- `src/seeds/plants/achira-data.yml`
- `src/seeds/plants/acorn-squash-data.yml`
- `src/seeds/plants/african-blue-basil-data.yml`
- `src/seeds/plants/african-breadfruit-data.yml`
- `src/seeds/plants/african-locust-bean-data.yml`
- `src/seeds/plants/agave-data.yml`
- `src/seeds/plants/ahipa-data.yml`
- `src/seeds/plants/air-potato-data.yml`
- `src/seeds/plants/albizia-lebbeck-data.yml`
- `src/seeds/plants/alder-data.yml`
- `src/seeds/plants/alexanders-data.yml`
- `src/seeds/plants/allegheny-chinquapin-data.yml`
- `src/seeds/plants/allegheny-serviceberry-data.yml`
- `src/seeds/plants/allegheny-stonecrop-data.yml`
- `src/seeds/plants/almond-tree-data.yml`
- `src/seeds/plants/aloe-data.yml`
- `src/seeds/plants/alsike-clover-data.yml`
- `src/seeds/plants/alternanthera-data.yml`
- `src/seeds/plants/alternate-leaf-dogwood-data.yml`
- `src/seeds/plants/amaranth-data.yml`
- `src/seeds/plants/american-beauty-plum-data.yml`
- `src/seeds/plants/american-black-currant-data.yml`
- `src/seeds/plants/american-elderberry-data.yml`
- `src/seeds/plants/american-hawthorn-data.yml`
- `src/seeds/plants/american-hazelnut-data.yml`
- `src/seeds/plants/american-lotus-data.yml`
- `src/seeds/plants/american-pennyroyal-data.yml`
- `src/seeds/plants/american-persimmon-data.yml`
- `src/seeds/plants/american-plum-data.yml`
- `src/seeds/plants/american-snowbell-data.yml`
- `src/seeds/plants/american-waterlily-data.yml`
- `src/seeds/plants/andrographis-data.yml`
- `src/seeds/plants/angelica-data.yml`
- `src/seeds/plants/angels-trumpet-data.yml`
- `src/seeds/plants/angled-loofah-data.yml`
- `src/seeds/plants/anise-hyssop-data.yml`
- `src/seeds/plants/apple-tree-data.yml`
- `src/seeds/plants/araza-data.yml`
- `src/seeds/plants/arbutus-data.yml`
- `src/seeds/plants/aronia-data.yml`
- `src/seeds/plants/arracacha-data.yml`
- `src/seeds/plants/arrow-arum-data.yml`
- `src/seeds/plants/arrowhead-data.yml`
- `src/seeds/plants/arrowleaf-balsamroot-data.yml`
- `src/seeds/plants/arrowroot-data.yml`
- `src/seeds/plants/arrowwood-viburnum-data.yml`
- `src/seeds/plants/artemisia-data.yml`

---

## When ALL Files Are Done

```bash
python3 validate.py --since 2h
python3 validate.py --fix --since 2h
./sync.sh --check
./sync.sh
git add -A
git commit -m "Purpose quality pass batch 1 of 19"
git push origin v2
rm review/purpose_batch_1_of_19.md
```

Zero warnings required before committing.
Then immediately start: review/purpose_batch_2_of_19.md
