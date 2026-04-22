# PermiePortal — Enrichment Audit & Auto-Fix

> Agent mode only. Operate on ONE plant file at a time.
> Goal: Detect and FIX weak, invalid, or suboptimal enrichment data.
> Do NOT explain changes. Apply fixes directly.

---

## Plants to Audit

Select plants where data_quality_score < 0.99 and description is not NEEDS_DATA:

```bash
python3 - << 'EOF'
import json
plants = json.load(open('src/data/plants.json'))
low = [p for p in plants
       if p['data_quality_score'] < 0.99
       and p.get('description') != 'NEEDS_DATA']
for p in sorted(low, key=lambda x: x['data_quality_score']):
    print(f"  {p['data_quality_score']:.3f}  src/seeds/plants/{p['slug']}-data.yml")
EOF
```

Work through each file returned, one at a time. After each file run:
```bash
./sync.sh --check 2>&1 | grep "⚠️" | grep -v "companions quarantined\|^  ⚠️  [0-9]"
```
Zero warnings required before moving to next plant.

---

## Reference Standard

Use src/seeds/plants/moringa-data.yml as the gold standard for:
- depth
- specificity
- usefulness to a grower
- ecological accuracy

---

## Core Principle

This is NOT a formatting pass.
This is a semantic + structural quality audit.

All output must:
- pass validation
- maintain 0.99+ quality score
- improve real-world usefulness

---

## Audit + Fix Rules

### 1. PURPOSE FIELD (CRITICAL)

Enforce ALL:

- Every plant_function MUST appear in purpose
- Every purpose line MUST map to a plant_function
- Use exact format:
  FunctionName: description -- mechanism

Fix the following issues:
- Weak descriptions → make specific and measurable
- Missing mechanisms → add how/why it works
- Generic phrases → replace with real behavior
- Incorrect mappings → correct them

DO NOT:
- invent new functions outside VALID_FUNCTIONS
- force-fit incorrect functions

If a function is unclear or invalid:
- REMOVE it (converter handles routing elsewhere)

---

### 2. COMPANIONS (HIGHEST RISK AREA)

You MUST optimize for:
- ecological validity
- decision-making usefulness
- non-redundancy

#### Enforce:

- MAX 5 companions_unresolved
- MAX 4 companion_categories
- Minimum 3 total companion references
- At least 1 resolved companion IF possible

#### Fix:

- Remove vague entries:
  plants, trees, vegetables, crops, flowers, shrubs

- Remove low-value generics:
  anything not actionable to a grower

- Replace weak entries with:
  - specific species (if known)
  - or better unresolved entries

- Deduplicate across ALL fields

#### Normalization:

If an unresolved entry likely maps to a real plant:
- Check if a slug exists: ls src/seeds/plants/SLUG-data.yml
- Move it to companions if valid
- Remove from unresolved

DO NOT:
- invent slugs
- duplicate across fields

#### Ordering (IMPORTANT):

Reorder ALL companion lists:

1. Strongest ecological relationship
2. Most useful to grower decisions
3. Most recognizable plants

---

### 3. COMPANION QUALITY (ANTI-OVERFITTING)

Fix this common failure:

If companions look like a generic "companion planting list":
- reduce list size
- prioritize ecological relationships instead

Examples of GOOD:
- shared soil conditions
- canopy layering
- nutrient interactions
- pest interactions

Examples of BAD:
- blog-style planting lists
- overly broad compatibility claims

---

### 4. PESTS (SEMANTIC FILTER REQUIRED)

Enforce:

- Minimum 2 pests (if cultivated plant)
- MUST exist in pests-data.yml (exact match)

Fix:

- Remove obscure or low-relevance pests
- Replace with:
  - common
  - well-documented
  - multi-region relevant pests

Prioritize:
- pests affecting yield
- pests commonly encountered by growers

Avoid:
- rare edge-case pests
- overly region-specific issues unless critical

---

### 5. DESCRIPTION QUALITY

Ensure:

- ≥400 characters
- covers:
  - origin + form + size
  - sun + water
  - propagation (2+ methods with timing)
  - harvest timing

Fix:

- overly generic wording
- missing propagation detail
- missing harvest timing
- weak specificity

Make it:
- practical
- actionable
- grounded in real growing behavior

---

### 6. CAUTIONS

- Remove filler or vague warnings
- Keep only:
  - real antagonistic relationships
  - meaningful growing risks

If none:
→ "None documented"

---

### 7. FIELD OBSERVATIONS

- MUST remain empty ("") unless clearly firsthand
- Remove any generic or inferred content

---

### 8. FINAL VALIDATION (MANDATORY BEFORE FINISH)

Ensure ALL:

- No duplicates across companion fields
- companions_unresolved ≤ 5
- companion_categories ≤ 4
- At least 1 resolved companion IF possible
- All pests valid + relevant
- Purpose fully aligned with plant_function
- No vague or placeholder content

If ANY rule fails:
→ fix it before completing

---

## Output Rules

- Modify the plant file directly
- Do NOT add explanations
- Do NOT summarize changes
- Do NOT leave TODOs or placeholders

Only output the corrected data.

## food_role Classification (edible plants only)

If `plant_function` includes `Edible`, the plant MUST have `food_role` set to one of:

- `anchor` — primary food backbone (fruit trees, staple crops, root crops, major vegetables)
- `support` — secondary edible (herbs, leafy greens, edible support plants)
- `specialty` — niche/novelty/medicinal-leaning edible (fungi, unusual edibles, carnivorous plants)

If `plant_function` does NOT include `Edible`, remove `food_role` entirely or leave it absent.

Classification rule:
> "Would I build a food-producing guild around this plant by default?"
> Yes → anchor | Maybe/secondary → support | No/niche → specialty

Examples:
- Tomato, Banana, Pigeon Pea, Moringa → anchor
- Basil, Lemongrass, Borage → support
- Shiitake, Shampoo Ginger, Florida Pusley → specialty
