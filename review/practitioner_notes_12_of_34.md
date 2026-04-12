# Practitioner Notes — Batch 12 of 34

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

### Dill
File: `src/seeds/plants/dill-data.yml`
Scientific: *Anethum graveolens*
Zone: 2-11 | Layer: Herbaceous
Functions: Edible, Medicinal, Pollinator, Wildlife Attractor, Border Plant, Pest Management

### Dinosaur Gourd
File: `src/seeds/plants/dinosaur-gourd-data.yml`
Scientific: *Lagenaria siceraria*
Zone: 3-11 | Layer: Vine
Functions: Ornamental, Edible, Fiber

### Duck Potato
File: `src/seeds/plants/duck-potato-data.yml`
Scientific: *Sagittaria latifolia*
Zone: 4-11 | Layer: Aquatic, Herbaceous, Root
Functions: Edible, Water Purifier, Wildlife Attractor

### Duckweed
File: `src/seeds/plants/duckweed-data.yml`
Scientific: *Lemna minor*
Zone: 4-10 | Layer: Aquatic
Functions: Edible, Animal Fodder, Water Purifier, Biofuel

### Dutch Clover
File: `src/seeds/plants/dutch-clover-data.yml`
Scientific: *Trifolium repens*
Zone: 3-10 | Layer: Ground Cover
Functions: Nitrogen Fixer, Pollinator, Wildlife Attractor, Mulcher, Dynamic Accumulator, Erosion Control, Animal Fodder, Border Plant, Ground Cover

### Dynamic accumulators
File: `src/seeds/plants/dynamic-accumulators-data.yml`
Scientific: *Various species (guild concept)*
Zone: 3-11 | Layer: Herbaceous
Functions: Dynamic Accumulator, Mulcher, Soil Improvement, Green Manure, Animal Fodder

### Earth Chestnut
File: `src/seeds/plants/earth-chestnut-data.yml`
Scientific: *Lathyrus tuberosus*
Zone: 6-9 | Layer: Herbaceous
Functions: Edible, Nitrogen Fixer, Ground Cover, Pollinator, Wildlife Attractor

### Echinacea
File: `src/seeds/plants/echinacea-data.yml`
Scientific: *Echinacea purpurea*
Zone: 3-9 | Layer: Herbaceous
Functions: Edible, Medicinal, Pollinator, Wildlife Attractor, Mulcher, Dynamic Accumulator, Border Plant

### Eddoe
File: `src/seeds/plants/eddoe-data.yml`
Scientific: *Colocasia esculenta (eddoe type)*
Zone: 8-12 | Layer: Herbaceous
Functions: Edible, Ground Cover, Animal Fodder, Mulcher

### Edible Hibiscus
File: `src/seeds/plants/edible-hibiscus-data.yml`
Scientific: *Abelmoschus manihot*
Zone: 8-12 | Layer: Shrub
Functions: Edible, Ornamental, Mulcher, Wildlife Attractor

### Egyptian Spinach
File: `src/seeds/plants/egyptian-spinach-data.yml`
Scientific: *Corchorus olitorius*
Zone: 9-12 | Layer: Herbaceous
Functions: Edible, Medicinal, Ground Cover, Dynamic Accumulator

### Elderberry
File: `src/seeds/plants/elderberry-data.yml`
Scientific: *Sambucus nigra*
Zone: 3-10 | Layer: Shrub
Functions: Edible, Medicinal, Pollinator, Wildlife Attractor, Dynamic Accumulator, Erosion Control, Windbreaker, Border Plant

### Elderflower
File: `src/seeds/plants/elderflower-data.yml`
Scientific: *Sambucus nigra*
Zone: 4-9 | Layer: Shrub
Functions: Edible, Medicinal, Wildlife Attractor, Border Plant, Mulcher

### Elecampane
File: `src/seeds/plants/elecampane-data.yml`
Scientific: *Inula helenium*
Zone: 4-9 | Layer: Herbaceous
Functions: Medicinal, Pollinator, Wildlife Attractor, Dynamic Accumulator, Biomass

### Elephant Foot Yam
File: `src/seeds/plants/elephant-foot-yam-data.yml`
Scientific: *Amorphophallus paeoniifolius*
Zone: 9-11 | Layer: Herbaceous, Root
Functions: Edible, Ornamental, Mulcher

### Elephant Grass
File: `src/seeds/plants/elephant-grass-data.yml`
Scientific: *Pennisetum purpureum*
Zone: 8-11 | Layer: Herbaceous
Functions: Animal Fodder, Erosion Control, Windbreaker, Biofuel

### Elliott Blueberry
File: `src/seeds/plants/elliott-blueberry-data.yml`
Scientific: *Vaccinium corymbosum 'Elliott'*
Zone: 7-9 | Layer: Shrub
Functions: Edible, Pollinator, Wildlife Attractor, Ornamental

### Epazote
File: `src/seeds/plants/epazote-data.yml`
Scientific: *Dysphania ambrosioides*
Zone: 8-11 | Layer: Herbaceous
Functions: Edible, Medicinal, Pest Management

### Evergreen Huckleberry
File: `src/seeds/plants/evergreen-huckleberry-data.yml`
Scientific: *Vaccinium ovatum*
Zone: 7-10 | Layer: Shrub
Functions: Edible, Wildlife Attractor, Border Plant, Erosion Control, Ornamental

### Fava Bean
File: `src/seeds/plants/fava-bean-data.yml`
Scientific: *Vicia faba*
Zone: 3-11 | Layer: Herbaceous
Functions: Edible, Nitrogen Fixer, Cover Crop


---

## When Done

```bash
python3 validate.py --since 2h
./sync.sh --check
./sync.sh
rm review/practitioner_notes_12_of_34.md
```

Then open `practitioner_notes_13_of_34.md`
