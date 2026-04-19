# PermiePortal — Purpose Quality Pass Batch 2 of 19

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

- `src/seeds/plants/arugula-data.yml`
- `src/seeds/plants/ashe-magnolia-data.yml`
- `src/seeds/plants/ashitaba-data.yml`
- `src/seeds/plants/asparagus-bean-data.yml`
- `src/seeds/plants/asparagus-data.yml`
- `src/seeds/plants/atemoya-data.yml`
- `src/seeds/plants/atlantic-white-cedar-data.yml`
- `src/seeds/plants/autumn-olive-data.yml`
- `src/seeds/plants/avocado-data.yml`
- `src/seeds/plants/azalea-data.yml`
- `src/seeds/plants/bacupari-data.yml`
- `src/seeds/plants/bacuri-data.yml`
- `src/seeds/plants/bael-fruit-data.yml`
- `src/seeds/plants/bald-cypress-data.yml`
- `src/seeds/plants/bamboo-data.yml`
- `src/seeds/plants/banana-passionfruit-data.yml`
- `src/seeds/plants/baobab-data.yml`
- `src/seeds/plants/barbados-cherry-data.yml`
- `src/seeds/plants/barley-data.yml`
- `src/seeds/plants/bay-bean-data.yml`
- `src/seeds/plants/beach-bean-data.yml`
- `src/seeds/plants/beach-morning-glory-data.yml`
- `src/seeds/plants/beach-strawberry-data.yml`
- `src/seeds/plants/beaked-hazelnut-data.yml`
- `src/seeds/plants/bearberry-cotoneaster-data.yml`
- `src/seeds/plants/bearberry-data.yml`
- `src/seeds/plants/bee-bush-data.yml`
- `src/seeds/plants/beebalm-data.yml`
- `src/seeds/plants/beet-data.yml`
- `src/seeds/plants/bell-pepper-data.yml`
- `src/seeds/plants/bengal-quince-data.yml`
- `src/seeds/plants/betony-data.yml`
- `src/seeds/plants/big-bluestem-data.yml`
- `src/seeds/plants/bigleaf-magnolia-data.yml`
- `src/seeds/plants/bignay-data.yml`
- `src/seeds/plants/bilimbi-data.yml`
- `src/seeds/plants/bird-of-paradise-data.yml`
- `src/seeds/plants/bismarck-palm-data.yml`
- `src/seeds/plants/bitter-melon-data.yml`
- `src/seeds/plants/bitter-orange-data.yml`
- `src/seeds/plants/bitter-yam-data.yml`
- `src/seeds/plants/black-chokeberry-data.yml`
- `src/seeds/plants/black-cohosh-data.yml`
- `src/seeds/plants/black-eyed-susan-data.yml`
- `src/seeds/plants/black-ginger-data.yml`
- `src/seeds/plants/black-medic-data.yml`
- `src/seeds/plants/black-mulga-data.yml`
- `src/seeds/plants/black-pepper-vine-data.yml`
- `src/seeds/plants/black-sage-data.yml`
- `src/seeds/plants/black-sapote-data.yml`

---

## When ALL Files Are Done

```bash
python3 validate.py --since 2h
python3 validate.py --fix --since 2h
./sync.sh --check
./sync.sh
git add -A
git commit -m "Purpose quality pass batch 2 of 19"
git push origin v2
rm review/purpose_batch_2_of_19.md
```

Zero warnings required before committing.
Then immediately start: review/purpose_batch_3_of_19.md
