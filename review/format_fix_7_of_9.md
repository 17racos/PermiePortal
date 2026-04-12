# Format Standardization — Batch 7 of 9

> **Agent mode only.** Fix format issues only — do NOT rewrite content.
> Preserve all existing botanical information. Only fix structure.

---

## Two Tasks

### Task 1 — Description Format
Descriptions must use this exact structure with emoji headers:
[Opening paragraph — what the plant is, origin, appearance, size]
☀️💧 Sun and Water Requirements:

[Sun preference]
[Water needs]
[Soil]

✂️ Propagation:

[Method 1 with timing]
[Method 2 with timing]

🌾 Harvest / Best Use Timing:

[When and how]


If the content is already there but uses plain headers like "Sun and water:"
or "Propagation:" — just add the emoji and reformat as bullets.
Do NOT rewrite the actual information.

### Task 2 — Purpose Format
Purpose must use bullet format with the function name bolded before a colon:

```yaml
  purpose: |-
    - Edible: explanation of how it serves this function
    - Nitrogen Fixer: explanation of the mechanism
    - Mulcher: explanation of the role
```

If purpose is currently a prose paragraph, convert it to this format.
Extract the function names from the plant_function list to use as bullet headers.
Do NOT lose any information — just restructure it.

---

## Geographic Rules
- Remove any leftover "subtropical and tropical Americas / subtropical:" labels
- Do NOT add regional framing — keep descriptions universal
- Temperatures: Fahrenheit with Celsius in parentheses

---

## Plants to Fix (15 in this batch)

### Sunrose
File: `src/seeds/plants/sunrose-data.yml`

Issues:
- purpose field is prose — needs bullet format

### Swamp Milkweed
File: `src/seeds/plants/swamp-milkweed-data.yml`

Issues:
- purpose field is prose — needs bullet format

### Sweet Alyssum
File: `src/seeds/plants/sweet-alyssum-data.yml`

Issues:
- purpose field is prose — needs bullet format

### Sweet Cassava variants
File: `src/seeds/plants/sweet-cassava-variants-data.yml`

Issues:
- purpose field is prose — needs bullet format

### Sweet Coltsfoot
File: `src/seeds/plants/sweet-coltsfoot-data.yml`

Issues:
- purpose field is prose — needs bullet format

### Sweet Flag
File: `src/seeds/plants/sweet-flag-data.yml`

Issues:
- purpose field is prose — needs bullet format

### Sweet Gale
File: `src/seeds/plants/sweet-gale-data.yml`

Issues:
- purpose field is prose — needs bullet format

### Sweet Leaf
File: `src/seeds/plants/sweet-leaf-data.yml`

Issues:
- description lacks structured emoji sections

### Sweet Woodruff
File: `src/seeds/plants/sweet-woodruff-data.yml`

Issues:
- purpose field is prose — needs bullet format

### Tamarisk
File: `src/seeds/plants/tamarisk-data.yml`

Issues:
- purpose field is prose — needs bullet format

### Tansy
File: `src/seeds/plants/tansy-data.yml`

Issues:
- purpose field is prose — needs bullet format

### Tea Tree
File: `src/seeds/plants/tea-tree-data.yml`

Issues:
- purpose field is prose — needs bullet format

### Tephrosia vogelii
File: `src/seeds/plants/tephrosia-vogelii-data.yml`

Issues:
- purpose field is prose — needs bullet format

### Texas Persimmon
File: `src/seeds/plants/texas-persimmon-data.yml`

Issues:
- purpose field is prose — needs bullet format

### Thai Basil
File: `src/seeds/plants/thai-basil-data.yml`

Issues:
- description lacks structured emoji sections
- purpose field is prose — needs bullet format


---

## When Done

```bash
python3 validate.py --since 2h
./sync.sh --check
./sync.sh
rm review/format_fix_7_of_9.md
```

Then open `format_fix_8_of_9.md`
