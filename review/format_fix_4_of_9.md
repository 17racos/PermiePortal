# Format Standardization — Batch 4 of 9

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

### Guanabana
File: `src/seeds/plants/guanabana-data.yml`

Issues:
- purpose field is prose — needs bullet format

### Guava
File: `src/seeds/plants/guava-data.yml`

Issues:
- purpose field is prose — needs bullet format

### Highbush Blueberry
File: `src/seeds/plants/highbush-blueberry-data.yml`

Issues:
- description contains geography label pattern

### Ivy Gourd
File: `src/seeds/plants/ivy-gourd-data.yml`

Issues:
- purpose field is prose — needs bullet format

### Jackfruit
File: `src/seeds/plants/jackfruit-data.yml`

Issues:
- description lacks structured emoji sections
- purpose field is prose — needs bullet format

### Jambolan
File: `src/seeds/plants/jambolan-data.yml`

Issues:
- purpose field is prose — needs bullet format

### Jamelao
File: `src/seeds/plants/jamelao-data.yml`

Issues:
- description lacks structured emoji sections

### Jatoba
File: `src/seeds/plants/jatoba-data.yml`

Issues:
- purpose field is prose — needs bullet format

### Jicama
File: `src/seeds/plants/jicama-data.yml`

Issues:
- description lacks structured emoji sections
- purpose field is prose — needs bullet format

### Jucara Palm
File: `src/seeds/plants/jucara-palm-data.yml`

Issues:
- description lacks structured emoji sections
- purpose field is prose — needs bullet format

### Jute
File: `src/seeds/plants/jute-data.yml`

Issues:
- purpose field is prose — needs bullet format

### Kwai Muk
File: `src/seeds/plants/kwai-muk-data.yml`

Issues:
- description lacks structured emoji sections
- description contains geography label pattern
- purpose field is prose — needs bullet format

### Lemon Basil
File: `src/seeds/plants/lemon-basil-data.yml`

Issues:
- description lacks structured emoji sections

### Longan
File: `src/seeds/plants/longan-data.yml`

Issues:
- purpose field is prose — needs bullet format

### Lotus
File: `src/seeds/plants/lotus-data.yml`

Issues:
- description lacks structured emoji sections
- purpose field is prose — needs bullet format


---

## When Done

```bash
python3 validate.py --since 2h
./sync.sh --check
./sync.sh
rm review/format_fix_4_of_9.md
```

Then open `format_fix_5_of_9.md`
