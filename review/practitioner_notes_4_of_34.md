# Practitioner Notes — Batch 4 of 34

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

### Beach Strawberry
File: `src/seeds/plants/beach-strawberry-data.yml`
Scientific: *Fragaria chiloensis*
Zone: 5-9 | Layer: Ground Cover, Herbaceous
Functions: Edible, Ground Cover, Erosion Control, Pollinator, Ornamental

### Bearberry
File: `src/seeds/plants/bearberry-data.yml`
Scientific: *Arctostaphylos uva-ursi*
Zone: 2-6 | Layer: Ground Cover, Shrub
Functions: Edible, Wildlife Attractor, Ground Cover, Erosion Control, Ornamental

### Beautyberry
File: `src/seeds/plants/beautyberry-data.yml`
Scientific: *Callicarpa americana*
Zone: 6-10 | Layer: Shrub
Functions: Edible, Medicinal, Wildlife Attractor, Border Plant

### Bee Bush
File: `src/seeds/plants/bee-bush-data.yml`
Scientific: *Aloysia gratissima*
Zone: 8-11 | Layer: Shrub
Functions: Wildlife Attractor, Border Plant, Erosion Control

### Bee Balm
File: `src/seeds/plants/bee-balm-data.yml`
Scientific: *Monarda didyma*
Zone: 3-9 | Layer: Herbaceous
Functions: Edible, Medicinal, Pollinator, Wildlife Attractor, Mulcher, Dynamic Accumulator, Border Plant, Pest Management

### Bergamot
File: `src/seeds/plants/bergamot-data.yml`
Scientific: *Monarda fistulosa*
Zone: 3-9 | Layer: Herbaceous
Functions: Edible, Medicinal, Pollinator, Wildlife Attractor

### Betony
File: `src/seeds/plants/betony-data.yml`
Scientific: *Stachys officinalis*
Zone: 4-8 | Layer: Herbaceous
Functions: Medicinal, Pollinator, Border Plant, Ground Cover, Ornamental

### Bignay
File: `src/seeds/plants/bignay-data.yml`
Scientific: *Antidesma bunius*
Zone: 10-11 | Layer: Tree, Shrub
Functions: Edible, Wildlife Attractor, Ornamental, Mulcher

### Bilimbi
File: `src/seeds/plants/bilimbi-data.yml`
Scientific: *Averrhoa bilimbi*
Zone: 10-11 | Layer: Tree
Functions: Edible, Ornamental, Wildlife Attractor

### Bird of Paradise
File: `src/seeds/plants/bird-of-paradise-data.yml`
Scientific: *Strelitzia reginae*
Zone: 9-11 | Layer: Shrub
Functions: Pollinator, Wildlife Attractor, Border Plant, Ground Cover

### Birdhouse Gourd
File: `src/seeds/plants/birdhouse-gourd-data.yml`
Scientific: *Lagenaria siceraria*
Zone: 3-11 | Layer: Vine
Functions: Edible, Ornamental, Wildlife Attractor

### Bismarck Palm
File: `src/seeds/plants/bismarck-palm-data.yml`
Scientific: *Bismarckia nobilis*
Zone: 10-11 | Layer: Tree
Functions: Ornamental, Windbreaker, Shade Provider

### Bitter Melon
File: `src/seeds/plants/bitter-melon-data.yml`
Scientific: *Momordica charantia*
Zone: 9-11 | Layer: Vine
Functions: Edible, Medicinal, Wildlife Attractor, Ground Cover

### Bitter Orange
File: `src/seeds/plants/bitter-orange-data.yml`
Scientific: *Citrus × aurantium*
Zone: 9-11 | Layer: Tree, Shrub
Functions: Edible, Medicinal, Ornamental, Wildlife Attractor

### Bitter Yam
File: `src/seeds/plants/bitter-yam-data.yml`
Scientific: *Dioscorea dumetorum*
Zone: 10-11 | Layer: Vine
Functions: Edible, Ground Cover, Biomass, Dynamic Accumulator

### Black-eyed Susan
File: `src/seeds/plants/black-eyed-susan-data.yml`
Scientific: *Rudbeckia hirta*
Zone: 3-9 | Layer: Herbaceous
Functions: Pollinator, Wildlife Attractor, Border Plant, Ornamental, Biomass

### Black Ginger
File: `src/seeds/plants/black-ginger-data.yml`
Scientific: *Kaempferia parviflora*
Zone: 9-11 | Layer: Herbaceous
Functions: Medicinal, Edible, Ground Cover

### Black Medic
File: `src/seeds/plants/black-medic-data.yml`
Scientific: *Medicago lupulina*
Zone: 3-8 | Layer: Herbaceous, Ground Cover
Functions: Nitrogen Fixer, Ground Cover, Animal Fodder, Pollinator, Biomass

### Black Mulga
File: `src/seeds/plants/black-mulga-data.yml`
Scientific: *Acacia aneura*
Zone: 9b-11 | Layer: Tree
Functions: Nitrogen Fixer, Animal Fodder, Windbreaker, Wildlife Attractor, Erosion Control, Mulcher

### Black Sage
File: `src/seeds/plants/black-sage-data.yml`
Scientific: *Salvia mellifera*
Zone: 8-11 | Layer: Shrub
Functions: Medicinal, Pollinator, Wildlife Attractor, Drought Tolerant


---

## When Done

```bash
python3 validate.py --since 2h
./sync.sh --check
./sync.sh
rm review/practitioner_notes_4_of_34.md
```

Then open `practitioner_notes_5_of_34.md`
