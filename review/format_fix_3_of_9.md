# Format Standardization — Batch 3 of 9

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

### Creeping Jenny
File: `src/seeds/plants/creeping-jenny-data.yml`

Issues:
- description lacks structured emoji sections
- purpose field is prose — needs bullet format

### Creeping Oregano
File: `src/seeds/plants/creeping-oregano-data.yml`

Issues:
- description lacks structured emoji sections

### Culantro
File: `src/seeds/plants/culantro-data.yml`

Issues:
- purpose field is prose — needs bullet format

### Damiana
File: `src/seeds/plants/damiana-data.yml`

Issues:
- description lacks structured emoji sections
- purpose field is prose — needs bullet format

### Dinosaur Gourd
File: `src/seeds/plants/dinosaur-gourd-data.yml`

Issues:
- description lacks structured emoji sections

### Dynamic accumulators
File: `src/seeds/plants/dynamic-accumulators-data.yml`

Issues:
- description contains geography label pattern

### Edible Hibiscus
File: `src/seeds/plants/edible-hibiscus-data.yml`

Issues:
- description lacks structured emoji sections
- purpose field is prose — needs bullet format

### Elephant Foot Yam
File: `src/seeds/plants/elephant-foot-yam-data.yml`

Issues:
- description lacks structured emoji sections
- purpose field is prose — needs bullet format

### Fever Grass
File: `src/seeds/plants/fever-grass-data.yml`

Issues:
- description lacks structured emoji sections

### Flax
File: `src/seeds/plants/flax-data.yml`

Issues:
- description lacks structured emoji sections
- description contains geography label pattern
- purpose field is prose — needs bullet format

### Glasswort
File: `src/seeds/plants/glasswort-data.yml`

Issues:
- description contains geography label pattern

### Gnetum
File: `src/seeds/plants/gnetum-data.yml`

Issues:
- description lacks structured emoji sections
- purpose field is prose — needs bullet format

### Groundnut
File: `src/seeds/plants/groundnut-apios-data.yml`

Issues:
- description lacks structured emoji sections
- purpose field is prose — needs bullet format

### Groundplum Milkvetch
File: `src/seeds/plants/groundplum-milkvetch-data.yml`

Issues:
- description lacks structured emoji sections
- purpose field is prose — needs bullet format

### Grumixama
File: `src/seeds/plants/grumixama-data.yml`

Issues:
- purpose field is prose — needs bullet format


---

## When Done

```bash
python3 validate.py --since 2h
./sync.sh --check
./sync.sh
rm review/format_fix_3_of_9.md
```

Then open `format_fix_4_of_9.md`
