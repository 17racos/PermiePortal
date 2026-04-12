# Format Standardization — Batch 8 of 9

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

### Tick Trefoil
File: `src/seeds/plants/tick-trefoil-data.yml`

Issues:
- purpose field is prose — needs bullet format

### Toothache Plant
File: `src/seeds/plants/toothache-plant-data.yml`

Issues:
- description lacks structured emoji sections
- purpose field is prose — needs bullet format

### Tropical Spinach
File: `src/seeds/plants/tropical-spinach-data.yml`

Issues:
- description lacks structured emoji sections
- purpose field is prose — needs bullet format

### Tulsi
File: `src/seeds/plants/tulsi-data.yml`

Issues:
- description lacks structured emoji sections
- purpose field is prose — needs bullet format

### Valerian
File: `src/seeds/plants/valerian-data.yml`

Issues:
- purpose field is prose — needs bullet format

### Vetiver Grass
File: `src/seeds/plants/vetiver-grass-data.yml`

Issues:
- description lacks structured emoji sections

### Walter's Viburnum
File: `src/seeds/plants/walters-viburnum-data.yml`

Issues:
- description lacks structured emoji sections
- purpose field is prose — needs bullet format

### Warrigal Greens
File: `src/seeds/plants/warrigal-greens-data.yml`

Issues:
- description lacks structured emoji sections
- purpose field is prose — needs bullet format

### Water Chestnut
File: `src/seeds/plants/water-chestnut-data.yml`

Issues:
- description lacks structured emoji sections
- purpose field is prose — needs bullet format

### Water Hyacinth
File: `src/seeds/plants/water-hyacinth-data.yml`

Issues:
- description lacks structured emoji sections
- purpose field is prose — needs bullet format

### Water Yam
File: `src/seeds/plants/water-yam-data.yml`

Issues:
- description lacks structured emoji sections
- purpose field is prose — needs bullet format

### Wax Gourd
File: `src/seeds/plants/wax-gourd-data.yml`

Issues:
- description lacks structured emoji sections

### Wax Jambu
File: `src/seeds/plants/wax-jambu-data.yml`

Issues:
- description lacks structured emoji sections
- purpose field is prose — needs bullet format

### White Sapote
File: `src/seeds/plants/white-sapote-data.yml`

Issues:
- purpose field is prose — needs bullet format

### White Yam
File: `src/seeds/plants/white-yam-data.yml`

Issues:
- description lacks structured emoji sections


---

## When Done

```bash
python3 validate.py --since 2h
./sync.sh --check
./sync.sh
rm review/format_fix_8_of_9.md
```

Then open `format_fix_9_of_9.md`
