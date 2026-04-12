# Practitioner Notes — Batch 25 of 34

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

### Red Button Ginger
File: `src/seeds/plants/red-button-ginger-data.yml`
Scientific: *Costus woodsonii*
Zone: 9-11 | Layer: Herbaceous
Functions: Edible, Medicinal, Wildlife Attractor, Erosion Control, Border Plant, Ground Cover

### Red Veined Sorrel
File: `src/seeds/plants/red-veined-sorrel-data.yml`
Scientific: *Rumex sanguineus var. sanguineus*
Zone: 5-8 | Layer: Ground Cover
Functions: Edible, Ground Cover, Ornamental

### Red Apple Tree
File: `src/seeds/plants/red-apple-tree-data.yml`
Scientific: *Malus domestica 'Red Delicious'*
Zone: 4-8 | Layer: Canopy
Functions: Edible, Medicinal, Wildlife Attractor, Pollinator, Windbreaker, Border Plant

### Reishi Host
File: `src/seeds/plants/reishi-host-data.yml`
Scientific: *Ganoderma sessile (eastern U.S. lacquered bracket; complex)*
Zone: 6-11 | Layer: Tree
Functions: Medicinal, Mulcher

### Rhododendron
File: `src/seeds/plants/rhododendron-data.yml`
Scientific: *Rhododendron ponticum*
Zone: 4-9 | Layer: Shrub
Functions: Ornamental, Pollinator, Wildlife Attractor, Erosion Control

### Rhubarb
File: `src/seeds/plants/rhubarb-data.yml`
Scientific: *Rheum × hybridum*
Zone: 3-8 | Layer: Herbaceous
Functions: Edible, Mulcher, Erosion Control

### Ribwort Plantain
File: `src/seeds/plants/ribwort-plantain-data.yml`
Scientific: *Plantago lanceolata*
Zone: 3-9 | Layer: Herbaceous, Ground Cover
Functions: Edible, Medicinal, Dynamic Accumulator, Animal Fodder

### Rice
File: `src/seeds/plants/rice-data.yml`
Scientific: *Oryza sativa*
Zone: 9-11 | Layer: Herbaceous
Functions: Edible, Wildlife Attractor, Mulcher, Erosion Control, Animal Fodder, Water Purifier, Ground Cover

### Rock Rose
File: `src/seeds/plants/rock-rose-data.yml`
Scientific: *Cistus salviifolius*
Zone: 8-10 | Layer: Shrub, Ground Cover
Functions: Ornamental, Ground Cover, Wildlife Attractor, Erosion Control, Mulcher

### Rollinia
File: `src/seeds/plants/rollinia-data.yml`
Scientific: *Rollinia deliciosa*
Zone: 10-11 | Layer: Tree
Functions: Edible, Ornamental, Wildlife Attractor

### Root Beer Plant
File: `src/seeds/plants/root-beer-plant-data.yml`
Scientific: *Piper auritum*
Zone: 9-11 | Layer: Shrub
Functions: Edible, Medicinal, Wildlife Attractor, Ground Cover

### Rose Apple
File: `src/seeds/plants/rose-apple-data.yml`
Scientific: *Syzygium jambos*
Zone: 9-11 | Layer: Tree
Functions: Edible, Wildlife Attractor, Ornamental

### Roselle
File: `src/seeds/plants/roselle-data.yml`
Scientific: *Hibiscus sabdariffa*
Zone: 8-11 | Layer: Herbaceous, Shrub
Functions: Edible, Medicinal, Wildlife Attractor

### Roselle Hibiscus
File: `src/seeds/plants/roselle-hibiscus-data.yml`
Scientific: *Hibiscus sabdariffa*
Zone: 9-12 | Layer: Herbaceous
Functions: Edible, Medicinal, Pollinator, Wildlife Attractor, Mulcher, Dynamic Accumulator, Border Plant

### Rosemary
File: `src/seeds/plants/rosemary-data.yml`
Scientific: *Rosmarinus officinalis*
Zone: 7-10 | Layer: Shrub
Functions: Edible, Medicinal, Pollinator, Wildlife Attractor, Windbreaker, Border Plant, Pest Management

### Rue
File: `src/seeds/plants/rue-data.yml`
Scientific: *Ruta graveolens*
Zone: 4-10 | Layer: Herbaceous
Functions: Medicinal, Pollinator, Wildlife Attractor, Pest Management, Border Plant

### Rumberry
File: `src/seeds/plants/rumberry-data.yml`
Scientific: *Myrciaria floribunda*
Zone: 10-11 | Layer: Shrub, Tree
Functions: Edible, Wildlife Attractor, Ornamental, Mulcher

### Russian Olive
File: `src/seeds/plants/russian-olive-data.yml`
Scientific: *Elaeagnus angustifolia*
Zone: 2-7 | Layer: Tree, Shrub
Functions: Nitrogen Fixer, Wildlife Attractor, Windbreaker, Animal Fodder

### Sabal Palm
File: `src/seeds/plants/sabal-palm-data.yml`
Scientific: *Sabal palmetto*
Zone: 8-11 | Layer: Tree, Canopy
Functions: Wildlife Attractor, Erosion Control, Windbreaker, Edible

### Sacred Basil
File: `src/seeds/plants/sacred-basil-data.yml`
Scientific: *Ocimum tenuiflorum*
Zone: 10-12 | Layer: Herbaceous
Functions: Medicinal, Pollinator, Edible, Pest Management


---

## When Done

```bash
python3 validate.py --since 2h
./sync.sh --check
./sync.sh
rm review/practitioner_notes_25_of_34.md
```

Then open `practitioner_notes_26_of_34.md`
