# Practitioner Notes — Batch 17 of 34

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

### Jucara Palm
File: `src/seeds/plants/jucara-palm-data.yml`
Scientific: *Euterpe edulis*
Zone: 10-12 | Layer: Tree
Functions: Edible, Ornamental, Wildlife Attractor, Shade Provider

### Jute
File: `src/seeds/plants/jute-data.yml`
Scientific: *Corchorus olitorius*
Zone: 8-12 | Layer: Herbaceous
Functions: Fiber, Edible, Cover Crop, Green Manure

### Kaffir Lime
File: `src/seeds/plants/kaffir-lime-data.yml`
Scientific: *Citrus hystrix*
Zone: 9-11 | Layer: Tree
Functions: Edible, Medicinal, Pest Management

### Kale
File: `src/seeds/plants/kale-data.yml`
Scientific: *Brassica oleracea var. acephala*
Zone: 7-10 | Layer: Herbaceous
Functions: Edible, Medicinal, Dynamic Accumulator, Wildlife Attractor, Border Plant

### Kangkong
File: `src/seeds/plants/kangkong-data.yml`
Scientific: *Ipomoea aquatica*
Zone: 9-11 | Layer: Aquatic, Herbaceous
Functions: Edible, Ground Cover, Soil Improvement

### Kapok Tree
File: `src/seeds/plants/kapok-tree-data.yml`
Scientific: *Ceiba pentandra*
Zone: 10b-12 | Layer: Tree
Functions: Fiber, Shade Provider, Wildlife Attractor, Windbreaker

### Katuk
File: `src/seeds/plants/katuk-data.yml`
Scientific: *Sauropus androgynus*
Zone: 10-12 | Layer: Shrub
Functions: Edible, Medicinal, Nitrogen Fixer, Wildlife Attractor, Mulcher, Dynamic Accumulator, Erosion Control, Animal Fodder, Border Plant, Ground Cover

### Kava
File: `src/seeds/plants/kava-data.yml`
Scientific: *Piper methysticum*
Zone: 10-11 | Layer: Shrub, Herbaceous
Functions: Medicinal, Ground Cover, Mulcher

### Kenaf
File: `src/seeds/plants/kenaf-data.yml`
Scientific: *Hibiscus cannabinus*
Zone: 6-12 | Layer: Herbaceous
Functions: Fiber, Cover Crop, Animal Fodder, Green Manure

### Kinnikinnick
File: `src/seeds/plants/kinnikinnick-data.yml`
Scientific: *Arctostaphylos uva-ursi*
Zone: 2-8 | Layer: Ground Cover, Shrub
Functions: Ground Cover, Wildlife Attractor, Medicinal, Ornamental

### Konjac
File: `src/seeds/plants/konjac-data.yml`
Scientific: *Amorphophallus konjac*
Zone: 8-11 | Layer: Herbaceous, Root
Functions: Edible, Ornamental, Biomass

### Kratom
File: `src/seeds/plants/kratom-data.yml`
Scientific: *Mitragyna speciosa*
Zone: 11-12 | Layer: Tree
Functions: Medicinal, Mulcher

### Kumquat
File: `src/seeds/plants/kumquat-data.yml`
Scientific: *Citrus japonica*
Zone: 8-11 | Layer: Shrub
Functions: Edible, Medicinal, Pollinator, Wildlife Attractor, Border Plant

### Kwai Muk
File: `src/seeds/plants/kwai-muk-data.yml`
Scientific: *Artocarpus hypargyraeus*
Zone: 10-11 | Layer: Tree
Functions: Edible, Ornamental, Windbreaker, Mulcher

### Lablab Bean
File: `src/seeds/plants/lablab-bean-data.yml`
Scientific: *Lablab purpureus*
Zone: 10-11 | Layer: Vine
Functions: Edible, Nitrogen Fixer, Ground Cover, Animal Fodder, Pollinator, Mulcher

### Lantana
File: `src/seeds/plants/lantana-data.yml`
Scientific: *Lantana camara*
Zone: 8-11 | Layer: Shrub, Ground Cover
Functions: Pollinator, Wildlife Attractor, Ground Cover, Border Plant

### Lavender
File: `src/seeds/plants/lavender-data.yml`
Scientific: *Lavandula angustifolia*
Zone: 5-9 | Layer: Herbaceous
Functions: Medicinal, Pollinator, Wildlife Attractor, Mulcher, Dynamic Accumulator, Border Plant, Pest Management

### Lead Plant
File: `src/seeds/plants/lead-plant-data.yml`
Scientific: *Amorpha canescens*
Zone: 2-9 | Layer: Shrub
Functions: Nitrogen Fixer, Wildlife Attractor, Erosion Control, Mulcher, Ornamental

### Lemon Basil
File: `src/seeds/plants/lemon-basil-data.yml`
Scientific: *Ocimum × citriodorum*
Zone: 9-11 | Layer: Herbaceous
Functions: Edible, Pollinator, Pest Management

### Lemon Eucalyptus
File: `src/seeds/plants/lemon-eucalyptus-data.yml`
Scientific: *Corymbia citriodora*
Zone: 9-11 | Layer: Tree
Functions: Medicinal, Windbreaker, Mulcher, Wildlife Attractor, Ornamental


---

## When Done

```bash
python3 validate.py --since 2h
./sync.sh --check
./sync.sh
rm review/practitioner_notes_17_of_34.md
```

Then open `practitioner_notes_18_of_34.md`
