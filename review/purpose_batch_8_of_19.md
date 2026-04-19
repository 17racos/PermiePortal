# PermiePortal — Purpose Quality Pass Batch 8 of 19

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

- `src/seeds/plants/golden-currant-data.yml`
- `src/seeds/plants/goldenmane-tickseed-data.yml`
- `src/seeds/plants/good-king-henry-data.yml`
- `src/seeds/plants/gooseberry-data.yml`
- `src/seeds/plants/gopher-apple-data.yml`
- `src/seeds/plants/gopher-tortoise-burrow-plants-data.yml`
- `src/seeds/plants/gorse-data.yml`
- `src/seeds/plants/gotu-kola-data.yml`
- `src/seeds/plants/goumi-data.yml`
- `src/seeds/plants/grapefruit-data.yml`
- `src/seeds/plants/great-blue-lobelia-data.yml`
- `src/seeds/plants/green-and-gold-data.yml`
- `src/seeds/plants/green-bean-data.yml`
- `src/seeds/plants/green-hawthorn-data.yml`
- `src/seeds/plants/green_apple_tree-data.yml`
- `src/seeds/plants/ground-cherry-data.yml`
- `src/seeds/plants/groundnut-data.yml`
- `src/seeds/plants/groundplum-milkvetch-data.yml`
- `src/seeds/plants/groundsel-tree-data.yml`
- `src/seeds/plants/grumichama-data.yml`
- `src/seeds/plants/guava-data.yml`
- `src/seeds/plants/guayule-data.yml`
- `src/seeds/plants/gulf-muhly-data.yml`
- `src/seeds/plants/hairawn-muhly-data.yml`
- `src/seeds/plants/hairy-beggarsticks-data.yml`
- `src/seeds/plants/hairy-grama-data.yml`
- `src/seeds/plants/hairy-indigo-data.yml`
- `src/seeds/plants/hawthorn-data.yml`
- `src/seeds/plants/hedge-cotoneaster-data.yml`
- `src/seeds/plants/hemp-data.yml`
- `src/seeds/plants/henequen-data.yml`
- `src/seeds/plants/hercules-club-data.yml`
- `src/seeds/plants/highbush-blueberry-data.yml`
- `src/seeds/plants/highbush-cranberry-data.yml`
- `src/seeds/plants/hoary-plantain-data.yml`
- `src/seeds/plants/hog-plum-data.yml`
- `src/seeds/plants/holy_basil-data.yml`
- `src/seeds/plants/honey-melon-sage-data.yml`
- `src/seeds/plants/honeyberry-data.yml`
- `src/seeds/plants/hop-shoots-data.yml`
- `src/seeds/plants/horehound-data.yml`
- `src/seeds/plants/horse-nettle-data.yml`
- `src/seeds/plants/hortulan-plum-data.yml`
- `src/seeds/plants/huacatay-data.yml`
- `src/seeds/plants/hummingbird-sage-data.yml`
- `src/seeds/plants/hyacinth-bean-data.yml`
- `src/seeds/plants/ice-plant-data.yml`
- `src/seeds/plants/ice_cream_bean_tree-data.yml`
- `src/seeds/plants/iceberg-lettuce-data.yml`
- `src/seeds/plants/ilama-data.yml`

---

## When ALL Files Are Done

```bash
python3 validate.py --since 2h
python3 validate.py --fix --since 2h
./sync.sh --check
./sync.sh
git add -A
git commit -m "Purpose quality pass batch 8 of 19"
git push origin v2
rm review/purpose_batch_8_of_19.md
```

Zero warnings required before committing.
Do NOT stop. Do NOT wait for user input.
Immediately read and execute review/purpose_batch_9_of_19.md next.
Continue until all 19 batches are complete.
