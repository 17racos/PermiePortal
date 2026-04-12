# Format Standardization — Batch 9 of 9

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

## Plants to Fix (4 in this batch)

### Wild Leek
File: `src/seeds/plants/wild-leek-data.yml`

Issues:
- description lacks structured emoji sections
- purpose field is prose — needs bullet format

### Wild Passionfruit
File: `src/seeds/plants/wild-passionfruit-data.yml`

Issues:
- description lacks structured emoji sections
- purpose field is prose — needs bullet format

### Wisteria
File: `src/seeds/plants/wisteria-data.yml`

Issues:
- description lacks structured emoji sections
- description contains geography label pattern
- purpose field is prose — needs bullet format

### Yellow Dock
File: `src/seeds/plants/yellow-dock-data.yml`

Issues:
- description lacks structured emoji sections
- purpose field is prose — needs bullet format


---

## When Done

```bash
python3 validate.py --since 2h
./sync.sh --check
./sync.sh
rm review/format_fix_9_of_9.md
```

✅ Final batch — commit:
```bash
git add -A && git commit -m 'standardize description and purpose format'
```
