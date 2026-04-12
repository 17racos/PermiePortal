# Practitioner Notes — Batch 27 of 34

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

### Sesbania grandiflora
File: `src/seeds/plants/sesbania-grandiflora-data.yml`
Scientific: *Sesbania grandiflora*
Zone: 10-12 | Layer: Tree
Functions: Edible, Nitrogen Fixer, Animal Fodder, Shade Provider, Biomass

### Shampoo Ginger
File: `src/seeds/plants/shampoo-ginger-data.yml`
Scientific: *Zingiber zerumbet*
Zone: 9-11 | Layer: Herbaceous
Functions: Medicinal, Edible, Ground Cover, Mulcher, Wildlife Attractor

### Sheep Sorrel
File: `src/seeds/plants/sheep-sorrel-data.yml`
Scientific: *Rumex acetosella*
Zone: 3-9 | Layer: Herbaceous, Ground Cover
Functions: Edible, Dynamic Accumulator, Ground Cover

### Shiitake Oak
File: `src/seeds/plants/shiitake-oak-data.yml`
Scientific: *Lentinula edodes*
Zone: 6-11 | Layer: Tree
Functions: Edible, Medicinal, Timber, Mulcher

### Shiny Blueberry
File: `src/seeds/plants/shiny-blueberry-data.yml`
Scientific: *Vaccinium myrsinites*
Zone: 7-10 | Layer: Shrub
Functions: Edible, Wildlife Attractor, Ground Cover, Pollinator

### Shiso
File: `src/seeds/plants/shiso-data.yml`
Scientific: *Perilla frutescens*
Zone: 5-11 | Layer: Herbaceous
Functions: Edible, Pollinator, Pest Management, Ornamental

### Siberian Peashrub
File: `src/seeds/plants/siberian-peashrub-data.yml`
Scientific: *Caragana arborescens*
Zone: 2-8 | Layer: Shrub, Tree
Functions: Nitrogen Fixer, Animal Fodder, Windbreaker, Wildlife Attractor, Erosion Control

### Siberian Pea Shrub
File: `src/seeds/plants/siberian-pea-shrub-data.yml`
Scientific: *Caragana arborescens*
Zone: 2-7 | Layer: Shrub
Functions: Edible, Nitrogen Fixer, Windbreaker, Erosion Control, Animal Fodder

### Silk Oak
File: `src/seeds/plants/silk-oak-data.yml`
Scientific: *Grevillea robusta*
Zone: 9-11 | Layer: Tree
Functions: Shade Provider, Windbreaker, Wildlife Attractor, Mulcher, Ornamental

### Silverberry
File: `src/seeds/plants/silverberry-data.yml`
Scientific: *Elaeagnus commutata*
Zone: 2-7 | Layer: Shrub
Functions: Edible, Nitrogen Fixer, Wildlife Attractor, Windbreaker, Erosion Control

### Simpson Stopper
File: `src/seeds/plants/simpson-stopper-data.yml`
Scientific: *Myrcianthes fragrans*
Zone: 9b-11 | Layer: Shrub
Functions: Edible, Wildlife Attractor, Ornamental, Pollinator, Border Plant

### Singapore Daisy
File: `src/seeds/plants/singapore-daisy-data.yml`
Scientific: *Sphagneticola trilobata*
Zone: 9-11 | Layer: Ground Cover
Functions: Ground Cover, Erosion Control, Pollinator

### Sisal
File: `src/seeds/plants/sisal-data.yml`
Scientific: *Agave sisalana*
Zone: 9-12 | Layer: Herbaceous
Functions: Fiber, Erosion Control, Ornamental, Animal Fodder

### Skirret
File: `src/seeds/plants/skirret-data.yml`
Scientific: *Sium sisarum*
Zone: 4-9 | Layer: Herb
Functions: Edible, Ground Cover, Water Retention

### Skullcap
File: `src/seeds/plants/skullcap-data.yml`
Scientific: *Scutellaria lateriflora*
Zone: 4-8 | Layer: Herbaceous, Ground Cover
Functions: Medicinal, Pollinator, Wildlife Attractor, Ground Cover

### Snake Gourd
File: `src/seeds/plants/snake-gourd-data.yml`
Scientific: *Trichosanthes cucumerina*
Zone: 10-12 | Layer: Vine
Functions: Edible, Ornamental, Shade Provider

### Snow Pea
File: `src/seeds/plants/snow-pea-data.yml`
Scientific: *Pisum sativum var. saccharatum*
Zone: 3-9 | Layer: Herbaceous
Functions: Edible, Nitrogen Fixer, Ground Cover

### Snowberry
File: `src/seeds/plants/snowberry-data.yml`
Scientific: *Symphoricarpos albus*
Zone: 3-7 | Layer: Shrub
Functions: Wildlife Attractor, Erosion Control, Ornamental

### Society Garlic
File: `src/seeds/plants/society-garlic-data.yml`
Scientific: *Tulbaghia violacea*
Zone: 7-10 | Layer: Ground Cover
Functions: Edible, Medicinal, Pest Management, Ground Cover

### Softstem Bulrush
File: `src/seeds/plants/softstem-bulrush-data.yml`
Scientific: *Schoenoplectus tabernaemontani*
Zone: 4-11 | Layer: Aquatic, Herbaceous
Functions: Erosion Control, Wildlife Attractor, Water Purifier


---

## When Done

```bash
python3 validate.py --since 2h
./sync.sh --check
./sync.sh
rm review/practitioner_notes_27_of_34.md
```

Then open `practitioner_notes_28_of_34.md`
