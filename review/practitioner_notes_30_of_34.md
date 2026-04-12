# Practitioner Notes — Batch 30 of 34

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

### Tansy
File: `src/seeds/plants/tansy-data.yml`
Scientific: *Tanacetum vulgare*
Zone: 4-8 | Layer: Herb
Functions: Pest Management, Medicinal, Ornamental

### Tarragon
File: `src/seeds/plants/tarragon-data.yml`
Scientific: *Artemisia dracunculus*
Zone: 4-8 | Layer: Shrub
Functions: Edible, Medicinal, Pollinator

### Taro
File: `src/seeds/plants/taro-data.yml`
Scientific: *Colocasia esculenta*
Zone: 8-11 | Layer: Herbaceous
Functions: Edible, Animal Fodder, Ground Cover

### Tea Tree
File: `src/seeds/plants/tea-tree-data.yml`
Scientific: *Melaleuca alternifolia*
Zone: 8-11 | Layer: Shrub, Tree
Functions: Medicinal, Wildlife Attractor, Windbreaker

### Tephrosia vogelii
File: `src/seeds/plants/tephrosia-vogelii-data.yml`
Scientific: *Tephrosia vogelii*
Zone: 10-12 | Layer: Shrub
Functions: Nitrogen Fixer, Biomass, Pest Management

### Texas Olive
File: `src/seeds/plants/texas-olive-data.yml`
Scientific: *Cordia boissieri*
Zone: 9-11 | Layer: Sub-Canopy, Shrub
Functions: Ornamental, Wildlife Attractor, Erosion Control

### Texas Persimmon
File: `src/seeds/plants/texas-persimmon-data.yml`
Scientific: *Diospyros texana*
Zone: 7-10 | Layer: Tree
Functions: Edible, Wildlife Attractor, Erosion Control

### Thai Basil
File: `src/seeds/plants/thai-basil-data.yml`
Scientific: *Ocimum basilicum var. thyrsiflorum*
Zone: 9-11 | Layer: Herbaceous
Functions: Edible, Pollinator, Pest Management

### Thyme
File: `src/seeds/plants/thyme-data.yml`
Scientific: *Thymus vulgaris*
Zone: 4-9 | Layer: Herbaceous, Ground Cover
Functions: Edible, Medicinal, Pollinator, Wildlife Attractor, Mulcher, Dynamic Accumulator, Border Plant, Pest Management

### Tick Trefoil
File: `src/seeds/plants/tick-trefoil-data.yml`
Scientific: *Desmodium paniculatum*
Zone: 4-9 | Layer: Herb
Functions: Nitrogen Fixer, Wildlife Attractor, Ground Cover

### Tickseed Sunflower
File: `src/seeds/plants/tickseed-sunflower-data.yml`
Scientific: *Bidens aristosa*
Zone: 5-10 | Layer: Herb, Ground Cover
Functions: Wildlife Attractor, Pollinator, Erosion Control, Ornamental, Edible

### Tithonia
File: `src/seeds/plants/tithonia-data.yml`
Scientific: *Tithonia rotundifolia*
Zone: 8-11 | Layer: Herbaceous, Shrub
Functions: Pollinator, Wildlife Attractor, Mulcher, Dynamic Accumulator, Border Plant

### Toothache Plant
File: `src/seeds/plants/toothache-plant-data.yml`
Scientific: *Acmella oleracea*
Zone: 9-12 | Layer: Herbaceous
Functions: Edible, Medicinal, Pollinator, Ornamental

### Topinambur
File: `src/seeds/plants/topinambur-data.yml`
Scientific: *Helianthus tuberosus*
Zone: 3-9 | Layer: Herbaceous, Root
Functions: Edible, Animal Fodder, Mulcher, Wildlife Attractor, Dynamic Accumulator

### Tree Collard
File: `src/seeds/plants/tree-collard-data.yml`
Scientific: *Brassica oleracea var. acephala 'Tree Collard'*
Zone: 8-10 | Layer: Shrub
Functions: Edible, Wildlife Attractor, Mulcher, Dynamic Accumulator, Erosion Control, Animal Fodder, Border Plant

### Tree Medick
File: `src/seeds/plants/tree-medick-data.yml`
Scientific: *Medicago arborea*
Zone: 8-10 | Layer: Shrub
Functions: Nitrogen Fixer, Animal Fodder, Soil Improvement, Erosion Control, Ornamental

### Tree Spinach
File: `src/seeds/plants/tree-spinach-data.yml`
Scientific: *Cnidoscolus aconitifolius*
Zone: 9-11 | Layer: Shrub
Functions: Edible, Mulcher, Animal Fodder

### Tropical Spinach
File: `src/seeds/plants/tropical-spinach-data.yml`
Scientific: *Basella alba (primary)*
Zone: 9-12 | Layer: Vine
Functions: Edible, Ground Cover, Shade Provider, Pollinator

### Tuberous Nasturtium
File: `src/seeds/plants/tuberous-nasturtium-data.yml`
Scientific: *Tropaeolum tuberosum*
Zone: 8-11 | Layer: Vine, Root
Functions: Edible, Ground Cover, Ornamental, Wildlife Attractor, Dynamic Accumulator

### Tucumã Palm
File: `src/seeds/plants/tucumã-palm-data.yml`
Scientific: *Astrocaryum vulgare*
Zone: 10-11 | Layer: Tree
Functions: Edible, Fiber, Wildlife Attractor


---

## When Done

```bash
python3 validate.py --since 2h
./sync.sh --check
./sync.sh
rm review/practitioner_notes_30_of_34.md
```

Then open `practitioner_notes_31_of_34.md`
