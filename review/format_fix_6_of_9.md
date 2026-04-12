# Format Standardization — Batch 6 of 9

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

### Pitomba
File: `src/seeds/plants/pitomba-data.yml`

Issues:
- description lacks structured emoji sections

### Pomelo
File: `src/seeds/plants/pomelo-data.yml`

Issues:
- description lacks structured emoji sections
- purpose field is prose — needs bullet format

### Pond Apple
File: `src/seeds/plants/pond-apple-data.yml`

Issues:
- description lacks structured emoji sections
- purpose field is prose — needs bullet format

### Rose Apple
File: `src/seeds/plants/rose-apple-data.yml`

Issues:
- purpose field is prose — needs bullet format

### Sabal Palm
File: `src/seeds/plants/sabal-palm-data.yml`

Issues:
- purpose field is prose — needs bullet format

### Samphire
File: `src/seeds/plants/samphire-data.yml`

Issues:
- purpose field is prose — needs bullet format

### Sassafras
File: `src/seeds/plants/sassafras-data.yml`

Issues:
- purpose field is prose — needs bullet format

### Sea Purslane
File: `src/seeds/plants/sea-purslane-data.yml`

Issues:
- description lacks structured emoji sections
- purpose field is prose — needs bullet format

### Sheep Sorrel
File: `src/seeds/plants/sheep-sorrel-data.yml`

Issues:
- purpose field is prose — needs bullet format

### Simpson Stopper
File: `src/seeds/plants/simpson-stopper-data.yml`

Issues:
- description contains geography label pattern

### Skirret
File: `src/seeds/plants/skirret-data.yml`

Issues:
- purpose field is prose — needs bullet format

### Snowberry
File: `src/seeds/plants/snowberry-data.yml`

Issues:
- purpose field is prose — needs bullet format

### Softstem Bulrush
File: `src/seeds/plants/softstem-bulrush-data.yml`

Issues:
- purpose field is prose — needs bullet format

### Soursop Leaf
File: `src/seeds/plants/soursop-leaf-data.yml`

Issues:
- purpose field is prose — needs bullet format

### Stinging Nettle
File: `src/seeds/plants/stinging-nettle-data.yml`

Issues:
- purpose field is prose — needs bullet format


---

## When Done

```bash
python3 validate.py --since 2h
./sync.sh --check
./sync.sh
rm review/format_fix_6_of_9.md
```

Then open `format_fix_7_of_9.md`
