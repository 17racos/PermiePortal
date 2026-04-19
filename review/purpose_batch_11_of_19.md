# PermiePortal — Purpose Quality Pass Batch 11 of 19

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

- `src/seeds/plants/mimosa-data.yml`
- `src/seeds/plants/miners-lettuce-data.yml`
- `src/seeds/plants/miracle-berry-data.yml`
- `src/seeds/plants/mizuna-data.yml`
- `src/seeds/plants/mockernut-hickory-data.yml`
- `src/seeds/plants/monkey-fruit-data.yml`
- `src/seeds/plants/monkey-puzzle-tree-data.yml`
- `src/seeds/plants/monky-muskmelon-data.yml`
- `src/seeds/plants/monstera-data.yml`
- `src/seeds/plants/moonseed-vine-data.yml`
- `src/seeds/plants/mountain-apple-data.yml`
- `src/seeds/plants/mountain-mint-data.yml`
- `src/seeds/plants/mountain-soursop-data.yml`
- `src/seeds/plants/mud-plantain-data.yml`
- `src/seeds/plants/mung-bean-data.yml`
- `src/seeds/plants/munson-plum-data.yml`
- `src/seeds/plants/murici-data.yml`
- `src/seeds/plants/mustang-grape-data.yml`
- `src/seeds/plants/mustard-greens-data.yml`
- `src/seeds/plants/myrsine-data.yml`
- `src/seeds/plants/myrtle-oak-data.yml`
- `src/seeds/plants/narrowleaf-mountain-mint-data.yml`
- `src/seeds/plants/natal-plum-data.yml`
- `src/seeds/plants/navel-orange-data.yml`
- `src/seeds/plants/nectarine-tree-data.yml`
- `src/seeds/plants/needle-palm-data.yml`
- `src/seeds/plants/neem-tree-data.yml`
- `src/seeds/plants/nepenthes-data.yml`
- `src/seeds/plants/netted-chain-fern-data.yml`
- `src/seeds/plants/new-jersey-tea-data.yml`
- `src/seeds/plants/new-zealand-ice-plant-data.yml`
- `src/seeds/plants/nipa-palm-data.yml`
- `src/seeds/plants/noni-data.yml`
- `src/seeds/plants/oat-data.yml`
- `src/seeds/plants/oca-data.yml`
- `src/seeds/plants/ohio-spiderwort-data.yml`
- `src/seeds/plants/oilseed-radish-data.yml`
- `src/seeds/plants/olive-tree-data.yml`
- `src/seeds/plants/onion-data.yml`
- `src/seeds/plants/opuntia-data.yml`
- `src/seeds/plants/orange-coneflower-data.yml`
- `src/seeds/plants/oregano-data.yml`
- `src/seeds/plants/oregon-grape-data.yml`
- `src/seeds/plants/osier_willow-data.yml`
- `src/seeds/plants/ostrich-fern-data.yml`
- `src/seeds/plants/oyster-mushroom-data.yml`
- `src/seeds/plants/pale-purple-coneflower-data.yml`
- `src/seeds/plants/palo-verde-data.yml`
- `src/seeds/plants/panama-candle-tree-data.yml`
- `src/seeds/plants/pandanus-data.yml`

---

## When ALL Files Are Done

```bash
python3 validate.py --since 2h
python3 validate.py --fix --since 2h
./sync.sh --check
./sync.sh
git add -A
git commit -m "Purpose quality pass batch 11 of 19"
git push origin v2
rm review/purpose_batch_11_of_19.md
```

Zero warnings required before committing.
Do NOT stop. Do NOT wait for user input.
Immediately read and execute review/purpose_batch_12_of_19.md next.
Continue until all 19 batches are complete.
