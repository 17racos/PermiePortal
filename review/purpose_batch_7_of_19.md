# PermiePortal — Purpose Quality Pass Batch 7 of 19

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

- `src/seeds/plants/edible-hibiscus-data.yml`
- `src/seeds/plants/eggplant-data.yml`
- `src/seeds/plants/elderberry-wine-data.yml`
- `src/seeds/plants/elecampane-data.yml`
- `src/seeds/plants/elephant-apple-data.yml`
- `src/seeds/plants/elephant-foot-yam-data.yml`
- `src/seeds/plants/elephant_grass-data.yml`
- `src/seeds/plants/elephantopus-data.yml`
- `src/seeds/plants/elliott-blueberry-data.yml`
- `src/seeds/plants/elliotts-bluestem-data.yml`
- `src/seeds/plants/epazote-data.yml`
- `src/seeds/plants/evergreen-huckleberry-data.yml`
- `src/seeds/plants/false-indigo-data.yml`
- `src/seeds/plants/fetterbush-data.yml`
- `src/seeds/plants/fever-few-data.yml`
- `src/seeds/plants/fiber-and-industrial-data.yml`
- `src/seeds/plants/finger-cherry-data.yml`
- `src/seeds/plants/finger-lime-data.yml`
- `src/seeds/plants/fireweed-data.yml`
- `src/seeds/plants/fish-mint-data.yml`
- `src/seeds/plants/flatwoods-plum-data.yml`
- `src/seeds/plants/flax-data.yml`
- `src/seeds/plants/floating-heart-data.yml`
- `src/seeds/plants/florida-anise-data.yml`
- `src/seeds/plants/florida-boxwood-data.yml`
- `src/seeds/plants/florida-gamagrass-data.yml`
- `src/seeds/plants/florida-leadplant-data.yml`
- `src/seeds/plants/florida-maple-data.yml`
- `src/seeds/plants/florida-mint-data.yml`
- `src/seeds/plants/florida-paintbrush-data.yml`
- `src/seeds/plants/florida-pusley-data.yml`
- `src/seeds/plants/florida-tasselflower-data.yml`
- `src/seeds/plants/florida-thatch-palm-data.yml`
- `src/seeds/plants/florida-willow-data.yml`
- `src/seeds/plants/fringe-tree-data.yml`
- `src/seeds/plants/frogfruit-data.yml`
- `src/seeds/plants/frost-grape-data.yml`
- `src/seeds/plants/frosted-hawthorn-data.yml`
- `src/seeds/plants/fruit-sage-data.yml`
- `src/seeds/plants/galangal-data.yml`
- `src/seeds/plants/garden-huckleberry-data.yml`
- `src/seeds/plants/gaura-data.yml`
- `src/seeds/plants/giant-bulrush-data.yml`
- `src/seeds/plants/giant-granadilla-data.yml`
- `src/seeds/plants/glasswort-data.yml`
- `src/seeds/plants/globe-thistle-data.yml`
- `src/seeds/plants/gnetum-data.yml`
- `src/seeds/plants/goat-plum-data.yml`
- `src/seeds/plants/goats-rue-data.yml`
- `src/seeds/plants/golden-chinquapin-data.yml`

---

## When ALL Files Are Done

```bash
python3 validate.py --since 2h
python3 validate.py --fix --since 2h
./sync.sh --check
./sync.sh
git add -A
git commit -m "Purpose quality pass batch 7 of 19"
git push origin v2
rm review/purpose_batch_7_of_19.md
```

Zero warnings required before committing.
Then immediately start: review/purpose_batch_8_of_19.md
