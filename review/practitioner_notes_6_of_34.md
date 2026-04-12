# Practitioner Notes — Batch 6 of 34

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

### Breadfruit
File: `src/seeds/plants/breadfruit-data.yml`
Scientific: *Artocarpus altilis*
Zone: 10-11 | Layer: Tree, Canopy
Functions: Edible, Mulcher, Animal Fodder

### Broadleaf Plantain
File: `src/seeds/plants/broadleaf-plantain-data.yml`
Scientific: *Plantago major*
Zone: 3-10 | Layer: Herbaceous, Ground Cover
Functions: Edible, Medicinal, Dynamic Accumulator, Ground Cover

### Broccoli
File: `src/seeds/plants/broccoli-data.yml`
Scientific: *Brassica oleracea var. italica*
Zone: 2-11 | Layer: Herbaceous
Functions: Edible, Medicinal, Pollinator, Ground Cover

### Buck Plantain
File: `src/seeds/plants/buck-plantain-data.yml`
Scientific: *Plantago coronopus*
Zone: 4-10 | Layer: Herbaceous, Ground Cover
Functions: Edible, Medicinal, Dynamic Accumulator, Animal Fodder, Border Plant

### Buckwheat
File: `src/seeds/plants/buckwheat-data.yml`
Scientific: *Fagopyrum esculentum*
Zone: 3-10 | Layer: Herbaceous
Functions: Edible, Green Manure, Pollinator, Wildlife Attractor

### Buddha Hand
File: `src/seeds/plants/buddha-hand-data.yml`
Scientific: *Citrus medica var. sarcodactylis*
Zone: 9-11 | Layer: Tree, Shrub
Functions: Edible, Ornamental, Border Plant, Wildlife Attractor

### Buffalo Berry
File: `src/seeds/plants/buffalo-berry-data.yml`
Scientific: *Shepherdia argentea*
Zone: 2-7 | Layer: Shrub
Functions: Edible, Nitrogen Fixer, Wildlife Attractor, Windbreaker

### Buffalo Gourd
File: `src/seeds/plants/buffalo-gourd-data.yml`
Scientific: *Cucurbita foetidissima*
Zone: 7-11 | Layer: Vine, Ground Cover
Functions: Edible, Fiber, Ground Cover, Wildlife Attractor

### Buffalo Grass
File: `src/seeds/plants/buffalo-grass-data.yml`
Scientific: *Bouteloua dactyloides*
Zone: 4-8 | Layer: Ground Cover, Herbaceous
Functions: Ground Cover, Erosion Control, Drought Tolerant

### Bulbine
File: `src/seeds/plants/bulbine-data.yml`
Scientific: *Bulbine frutescens*
Zone: 9-11 | Layer: Ground Cover
Functions: Edible, Medicinal, Ground Cover, Wildlife Attractor

### Burdock
File: `src/seeds/plants/burdock-data.yml`
Scientific: *Arctium lappa*
Zone: 3-9 | Layer: Herbaceous, Root
Functions: Edible, Medicinal, Dynamic Accumulator, Animal Fodder

### Buriti Palm
File: `src/seeds/plants/buriti-palm-data.yml`
Scientific: *Mauritia flexuosa*
Zone: 11-12 | Layer: Tree, Canopy
Functions: Edible, Wildlife Attractor, Mulcher

### Bushel Gourd
File: `src/seeds/plants/bushel-gourd-data.yml`
Scientific: *Lagenaria siceraria*
Zone: 3-11 | Layer: Vine
Functions: Edible, Ornamental, Animal Fodder

### Butia Palm
File: `src/seeds/plants/butia-palm-data.yml`
Scientific: *Butia capitata*
Zone: 8-11 | Layer: Tree
Functions: Edible, Ornamental, Windbreaker, Wildlife Attractor

### Butterfly Ginger
File: `src/seeds/plants/butterfly-ginger-data.yml`
Scientific: *Hedychium coronarium*
Zone: 8-11 | Layer: Herbaceous
Functions: Edible, Medicinal, Pollinator, Wildlife Attractor, Ground Cover, Erosion Control

### Butterwort
File: `src/seeds/plants/butterwort-data.yml`
Scientific: *Pinguicula spp.*
Zone: 7-10 | Layer: Ground Cover
Functions: Pest Management, Ground Cover, Ornamental, Pollinator

### Cacao
File: `src/seeds/plants/cacao-data.yml`
Scientific: *Theobroma cacao*
Zone: 11-12 | Layer: Sub-Canopy
Functions: Edible, Medicinal, Wildlife Attractor

### Caimito
File: `src/seeds/plants/caimito-data.yml`
Scientific: *Chrysophyllum cainito*
Zone: 10-11 | Layer: Tree
Functions: Edible, Shade Provider, Wildlife Attractor

### Calabaza
File: `src/seeds/plants/calabaza-data.yml`
Scientific: *Cucurbita moschata*
Zone: 3-11 | Layer: Vine, Ground Cover
Functions: Edible, Ground Cover, Wildlife Attractor

### Calamondin
File: `src/seeds/plants/calamondin-data.yml`
Scientific: *× Citrofortunella microcarpa*
Zone: 9-11 | Layer: Shrub
Functions: Edible, Ornamental, Wildlife Attractor


---

## When Done

```bash
python3 validate.py --since 2h
./sync.sh --check
./sync.sh
rm review/practitioner_notes_6_of_34.md
```

Then open `practitioner_notes_7_of_34.md`
