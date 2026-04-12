# Practitioner Notes — Batch 28 of 34

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

### Sorrel
File: `src/seeds/plants/sorrel-data.yml`
Scientific: *Rumex acetosa*
Zone: 3-7 | Layer: Ground Cover
Functions: Edible, Medicinal, Ground Cover, Wildlife Attractor

### Sour Orange
File: `src/seeds/plants/sour-orange-data.yml`
Scientific: *Citrus × aurantium*
Zone: 9-11 | Layer: Tree, Shrub
Functions: Edible, Medicinal, Wildlife Attractor, Windbreaker

### Soursop
File: `src/seeds/plants/soursop-data.yml`
Scientific: *Annona muricata*
Zone: 10-11 | Layer: Tree
Functions: Edible, Medicinal, Shade Provider, Wildlife Attractor, Ornamental

### Soursop Leaf
File: `src/seeds/plants/soursop-leaf-data.yml`
Scientific: *Annona muricata*
Zone: 10-11 | Layer: Tree
Functions: Medicinal, Edible, Mulcher, Wildlife Attractor

### Southern Magnolia
File: `src/seeds/plants/southern-magnolia-data.yml`
Scientific: *Magnolia grandiflora*
Zone: 7-10 | Layer: Tree, Canopy
Functions: Wildlife Attractor, Shade Provider, Windbreaker, Ornamental

### Sparkleberry
File: `src/seeds/plants/sparkleberry-data.yml`
Scientific: *Vaccinium arboreum*
Zone: 7-10 | Layer: Shrub
Functions: Edible, Wildlife Attractor, Ornamental, Pollinator

### Spatterdock
File: `src/seeds/plants/spatterdock-data.yml`
Scientific: *Nuphar advena*
Zone: 4-11 | Layer: Aquatic
Functions: Edible, Wildlife Attractor, Erosion Control, Border Plant

### Spicebush
File: `src/seeds/plants/spicebush-data.yml`
Scientific: *Lindera benzoin*
Zone: 4-9 | Layer: Shrub
Functions: Edible, Wildlife Attractor, Medicinal, Border Plant

### Spilanthes
File: `src/seeds/plants/spilanthes-data.yml`
Scientific: *Acmella oleracea*
Zone: 9-11 | Layer: Herbaceous, Ground Cover
Functions: Edible, Medicinal, Wildlife Attractor

### St. John's Mint
File: `src/seeds/plants/st-johns-mint-data.yml`
Scientific: *Clinopodium brownei*
Zone: 7-11 | Layer: Ground Cover
Functions: Edible, Medicinal, Ground Cover, Pest Management

### Starfruit
File: `src/seeds/plants/starfruit-data.yml`
Scientific: *Averrhoa carambola*
Zone: 10-11 | Layer: Tree
Functions: Edible, Ornamental, Wildlife Attractor

### Stinging Nettle
File: `src/seeds/plants/stinging-nettle-data.yml`
Scientific: *Urtica dioica*
Zone: 3-10 | Layer: Herbaceous
Functions: Edible, Medicinal, Dynamic Accumulator, Animal Fodder, Mulcher

### Stinging Tree
File: `src/seeds/plants/stinging-tree-data.yml`
Scientific: *Dendrocnide moroides*
Zone: 10-12 | Layer: Tree
Functions: Wildlife Attractor, Border Plant

### Strawberry
File: `src/seeds/plants/strawberry-data.yml`
Scientific: *Fragaria × ananassa*
Zone: 3-10 | Layer: Ground Cover
Functions: Edible, Wildlife Attractor, Pollinator, Border Plant, Dynamic Accumulator

### Strawberry Guava
File: `src/seeds/plants/strawberry-guava-data.yml`
Scientific: *Psidium cattleyanum*
Zone: 9-11 | Layer: Shrub, Tree
Functions: Edible, Wildlife Attractor, Windbreaker, Border Plant

### Sugar Apple
File: `src/seeds/plants/sugar-apple-data.yml`
Scientific: *Annona squamosa*
Zone: 10-11 | Layer: Tree
Functions: Edible, Wildlife Attractor, Shade Provider, Ornamental

### Sun Hemp
File: `src/seeds/plants/sun-hemp-data.yml`
Scientific: *Crotalaria juncea*
Zone: 8-12 | Layer: Herbaceous
Functions: Nitrogen Fixer, Mulcher, Dynamic Accumulator, Erosion Control, Biofuel

### Sunchoke
File: `src/seeds/plants/sunchoke-data.yml`
Scientific: *Helianthus tuberosus*
Zone: 3-8 | Layer: Root, Sub-Canopy
Functions: Edible, Biofuel, Wildlife Attractor, Erosion Control

### Sundew
File: `src/seeds/plants/sundew-data.yml`
Scientific: *Drosera spp.*
Zone: 6-9 | Layer: Ground Cover
Functions: Pest Management, Wildlife Attractor, Ground Cover

### Sunflower
File: `src/seeds/plants/sunflower-data.yml`
Scientific: *Helianthus annuus*
Zone: 2-11 | Layer: Herbaceous
Functions: Edible, Wildlife Attractor, Pollinator, Mulcher, Dynamic Accumulator, Erosion Control, Windbreaker, Border Plant, Biofuel


---

## When Done

```bash
python3 validate.py --since 2h
./sync.sh --check
./sync.sh
rm review/practitioner_notes_28_of_34.md
```

Then open `practitioner_notes_29_of_34.md`
