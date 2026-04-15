# PermiePortal — Cursor Agent: Add Symptoms to All Pest YAMLs

Paste this entire prompt into Cursor Agent (not chat — Agent mode).

---

## Task

Add a `symptoms` field to every pest YAML file in `src/seeds/pests/`.
Do NOT modify any other fields.

---

## Symptoms Taxonomy

Use ONLY these standardized symptom tags — do not invent new ones:
holes-in-leaves
yellowing-leaves
wilting
sticky-residue
white-powder
leaf-spots
curling-leaves
webbing
chewed-stems
stem-damage
root-damage
fruit-damage
black-coating
distorted-growth
tunneling
galls
dropping-leaves
silvery-streaking
brown-edges
die-back
sooty-deposits
slime-trails
skeletonized-leaves
bark-damage
crown-damage

---

## Format

Add symptoms as a YAML list immediately after the `characteristics:` field
and before `control_methods:`:

```yaml
  symptoms:
  - holes-in-leaves
  - chewed-stems
  - wilting
```

---

## Examples

**Aphids:**
```yaml
  symptoms:
  - sticky-residue
  - curling-leaves
  - yellowing-leaves
  - distorted-growth
```

**Spider Mites:**
```yaml
  symptoms:
  - yellowing-leaves
  - webbing
  - silvery-streaking
  - brown-edges
```

**Powdery Mildew:**
```yaml
  symptoms:
  - white-powder
  - distorted-growth
  - yellowing-leaves
  - dropping-leaves
```

**Borers:**
```yaml
  symptoms:
  - tunneling
  - stem-damage
  - wilting
  - die-back
  - bark-damage
```

**Root Rot:**
```yaml
  symptoms:
  - wilting
  - root-damage
  - yellowing-leaves
  - dropping-leaves
  - crown-damage
```

---

## Rules

- Every pest must have 2-5 symptoms minimum
- Use only tags from the taxonomy above
- Place symptoms AFTER characteristics: and BEFORE control_methods:
- Do NOT use em dashes (—) anywhere
- Do NOT change any other fields
- Skip pests-data.yml and pests-data.yml.bak

---

## After Completing All Files
./sync.sh 2>&1 | grep -E "Pests:|Warnings:"
git add -A
git commit -m "Add symptoms field to all 200 pest YAMLs"
git push origin v2
