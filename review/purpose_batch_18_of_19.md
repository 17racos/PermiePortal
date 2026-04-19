# PermiePortal — Purpose Quality Pass Batch 18 of 19

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

- `src/seeds/plants/wax-myrtle-data.yml`
- `src/seeds/plants/weeping-lovegrass-data.yml`
- `src/seeds/plants/western-soapberry-data.yml`
- `src/seeds/plants/wheat-data.yml`
- `src/seeds/plants/white-sage-data.yml`
- `src/seeds/plants/white-sapote-data.yml`
- `src/seeds/plants/white-stopper-data.yml`
- `src/seeds/plants/white-wild-indigo-data.yml`
- `src/seeds/plants/white-yam-data.yml`
- `src/seeds/plants/wild-anise-data.yml`
- `src/seeds/plants/wild-basil-data.yml`
- `src/seeds/plants/wild-blue-phlox-data.yml`
- `src/seeds/plants/wild-caraway-data.yml`
- `src/seeds/plants/wild-carrot-data.yml`
- `src/seeds/plants/wild-chervil-data.yml`
- `src/seeds/plants/wild-coffee-data.yml`
- `src/seeds/plants/wild-columbine-data.yml`
- `src/seeds/plants/wild-crabapple-data.yml`
- `src/seeds/plants/wild-cumin-data.yml`
- `src/seeds/plants/wild-eggplant-data.yml`
- `src/seeds/plants/wild-ginger-data.yml`
- `src/seeds/plants/wild-guava-data.yml`
- `src/seeds/plants/wild-indigo-bush-data.yml`
- `src/seeds/plants/wild-indigo-data.yml`
- `src/seeds/plants/wild-lime-data.yml`
- `src/seeds/plants/wild-mustard-greens-data.yml`
- `src/seeds/plants/wild-olive-data.yml`
- `src/seeds/plants/wild-oregano-data.yml`
- `src/seeds/plants/wild-passionfruit-data.yml`
- `src/seeds/plants/wild-petunia-data.yml`
- `src/seeds/plants/wild-rice-data.yml`
- `src/seeds/plants/wild-sarsaparilla-data.yml`
- `src/seeds/plants/wild-senna-data.yml`
- `src/seeds/plants/wild-stonecrop-data.yml`
- `src/seeds/plants/wild-sweet-potato-data.yml`
- `src/seeds/plants/windmill-palm-data.yml`
- `src/seeds/plants/wine-cap-data.yml`
- `src/seeds/plants/winged-bean-data.yml`
- `src/seeds/plants/winter-rye-data.yml`
- `src/seeds/plants/winter-savory-data.yml`
- `src/seeds/plants/winter-squash-data.yml`
- `src/seeds/plants/wiregrass-data.yml`
- `src/seeds/plants/wireweed-data.yml`
- `src/seeds/plants/wisteria-data.yml`
- `src/seeds/plants/wonderberry-data.yml`
- `src/seeds/plants/wood-sorrel-data.yml`
- `src/seeds/plants/woodland-sunflower-data.yml`
- `src/seeds/plants/yacon-data.yml`
- `src/seeds/plants/yam-daisy-data.yml`
- `src/seeds/plants/yaupon-holly-data.yml`

---

## When ALL Files Are Done

```bash
python3 validate.py --since 2h
python3 validate.py --fix --since 2h
./sync.sh --check
./sync.sh
git add -A
git commit -m "Purpose quality pass batch 18 of 19"
git push origin v2
rm review/purpose_batch_18_of_19.md
```

Zero warnings required before committing.
Then immediately start: review/purpose_batch_19_of_19.md
