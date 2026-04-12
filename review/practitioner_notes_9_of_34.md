# Practitioner Notes — Batch 9 of 34

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

### Chiltepin Pepper Tree
File: `src/seeds/plants/chiltepin-pepper-tree-data.yml`
Scientific: *Capsicum annuum var. glabriusculum*
Zone: 9-11 | Layer: Shrub
Functions: Edible, Wildlife Attractor, Border Plant, Ornamental

### Chinese Fan Palm
File: `src/seeds/plants/chinese-fan-palm-data.yml`
Scientific: *Livistona chinensis*
Zone: 9-11 | Layer: Tree
Functions: Ornamental, Edible, Shade Provider, Wildlife Attractor

### Chinese Lantern
File: `src/seeds/plants/chinese-lantern-data.yml`
Scientific: *Physalis alkekengi*
Zone: 3-9 | Layer: Herbaceous
Functions: Edible, Medicinal, Pollinator, Ground Cover

### Chinese Water Chestnut
File: `src/seeds/plants/chinese-water-chestnut-data.yml`
Scientific: *Eleocharis dulcis*
Zone: 8-11 | Layer: Aquatic, Root
Functions: Edible, Water Purifier, Aquatic, Biomass

### Chinese Yam
File: `src/seeds/plants/chinese-yam-data.yml`
Scientific: *Dioscorea polystachya*
Zone: 5-9 | Layer: Vine, Root
Functions: Edible, Ground Cover, Biomass, Dynamic Accumulator

### Chives
File: `src/seeds/plants/chives-data.yml`
Scientific: *Allium schoenoprasum*
Zone: 3-9 | Layer: Ground Cover
Functions: Edible, Pollinator, Wildlife Attractor, Pest Management, Border Plant

### Cinnamon Basil
File: `src/seeds/plants/cinnamon-basil-data.yml`
Scientific: *Ocimum basilicum 'Cinnamon'*
Zone: 9-11 | Layer: Herbaceous
Functions: Edible, Pollinator, Pest Management, Ornamental

### Cinnamon Vine
File: `src/seeds/plants/cinnamon-vine-data.yml`
Scientific: *Dioscorea polystachya*
Zone: 5-11 | Layer: Vine, Root
Functions: Edible, Ground Cover, Wildlife Attractor

### Cistus
File: `src/seeds/plants/cistus-data.yml`
Scientific: *Cistus spp.*
Zone: 8-11 | Layer: Shrub, Ground Cover
Functions: Ornamental, Wildlife Attractor, Erosion Control, Border Plant

### Citron
File: `src/seeds/plants/citron-data.yml`
Scientific: *Citrus medica*
Zone: 9-11 | Layer: Tree, Shrub
Functions: Edible, Ornamental, Medicinal

### Clary Sage
File: `src/seeds/plants/clary-sage-data.yml`
Scientific: *Salvia sclarea*
Zone: 5-9 | Layer: Herbaceous
Functions: Medicinal, Ornamental, Wildlife Attractor, Edible

### Western miner's lettuce
File: `src/seeds/plants/western-miners-lettuce-data.yml`
Scientific: *Claytonia perfoliata*
Zone: 6-11 | Layer: Herbaceous, Ground Cover
Functions: Edible, Ground Cover, Dynamic Accumulator, Mulcher

### Cleveland Sage
File: `src/seeds/plants/cleveland-sage-data.yml`
Scientific: *Salvia clevelandii*
Zone: 8-11 | Layer: Shrub, Herbaceous
Functions: Pollinator, Wildlife Attractor, Medicinal, Border Plant

### Coastal Rosemary
File: `src/seeds/plants/coastal-rosemary-data.yml`
Scientific: *Westringia fruticosa*
Zone: 9-11 | Layer: Shrub
Functions: Ornamental, Wildlife Attractor, Border Plant, Windbreaker

### Cobra Lily
File: `src/seeds/plants/cobra-lily-data.yml`
Scientific: *Darlingtonia californica*
Zone: 7-10 | Layer: Herbaceous
Functions: Pest Management, Wildlife Attractor, Ground Cover

### Coccinia
File: `src/seeds/plants/coccinia-data.yml`
Scientific: *Coccinia grandis*
Zone: 10-11 | Layer: Vine
Functions: Edible, Ground Cover, Wildlife Attractor

### Coco Plum
File: `src/seeds/plants/coco-plum-data.yml`
Scientific: *Chrysobalanus icaco*
Zone: 10b-11 | Layer: Shrub
Functions: Edible, Erosion Control, Wildlife Attractor, Windbreaker

### Coconut Tree
File: `src/seeds/plants/coconut-tree-data.yml`
Scientific: *Cocos nucifera*
Zone: 10-12 | Layer: Canopy
Functions: Edible, Medicinal, Mulcher, Biofuel, Wildlife Attractor, Windbreaker

### Coffee Senna
File: `src/seeds/plants/coffee-senna-data.yml`
Scientific: *Senna occidentalis*
Zone: 8-11 | Layer: Herbaceous
Functions: Biomass, Nitrogen Fixer, Wildlife Attractor, Pest Management

### Comfrey
File: `src/seeds/plants/comfrey-data.yml`
Scientific: *Symphytum officinale*
Zone: 3-9 | Layer: Herbaceous
Functions: Medicinal, Wildlife Attractor, Mulcher, Dynamic Accumulator, Erosion Control, Animal Fodder, Border Plant


---

## When Done

```bash
python3 validate.py --since 2h
./sync.sh --check
./sync.sh
rm review/practitioner_notes_9_of_34.md
```

Then open `practitioner_notes_10_of_34.md`
