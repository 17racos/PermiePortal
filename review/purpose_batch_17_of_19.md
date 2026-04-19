# PermiePortal — Purpose Quality Pass Batch 17 of 19

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

- `src/seeds/plants/tickseed-sunflower-data.yml`
- `src/seeds/plants/tilo-data.yml`
- `src/seeds/plants/toothache-plant-data.yml`
- `src/seeds/plants/toyon-data.yml`
- `src/seeds/plants/tree-collard-data.yml`
- `src/seeds/plants/tree-medik-data.yml`
- `src/seeds/plants/tree-spinach-data.yml`
- `src/seeds/plants/tropical-almond-data.yml`
- `src/seeds/plants/tropical-spinach-data.yml`
- `src/seeds/plants/tucuma-palm-data.yml`
- `src/seeds/plants/tulsi-data.yml`
- `src/seeds/plants/turkey-oak-data.yml`
- `src/seeds/plants/turkey-tail-data.yml`
- `src/seeds/plants/turkish-rocket-data.yml`
- `src/seeds/plants/turmeric-ginger-data.yml`
- `src/seeds/plants/turnip-data.yml`
- `src/seeds/plants/twinflower-data.yml`
- `src/seeds/plants/ulluco-data.yml`
- `src/seeds/plants/umbrella-magnolia-data.yml`
- `src/seeds/plants/uvaia-data.yml`
- `src/seeds/plants/valencia-orange-data.yml`
- `src/seeds/plants/velvet-bean-data.yml`
- `src/seeds/plants/velvetleaf-data.yml`
- `src/seeds/plants/venus-flytrap-data.yml`
- `src/seeds/plants/verbena-bonariensis-data.yml`
- `src/seeds/plants/vetiver-grass-data.yml`
- `src/seeds/plants/vietnamese-mint-data.yml`
- `src/seeds/plants/vines-data.yml`
- `src/seeds/plants/viper-bugloss-data.yml`
- `src/seeds/plants/virginia-buttonweed-data.yml`
- `src/seeds/plants/virginia-mountain-mint-data.yml`
- `src/seeds/plants/virginia-rose-data.yml`
- `src/seeds/plants/vitex-data.yml`
- `src/seeds/plants/walking-onion-data.yml`
- `src/seeds/plants/walnut-tree-data.yml`
- `src/seeds/plants/walters-viburnum-data.yml`
- `src/seeds/plants/warrigal-greens-data.yml`
- `src/seeds/plants/water-aquatic-data.yml`
- `src/seeds/plants/water-hickory-data.yml`
- `src/seeds/plants/water-hyacinth-data.yml`
- `src/seeds/plants/water-lettuce-data.yml`
- `src/seeds/plants/water-mimosa-data.yml`
- `src/seeds/plants/water-plantain-data.yml`
- `src/seeds/plants/water-yam-data.yml`
- `src/seeds/plants/watercress-data.yml`
- `src/seeds/plants/watermelon-data.yml`
- `src/seeds/plants/watershield-data.yml`
- `src/seeds/plants/wax-apple-data.yml`
- `src/seeds/plants/wax-currant-data.yml`
- `src/seeds/plants/wax-gourd-data.yml`

---

## When ALL Files Are Done

```bash
python3 validate.py --since 2h
python3 validate.py --fix --since 2h
./sync.sh --check
./sync.sh
git add -A
git commit -m "Purpose quality pass batch 17 of 19"
git push origin v2
rm review/purpose_batch_17_of_19.md
```

Zero warnings required before committing.
Do NOT stop. Do NOT wait for user input.
Immediately read and execute review/purpose_batch_18_of_19.md next.
Continue until all 19 batches are complete.
