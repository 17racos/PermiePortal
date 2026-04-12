# Practitioner Notes — Batch 20 of 34

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

### Milk Vetch
File: `src/seeds/plants/milk-vetch-data.yml`
Scientific: *Astragalus canadensis*
Zone: 3-8 | Layer: Herbaceous
Functions: Nitrogen Fixer, Wildlife Attractor, Pollinator, Animal Fodder

### Milkweed
File: `src/seeds/plants/milkweed-data.yml`
Scientific: *Asclepias spp.*
Zone: 3-9 | Layer: Ground Cover, Shrub
Functions: Edible, Medicinal, Wildlife Attractor, Erosion Control

### Millet
File: `src/seeds/plants/millet-data.yml`
Scientific: *Panicum miliaceum*
Zone: 2-11 | Layer: Herbaceous
Functions: Edible, Animal Fodder, Erosion Control, Ground Cover

### Mimosa
File: `src/seeds/plants/mimosa-data.yml`
Scientific: *Albizia julibrissin*
Zone: 7-10 | Layer: Tree
Functions: Nitrogen Fixer, Shade Provider, Wildlife Attractor, Ornamental

### Miner's Lettuce
File: `src/seeds/plants/miners-lettuce-data.yml`
Scientific: *Claytonia perfoliata*
Zone: 6-10 | Layer: Ground Cover, Herbaceous
Functions: Edible, Ground Cover, Wildlife Attractor, Dynamic Accumulator

### Mint
File: `src/seeds/plants/mint-data.yml`
Scientific: *Mentha spp.*
Zone: 3-11 | Layer: Herbaceous
Functions: Edible, Medicinal, Pollinator, Wildlife Attractor, Mulcher, Dynamic Accumulator, Erosion Control, Border Plant

### Miracle Berry
File: `src/seeds/plants/miracle-berry-data.yml`
Scientific: *Synsepalum dulcificum*
Zone: 10-11 | Layer: Shrub
Functions: Edible, Ornamental, Wildlife Attractor

### Miracle Fruit
File: `src/seeds/plants/miracle-fruit-data.yml`
Scientific: *Synsepalum dulcificum*
Zone: 10-11 | Layer: Shrub
Functions: Edible, Medicinal, Pollinator, Wildlife Attractor, Border Plant

### Money Tree
File: `src/seeds/plants/money-tree-data.yml`
Scientific: *Pachira aquatica*
Zone: 10-12 | Layer: Sub-Canopy
Functions: Edible, Medicinal, Wildlife Attractor, Indoor Plant

### Monkey Puzzle Tree
File: `src/seeds/plants/monkey-puzzle-tree-data.yml`
Scientific: *Araucaria araucana*
Zone: 7-10 | Layer: Tree
Functions: Ornamental, Windbreaker, Shade Provider, Edible

### Monky Muskmelon
File: `src/seeds/plants/monky-muskmelon-data.yml`
Scientific: *Cucumis melo (Reticulatus Group)*
Zone: 4-11 | Layer: Vine
Functions: Edible, Pollinator, Ground Cover

### Monstera
File: `src/seeds/plants/monstera-data.yml`
Scientific: *Monstera deliciosa*
Zone: 10-12 | Layer: Vine, Sub-Canopy
Functions: Edible, Ornamental, Air Purifier

### Moringa
File: `src/seeds/plants/moringa-data.yml`
Scientific: *Moringa oleifera*
Zone: 9-11 | Layer: Tree
Functions: Edible, Medicinal, Nitrogen Fixer, Mulcher, Dynamic Accumulator, Erosion Control, Animal Fodder, Windbreaker

### Motherwort
File: `src/seeds/plants/motherwort-data.yml`
Scientific: *Leonurus cardiaca*
Zone: 4-8 | Layer: Herbaceous
Functions: Medicinal, Wildlife Attractor, Mulcher, Dynamic Accumulator

### Mountain Soursop
File: `src/seeds/plants/mountain-soursop-data.yml`
Scientific: *Annona montana*
Zone: 10-11 | Layer: Tree
Functions: Edible, Wildlife Attractor, Shade Provider, Medicinal

### Mud Plantain
File: `src/seeds/plants/mud-plantain-data.yml`
Scientific: *Heteranthera limosa*
Zone: 6-11 | Layer: Aquatic, Herbaceous
Functions: Wildlife Attractor, Border Plant, Erosion Control

### Mugwort
File: `src/seeds/plants/mugwort-data.yml`
Scientific: *Artemisia vulgaris*
Zone: 3-9 | Layer: Herbaceous
Functions: Medicinal, Pest Management, Dynamic Accumulator, Wildlife Attractor

### Muhly Grass
File: `src/seeds/plants/muhly-grass-data.yml`
Scientific: *Muhlenbergia capillaris*
Zone: 6-10 | Layer: Herbaceous
Functions: Ornamental, Erosion Control, Wildlife Attractor

### Mulberry Tree
File: `src/seeds/plants/mulberry-tree-data.yml`
Scientific: *Morus spp.*
Zone: 4-10 | Layer: Tree
Functions: Edible, Medicinal, Wildlife Attractor, Mulcher, Dynamic Accumulator, Erosion Control, Animal Fodder, Windbreaker, Border Plant

### Mung Bean
File: `src/seeds/plants/mung-bean-data.yml`
Scientific: *Vigna radiata*
Zone: 6-13 | Layer: Herbaceous
Functions: Edible, Nitrogen Fixer, Ground Cover


---

## When Done

```bash
python3 validate.py --since 2h
./sync.sh --check
./sync.sh
rm review/practitioner_notes_20_of_34.md
```

Then open `practitioner_notes_21_of_34.md`
