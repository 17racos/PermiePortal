# Practitioner Notes — Batch 26 of 34

> **Agent mode only.** Add `practitioner_notes` to each listed plant YAML.
> Do NOT change any other fields. Do NOT create new files.

---

## What Is practitioner_notes

A field containing 2–5 short declarative facts that a knowledgeable grower
would tell another grower standing in the field. Things not obvious from the
description. Things that change how you grow or use the plant.

**Format in YAML:**
```yaml
  practitioner_notes: |-
    First fact here.
    Second fact here.
    Third fact here.
```

Each fact on its own line. No bullet characters. No numbering.
Use the `|-` block scalar so newlines are preserved.

---

## Content Rules

**Write facts like these:**
- Specific numbers: "Leaves contain gram-for-gram more calcium than milk"
- Coppicing/management: "Coppice hard at 1m (3ft) annually — tall trees make harvest impractical"
- Toxicity warnings: "All parts toxic raw; cooking destroys the cyanogenic glycosides"
- Propagation edge cases: "Seeds viable for 1 year maximum — always use fresh seed"
- Ecological surprises: "One of few plants that fixes nitrogen AND accumulates phosphorus simultaneously"
- Processing notes: "Dry leaves at under 40°C (104°F) or nutrient content degrades significantly"
- Guild roles: "Aggressive root competition — plant 3m (10ft) from fruit trees minimum"
- Historical/ethnobotanical: "Traditional use as a water clarifier — crushed seeds settle turbid water"

**Do NOT write:**
- Anything already in the description or purpose field
- Generic praise: "this is a very useful plant"
- Regional framing: "popular in Florida" or "grows well in the Caribbean"
- Vague statements: "has many uses"
- More than 5 facts

**Geographic standard:** All of the Americas, zones 3–13.
Use universal language. Temperatures in Fahrenheit with Celsius in
parentheses where relevant: "frost-hardy to 10°F (-12°C)"

---

## Plants (20 total in this batch)

### Sage
File: `src/seeds/plants/sage-data.yml`
Scientific: *Salvia officinalis*
Zone: 4-10 | Layer: Herbaceous
Functions: Edible, Medicinal, Pollinator, Wildlife Attractor, Border Plant, Pest Management

### Salal
File: `src/seeds/plants/salal-data.yml`
Scientific: *Gaultheria shallon*
Zone: 7-9 | Layer: Shrub, Ground Cover
Functions: Edible, Ground Cover, Wildlife Attractor, Erosion Control

### Saltbush
File: `src/seeds/plants/saltbush-data.yml`
Scientific: *Atriplex halimus*
Zone: 8-11 | Layer: Shrub
Functions: Edible, Animal Fodder, Erosion Control, Windbreaker, Dynamic Accumulator

### Saltgrass
File: `src/seeds/plants/saltgrass-data.yml`
Scientific: *Distichlis spicata*
Zone: 4-11 | Layer: Herbaceous, Ground Cover
Functions: Erosion Control, Ground Cover, Wildlife Attractor, Water Retention

### Samphire
File: `src/seeds/plants/samphire-data.yml`
Scientific: *Salicornia europaea*
Zone: 5-10 | Layer: Herbaceous, Ground Cover
Functions: Edible, Erosion Control, Wildlife Attractor

### Sand Cherry
File: `src/seeds/plants/sand-cherry-data.yml`
Scientific: *Prunus pumila*
Zone: 2-7 | Layer: Shrub
Functions: Edible, Wildlife Attractor, Erosion Control, Border Plant, Ornamental

### Sapodilla
File: `src/seeds/plants/sapodilla-data.yml`
Scientific: *Manilkara zapota*
Zone: 10-12 | Layer: Tree
Functions: Edible, Shade Provider, Wildlife Attractor, Timber

### Sassafras
File: `src/seeds/plants/sassafras-data.yml`
Scientific: *Sassafras albidum*
Zone: 4-9 | Layer: Tree
Functions: Edible, Wildlife Attractor, Medicinal, Mulcher

### Saw Palmetto
File: `src/seeds/plants/saw-palmetto-data.yml`
Scientific: *Serenoa repens*
Zone: 8-10 | Layer: Shrub
Functions: Edible, Medicinal, Wildlife Attractor, Ground Cover, Erosion Control

### Scorpion Weed
File: `src/seeds/plants/scorpion-weed-data.yml`
Scientific: *Heliotropium angiospermum*
Zone: 8b-11 | Layer: Herbaceous, Ground Cover
Functions: Wildlife Attractor, Border Plant, Erosion Control

### Screw Pine
File: `src/seeds/plants/screw-pine-data.yml`
Scientific: *Pandanus utilis*
Zone: 10-12 | Layer: Tree
Functions: Edible, Fiber, Erosion Control, Windbreaker, Ornamental

### Sea Buckthorn
File: `src/seeds/plants/sea-buckthorn-data.yml`
Scientific: *Hippophae rhamnoides*
Zone: 3-7 | Layer: Shrub
Functions: Edible, Nitrogen Fixer, Wildlife Attractor, Erosion Control, Windbreaker, Medicinal

### Sea Kale
File: `src/seeds/plants/sea-kale-data.yml`
Scientific: *Crambe maritima*
Zone: 4-9 | Layer: Herbaceous, Ground Cover
Functions: Edible, Ground Cover, Erosion Control, Ornamental, Dynamic Accumulator

### Sea Plantain
File: `src/seeds/plants/sea-plantain-data.yml`
Scientific: *Plantago maritima*
Zone: 3-9 | Layer: Herbaceous, Ground Cover
Functions: Edible, Medicinal, Erosion Control, Wildlife Attractor

### Sea Purslane
File: `src/seeds/plants/sea-purslane-data.yml`
Scientific: *Sesuvium portulacastrum*
Zone: 9-11 | Layer: Ground Cover, Aquatic
Functions: Edible, Erosion Control, Ground Cover, Wildlife Attractor

### Seagrape
File: `src/seeds/plants/seagrape-data.yml`
Scientific: *Coccoloba uvifera*
Zone: 10-11 | Layer: Shrub, Tree
Functions: Edible, Erosion Control, Wildlife Attractor, Windbreaker

### Sedum
File: `src/seeds/plants/sedum-data.yml`
Scientific: *Sedum spp.*
Zone: 3-9 | Layer: Ground Cover
Functions: Ground Cover, Pollinator, Drought Tolerant, Ornamental

### Seminole Pumpkin
File: `src/seeds/plants/seminole-pumpkin-data.yml`
Scientific: *Cucurbita moschata*
Zone: 8-11 | Layer: Vine
Functions: Edible, Ground Cover, Animal Fodder

### Sensitive Plant
File: `src/seeds/plants/sensitive-plant-data.yml`
Scientific: *Mimosa pudica*
Zone: 9-11 | Layer: Herbaceous, Ground Cover
Functions: Nitrogen Fixer, Soil Improvement, Wildlife Attractor, Ornamental

### Sesbania
File: `src/seeds/plants/sesbania-data.yml`
Scientific: *Sesbania spp.*
Zone: 9-11 | Layer: Sub-Canopy, Shrub, Aquatic
Functions: Nitrogen Fixer, Animal Fodder, Biofuel, Soil Improvement, Ornamental


---

## When Done

```bash
python3 validate.py --since 2h
./sync.sh --check
./sync.sh
rm review/practitioner_notes_26_of_34.md
```

Then open `practitioner_notes_27_of_34.md`
