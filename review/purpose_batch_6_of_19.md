# PermiePortal — Purpose Quality Pass Batch 6 of 19

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

- `src/seeds/plants/creeping-phlox-data.yml`
- `src/seeds/plants/creeping-raspberry-data.yml`
- `src/seeds/plants/creeping-rosemary-data.yml`
- `src/seeds/plants/creeping-thyme-data.yml`
- `src/seeds/plants/crimson_clover-data.yml`
- `src/seeds/plants/crossvine-data.yml`
- `src/seeds/plants/crotalaria-data.yml`
- `src/seeds/plants/crowberry-data.yml`
- `src/seeds/plants/crown-vetch-data.yml`
- `src/seeds/plants/cucamelon-data.yml`
- `src/seeds/plants/cucumber-data.yml`
- `src/seeds/plants/culantro-data.yml`
- `src/seeds/plants/cupuacu-data.yml`
- `src/seeds/plants/currant-data.yml`
- `src/seeds/plants/curry-leaf-tree-data.yml`
- `src/seeds/plants/curry-plant-data.yml`
- `src/seeds/plants/custard-apple-data.yml`
- `src/seeds/plants/cythera-data.yml`
- `src/seeds/plants/dahoon-holly-data.yml`
- `src/seeds/plants/daikon-data.yml`
- `src/seeds/plants/damiana-data.yml`
- `src/seeds/plants/darrow-blueberry-data.yml`
- `src/seeds/plants/deerberry-data.yml`
- `src/seeds/plants/dense-blazingstar-data.yml`
- `src/seeds/plants/desert-date-data.yml`
- `src/seeds/plants/desert-hackberry-data.yml`
- `src/seeds/plants/desert-ironwood-data.yml`
- `src/seeds/plants/desert-marigold-data.yml`
- `src/seeds/plants/desert-sage-data.yml`
- `src/seeds/plants/desert-willow-data.yml`
- `src/seeds/plants/desert-yam-data.yml`
- `src/seeds/plants/devils-trumpet-data.yml`
- `src/seeds/plants/dewberry-data.yml`
- `src/seeds/plants/dichondra-data.yml`
- `src/seeds/plants/dogfennel-data.yml`
- `src/seeds/plants/dollarweed-data.yml`
- `src/seeds/plants/dotted-hawthorn-data.yml`
- `src/seeds/plants/downy-rose-myrtle-data.yml`
- `src/seeds/plants/downy-serviceberry-data.yml`
- `src/seeds/plants/dragon-fruit-data.yml`
- `src/seeds/plants/duckweed-data.yml`
- `src/seeds/plants/dwarf-huckleberry-data.yml`
- `src/seeds/plants/dwarf-live-oak-data.yml`
- `src/seeds/plants/dwarf-palmetto-data.yml`
- `src/seeds/plants/earth-chestnut-data.yml`
- `src/seeds/plants/eastern-blazingstar-data.yml`
- `src/seeds/plants/eastern-gamagrass-data.yml`
- `src/seeds/plants/eastern-redbud-data.yml`
- `src/seeds/plants/ebony-spleenwort-data.yml`
- `src/seeds/plants/eddoe-data.yml`

---

## When ALL Files Are Done

```bash
python3 validate.py --since 2h
python3 validate.py --fix --since 2h
./sync.sh --check
./sync.sh
git add -A
git commit -m "Purpose quality pass batch 6 of 19"
git push origin v2
rm review/purpose_batch_6_of_19.md
```

Zero warnings required before committing.
Do NOT stop. Do NOT wait for user input.
Immediately read and execute review/purpose_batch_7_of_19.md next.
Continue until all 19 batches are complete.
