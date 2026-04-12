# Practitioner Notes — Batch 22 of 34

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

### Oyster Mushroom Host
File: `src/seeds/plants/oyster-mushroom-host-data.yml`
Scientific: *Pleurotus ostreatus*
Zone: 5-12 | Layer: Tree
Functions: Edible, Medicinal, Mulcher, Soil Improvement

### Palo Verde
File: `src/seeds/plants/palo-verde-data.yml`
Scientific: *Parkinsonia florida*
Zone: 8-11 | Layer: Tree
Functions: Nitrogen Fixer, Shade Provider, Wildlife Attractor, Ornamental

### Palmetto Palm
File: `src/seeds/plants/palmetto-palm-data.yml`
Scientific: *Sabal palmetto*
Zone: 8-11 | Layer: Canopy
Functions: Edible, Medicinal, Wildlife Attractor, Windbreaker, Erosion Control

### Pandanus
File: `src/seeds/plants/pandanus-data.yml`
Scientific: *Pandanus tectorius*
Zone: 10-13 | Layer: Tree
Functions: Fiber, Ornamental, Windbreaker, Erosion Control

### Papaya
File: `src/seeds/plants/papaya-data.yml`
Scientific: *Carica papaya*
Zone: 9-11 | Layer: Canopy
Functions: Edible, Medicinal, Wildlife Attractor, Mulcher, Dynamic Accumulator, Erosion Control, Animal Fodder, Border Plant, Pest Management

### Papyrus
File: `src/seeds/plants/papyrus-data.yml`
Scientific: *Cyperus papyrus*
Zone: 9-11 | Layer: Aquatic
Functions: Water Purifier, Wildlife Attractor, Border Plant

### Parsley
File: `src/seeds/plants/parsley-data.yml`
Scientific: *Petroselinum crispum*
Zone: 2-11 | Layer: Herbaceous
Functions: Edible, Medicinal, Ground Cover

### Parsnip
File: `src/seeds/plants/parsnip-data.yml`
Scientific: *Pastinaca sativa*
Zone: 2-9 | Layer: Herbaceous
Functions: Edible, Dynamic Accumulator, Erosion Control, Wildlife Attractor

### Partridge Acacia
File: `src/seeds/plants/partridge-acacia-data.yml`
Scientific: *Vachellia farnesiana*
Zone: 8-11 | Layer: Tree, Shrub
Functions: Nitrogen Fixer, Wildlife Attractor, Windbreaker, Border Plant

### Partridge Pea
File: `src/seeds/plants/partridge-pea-data.yml`
Scientific: *Chamaecrista fasciculata*
Zone: 3-9 | Layer: Herbaceous
Functions: Nitrogen Fixer, Wildlife Attractor, Soil Improvement, Ground Cover

### Partridgeberry
File: `src/seeds/plants/partridgeberry-data.yml`
Scientific: *Mitchella repens*
Zone: 3-7 | Layer: Ground Cover
Functions: Edible, Wildlife Attractor, Ornamental, Ground Cover

### Passionflower
File: `src/seeds/plants/passionflower-data.yml`
Scientific: *Passiflora incarnata*
Zone: 5-9 | Layer: Vine
Functions: Edible, Medicinal, Pollinator, Wildlife Attractor, Ornamental

### Paw Paw
File: `src/seeds/plants/paw-paw-data.yml`
Scientific: *Asimina triloba*
Zone: 5-9 | Layer: Sub-Canopy, Shrub
Functions: Edible, Medicinal, Wildlife Attractor, Pollinator, Border Plant, Erosion Control

### Pawpaw
File: `src/seeds/plants/pawpaw-data.yml`
Scientific: *Asimina triloba*
Zone: 5-9 | Layer: Tree
Functions: Edible, Wildlife Attractor, Shade Provider, Mulcher

### Pea
File: `src/seeds/plants/pea-data.yml`
Scientific: *Pisum sativum*
Zone: 2-11 | Layer: Herbaceous
Functions: Edible, Nitrogen Fixer, Ground Cover

### Peach Palm
File: `src/seeds/plants/peach-palm-data.yml`
Scientific: *Bactris gasipaes*
Zone: 10-11 | Layer: Tree
Functions: Edible, Animal Fodder, Mulcher, Windbreaker, Wildlife Attractor

### Peanut Butter Fruit Tree
File: `src/seeds/plants/peanut-butter-fruit-tree-data.yml`
Scientific: *Bunchosia argentea*
Zone: 10-11 | Layer: Tree, Shrub
Functions: Edible, Pollinator, Wildlife Attractor, Ornamental, Shade Provider

### Peanut Tree
File: `src/seeds/plants/peanut-tree-data.yml`
Scientific: *Sterculia quadrifida*
Zone: 10-12 | Layer: Sub-Canopy, Shrub
Functions: Edible, Wildlife Attractor, Ornamental

### Pear Tree
File: `src/seeds/plants/pear-tree-data.yml`
Scientific: *Pyrus communis*
Zone: 4-9 | Layer: Canopy, Sub-Canopy
Functions: Edible, Wildlife Attractor, Windbreaker, Border Plant, Erosion Control

### Pecan Tree
File: `src/seeds/plants/pecan-tree-data.yml`
Scientific: *Carya illinoinensis*
Zone: 5-9 | Layer: Canopy
Functions: Edible, Wildlife Attractor, Windbreaker, Erosion Control, Animal Fodder, Dynamic Accumulator


---

## When Done

```bash
python3 validate.py --since 2h
./sync.sh --check
./sync.sh
rm review/practitioner_notes_22_of_34.md
```

Then open `practitioner_notes_23_of_34.md`
