# PermiePortal — Purpose Quality Pass Batch 19 of 19

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

- `src/seeds/plants/yellow-coneflower-data.yml`
- `src/seeds/plants/yellow-dock-data.yml`
- `src/seeds/plants/yellow-jessamine-data.yml`
- `src/seeds/plants/yellow-sweet-clover-data.yml`
- `src/seeds/plants/yellow-waterlily-data.yml`
- `src/seeds/plants/yellow-yam-data.yml`
- `src/seeds/plants/yellowhorn-tree-data.yml`
- `src/seeds/plants/yerba-mate-data.yml`
- `src/seeds/plants/yerba-santa-data.yml`
- `src/seeds/plants/yuzu-data.yml`
- `src/seeds/plants/zigzag-spiderwort-data.yml`
- `src/seeds/plants/zucchini-data.yml`

---

## When ALL Files Are Done

```bash
python3 validate.py --since 2h
python3 validate.py --fix --since 2h
./sync.sh --check
./sync.sh
git add -A
git commit -m "Purpose quality pass batch 19 of 19"
git push origin v2
rm review/purpose_batch_19_of_19.md
```

Zero warnings required before committing.
Then immediately start: review/purpose_batch_done_of_19.md
