# PermiePortal — Purpose Quality Pass Batch 15 of 19

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

- `src/seeds/plants/sesbania-grandiflora-data.yml`
- `src/seeds/plants/shagbark-hickory-data.yml`
- `src/seeds/plants/shallot-data.yml`
- `src/seeds/plants/shampoo-ginger-data.yml`
- `src/seeds/plants/shaving-brush-tree-data.yml`
- `src/seeds/plants/sheep-sorrel-data.yml`
- `src/seeds/plants/shiitake-data.yml`
- `src/seeds/plants/shining-coneflower-data.yml`
- `src/seeds/plants/shiny-blueberry-data.yml`
- `src/seeds/plants/shiso-data.yml`
- `src/seeds/plants/sicklepod-data.yml`
- `src/seeds/plants/sida-data.yml`
- `src/seeds/plants/sideoats-grama-data.yml`
- `src/seeds/plants/silk-oak-data.yml`
- `src/seeds/plants/silverbell-tree-data.yml`
- `src/seeds/plants/silverberry-data.yml`
- `src/seeds/plants/silverleaf-cotoneaster-data.yml`
- `src/seeds/plants/simpson-stopper-data.yml`
- `src/seeds/plants/singapore-daisy-data.yml`
- `src/seeds/plants/sisal-data.yml`
- `src/seeds/plants/skirret-data.yml`
- `src/seeds/plants/slash-pine-data.yml`
- `src/seeds/plants/snake-gourd-data.yml`
- `src/seeds/plants/snow_pea-data.yml`
- `src/seeds/plants/snowberry-data.yml`
- `src/seeds/plants/soapberry-data.yml`
- `src/seeds/plants/softstem-bulrush-data.yml`
- `src/seeds/plants/sorghum-data.yml`
- `src/seeds/plants/sorrel-data.yml`
- `src/seeds/plants/sour-orange-data.yml`
- `src/seeds/plants/soursop-data.yml`
- `src/seeds/plants/soursop-leaf-data.yml`
- `src/seeds/plants/southern-crabapple-data.yml`
- `src/seeds/plants/southern-hawthorn-data.yml`
- `src/seeds/plants/southern-magnolia-data.yml`
- `src/seeds/plants/southern-red-cedar-data.yml`
- `src/seeds/plants/southern-shield-fern-data.yml`
- `src/seeds/plants/spanish-needles-data.yml`
- `src/seeds/plants/spanish-plum-data.yml`
- `src/seeds/plants/sparkleberry-data.yml`
- `src/seeds/plants/spatterdock-data.yml`
- `src/seeds/plants/spicebush-data.yml`
- `src/seeds/plants/spiderwort-data.yml`
- `src/seeds/plants/spikenard-data.yml`
- `src/seeds/plants/spinach-data.yml`
- `src/seeds/plants/split-beard-bluestem-data.yml`
- `src/seeds/plants/spotted-bee-balm-data.yml`
- `src/seeds/plants/spruce-pine-data.yml`
- `src/seeds/plants/stevia-data.yml`
- `src/seeds/plants/stinging-tree-data.yml`

---

## When ALL Files Are Done

```bash
python3 validate.py --since 2h
python3 validate.py --fix --since 2h
./sync.sh --check
./sync.sh
git add -A
git commit -m "Purpose quality pass batch 15 of 19"
git push origin v2
rm review/purpose_batch_15_of_19.md
```

Zero warnings required before committing.
Then immediately start: review/purpose_batch_16_of_19.md
