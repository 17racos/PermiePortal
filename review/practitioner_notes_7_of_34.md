# Practitioner Notes — Batch 7 of 34

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

### Calathea
File: `src/seeds/plants/calathea-data.yml`
Scientific: *Calathea spp.*
Zone: 11-12 | Layer: Herbaceous
Functions: Ground Cover, Ornamental, Shade Provider

### Calendula
File: `src/seeds/plants/calendula-data.yml`
Scientific: *Calendula officinalis*
Zone: 2-11 | Layer: Ground Cover
Functions: Edible, Medicinal, Pollinator, Wildlife Attractor, Pest Management, Ground Cover

### California Poppy
File: `src/seeds/plants/california-poppy-data.yml`
Scientific: *Eschscholzia californica*
Zone: 6-11 | Layer: Herbaceous, Ground Cover
Functions: Edible, Pollinator, Ornamental, Wildlife Attractor

### Cambuca
File: `src/seeds/plants/cambuca-data.yml`
Scientific: *Campomanesia phaea*
Zone: 9b-11 | Layer: Tree, Shrub
Functions: Edible, Ornamental, Wildlife Attractor

### Camu Camu
File: `src/seeds/plants/camu-camu-data.yml`
Scientific: *Myrciaria dubia*
Zone: 10-11 | Layer: Shrub, Tree
Functions: Edible, Wildlife Attractor, Erosion Control

### Candle Nut Tree
File: `src/seeds/plants/candle-nut-tree-data.yml`
Scientific: *Aleurites moluccanus*
Zone: 10-12 | Layer: Tree
Functions: Edible, Medicinal, Mulcher, Windbreaker

### Canistel
File: `src/seeds/plants/canistel-data.yml`
Scientific: *Pouteria campechiana*
Zone: 10-11 | Layer: Tree
Functions: Edible, Wildlife Attractor, Shade Provider

### Canna Lily
File: `src/seeds/plants/canna-lily-data.yml`
Scientific: *Canna × generalis*
Zone: 7-11 | Layer: Herbaceous
Functions: Edible, Ornamental, Mulcher, Wildlife Attractor

### Canopy Trees
File: `src/seeds/plants/canopy-trees-data.yml`
Scientific: *Various spp.*
Zone: 4-12 | Layer: Canopy
Functions: Shade Provider, Windbreaker, Wildlife Attractor, Timber

### Carambola
File: `src/seeds/plants/carambola-data.yml`
Scientific: *Averrhoa carambola*
Zone: 10-12 | Layer: Sub-Canopy
Functions: Edible, Medicinal, Wildlife Attractor, Ornamental

### Cardamom
File: `src/seeds/plants/cardamom-data.yml`
Scientific: *Elettaria cardamomum*
Zone: 10-12 | Layer: Herbaceous
Functions: Edible, Medicinal, Wildlife Attractor

### Cardinal Flower
File: `src/seeds/plants/cardinal-flower-data.yml`
Scientific: *Lobelia cardinalis*
Zone: 3-9 | Layer: Herbaceous, Aquatic
Functions: Pollinator, Wildlife Attractor, Ornamental

### Carob Tree
File: `src/seeds/plants/carob-tree-data.yml`
Scientific: *Ceratonia siliqua*
Zone: 9-11 | Layer: Tree
Functions: Edible, Animal Fodder, Shade Provider, Windbreaker

### Carpet Bugle
File: `src/seeds/plants/carpet-bugle-data.yml`
Scientific: *Ajuga reptans*
Zone: 3-10 | Layer: Ground Cover, Herbaceous
Functions: Ground Cover, Ornamental, Pollinator, Pest Management

### Carrot
File: `src/seeds/plants/carrot-data.yml`
Scientific: *Daucus carota subsp. sativus*
Zone: 3-10 | Layer: Root
Functions: Edible, Medicinal, Pollinator, Wildlife Attractor, Dynamic Accumulator, Border Plant

### Cassabanana root systems
File: `src/seeds/plants/cassabanana-root-systems-data.yml`
Scientific: *Sicana odorifera*
Zone: 10-12 | Layer: Vine, Root
Functions: Edible, Ground Cover, Biomass, Shade Provider

### Cassava
File: `src/seeds/plants/cassava-data.yml`
Scientific: *Manihot esculenta*
Zone: 8-12 | Layer: Shrub
Functions: Edible, Animal Fodder, Erosion Control, Biofuel

### Cassia alata
File: `src/seeds/plants/cassia-alata-data.yml`
Scientific: *Senna alata*
Zone: 9-12 | Layer: Shrub, Herbaceous
Functions: Medicinal, Biomass, Ornamental, Wildlife Attractor

### Catnip
File: `src/seeds/plants/catnip-data.yml`
Scientific: *Nepeta cataria*
Zone: 3-9 | Layer: Ground Cover
Functions: Medicinal, Pollinator, Wildlife Attractor, Pest Management

### Cattail
File: `src/seeds/plants/cattail-data.yml`
Scientific: *Typha latifolia*
Zone: 3-10 | Layer: Herbaceous, Aquatic, Root
Functions: Edible, Water Purifier, Wildlife Attractor, Mulcher


---

## When Done

```bash
python3 validate.py --since 2h
./sync.sh --check
./sync.sh
rm review/practitioner_notes_7_of_34.md
```

Then open `practitioner_notes_8_of_34.md`
