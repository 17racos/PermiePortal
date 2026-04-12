# Practitioner Notes — Batch 10 of 34

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

### Coontie
File: `src/seeds/plants/coontie-data.yml`
Scientific: *Zamia integrifolia*
Zone: (8b-11) | Layer: Herbaceous
Functions: Ground Cover, Wildlife Attractor, Medicinal

### Coquinho Azedo
File: `src/seeds/plants/coquinho-azedo-data.yml`
Scientific: *Psidium friedrichsthalianum*
Zone: 10-11 | Layer: Tree, Shrub
Functions: Edible, Wildlife Attractor, Pollinator

### Coral Bean
File: `src/seeds/plants/coral-bean-data.yml`
Scientific: *Erythrina herbacea*
Zone: 7-10 | Layer: Shrub
Functions: Edible, Medicinal, Wildlife Attractor, Erosion Control, Border Plant

### Coralberry
File: `src/seeds/plants/coralberry-data.yml`
Scientific: *Symphoricarpos orbiculatus*
Zone: 4-9 | Layer: Shrub
Functions: Wildlife Attractor, Erosion Control, Border Plant, Ornamental

### Cordyceps Host
File: `src/seeds/plants/cordyceps-host-data.yml`
Scientific: *Cordyceps militaris*
Zone: 5-11 | Layer: Herbaceous
Functions: Edible, Medicinal

### Coreopsis
File: `src/seeds/plants/coreopsis-data.yml`
Scientific: *Coreopsis lanceolata*
Zone: 4-10 | Layer: Herbaceous
Functions: Ornamental, Pollinator, Wildlife Attractor, Ground Cover

### Corsican Gourd
File: `src/seeds/plants/corsican-gourd-data.yml`
Scientific: *Lagenaria siceraria*
Zone: 3-11 | Layer: Vine
Functions: Edible, Ornamental, Fiber

### Corsican Mint
File: `src/seeds/plants/corsican-mint-data.yml`
Scientific: *Mentha requienii*
Zone: 6-9 | Layer: Ground Cover, Herbaceous
Functions: Edible, Ground Cover, Ornamental

### Corsican Stonecrop
File: `src/seeds/plants/corsican-stonecrop-data.yml`
Scientific: *Sedum dasyphyllum*
Zone: 7-11 | Layer: Ground Cover
Functions: Ornamental, Ground Cover, Erosion Control, Water Retention

### Costmary
File: `src/seeds/plants/costmary-data.yml`
Scientific: *Tanacetum balsamita*
Zone: 4-9 | Layer: Herbaceous
Functions: Edible, Medicinal, Ornamental, Pest Management

### Cranberry
File: `src/seeds/plants/cranberry-data.yml`
Scientific: *Vaccinium macrocarpon*
Zone: 2-7 | Layer: Ground Cover
Functions: Edible, Medicinal, Ground Cover, Wildlife Attractor

### Cranberry Hibiscus
File: `src/seeds/plants/cranberry-hibiscus-data.yml`
Scientific: *Hibiscus acetosella*
Zone: 8-11 | Layer: Shrub
Functions: Edible, Medicinal, Pollinator, Wildlife Attractor, Mulcher, Dynamic Accumulator, Border Plant

### Creeping Jenny
File: `src/seeds/plants/creeping-jenny-data.yml`
Scientific: *Lysimachia nummularia*
Zone: 4-9 | Layer: Ground Cover
Functions: Ground Cover, Ornamental, Erosion Control, Wildlife Attractor

### Creeping Oregano
File: `src/seeds/plants/creeping-oregano-data.yml`
Scientific: *Origanum vulgare*
Zone: 5-9 | Layer: Herbaceous, Ground Cover
Functions: Edible, Ground Cover, Pollinator

### Creeping Phlox
File: `src/seeds/plants/creeping-phlox-data.yml`
Scientific: *Phlox subulata*
Zone: 3-9 | Layer: Ground Cover
Functions: Ornamental, Pollinator, Ground Cover, Erosion Control

### Creeping Raspberry
File: `src/seeds/plants/creeping-raspberry-data.yml`
Scientific: *Rubus hayata-koidzumii*
Zone: 7-11 | Layer: Ground Cover
Functions: Edible, Ground Cover, Erosion Control, Wildlife Attractor

### Creeping Rosemary
File: `src/seeds/plants/creeping-rosemary-data.yml`
Scientific: *Salvia rosmarinus 'Prostratus'*
Zone: 8-11 | Layer: Ground Cover, Shrub
Functions: Edible, Medicinal, Pollinator, Border Plant, Pest Management

### Creeping Thyme
File: `src/seeds/plants/creeping-thyme-data.yml`
Scientific: *Thymus serpyllum*
Zone: 4-9 | Layer: Ground Cover, Herbaceous
Functions: Edible, Medicinal, Pollinator, Ground Cover

### Crimson Clover
File: `src/seeds/plants/crimson-clover-data.yml`
Scientific: *Trifolium incarnatum*
Zone: 6-9 | Layer: Ground Cover
Functions: Nitrogen Fixer, Pollinator, Wildlife Attractor, Mulcher, Dynamic Accumulator, Erosion Control, Animal Fodder, Border Plant, Pest Management

### Crown Vetch
File: `src/seeds/plants/crown-vetch-data.yml`
Scientific: *Securigera varia*
Zone: 4-9 | Layer: Herbaceous, Ground Cover
Functions: Nitrogen Fixer, Erosion Control, Biomass, Animal Fodder


---

## When Done

```bash
python3 validate.py --since 2h
./sync.sh --check
./sync.sh
rm review/practitioner_notes_10_of_34.md
```

Then open `practitioner_notes_11_of_34.md`
