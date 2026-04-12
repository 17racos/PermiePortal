# Practitioner Notes — Batch 33 of 34

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

### Wild Coriander
File: `src/seeds/plants/wild-coriander-data.yml`
Scientific: *Eryngium foetidum*
Zone: 9-12 | Layer: Herbaceous
Functions: Edible, Medicinal, Pollinator, Border Plant

### Wild Cumin
File: `src/seeds/plants/wild-cumin-data.yml`
Scientific: *Cuminum cyminum*
Zone: 5-10 | Layer: Herbaceous
Functions: Edible, Medicinal, Pollinator, Border Plant

### Wild Dill
File: `src/seeds/plants/wild-dill-data.yml`
Scientific: *Anethum graveolens*
Zone: 8-11 | Layer: Herbaceous
Functions: Edible, Pollinator, Wildlife Attractor, Border Plant

### Wild Fennel
File: `src/seeds/plants/wild-fennel-data.yml`
Scientific: *Foeniculum vulgare*
Zone: 5-11 | Layer: Herbaceous
Functions: Edible, Medicinal, Pollinator, Wildlife Attractor, Border Plant, Dynamic Accumulator

### Wild Ginger
File: `src/seeds/plants/wild-ginger-data.yml`
Scientific: *Asarum canadense*
Zone: 4-7 | Layer: Ground Cover, Herbaceous
Functions: Ground Cover, Medicinal, Wildlife Attractor

### Wild Indigo
File: `src/seeds/plants/wild-indigo-data.yml`
Scientific: *Baptisia tinctoria*
Zone: 3-9 | Layer: Herbaceous
Functions: Nitrogen Fixer, Ornamental, Wildlife Attractor, Dynamic Accumulator

### Wild Leek
File: `src/seeds/plants/wild-leek-data.yml`
Scientific: *Allium tricoccum*
Zone: 3-8 | Layer: Herbaceous, Root
Functions: Edible, Wildlife Attractor, Medicinal

### Wild Mustard Greens
File: `src/seeds/plants/wild-mustard-greens-data.yml`
Scientific: *Brassica juncea*
Zone: 6-11 | Layer: Herb
Functions: Edible, Dynamic Accumulator, Wildlife Attractor, Biomass

### Wild Olive
File: `src/seeds/plants/wild-olive-data.yml`
Scientific: *Osmanthus americanus*
Zone: 6-9 | Layer: Shrub, Tree
Functions: Wildlife Attractor, Border Plant, Windbreaker, Ornamental

### Wild Parsnip
File: `src/seeds/plants/wild-parsnip-data.yml`
Scientific: *Pastinaca sativa*
Zone: 3-9 | Layer: Herbaceous
Functions: Wildlife Attractor, Border Plant, Dynamic Accumulator

### Wild Passionfruit
File: `src/seeds/plants/wild-passionfruit-data.yml`
Scientific: *Passiflora foetida*
Zone: 9-11 | Layer: Vine, Herbaceous
Functions: Edible, Wildlife Attractor, Ground Cover, Medicinal

### Wild Sweet Potato
File: `src/seeds/plants/wild-sweet-potato-data.yml`
Scientific: *Ipomoea pandurata*
Zone: 4-9 | Layer: Vine, Root
Functions: Edible, Ground Cover, Wildlife Attractor, Erosion Control

### Wild Tarragon
File: `src/seeds/plants/wild-tarragon-data.yml`
Scientific: *Artemisia dracunculus*
Zone: 4-9 | Layer: Herbaceous
Functions: Edible, Medicinal, Pollinator, Border Plant

### Windmill Palm
File: `src/seeds/plants/windmill-palm-data.yml`
Scientific: *Trachycarpus fortunei*
Zone: 7-11 | Layer: Tree
Functions: Ornamental, Windbreaker, Wildlife Attractor, Mulcher

### Wine Cap Substrate
File: `src/seeds/plants/wine-cap-substrate-data.yml`
Scientific: *Stropharia rugosoannulata*
Zone: 5-11 | Layer: Ground Cover
Functions: Edible, Mulcher, Soil Improvement

### Winged Bean
File: `src/seeds/plants/winged-bean-data.yml`
Scientific: *Psophocarpus tetragonolobus*
Zone: 9-11 | Layer: Vine
Functions: Edible, Nitrogen Fixer, Ground Cover, Animal Fodder

### Wisteria
File: `src/seeds/plants/wisteria-data.yml`
Scientific: *Wisteria spp.*
Zone: 5-9 | Layer: Vine
Functions: Ornamental, Nitrogen Fixer, Wildlife Attractor, Shade Provider

### Wood Sorrel
File: `src/seeds/plants/wood-sorrel-data.yml`
Scientific: *Oxalis violacea*
Zone: 5-9 | Layer: Herbaceous, Ground Cover
Functions: Edible, Ground Cover, Wildlife Attractor

### Wormwood
File: `src/seeds/plants/wormwood-data.yml`
Scientific: *Artemisia absinthium*
Zone: 4-9 | Layer: Shrub
Functions: Medicinal, Pest Management, Border Plant, Wildlife Attractor

### Yacon
File: `src/seeds/plants/yacon-data.yml`
Scientific: *Smallanthus sonchifolius*
Zone: 7-11 | Layer: Herbaceous, Root
Functions: Edible, Mulcher, Dynamic Accumulator


---

## When Done

```bash
python3 validate.py --since 2h
./sync.sh --check
./sync.sh
rm review/practitioner_notes_33_of_34.md
```

Then open `practitioner_notes_34_of_34.md`
