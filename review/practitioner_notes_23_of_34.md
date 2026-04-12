# Practitioner Notes — Batch 23 of 34

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

### Penguin Gourd
File: `src/seeds/plants/penguin-gourd-data.yml`
Scientific: *Lagenaria siceraria*
Zone: 3-11 | Layer: Vine
Functions: Ornamental, Edible, Fiber

### Pennyroyal
File: `src/seeds/plants/pennyroyal-data.yml`
Scientific: *Mentha pulegium*
Zone: 6-9 | Layer: Herbaceous, Ground Cover
Functions: Medicinal, Pollinator, Ground Cover, Pest Management

### Perennial Basil
File: `src/seeds/plants/perennial-basil-data.yml`
Scientific: *Ocimum gratissimum*
Zone: 9-11 | Layer: Herbaceous, Shrub
Functions: Edible, Medicinal, Wildlife Attractor

### Perennial Leek
File: `src/seeds/plants/perennial-leek-data.yml`
Scientific: *Allium ampeloprasum*
Zone: 6-10 | Layer: Herbaceous, Ground Cover
Functions: Edible, Ground Cover, Pest Management, Pollinator

### Perennial Peanut
File: `src/seeds/plants/perennial-peanut-data.yml`
Scientific: *Arachis glabrata*
Zone: 8-11 | Layer: Ground Cover
Functions: Edible, Nitrogen Fixer, Ground Cover, Erosion Control, Animal Fodder

### Persimmon Tree
File: `src/seeds/plants/persimmon-tree-data.yml`
Scientific: *Diospyros spp.*
Zone: 4-10 | Layer: Canopy, Sub-Canopy
Functions: Edible, Wildlife Attractor, Windbreaker, Border Plant, Erosion Control

### Phacelia
File: `src/seeds/plants/phacelia-data.yml`
Scientific: *Phacelia tanacetifolia*
Zone: 2-11 | Layer: Herbaceous
Functions: Pollinator, Green Manure, Ground Cover, Wildlife Attractor

### Pickerelweed
File: `src/seeds/plants/pickerelweed-data.yml`
Scientific: *Pontederia cordata*
Zone: 3-11 | Layer: Aquatic
Functions: Edible, Wildlife Attractor, Water Purifier, Ornamental

### Piedmont Purslane
File: `src/seeds/plants/piedmont-purslane-data.yml`
Scientific: *Portulaca pilosa*
Zone: 5-11 | Layer: Herbaceous, Ground Cover
Functions: Edible, Ground Cover, Wildlife Attractor

### Pigeon Pea
File: `src/seeds/plants/pigeon-pea-data.yml`
Scientific: *Cajanus cajan*
Zone: 9-13 | Layer: Shrub, Sub-Canopy
Functions: Edible, Nitrogen Fixer, Mulcher, Dynamic Accumulator, Erosion Control, Animal Fodder, Wildlife Attractor, Windbreaker

### Pigeonwood
File: `src/seeds/plants/pigeonwood-data.yml`
Scientific: *Trema orientalis*
Zone: 10-12 | Layer: Tree, Shrub
Functions: Wildlife Attractor, Biomass, Erosion Control, Animal Fodder, Mulcher

### Pineapple Pear
File: `src/seeds/plants/pineapple-pear-data.yml`
Scientific: *Pyrus communis 'Pineapple'*
Zone: 5-9 | Layer: Sub-Canopy
Functions: Edible, Pollinator, Wildlife Attractor, Nitrogen Fixer, Dynamic Accumulator, Erosion Control, Windbreaker, Border Plant, Pest Management

### Pineapple Guava
File: `src/seeds/plants/pineapple-guava-data.yml`
Scientific: *Acca sellowiana*
Zone: 8-11 | Layer: Shrub
Functions: Edible, Pollinator, Wildlife Attractor, Windbreaker, Border Plant

### Pindo Palm
File: `src/seeds/plants/pindo-palm-data.yml`
Scientific: *Butia capitata*
Zone: 8-11 | Layer: Tree
Functions: Edible, Ornamental, Windbreaker, Wildlife Attractor

### Pineapple Sage
File: `src/seeds/plants/pineapple-sage-data.yml`
Scientific: *Salvia elegans*
Zone: 8-11 | Layer: Herbaceous, Shrub
Functions: Edible, Medicinal, Pollinator, Wildlife Attractor, Mulcher, Dynamic Accumulator, Erosion Control, Border Plant

### Pineapple
File: `src/seeds/plants/pineapple-data.yml`
Scientific: *Ananas comosus*
Zone: 9-12 | Layer: Ground Cover
Functions: Edible, Medicinal, Wildlife Attractor, Ground Cover

### Piper
File: `src/seeds/plants/piper-data.yml`
Scientific: *Piper spp.*
Zone: 10-12 | Layer: Shrub, Vine
Functions: Edible, Medicinal, Pollinator, Wildlife Attractor, Ground Cover

### Pitanga
File: `src/seeds/plants/pitanga-data.yml`
Scientific: *Eugenia uniflora*
Zone: 9-11 | Layer: Shrub, Tree
Functions: Edible, Wildlife Attractor, Ornamental, Border Plant

### Pitcher Plant
File: `src/seeds/plants/pitcher-plant-data.yml`
Scientific: *Sarracenia purpurea*
Zone: 3-9 | Layer: Herbaceous
Functions: Pest Management, Wildlife Attractor, Ground Cover

### Pitomba
File: `src/seeds/plants/pitomba-data.yml`
Scientific: *Eugenia luschnathiana*
Zone: 9b-11 | Layer: Tree, Shrub
Functions: Edible, Ornamental, Wildlife Attractor


---

## When Done

```bash
python3 validate.py --since 2h
./sync.sh --check
./sync.sh
rm review/practitioner_notes_23_of_34.md
```

Then open `practitioner_notes_24_of_34.md`
