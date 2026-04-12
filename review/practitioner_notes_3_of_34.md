# Practitioner Notes — Batch 3 of 34

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

### Artemisia
File: `src/seeds/plants/artemisia-data.yml`
Scientific: *Artemisia annua*
Zone: 2-11 | Layer: Herbaceous
Functions: Medicinal, Pest Management, Wildlife Attractor, Border Plant

### Ashitaba
File: `src/seeds/plants/ashitaba-data.yml`
Scientific: *Angelica keiskei*
Zone: 9-11 | Layer: Herbaceous
Functions: Edible, Medicinal, Pollinator, Ornamental

### Ashwagandha
File: `src/seeds/plants/ashwagandha-data.yml`
Scientific: *Withania somnifera*
Zone: 9-12 | Layer: Herbaceous
Functions: Medicinal, Wildlife Attractor, Erosion Control, Dynamic Accumulator

### Asparagus Bean
File: `src/seeds/plants/asparagus-bean-data.yml`
Scientific: *Vigna unguiculata subsp. sesquipedalis*
Zone: 3-11 | Layer: Vine
Functions: Edible, Nitrogen Fixer, Pollinator, Animal Fodder

### Asparagus
File: `src/seeds/plants/asparagus-data.yml`
Scientific: *Asparagus officinalis*
Zone: 3-8 | Layer: Herbaceous
Functions: Edible, Medicinal, Ground Cover

### Atemoya
File: `src/seeds/plants/atemoya-data.yml`
Scientific: *Annona × atemoya*
Zone: 10-11 | Layer: Tree
Functions: Edible, Shade Provider, Wildlife Attractor, Ornamental

### Autumn Olive
File: `src/seeds/plants/autumn-olive-data.yml`
Scientific: *Elaeagnus umbellata*
Zone: 4-9 | Layer: Shrub
Functions: Edible, Nitrogen Fixer, Wildlife Attractor, Windbreaker

### Autumnberry
File: `src/seeds/plants/autumnberry-data.yml`
Scientific: *Elaeagnus umbellata*
Zone: 4-9 | Layer: Shrub
Functions: Edible, Nitrogen Fixer, Wildlife Attractor, Erosion Control, Border Plant

### Avocado
File: `src/seeds/plants/avocado-data.yml`
Scientific: *Persea americana*
Zone: 9-11 | Layer: Canopy
Functions: Edible, Medicinal, Wildlife Attractor, Windbreaker, Border Plant

### Azalea
File: `src/seeds/plants/azalea-data.yml`
Scientific: *Rhododendron spp.*
Zone: 5-9 | Layer: Shrub
Functions: Pollinator, Wildlife Attractor, Border Plant, Ground Cover

### Bactris Gasipaes
File: `src/seeds/plants/bactris-gasipaes-data.yml`
Scientific: *Bactris gasipaes*
Zone: 10-11 | Layer: Tree
Functions: Edible, Animal Fodder, Mulcher, Windbreaker, Wildlife Attractor

### Bacupari
File: `src/seeds/plants/bacupari-data.yml`
Scientific: *Garcinia gardneriana*
Zone: 10-12 | Layer: Tree
Functions: Edible, Wildlife Attractor, Shade Provider

### Bacuri
File: `src/seeds/plants/bacuri-data.yml`
Scientific: *Platonia insignis*
Zone: 10-11 | Layer: Tree
Functions: Edible, Timber, Wildlife Attractor

### Bamboo
File: `src/seeds/plants/bamboo-data.yml`
Scientific: *Bambusoideae*
Zone: 5-10 | Layer: Canopy, Sub-Canopy
Functions: Edible, Medicinal, Wildlife Attractor, Erosion Control, Windbreaker, Border Plant, Ground Cover, Biofuel

### Banana
File: `src/seeds/plants/banana-data.yml`
Scientific: *Musa spp.*
Zone: 9-11 | Layer: Canopy
Functions: Edible, Mulcher, Animal Fodder, Windbreaker, Border Plant

### Banana Passionfruit
File: `src/seeds/plants/banana-passionfruit-data.yml`
Scientific: *Passiflora tarminiana*
Zone: 9-11 | Layer: Vine
Functions: Edible, Ornamental, Wildlife Attractor, Shade Provider

### Baobab
File: `src/seeds/plants/baobab-data.yml`
Scientific: *Adansonia digitata*
Zone: 10b-11 | Layer: Tree
Functions: Edible, Medicinal, Wildlife Attractor, Shade Provider, Water Retention, Ornamental

### Baptisia
File: `src/seeds/plants/baptisia-data.yml`
Scientific: *Baptisia australis*
Zone: 3-9 | Layer: Herbaceous
Functions: Nitrogen Fixer, Ornamental, Wildlife Attractor, Dynamic Accumulator

### Barbados Cherry
File: `src/seeds/plants/barbados-cherry-data.yml`
Scientific: *Malpighia emarginata*
Zone: 9-11 | Layer: Shrub, Sub-Canopy
Functions: Edible, Medicinal, Wildlife Attractor, Ornamental

### Basil
File: `src/seeds/plants/basil-data.yml`
Scientific: *Ocimum basilicum*
Zone: 9-11 | Layer: Herbaceous
Functions: Edible, Medicinal, Pollinator, Wildlife Attractor, Border Plant, Pest Management


---

## When Done

```bash
python3 validate.py --since 2h
./sync.sh --check
./sync.sh
rm review/practitioner_notes_3_of_34.md
```

Then open `practitioner_notes_4_of_34.md`
