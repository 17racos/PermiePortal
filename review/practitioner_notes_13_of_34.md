# Practitioner Notes — Batch 13 of 34

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

### Feijoa
File: `src/seeds/plants/feijoa-data.yml`
Scientific: *Acca sellowiana*
Zone: 8-11 | Layer: Shrub, Tree
Functions: Edible, Ornamental, Windbreaker, Wildlife Attractor

### Fennel
File: `src/seeds/plants/fennel-data.yml`
Scientific: *Foeniculum vulgare*
Zone: 4-10 | Layer: Herbaceous
Functions: Edible, Medicinal, Pollinator, Wildlife Attractor, Dynamic Accumulator, Border Plant

### Fever Few
File: `src/seeds/plants/fever-few-data.yml`
Scientific: *Tanacetum parthenium*
Zone: 5-9 | Layer: Herbaceous
Functions: Medicinal, Pollinator, Pest Management, Ornamental

### Fever Grass
File: `src/seeds/plants/fever-grass-data.yml`
Scientific: *Cymbopogon citratus*
Zone: 9-11 | Layer: Herbaceous
Functions: Edible, Medicinal, Pest Management, Mulcher

### Fiber and Industrial
File: `src/seeds/plants/fiber-and-industrial-data.yml`
Scientific: *Various spp.*
Zone: 4-12 | Layer: Herbaceous, Shrub, Tree
Functions: Animal Fodder, Mulcher, Erosion Control, Edible

### Fig
File: `src/seeds/plants/fig-data.yml`
Scientific: *Ficus carica*
Zone: 7-11 | Layer: Tree
Functions: Edible, Medicinal, Wildlife Attractor, Dynamic Accumulator, Erosion Control, Windbreaker, Border Plant

### Finger Lime
File: `src/seeds/plants/finger-lime-data.yml`
Scientific: *Citrus australasica*
Zone: 10-11 | Layer: Shrub, Tree
Functions: Edible, Ornamental, Pollinator

### Firebush
File: `src/seeds/plants/firebush-data.yml`
Scientific: *Hamelia patens*
Zone: 9-11 | Layer: Shrub
Functions: Pollinator, Wildlife Attractor, Medicinal, Border Plant

### Fireweed
File: `src/seeds/plants/fireweed-data.yml`
Scientific: *Chamaenerion angustifolium*
Zone: 2-8 | Layer: Herbaceous
Functions: Edible, Pollinator, Wildlife Attractor, Biomass, Mulcher

### Fish Mint
File: `src/seeds/plants/fish-mint-data.yml`
Scientific: *Houttuynia cordata*
Zone: 5-11 | Layer: Ground Cover, Aquatic
Functions: Edible, Medicinal, Ground Cover, Aquatic

### Flax
File: `src/seeds/plants/flax-data.yml`
Scientific: *Linum usitatissimum*
Zone: 2-9 | Layer: Herbaceous
Functions: Fiber, Edible, Cover Crop, Pollinator

### Floating Heart
File: `src/seeds/plants/floating-heart-data.yml`
Scientific: *Nymphoides aquatica*
Zone: 6-11 | Layer: Aquatic
Functions: Wildlife Attractor, Border Plant

### Frogfruit
File: `src/seeds/plants/frogfruit-data.yml`
Scientific: *Phyla nodiflora*
Zone: 6-11 | Layer: Ground Cover
Functions: Ground Cover, Pollinator, Erosion Control, Ornamental, Wildlife Attractor

### Fruit Sage
File: `src/seeds/plants/fruit-sage-data.yml`
Scientific: *Salvia elegans*
Zone: 8-11 | Layer: Herbaceous
Functions: Edible, Medicinal, Pollinator, Ornamental, Wildlife Attractor

### Galangal
File: `src/seeds/plants/galangal-data.yml`
Scientific: *Alpinia galanga*
Zone: 9-11 | Layer: Herbaceous
Functions: Edible, Medicinal, Pollinator, Wildlife Attractor

### Garlic
File: `src/seeds/plants/garlic-data.yml`
Scientific: *Allium sativum*
Zone: 3-10 | Layer: Herbaceous
Functions: Edible, Medicinal, Pest Management, Dynamic Accumulator, Border Plant

### Gaura
File: `src/seeds/plants/gaura-data.yml`
Scientific: *Oenothera lindheimeri*
Zone: 5-9 | Layer: Herbaceous
Functions: Ornamental, Pollinator, Wildlife Attractor, Border Plant, Erosion Control

### Giant Bulrush
File: `src/seeds/plants/giant-bulrush-data.yml`
Scientific: *Schoenoplectus californicus*
Zone: 5-11 | Layer: Aquatic, Herbaceous
Functions: Water Purifier, Wildlife Attractor, Mulcher, Erosion Control

### Giant Granadilla
File: `src/seeds/plants/giant-granadilla-data.yml`
Scientific: *Passiflora quadrangularis*
Zone: 10-11 | Layer: Vine
Functions: Edible, Wildlife Attractor, Shade Provider, Ornamental

### Ginger
File: `src/seeds/plants/ginger-data.yml`
Scientific: *Zingiber officinale*
Zone: 8-12 | Layer: Herbaceous
Functions: Edible, Medicinal, Mulcher, Dynamic Accumulator, Border Plant


---

## When Done

```bash
python3 validate.py --since 2h
./sync.sh --check
./sync.sh
rm review/practitioner_notes_13_of_34.md
```

Then open `practitioner_notes_14_of_34.md`
