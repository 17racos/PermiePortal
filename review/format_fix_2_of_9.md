# Format Standardization — Batch 2 of 9

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

### Bottle Gourd
File: `src/seeds/plants/bottle-gourd-data.yml`

Issues:
- description lacks structured emoji sections
- purpose field is prose — needs bullet format

### Breadfruit
File: `src/seeds/plants/breadfruit-data.yml`

Issues:
- description lacks structured emoji sections

### Broadleaf Plantain
File: `src/seeds/plants/broadleaf-plantain-data.yml`

Issues:
- description lacks structured emoji sections

### Buckwheat
File: `src/seeds/plants/buckwheat-data.yml`

Issues:
- description lacks structured emoji sections
- purpose field is prose — needs bullet format

### Buffalo Grass
File: `src/seeds/plants/buffalo-grass-data.yml`

Issues:
- purpose field is prose — needs bullet format

### Bushel Gourd
File: `src/seeds/plants/bushel-gourd-data.yml`

Issues:
- description lacks structured emoji sections
- purpose field is prose — needs bullet format

### Butia Palm
File: `src/seeds/plants/butia-palm-data.yml`

Issues:
- description lacks structured emoji sections

### Caimito
File: `src/seeds/plants/caimito-data.yml`

Issues:
- purpose field is prose — needs bullet format

### Calamondin
File: `src/seeds/plants/calamondin-data.yml`

Issues:
- description lacks structured emoji sections
- purpose field is prose — needs bullet format

### Cambuca
File: `src/seeds/plants/cambuca-data.yml`

Issues:
- description lacks structured emoji sections

### Camu Camu
File: `src/seeds/plants/camu-camu-data.yml`

Issues:
- description lacks structured emoji sections
- purpose field is prose — needs bullet format

### Canopy Trees
File: `src/seeds/plants/canopy-trees-data.yml`

Issues:
- description lacks structured emoji sections
- description contains geography label pattern
- purpose field is prose — needs bullet format

### Cardinal Flower
File: `src/seeds/plants/cardinal-flower-data.yml`

Issues:
- description lacks structured emoji sections
- purpose field is prose — needs bullet format

### Cherimoya
File: `src/seeds/plants/cherimoya-data.yml`

Issues:
- description lacks structured emoji sections
- purpose field is prose — needs bullet format

### Chinese Fan Palm
File: `src/seeds/plants/chinese-fan-palm-data.yml`

Issues:
- description lacks structured emoji sections
- purpose field is prose — needs bullet format


---

## When Done

```bash
python3 validate.py --since 2h
./sync.sh --check
./sync.sh
rm review/format_fix_2_of_9.md
```

Then open `format_fix_3_of_9.md`
