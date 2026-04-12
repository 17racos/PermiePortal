# Practitioner Notes — Batch 24 of 34

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

### Plantain
File: `src/seeds/plants/plantain-data.yml`
Scientific: *Plantago major*
Zone: 3-9 | Layer: Ground Cover
Functions: Edible, Medicinal, Ground Cover, Erosion Control, Dynamic Accumulator

### Pollinator Support
File: `src/seeds/plants/pollinator-support-data.yml`
Scientific: *Polyculture (multiple species)*
Zone: 8-11 | Layer: Herbaceous, Shrub, Tree
Functions: Pollinator, Wildlife Attractor, Nitrogen Fixer, Pest Management, Border Plant, Mulcher

### Pomegranate Tree
File: `src/seeds/plants/pomegranate-tree-data.yml`
Scientific: *Punica granatum*
Zone: 7-11 | Layer: Shrub, Tree
Functions: Edible, Medicinal, Pollinator, Wildlife Attractor, Windbreaker, Erosion Control, Border Plant

### Pomelo
File: `src/seeds/plants/pomelo-data.yml`
Scientific: *Citrus maxima*
Zone: 9-11 | Layer: Tree
Functions: Edible, Ornamental, Wildlife Attractor, Shade Provider

### Pond Apple
File: `src/seeds/plants/pond-apple-data.yml`
Scientific: *Annona glabra*
Zone: 10-11 | Layer: Tree
Functions: Edible, Wildlife Attractor, Erosion Control, Shade Provider

### Ponytail Palm
File: `src/seeds/plants/ponytail-palm-data.yml`
Scientific: *Beaucarnea recurvata*
Zone: 9-12 | Layer: Shrub
Functions: Ornamental, Indoor Plant, Wildlife Attractor

### Potato
File: `src/seeds/plants/potato-data.yml`
Scientific: *Solanum tuberosum*
Zone: 3-10 | Layer: Herbaceous
Functions: Edible, Animal Fodder, Ground Cover

### Potato Mint
File: `src/seeds/plants/potato-mint-data.yml`
Scientific: *Plectranthus rotundifolius*
Zone: 9-12 | Layer: Herbaceous
Functions: Edible, Medicinal, Mulcher, Dynamic Accumulator, Ground Cover

### Prairie Acacia
File: `src/seeds/plants/prairie-acacia-data.yml`
Scientific: *Vachellia angustissima*
Zone: 8-11 | Layer: Shrub, Tree
Functions: Nitrogen Fixer, Wildlife Attractor, Animal Fodder, Erosion Control, Mulcher

### Prairie Potato
File: `src/seeds/plants/prairie-potato-data.yml`
Scientific: *Pediomelum esculentum*
Zone: 3-8 | Layer: Herbaceous, Ground Cover
Functions: Edible, Nitrogen Fixer, Ground Cover, Wildlife Attractor

### Prairie Turnip
File: `src/seeds/plants/prairie-turnip-data.yml`
Scientific: *Pediomelum esculentum*
Zone: 3-8 | Layer: Herbaceous, Root
Functions: Edible, Nitrogen Fixer, Wildlife Attractor, Soil Improvement

### Purple Passionflower
File: `src/seeds/plants/purple-passionflower-data.yml`
Scientific: *Passiflora incarnata*
Zone: 6-10 | Layer: Vine
Functions: Edible, Medicinal, Wildlife Attractor, Ground Cover

### Purslane
File: `src/seeds/plants/purslane-data.yml`
Scientific: *Portulaca oleracea*
Zone: 5-11 | Layer: Ground Cover
Functions: Edible, Medicinal, Ground Cover, Dynamic Accumulator, Wildlife Attractor

### Queensland Arrowroot
File: `src/seeds/plants/queensland-arrowroot-data.yml`
Scientific: *Canna indica*
Zone: 8-12 | Layer: Herbaceous
Functions: Edible, Mulcher, Wildlife Attractor, Ornamental

### Radish
File: `src/seeds/plants/radish-data.yml`
Scientific: *Raphanus sativus*
Zone: 2-11 | Layer: Herbaceous
Functions: Edible, Dynamic Accumulator, Pest Management, Mulcher, Erosion Control

### Ramie
File: `src/seeds/plants/ramie-data.yml`
Scientific: *Boehmeria nivea*
Zone: 7-10 | Layer: Herbaceous, Shrub
Functions: Fiber, Mulcher, Dynamic Accumulator

### Ramps
File: `src/seeds/plants/ramps-data.yml`
Scientific: *Allium tricoccum*
Zone: 3-8 | Layer: Herbaceous, Root
Functions: Edible, Medicinal, Wildlife Attractor

### Rangpur Lime
File: `src/seeds/plants/rangpur-lime-data.yml`
Scientific: *Citrus × limonia*
Zone: 8-11 | Layer: Tree
Functions: Edible, Wildlife Attractor, Border Plant, Windbreaker

### Raspberry
File: `src/seeds/plants/raspberry-data.yml`
Scientific: *Rubus idaeus*
Zone: 3-9 | Layer: Shrub
Functions: Edible, Medicinal, Pollinator, Wildlife Attractor, Erosion Control

### Rattlebox
File: `src/seeds/plants/rattlebox-data.yml`
Scientific: *Crotalaria spectabilis*
Zone: 8-11 | Layer: Herbaceous
Functions: Nitrogen Fixer, Green Manure, Ornamental


---

## When Done

```bash
python3 validate.py --since 2h
./sync.sh --check
./sync.sh
rm review/practitioner_notes_24_of_34.md
```

Then open `practitioner_notes_25_of_34.md`
