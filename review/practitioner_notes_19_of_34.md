# Practitioner Notes — Batch 19 of 34

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

### Malabar Chestnut
File: `src/seeds/plants/malabar-chestnut-data.yml`
Scientific: *Pachira aquatica*
Zone: 10-11 | Layer: Tree
Functions: Edible, Ornamental, Wildlife Attractor

### Malanga
File: `src/seeds/plants/malanga-data.yml`
Scientific: *Xanthosoma sagittifolium*
Zone: 9-11 | Layer: Herbaceous, Root
Functions: Edible, Mulcher, Dynamic Accumulator

### Malabar Spinach
File: `src/seeds/plants/malabar-spinach-data.yml`
Scientific: *Basella alba*
Zone: 9-12 | Layer: Vine
Functions: Edible, Medicinal, Wildlife Attractor, Mulcher, Dynamic Accumulator, Erosion Control, Border Plant, Ground Cover

### Mamey Sapote
File: `src/seeds/plants/mamey-sapote-data.yml`
Scientific: *Pouteria sapota*
Zone: 10-11 | Layer: Tree
Functions: Edible, Ornamental, Wildlife Attractor, Mulcher

### Mango
File: `src/seeds/plants/mango-data.yml`
Scientific: *Mangifera indica*
Zone: 10-11 | Layer: Canopy
Functions: Edible, Medicinal, Wildlife Attractor, Windbreaker, Border Plant

### Mangrove Bean
File: `src/seeds/plants/mangrove-bean-data.yml`
Scientific: *Canavalia rosea*
Zone: 10-12 | Layer: Ground Cover, Vine
Functions: Nitrogen Fixer, Ground Cover, Erosion Control, Wildlife Attractor

### Marang
File: `src/seeds/plants/marang-data.yml`
Scientific: *Artocarpus odoratissimus*
Zone: 10-12 | Layer: Tree, Canopy
Functions: Edible, Shade Provider, Wildlife Attractor, Mulcher

### Marigold
File: `src/seeds/plants/marigold-data.yml`
Scientific: *Tagetes spp.*
Zone: 2-11 | Layer: Herbaceous
Functions: Edible, Medicinal, Pollinator, Wildlife Attractor, Pest Management, Border Plant, Water Purifier

### Marjoram
File: `src/seeds/plants/marjoram-data.yml`
Scientific: *Origanum majorana*
Zone: 9-11 | Layer: Herbaceous
Functions: Edible, Medicinal, Pollinator, Ground Cover

### Marlberry
File: `src/seeds/plants/marlberry-data.yml`
Scientific: *Ardisia escallonioides*
Zone: 9-11 | Layer: Shrub
Functions: Wildlife Attractor, Ornamental, Shade Provider, Edible

### Marsh Hibiscus
File: `src/seeds/plants/marsh-hibiscus-data.yml`
Scientific: *Hibiscus moscheutos*
Zone: 4-10 | Layer: Herb, Shrub
Functions: Ornamental, Pollinator, Wildlife Attractor, Water Retention

### Marsh Marigold
File: `src/seeds/plants/marsh-marigold-data.yml`
Scientific: *Caltha palustris*
Zone: 3-7 | Layer: Herbaceous, Aquatic
Functions: Ornamental, Wildlife Attractor, Pollinator, Water Retention

### Marsh Pennywort
File: `src/seeds/plants/marsh-pennywort-data.yml`
Scientific: *Hydrocotyle umbellata*
Zone: 5-11 | Layer: Ground Cover, Aquatic
Functions: Ground Cover, Aquatic, Wildlife Attractor, Edible

### Mashua
File: `src/seeds/plants/mashua-data.yml`
Scientific: *Tropaeolum tuberosum*
Zone: 8-11 | Layer: Vine, Root
Functions: Edible, Ground Cover, Ornamental, Wildlife Attractor

### Mayhaw
File: `src/seeds/plants/mayhaw-data.yml`
Scientific: *Crataegus opaca*
Zone: 7-10 | Layer: Tree, Shrub
Functions: Edible, Wildlife Attractor, Ornamental

### Maypop
File: `src/seeds/plants/maypop-data.yml`
Scientific: *Passiflora incarnata*
Zone: 5-9 | Layer: Vine, Herbaceous
Functions: Edible, Medicinal, Pollinator, Wildlife Attractor

### Mazus
File: `src/seeds/plants/mazus-data.yml`
Scientific: *Mazus reptans*
Zone: 5-9 | Layer: Ground Cover, Herbaceous
Functions: Ground Cover, Ornamental, Pollinator, Border Plant

### Meadowsweet
File: `src/seeds/plants/meadowsweet-data.yml`
Scientific: *Filipendula ulmaria*
Zone: 3-8 | Layer: Herbaceous
Functions: Medicinal, Pollinator, Wildlife Attractor, Ornamental

### Mexican Bush Sage
File: `src/seeds/plants/mexican-bush-sage-data.yml`
Scientific: *Salvia leucantha*
Zone: 8-11 | Layer: Shrub
Functions: Pollinator, Ornamental, Wildlife Attractor, Border Plant

### Mexican Tarragon
File: `src/seeds/plants/mexican-tarragon-data.yml`
Scientific: *Tagetes lucida*
Zone: 8-11 | Layer: Herbaceous
Functions: Edible, Medicinal, Ornamental, Wildlife Attractor


---

## When Done

```bash
python3 validate.py --since 2h
./sync.sh --check
./sync.sh
rm review/practitioner_notes_19_of_34.md
```

Then open `practitioner_notes_20_of_34.md`
