# Practitioner Notes — Batch 14 of 34

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

### Glasswort
File: `src/seeds/plants/glasswort-data.yml`
Scientific: *Salicornia spp.*
Zone: 5-11 | Layer: Aquatic
Functions: Edible, Ground Cover, Wildlife Attractor, Soil Improvement

### Globe Thistle
File: `src/seeds/plants/globe-thistle-data.yml`
Scientific: *Echinops ritro*
Zone: 3-8 | Layer: Herbaceous
Functions: Ornamental, Pollinator, Wildlife Attractor, Border Plant, Dynamic Accumulator

### Gnetum
File: `src/seeds/plants/gnetum-data.yml`
Scientific: *Gnetum gnemon*
Zone: 10-12 | Layer: Tree
Functions: Edible, Ornamental, Shade Provider, Wildlife Attractor

### Goat's Rue
File: `src/seeds/plants/goats-rue-data.yml`
Scientific: *Galega officinalis*
Zone: 4-8 | Layer: Herbaceous
Functions: Nitrogen Fixer, Medicinal, Wildlife Attractor, Animal Fodder

### Goji Berry
File: `src/seeds/plants/goji-berry-data.yml`
Scientific: *Lycium barbarum*
Zone: 5-9 | Layer: Shrub
Functions: Edible, Medicinal, Wildlife Attractor, Border Plant

### Good King Henry
File: `src/seeds/plants/good-king-henry-data.yml`
Scientific: *Blitum bonus-henricus*
Zone: 3-9 | Layer: Herbaceous
Functions: Edible, Ground Cover, Dynamic Accumulator, Wildlife Attractor

### Gooseberry
File: `src/seeds/plants/gooseberry-data.yml`
Scientific: *Ribes uva-crispa*
Zone: 3-8 | Layer: Shrub
Functions: Edible, Wildlife Attractor, Border Plant

### Gopher Apple
File: `src/seeds/plants/gopher-apple-data.yml`
Scientific: *Geobalanus oblongifolius*
Zone: 8b-10b | Layer: Ground Cover
Functions: Wildlife Attractor, Ground Cover, Erosion Control, Drought Tolerant

### Gotu Kola
File: `src/seeds/plants/gotu-kola-data.yml`
Scientific: *Centella asiatica*
Zone: 8-11 | Layer: Ground Cover
Functions: Edible, Medicinal, Ground Cover

### Goumi Berry
File: `src/seeds/plants/goumi-berry-data.yml`
Scientific: *Elaeagnus multiflora*
Zone: 5-9 | Layer: Shrub
Functions: Edible, Nitrogen Fixer, Wildlife Attractor, Border Plant, Erosion Control

### Gravel Root
File: `src/seeds/plants/gravel-root-data.yml`
Scientific: *Eutrochium purpureum*
Zone: 3-9 | Layer: Herbaceous
Functions: Medicinal, Pollinator, Wildlife Attractor, Water Retention, Biomass

### Graviola
File: `src/seeds/plants/graviola-data.yml`
Scientific: *Annona muricata*
Zone: 10-11 | Layer: Tree
Functions: Edible, Medicinal, Wildlife Attractor, Shade Provider

### Green and Gold
File: `src/seeds/plants/green-and-gold-data.yml`
Scientific: *Chrysogonum virginianum*
Zone: 5-9 | Layer: Ground Cover, Herb
Functions: Ground Cover, Pollinator, Ornamental, Erosion Control

### Green Bean
File: `src/seeds/plants/green-bean-data.yml`
Scientific: *Phaseolus vulgaris*
Zone: 3-10 | Layer: Herbaceous
Functions: Edible, Nitrogen Fixer, Pollinator, Ground Cover

### Green Apple Tree
File: `src/seeds/plants/green-apple-tree-data.yml`
Scientific: *Malus domestica 'Granny Smith'*
Zone: 4-8 | Layer: Canopy
Functions: Edible, Medicinal, Wildlife Attractor, Pollinator, Windbreaker, Border Plant

### Groundnut
File: `src/seeds/plants/groundnut-data.yml`
Scientific: *Apios americana*
Zone: 3-9 | Layer: Vine, Root
Functions: Edible, Nitrogen Fixer, Wildlife Attractor

### Groundnut
File: `src/seeds/plants/groundnut-data.yml`
Scientific: *Apios americana*
Zone: 3-9 | Layer: Vine, Root
Functions: Edible, Nitrogen Fixer, Wildlife Attractor, Ground Cover

### Groundplum Milkvetch
File: `src/seeds/plants/groundplum-milkvetch-data.yml`
Scientific: *Astragalus crassicarpus*
Zone: 4-8 | Layer: Herbaceous
Functions: Edible, Nitrogen Fixer, Wildlife Attractor, Ground Cover

### Grumichama
File: `src/seeds/plants/grumichama-data.yml`
Scientific: *Eugenia brasiliensis*
Zone: 10-11 | Layer: Tree, Shrub
Functions: Edible, Wildlife Attractor, Ornamental

### Grumixama
File: `src/seeds/plants/grumixama-data.yml`
Scientific: *Eugenia brasiliensis*
Zone: 9-11 | Layer: Tree
Functions: Edible, Wildlife Attractor, Ornamental


---

## When Done

```bash
python3 validate.py --since 2h
./sync.sh --check
./sync.sh
rm review/practitioner_notes_14_of_34.md
```

Then open `practitioner_notes_15_of_34.md`
