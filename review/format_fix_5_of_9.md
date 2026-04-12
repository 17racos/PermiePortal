# Format Standardization — Batch 5 of 9

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

### Lychee
File: `src/seeds/plants/lychee-data.yml`

Issues:
- purpose field is prose — needs bullet format

### Maypop
File: `src/seeds/plants/maypop-data.yml`

Issues:
- description lacks structured emoji sections
- purpose field is prose — needs bullet format

### Milkweed
File: `src/seeds/plants/milkweed-data.yml`

Issues:
- purpose field is prose — needs bullet format

### Monky Muskmelon
File: `src/seeds/plants/monky-muskmelon-data.yml`

Issues:
- description lacks structured emoji sections
- purpose field is prose — needs bullet format

### Motherwort
File: `src/seeds/plants/motherwort-data.yml`

Issues:
- description lacks structured emoji sections
- purpose field is prose — needs bullet format

### Needle Palm
File: `src/seeds/plants/needle-palm-data.yml`

Issues:
- purpose field is prose — needs bullet format

### Neem
File: `src/seeds/plants/neem-data.yml`

Issues:
- description lacks structured emoji sections
- purpose field is prose — needs bullet format

### New Zealand Spinach
File: `src/seeds/plants/new-zealand-spinach-data.yml`

Issues:
- description lacks structured emoji sections
- purpose field is prose — needs bullet format

### Noni
File: `src/seeds/plants/noni-data.yml`

Issues:
- description lacks structured emoji sections

### Ostrich Fern
File: `src/seeds/plants/ostrich-fern-data.yml`

Issues:
- description lacks structured emoji sections
- purpose field is prose — needs bullet format

### Papyrus
File: `src/seeds/plants/papyrus-data.yml`

Issues:
- description lacks structured emoji sections

### Penguin Gourd
File: `src/seeds/plants/penguin-gourd-data.yml`

Issues:
- description lacks structured emoji sections

### Phacelia
File: `src/seeds/plants/phacelia-data.yml`

Issues:
- description lacks structured emoji sections

### Piedmont Purslane
File: `src/seeds/plants/piedmont-purslane-data.yml`

Issues:
- description lacks structured emoji sections

### Pitanga
File: `src/seeds/plants/pitanga-data.yml`

Issues:
- purpose field is prose — needs bullet format


---

## When Done

```bash
python3 validate.py --since 2h
./sync.sh --check
./sync.sh
rm review/format_fix_5_of_9.md
```

Then open `format_fix_6_of_9.md`
