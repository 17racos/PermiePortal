# Practitioner Notes — Batch 1 of 34

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

### Abiu
File: `src/seeds/plants/abiu-data.yml`
Scientific: *Pouteria caimito*
Zone: 10-11 | Layer: Tree
Functions: Edible, Wildlife Attractor, Shade Provider

### Acacia
File: `src/seeds/plants/acacia-data.yml`
Scientific: *Acacia spp.*
Zone: 9-11 | Layer: Canopy
Functions: Nitrogen Fixer, Pollinator, Wildlife Attractor, Erosion Control, Windbreaker, Biofuel

### Açaí Palm
File: `src/seeds/plants/açaí-palm-data.yml`
Scientific: *Euterpe oleracea*
Zone: 10-11 | Layer: Tree
Functions: Edible, Wildlife Attractor, Mulcher

### Acerola Cherry
File: `src/seeds/plants/acerola-cherry-data.yml`
Scientific: *Malpighia emarginata*
Zone: 9-11 | Layer: Shrub
Functions: Edible, Medicinal, Wildlife Attractor, Ornamental

### Achira
File: `src/seeds/plants/achira-data.yml`
Scientific: *Canna indica*
Zone: 7-11 | Layer: Herbaceous, Root
Functions: Edible, Ornamental, Mulcher, Animal Fodder

### Acorn Squash
File: `src/seeds/plants/acorn-squash-data.yml`
Scientific: *Cucurbita pepo var. turbinata*
Zone: 3-10 | Layer: Herbaceous
Functions: Edible, Ground Cover, Animal Fodder

### African Blue Basil
File: `src/seeds/plants/african-blue-basil-data.yml`
Scientific: *Ocimum basilicum × Ocimum kilimandscharicum*
Zone: 9-11 | Layer: Herbaceous
Functions: Edible, Pollinator, Pest Management, Ornamental

### African Breadfruit
File: `src/seeds/plants/african-breadfruit-data.yml`
Scientific: *Treculia africana*
Zone: 10b-11 | Layer: Tree
Functions: Edible, Wildlife Attractor, Shade Provider, Mulcher, Biomass, Ornamental

### African Locust Bean
File: `src/seeds/plants/african-locust-bean-data.yml`
Scientific: *Parkia biglobosa*
Zone: 10b-11 | Layer: Tree
Functions: Edible, Nitrogen Fixer, Animal Fodder, Shade Provider, Mulcher, Wildlife Attractor

### Agave Americana
File: `src/seeds/plants/agave-americana-data.yml`
Scientific: *Agave americana*
Zone: 8-11 | Layer: Herbaceous
Functions: Edible, Ornamental, Erosion Control, Border Plant

### Agave
File: `src/seeds/plants/agave-data.yml`
Scientific: *Agave spp.*
Zone: 7-11 | Layer: Ground Cover
Functions: Biofuel, Fiber, Ornamental

### Agrimony
File: `src/seeds/plants/agrimony-data.yml`
Scientific: *Agrimonia eupatoria*
Zone: 5-9 | Layer: Herbaceous
Functions: Medicinal, Pollinator, Wildlife Attractor, Border Plant, Ground Cover

### Aguaje Palm
File: `src/seeds/plants/aguaje-palm-data.yml`
Scientific: *Mauritia flexuosa*
Zone: 10-12 | Layer: Tree
Functions: Edible, Wildlife Attractor, Erosion Control

### Ahipa
File: `src/seeds/plants/ahipa-data.yml`
Scientific: *Pachyrhizus ahipa*
Zone: 9-11 | Layer: Herbaceous, Vine, Root
Functions: Edible, Nitrogen Fixer, Green Manure

### Air Potato
File: `src/seeds/plants/air-potato-data.yml`
Scientific: *Dioscorea bulbifera*
Zone: 9-11 | Layer: Vine
Functions: Ground Cover

### Albizia lebbeck
File: `src/seeds/plants/albizia-lebbeck-data.yml`
Scientific: *Albizia lebbeck*
Zone: 10b-11 | Layer: Tree
Functions: Nitrogen Fixer, Shade Provider, Animal Fodder, Mulcher, Windbreaker, Ornamental

### Alder
File: `src/seeds/plants/alder-data.yml`
Scientific: *Alnus serrulata*
Zone: 4-9 | Layer: Tree, Shrub
Functions: Nitrogen Fixer, Wildlife Attractor, Erosion Control, Mulcher, Water Purifier

### Alexanders
File: `src/seeds/plants/alexanders-data.yml`
Scientific: *Smyrnium olusatrum*
Zone: 5-9 | Layer: Herbaceous
Functions: Edible, Wildlife Attractor, Border Plant, Dynamic Accumulator

### Alfalfa
File: `src/seeds/plants/alfalfa-data.yml`
Scientific: *Medicago sativa*
Zone: 3-10 | Layer: Sub-Canopy, Shrub
Functions: Edible, Nitrogen Fixer, Animal Fodder, Soil Improvement, Erosion Control, Pollinator

### Almond Tree
File: `src/seeds/plants/almond-tree-data.yml`
Scientific: *Prunus dulcis*
Zone: 7-9 | Layer: Canopy
Functions: Edible, Wildlife Attractor, Windbreaker, Border Plant


---

## When Done

```bash
python3 validate.py --since 2h
./sync.sh --check
./sync.sh
rm review/practitioner_notes_1_of_34.md
```

Then open `practitioner_notes_2_of_34.md`
