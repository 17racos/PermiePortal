# Practitioner Notes — Batch 8 of 34

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

### Cattley Guava
File: `src/seeds/plants/cattley-guava-data.yml`
Scientific: *Psidium cattleianum*
Zone: 9-12 | Layer: Shrub
Functions: Edible, Wildlife Attractor, Ornamental

### Caucasian Spinach
File: `src/seeds/plants/caucasian-spinach-data.yml`
Scientific: *Hablitzia tamnoides*
Zone: 4-8 | Layer: Vine, Herbaceous
Functions: Edible, Shade Provider, Wildlife Attractor, Ground Cover

### Caveman Club Gourd
File: `src/seeds/plants/caveman-club-gourd-data.yml`
Scientific: *Lagenaria siceraria*
Zone: 3-11 | Layer: Vine
Functions: Edible, Ornamental, Animal Fodder

### Celery
File: `src/seeds/plants/celery-data.yml`
Scientific: *Apium graveolens*
Zone: 2-10 | Layer: Herbaceous
Functions: Edible, Medicinal, Wildlife Attractor, Mulcher, Dynamic Accumulator, Border Plant

### Celtuce
File: `src/seeds/plants/celtuce-data.yml`
Scientific: *Lactuca sativa var. asparagina*
Zone: 4-9 | Layer: Herbaceous
Functions: Edible, Ground Cover, Biomass

### Century Plant
File: `src/seeds/plants/century-plant-data.yml`
Scientific: *Agave americana*
Zone: 8-11 | Layer: Herbaceous
Functions: Edible, Fiber, Ornamental, Erosion Control, Mulcher

### Ceylon Gooseberry Tree
File: `src/seeds/plants/ceylon-gooseberry-tree-data.yml`
Scientific: *Dovyalis hebecarpa*
Zone: 9-11 | Layer: Shrub, Tree
Functions: Edible, Wildlife Attractor, Border Plant, Windbreaker, Erosion Control

### Chaga Host
File: `src/seeds/plants/chaga-host-data.yml`
Scientific: *Inonotus obliquus*
Zone: 2-7 | Layer: Tree
Functions: Medicinal, Mulcher

### Chamomile
File: `src/seeds/plants/chamomile-data.yml`
Scientific: *Matricaria chamomilla (German Chamomile), Chamaemelum nobile (Roman Chamomile)*
Zone: 4-9 | Layer: Herbaceous
Functions: Edible, Medicinal, Pollinator, Wildlife Attractor, Mulcher, Dynamic Accumulator, Border Plant, Pest Management

### Chaya
File: `src/seeds/plants/chaya-data.yml`
Scientific: *Cnidoscolus aconitifolius*
Zone: 9-11 | Layer: Shrub
Functions: Edible, Medicinal, Wildlife Attractor, Mulcher, Dynamic Accumulator, Erosion Control, Animal Fodder

### Chayote
File: `src/seeds/plants/chayote-data.yml`
Scientific: *Sechium edule*
Zone: 8-11 | Layer: Vine
Functions: Edible, Mulcher, Ground Cover, Wildlife Attractor

### Cherimoya
File: `src/seeds/plants/cherimoya-data.yml`
Scientific: *Annona cherimola*
Zone: 10-11 | Layer: Tree
Functions: Edible, Ornamental, Shade Provider, Wildlife Attractor

### Chia
File: `src/seeds/plants/chia-data.yml`
Scientific: *Salvia hispanica*
Zone: 9-12 | Layer: Herbaceous
Functions: Edible, Medicinal, Pollinator, Wildlife Attractor, Mulcher, Dynamic Accumulator, Erosion Control, Animal Fodder, Border Plant, Pest Management, Biofuel, Ground Cover

### Chickasaw Plum
File: `src/seeds/plants/chickasaw-plum-data.yml`
Scientific: *Prunus angustifolia*
Zone: 5-9 | Layer: Tree, Shrub
Functions: Edible, Wildlife Attractor, Erosion Control, Mulcher

### Chicken of the Woods Host
File: `src/seeds/plants/chicken-of-the-woods-host-data.yml`
Scientific: *Laetiporus sulphureus (species complex)*
Zone: 4-11 | Layer: Tree
Functions: Edible, Mulcher, Wildlife Attractor

### Chickpea
File: `src/seeds/plants/chickpea-data.yml`
Scientific: *Cicer arietinum*
Zone: 2-10 | Layer: Herbaceous
Functions: Edible, Nitrogen Fixer, Ground Cover

### Chickweed
File: `src/seeds/plants/chickweed-data.yml`
Scientific: *Stellaria media*
Zone: 4-9 | Layer: Ground Cover
Functions: Edible, Medicinal, Ground Cover, Wildlife Attractor

### Chicory
File: `src/seeds/plants/chicory-data.yml`
Scientific: *Cichorium intybus*
Zone: 3-10 | Layer: Herbaceous, Root
Functions: Edible, Dynamic Accumulator, Pollinator, Ground Cover

### Chilean Pea
File: `src/seeds/plants/chilean-pea-data.yml`
Scientific: *Lathyrus chilensis*
Zone: 5-9 | Layer: Herbaceous, Ground Cover
Functions: Edible, Nitrogen Fixer, Pollinator, Wildlife Attractor, Ground Cover

### Chiltepin Pepper
File: `src/seeds/plants/chiltepin-pepper-data.yml`
Scientific: *Capsicum annuum var. glabriusculum*
Zone: 9-11 | Layer: Herbaceous, Shrub
Functions: Edible, Pest Management, Wildlife Attractor, Ornamental


---

## When Done

```bash
python3 validate.py --since 2h
./sync.sh --check
./sync.sh
rm review/practitioner_notes_8_of_34.md
```

Then open `practitioner_notes_9_of_34.md`
