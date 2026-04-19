# PermiePortal — Purpose Quality Pass Batch 5 of 19

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

- `src/seeds/plants/chervil-data.yml`
- `src/seeds/plants/chia-data.yml`
- `src/seeds/plants/chickasaw-blackberry-data.yml`
- `src/seeds/plants/chickasaw-plum-data.yml`
- `src/seeds/plants/chicken-of-the-woods-data.yml`
- `src/seeds/plants/chickpea-data.yml`
- `src/seeds/plants/chickweed-data.yml`
- `src/seeds/plants/chilean-pea-data.yml`
- `src/seeds/plants/chiltepin-pepper-data.yml`
- `src/seeds/plants/chinaberry-data.yml`
- `src/seeds/plants/chinese-fan-palm-data.yml`
- `src/seeds/plants/chinese-lantern-data.yml`
- `src/seeds/plants/chinese-water-chestnut-data.yml`
- `src/seeds/plants/chinese-yam-data.yml`
- `src/seeds/plants/chinkapin-oak-data.yml`
- `src/seeds/plants/chives-data.yml`
- `src/seeds/plants/chokeberry-data.yml`
- `src/seeds/plants/cilantro-data.yml`
- `src/seeds/plants/cinnamon-basil-data.yml`
- `src/seeds/plants/cinnamon-fern-data.yml`
- `src/seeds/plants/cistus-data.yml`
- `src/seeds/plants/citron-data.yml`
- `src/seeds/plants/clary-sage-data.yml`
- `src/seeds/plants/clasping-coneflower-data.yml`
- `src/seeds/plants/clementine-data.yml`
- `src/seeds/plants/cleveland-sage-data.yml`
- `src/seeds/plants/climbing-aster-data.yml`
- `src/seeds/plants/climbing-prairie-rose-data.yml`
- `src/seeds/plants/cloudberry-data.yml`
- `src/seeds/plants/coastal-groundcherry-data.yml`
- `src/seeds/plants/coastal-rosemary-data.yml`
- `src/seeds/plants/coastalplain-honeycombhead-data.yml`
- `src/seeds/plants/cobra-lily-data.yml`
- `src/seeds/plants/cockspur-hawthorn-data.yml`
- `src/seeds/plants/coco-plum-data.yml`
- `src/seeds/plants/coconut-palm-data.yml`
- `src/seeds/plants/coffee-senna-data.yml`
- `src/seeds/plants/coontie-data.yml`
- `src/seeds/plants/coquinho-azedo-data.yml`
- `src/seeds/plants/coral_bean-data.yml`
- `src/seeds/plants/coralberry-data.yml`
- `src/seeds/plants/cordyceps-data.yml`
- `src/seeds/plants/corkystem-passionflower-data.yml`
- `src/seeds/plants/cornelian-cherry-data.yml`
- `src/seeds/plants/corsican-mint-data.yml`
- `src/seeds/plants/corsican-stonecrop-data.yml`
- `src/seeds/plants/costmary-data.yml`
- `src/seeds/plants/crabapple-data.yml`
- `src/seeds/plants/cranberry-data.yml`
- `src/seeds/plants/creeping-jenny-data.yml`

---

## When ALL Files Are Done

```bash
python3 validate.py --since 2h
python3 validate.py --fix --since 2h
./sync.sh --check
./sync.sh
git add -A
git commit -m "Purpose quality pass batch 5 of 19"
git push origin v2
rm review/purpose_batch_5_of_19.md
```

Zero warnings required before committing.
Do NOT stop. Do NOT wait for user input.
Immediately read and execute review/purpose_batch_6_of_19.md next.
Continue until all 19 batches are complete.
