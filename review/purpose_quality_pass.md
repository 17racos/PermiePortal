# PermiePortal — Purpose Section Quality Pass

## YOUR TASK
You are Cursor Agent in Agent mode. Rewrite the `purpose:` field for every plant
YAML in `src/seeds/plants/` to match the Moringa gold standard.

Do NOT ask questions. Start immediately. Work through all files before running
any commands.

---

## Gold Standard Reference
Read this file first and internalize the voice and structure before writing anything:
`src/seeds/plants/moringa-data.yml`

Also read for additional reference:
`src/seeds/plants/okra-data.yml`
`src/seeds/plants/elderberry-data.yml`
`src/seeds/plants/comfrey-data.yml`

---

## Quality Standard

Each purpose entry must:

1. **Use this exact format for each function:**
Function Name: Specific explanation of how this plant performs this function
in a permaculture system -- what part, what benefit, what system behavior.

2. **Be specific, not generic.** Bad: "Edible: The fruit is edible." Good: "Edible:
   Ripe fruit harvested when skin gives slightly -- sweet-tart pulp eaten fresh,
   dried, or juiced; seeds roasted like nuts; young leaves used as pot herb."

3. **Capture ALL documented permaculture functions** for that plant. Common functions
   to check for each plant:
   - Edible (what part, how used, harvest timing)
   - Medicinal (what use, what part, any cautions)
   - Nitrogen Fixer (if legume or has root associations)
   - Dynamic Accumulator (what minerals, how released)
   - Mulcher / Chop-and-Drop (biomass production rate)
   - Animal Fodder (what animals, what parts)
   - Pollinator (what insects, when, what flowers)
   - Wildlife Attractor (birds, mammals, insects)
   - Windbreaker (height, density, placement)
   - Erosion Control (root system, soil stabilization)
   - Shade Provider (canopy density, what benefits below)
   - Water Retention (root system, mulch layer)
   - Ornamental (aesthetic value, design use)
   - Fiber (what fiber, what use)
   - Dye Plant (what color, what part)
   - Water Purification (if documented)
   - Plant Growth Stimulant (if documented)
   - Pest Repellent (what pests, what mechanism)
   - Habitat (what wildlife uses it for shelter/nesting)

4. **Use ' -- ' not em dashes (—)** — em dashes cause YAML parse errors

5. **Match the plant_function tags already in the file** — if plant_function lists
   "Nitrogen Fixer" then the purpose section must have a Nitrogen Fixer entry.
   You may ADD functions not currently listed in plant_function if well documented.

6. **Do not add functions that don't apply.** A decorative ornamental grass doesn't
   need a "Water Purification" entry. Use judgment.

7. **Minimum 3 functions per plant.** Most plants should have 4-8.

---

## Geographic Context
- Audience: All of the Americas — zones 3-13
- Do NOT write region-specific framing
- Universal climate language: temperate, subtropical, tropical
- Temperatures in Fahrenheit with Celsius in parentheses

---

## Process
1. Read moringa-data.yml and okra-data.yml to internalize the standard
2. For each plant file, read the existing purpose: field and plant_function: list
3. Rewrite purpose: to match gold standard quality
4. Only change the `purpose:` field -- do not touch any other fields
5. Work through ALL 1000+ files before running validation

---

## Files to Update
All files in `src/seeds/plants/` except `_archived_duplicates/`

Process them alphabetically. Skip any file where the purpose section already
clearly meets the gold standard (has 4+ specific entries with permaculture
system reasoning). When in doubt, improve it.

---

## When ALL Files Are Done

```bash
python3 validate.py --since 4h
python3 validate.py --fix --since 4h
./sync.sh --check
./sync.sh
git add -A
git commit -m "Purpose quality pass -- all plants updated to Moringa gold standard"
git push origin v2
rm review/purpose_quality_pass.md
```

Zero warnings required before committing.
