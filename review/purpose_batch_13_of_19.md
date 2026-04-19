# PermiePortal — Purpose Quality Pass Batch 13 of 19

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

- `src/seeds/plants/powderpuff-mimosa-data.yml`
- `src/seeds/plants/prairie-acacia-data.yml`
- `src/seeds/plants/prairie-blazingstar-data.yml`
- `src/seeds/plants/prairie-coneflower-data.yml`
- `src/seeds/plants/prairie-cordgrass-data.yml`
- `src/seeds/plants/prairie-crabapple-data.yml`
- `src/seeds/plants/prairie-phlox-data.yml`
- `src/seeds/plants/prairie-turnip-data.yml`
- `src/seeds/plants/prairie-wild-petunia-data.yml`
- `src/seeds/plants/prickly-ash-data.yml`
- `src/seeds/plants/prickly-elder-data.yml`
- `src/seeds/plants/pumpkin-data.yml`
- `src/seeds/plants/purple-chokeberry-data.yml`
- `src/seeds/plants/purple-lovegrass-data.yml`
- `src/seeds/plants/purple-salvia-data.yml`
- `src/seeds/plants/purslane-data.yml`
- `src/seeds/plants/quince-data.yml`
- `src/seeds/plants/quinoa-data.yml`
- `src/seeds/plants/radish-data.yml`
- `src/seeds/plants/ramie-data.yml`
- `src/seeds/plants/ramps-data.yml`
- `src/seeds/plants/rangpur-lime-data.yml`
- `src/seeds/plants/rattlebox-data.yml`
- `src/seeds/plants/rattlesnake-master-data.yml`
- `src/seeds/plants/red-bay-data.yml`
- `src/seeds/plants/red-button-ginger-data.yml`
- `src/seeds/plants/red-elderberry-data.yml`
- `src/seeds/plants/red-mulberry-data.yml`
- `src/seeds/plants/red-stopper-data.yml`
- `src/seeds/plants/red-veined-sorrel-data.yml`
- `src/seeds/plants/red_apple_tree-data.yml`
- `src/seeds/plants/redcurrant-data.yml`
- `src/seeds/plants/reishi-data.yml`
- `src/seeds/plants/resurrection-fern-data.yml`
- `src/seeds/plants/rhododendron-data.yml`
- `src/seeds/plants/rhubarb-data.yml`
- `src/seeds/plants/ribbon-palm-data.yml`
- `src/seeds/plants/riberry-data.yml`
- `src/seeds/plants/ribwort-plantain-data.yml`
- `src/seeds/plants/rice-data.yml`
- `src/seeds/plants/riverbank-grape-data.yml`
- `src/seeds/plants/rock-cotoneaster-data.yml`
- `src/seeds/plants/rock-rose-data.yml`
- `src/seeds/plants/rollinia-data.yml`
- `src/seeds/plants/rose-apple-data.yml`
- `src/seeds/plants/rough-blazingstar-data.yml`
- `src/seeds/plants/roughleaf-dogwood-data.yml`
- `src/seeds/plants/roundleaf-serviceberry-data.yml`
- `src/seeds/plants/royal-fern-data.yml`
- `src/seeds/plants/royal-palm-data.yml`

---

## When ALL Files Are Done

```bash
python3 validate.py --since 2h
python3 validate.py --fix --since 2h
./sync.sh --check
./sync.sh
git add -A
git commit -m "Purpose quality pass batch 13 of 19"
git push origin v2
rm review/purpose_batch_13_of_19.md
```

Zero warnings required before committing.
Then immediately start: review/purpose_batch_14_of_19.md
