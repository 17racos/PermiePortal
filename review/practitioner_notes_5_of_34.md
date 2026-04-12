# Practitioner Notes — Batch 5 of 34

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

### Black Sapote
File: `src/seeds/plants/black-sapote-data.yml`
Scientific: *Diospyros nigra*
Zone: 10-11 | Layer: Tree
Functions: Edible, Ornamental, Wildlife Attractor

### Black Locust
File: `src/seeds/plants/black-locust-data.yml`
Scientific: *Robinia pseudoacacia*
Zone: 3-8 | Layer: Canopy
Functions: Nitrogen Fixer, Pollinator, Erosion Control, Animal Fodder, Windbreaker, Border Plant

### Bladder Senna
File: `src/seeds/plants/bladder-senna-data.yml`
Scientific: *Colutea arborescens*
Zone: 5-9 | Layer: Shrub
Functions: Nitrogen Fixer, Ornamental, Wildlife Attractor, Border Plant, Mulcher

### Bladderwort
File: `src/seeds/plants/bladderwort-data.yml`
Scientific: *Utricularia spp.*
Zone: 4-10 | Layer: Aquatic
Functions: Water Purifier, Pest Management

### Blanket Flower
File: `src/seeds/plants/blanket-flower-data.yml`
Scientific: *Gaillardia aristata*
Zone: 3-10 | Layer: Herbaceous
Functions: Pollinator, Wildlife Attractor, Ornamental, Ground Cover

### Blue Agave
File: `src/seeds/plants/blue-agave-data.yml`
Scientific: *Agave tequilana*
Zone: 9-11 | Layer: Herbaceous
Functions: Edible, Mulcher, Erosion Control

### Blue Flag Iris
File: `src/seeds/plants/blue-flag-iris-data.yml`
Scientific: *Iris virginica*
Zone: 5-9 | Layer: Herbaceous, Aquatic
Functions: Ornamental, Wildlife Attractor, Erosion Control

### Blue Flax
File: `src/seeds/plants/blue-flax-data.yml`
Scientific: *Linum lewisii*
Zone: 5-9 | Layer: Herbaceous
Functions: Pollinator, Ornamental, Wildlife Attractor, Fiber

### Blue Pickerelweed
File: `src/seeds/plants/blue-pickerelweed-data.yml`
Scientific: *Pontederia cordata*
Zone: 3-11 | Layer: Aquatic, Herbaceous
Functions: Aquatic, Wildlife Attractor, Pollinator, Erosion Control

### Blue Sage
File: `src/seeds/plants/blue-sage-data.yml`
Scientific: *Salvia azurea*
Zone: 4-9 | Layer: Herbaceous
Functions: Pollinator, Wildlife Attractor, Border Plant, Medicinal

### Blue Star Creeper
File: `src/seeds/plants/blue-star-creeper-data.yml`
Scientific: *Isotoma fluviatilis*
Zone: 7-11 | Layer: Ground Cover, Herbaceous
Functions: Ground Cover, Ornamental, Pollinator, Water Retention

### Blue Vervain
File: `src/seeds/plants/blue-vervain-data.yml`
Scientific: *Verbena hastata*
Zone: 3-9 | Layer: Herbaceous
Functions: Medicinal, Pollinator, Wildlife Attractor, Biomass

### Blue Woodruff
File: `src/seeds/plants/blue-woodruff-data.yml`
Scientific: *Asperula orientalis*
Zone: 2-10 | Layer: Herbaceous, Ground Cover
Functions: Pollinator, Wildlife Attractor, Border Plant

### Blueberry
File: `src/seeds/plants/blueberry-data.yml`
Scientific: *Vaccinium spp.*
Zone: 3-10 | Layer: Shrub
Functions: Edible, Medicinal, Pollinator, Wildlife Attractor, Mulcher, Dynamic Accumulator, Erosion Control, Border Plant

### Bog Bean
File: `src/seeds/plants/bog-bean-data.yml`
Scientific: *Menyanthes trifoliata*
Zone: 3-8 | Layer: Aquatic, Herbaceous
Functions: Aquatic, Wildlife Attractor, Pollinator, Water Retention

### Bok Choy
File: `src/seeds/plants/bok-choy-data.yml`
Scientific: *Brassica rapa subsp. chinensis*
Zone: 2-11 | Layer: Herbaceous
Functions: Edible, Medicinal, Wildlife Attractor, Mulcher, Dynamic Accumulator, Border Plant

### Boneset
File: `src/seeds/plants/boneset-data.yml`
Scientific: *Eupatorium perfoliatum*
Zone: 3-8 | Layer: Herbaceous
Functions: Medicinal, Pollinator, Wildlife Attractor, Biomass

### Borage
File: `src/seeds/plants/borage-data.yml`
Scientific: *Borago officinalis*
Zone: 2-11 | Layer: Herbaceous
Functions: Edible, Medicinal, Pollinator, Wildlife Attractor, Mulcher, Dynamic Accumulator, Erosion Control, Border Plant, Pest Management

### Bottle Gourd
File: `src/seeds/plants/bottle-gourd-data.yml`
Scientific: *Lagenaria siceraria*
Zone: 3-11 | Layer: Vine
Functions: Edible, Ornamental, Fiber

### Brazilian Spinach
File: `src/seeds/plants/brazilian-spinach-data.yml`
Scientific: *Alternanthera sissoo*
Zone: 10-12 | Layer: Ground Cover
Functions: Edible, Ground Cover, Mulcher, Wildlife Attractor


---

## When Done

```bash
python3 validate.py --since 2h
./sync.sh --check
./sync.sh
rm review/practitioner_notes_5_of_34.md
```

Then open `practitioner_notes_6_of_34.md`
