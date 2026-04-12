# Format Standardization — Batch 1 of 9

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

### Açaí Palm
File: `src/seeds/plants/acai-palm-data.yml`

Issues:
- description lacks structured emoji sections
- purpose field is prose — needs bullet format

### Achira
File: `src/seeds/plants/achira-data.yml`

Issues:
- purpose field is prose — needs bullet format

### African Blue Basil
File: `src/seeds/plants/african-blue-basil-data.yml`

Issues:
- description lacks structured emoji sections
- purpose field is prose — needs bullet format

### Aguaje Palm
File: `src/seeds/plants/aguaje-palm-data.yml`

Issues:
- description lacks structured emoji sections
- purpose field is prose — needs bullet format

### American Elderberry
File: `src/seeds/plants/american-elderberry-data.yml`

Issues:
- description lacks structured emoji sections
- purpose field is prose — needs bullet format

### American Hazelnut
File: `src/seeds/plants/american-hazelnut-data.yml`

Issues:
- description lacks structured emoji sections

### Andrographis
File: `src/seeds/plants/andrographis-data.yml`

Issues:
- description lacks structured emoji sections
- purpose field is prose — needs bullet format

### Araza
File: `src/seeds/plants/araza-data.yml`

Issues:
- description lacks structured emoji sections
- purpose field is prose — needs bullet format

### Autumn Olive
File: `src/seeds/plants/autumn-olive-data.yml`

Issues:
- description lacks structured emoji sections
- purpose field is prose — needs bullet format

### Bacuri
File: `src/seeds/plants/bacuri-data.yml`

Issues:
- description lacks structured emoji sections
- purpose field is prose — needs bullet format

### Banana Passionfruit
File: `src/seeds/plants/banana-passionfruit-data.yml`

Issues:
- description lacks structured emoji sections
- purpose field is prose — needs bullet format

### Bismarck Palm
File: `src/seeds/plants/bismarck-palm-data.yml`

Issues:
- description lacks structured emoji sections
- purpose field is prose — needs bullet format

### Black Sapote
File: `src/seeds/plants/black-sapote-data.yml`

Issues:
- description lacks structured emoji sections
- purpose field is prose — needs bullet format

### Black Locust
File: `src/seeds/plants/black_locust-data.yml`

Issues:
- description lacks structured emoji sections

### Blue Flag Iris
File: `src/seeds/plants/blue-flag-iris-data.yml`

Issues:
- purpose field is prose — needs bullet format


---

## When Done

```bash
python3 validate.py --since 2h
./sync.sh --check
./sync.sh
rm review/format_fix_1_of_9.md
```

Then open `format_fix_2_of_9.md`
