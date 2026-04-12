# Practitioner Notes — Batch 21 of 34

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

### Murici
File: `src/seeds/plants/murici-data.yml`
Scientific: *Byrsonima crassifolia*
Zone: 10-11 | Layer: Tree, Shrub
Functions: Edible, Wildlife Attractor, Ornamental

### Mushroom Hosts
File: `src/seeds/plants/mushroom-hosts-data.yml`
Scientific: *Agaricomycetes (wood-decay fungi on diverse substrates)*
Zone: 8-11 | Layer: Tree, Shrub
Functions: Edible, Medicinal, Mulcher, Soil Improvement

### Myrsine
File: `src/seeds/plants/myrsine-data.yml`
Scientific: *Myrsine cubana*
Zone: 10a-11 | Layer: Shrub
Functions: Wildlife Attractor, Ornamental, Pollinator, Border Plant

### Nasturtium
File: `src/seeds/plants/nasturtium-data.yml`
Scientific: *Tropaeolum majus*
Zone: 9-11 | Layer: Herbaceous
Functions: Edible, Medicinal, Pollinator, Wildlife Attractor, Pest Management, Border Plant, Ground Cover

### Natal Plum
File: `src/seeds/plants/natal-plum-data.yml`
Scientific: *Carissa macrocarpa*
Zone: 9-11 | Layer: Shrub
Functions: Edible, Ornamental, Wildlife Attractor, Erosion Control

### Nectarine Tree
File: `src/seeds/plants/nectarine-tree-data.yml`
Scientific: *Prunus persica var. nucipersica*
Zone: 5-9 | Layer: Sub-Canopy
Functions: Edible, Pollinator, Wildlife Attractor, Border Plant

### Needle Palm
File: `src/seeds/plants/needle-palm-data.yml`
Scientific: *Rhapidophyllum hystrix*
Zone: 6-11 | Layer: Shrub, Ground Cover
Functions: Wildlife Attractor, Erosion Control, Windbreaker

### Neem
File: `src/seeds/plants/neem-data.yml`
Scientific: *Azadirachta indica*
Zone: 9-12 | Layer: Tree
Functions: Medicinal, Pest Management, Shade Provider, Windbreaker

### Nepenthes
File: `src/seeds/plants/nepenthes-data.yml`
Scientific: *Nepenthes spp.*
Zone: 10-12 | Layer: Shrub
Functions: Pest Management, Wildlife Attractor, Ground Cover

### New Jersey Tea
File: `src/seeds/plants/new-jersey-tea-data.yml`
Scientific: *Ceanothus americanus*
Zone: 4-9 | Layer: Shrub
Functions: Nitrogen Fixer, Pollinator, Wildlife Attractor, Border Plant

### New Zealand Spinach
File: `src/seeds/plants/new-zealand-spinach-data.yml`
Scientific: *Tetragonia tetragonoides*
Zone: 8-11 | Layer: Herbaceous
Functions: Edible, Ground Cover, Erosion Control, Wildlife Attractor

### Nipa Palm
File: `src/seeds/plants/nipa-palm-data.yml`
Scientific: *Nypa fruticans*
Zone: 10-13 | Layer: Aquatic, Tree
Functions: Aquatic, Biomass, Fiber, Wildlife Attractor

### Noni
File: `src/seeds/plants/noni-data.yml`
Scientific: *Morinda citrifolia*
Zone: 10-11 | Layer: Tree, Shrub
Functions: Edible, Medicinal, Wildlife Attractor

### Oca
File: `src/seeds/plants/oca-data.yml`
Scientific: *Oxalis tuberosa*
Zone: 8-11 | Layer: Herbaceous
Functions: Edible, Ground Cover, Mulcher, Dynamic Accumulator, Wildlife Attractor

### Okinawa Spinach
File: `src/seeds/plants/okinawa-spinach-data.yml`
Scientific: *Gynura bicolor*
Zone: 9-11 | Layer: Ground Cover
Functions: Edible, Medicinal, Wildlife Attractor, Mulcher, Dynamic Accumulator, Erosion Control, Animal Fodder, Ground Cover

### Onion
File: `src/seeds/plants/onion-data.yml`
Scientific: *Allium cepa*
Zone: 5-9 | Layer: Root
Functions: Edible, Medicinal, Pest Management

### Oregano
File: `src/seeds/plants/oregano-data.yml`
Scientific: *Origanum vulgare*
Zone: 4-10 | Layer: Herbaceous, Ground Cover
Functions: Edible, Medicinal, Pollinator, Wildlife Attractor, Mulcher, Dynamic Accumulator, Border Plant, Pest Management, Ground Cover

### Oregon Grape
File: `src/seeds/plants/oregon-grape-data.yml`
Scientific: *Berberis aquifolium*
Zone: 5-9 | Layer: Shrub
Functions: Edible, Medicinal, Wildlife Attractor, Border Plant, Pest Management

### Osier Willow
File: `src/seeds/plants/osier-willow-data.yml`
Scientific: *Salix viminalis*
Zone: 4-9 | Layer: Shrub, Tree
Functions: Wildlife Attractor, Erosion Control, Windbreaker, Border Plant, Dynamic Accumulator, Mulcher, Animal Fodder, Water Purifier

### Ostrich Fern
File: `src/seeds/plants/ostrich-fern-data.yml`
Scientific: *Matteuccia struthiopteris*
Zone: 3-7 | Layer: Herbaceous
Functions: Edible, Ornamental, Erosion Control, Wildlife Attractor


---

## When Done

```bash
python3 validate.py --since 2h
./sync.sh --check
./sync.sh
rm review/practitioner_notes_21_of_34.md
```

Then open `practitioner_notes_22_of_34.md`
