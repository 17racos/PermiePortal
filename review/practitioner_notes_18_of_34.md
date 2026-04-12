# Practitioner Notes — Batch 18 of 34

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

### Lemon Verbena
File: `src/seeds/plants/lemon-verbena-data.yml`
Scientific: *Aloysia citrodora*
Zone: 8-11 | Layer: Herbaceous, Shrub
Functions: Edible, Medicinal, Ornamental, Pollinator

### Lemon Balm
File: `src/seeds/plants/lemon-balm-data.yml`
Scientific: *Melissa officinalis*
Zone: 4-9 | Layer: Herbaceous
Functions: Edible, Medicinal, Pollinator, Wildlife Attractor, Dynamic Accumulator, Border Plant, Pest Management

### Lemon Tree
File: `src/seeds/plants/lemon-tree-data.yml`
Scientific: *Citrus limon*
Zone: 9-11 | Layer: Canopy
Functions: Edible, Medicinal, Pollinator, Wildlife Attractor, Border Plant

### Lemongrass
File: `src/seeds/plants/lemongrass-data.yml`
Scientific: *Cymbopogon citratus*
Zone: 9-12 | Layer: Herbaceous
Functions: Edible, Medicinal, Wildlife Attractor, Dynamic Accumulator, Erosion Control, Animal Fodder, Border Plant, Pest Management, Water Purifier

### Leren
File: `src/seeds/plants/leren-data.yml`
Scientific: *Calathea allouia*
Zone: 9-11 | Layer: Herbaceous, Root
Functions: Edible, Ground Cover, Ornamental

### Leucaena
File: `src/seeds/plants/leucaena-data.yml`
Scientific: *Leucaena leucocephala*
Zone: 10-11 | Layer: Tree
Functions: Nitrogen Fixer, Animal Fodder, Mulcher, Windbreaker

### Lime Tree
File: `src/seeds/plants/lime-tree-data.yml`
Scientific: *Citrus aurantiifolia*
Zone: 9-11 | Layer: Canopy
Functions: Edible, Medicinal, Pollinator, Wildlife Attractor, Border Plant

### Lion's Mane Host
File: `src/seeds/plants/lions-mane-host-data.yml`
Scientific: *Hericium erinaceus*
Zone: 4-9 | Layer: Tree
Functions: Edible, Medicinal, Mulcher

### Lobelia inflata
File: `src/seeds/plants/lobelia-inflata-data.yml`
Scientific: *Lobelia inflata*
Zone: 3-9 | Layer: Herb
Functions: Medicinal, Pollinator, Wildlife Attractor, Border Plant

### Longan
File: `src/seeds/plants/longan-data.yml`
Scientific: *Dimocarpus longan*
Zone: 10-11 | Layer: Tree
Functions: Edible, Shade Provider, Wildlife Attractor

### Longevity Spinach
File: `src/seeds/plants/longevity-spinach-data.yml`
Scientific: *Gynura procumbens*
Zone: 9-12 | Layer: Ground Cover
Functions: Edible, Medicinal, Wildlife Attractor, Mulcher, Dynamic Accumulator, Erosion Control, Border Plant, Ground Cover

### Loquat
File: `src/seeds/plants/loquat-data.yml`
Scientific: *Eriobotrya japonica*
Zone: 8-10 | Layer: Canopy
Functions: Edible, Wildlife Attractor, Medicinal, Pollinator, Mulcher, Erosion Control, Animal Fodder, Windbreaker, Border Plant

### Lotus
File: `src/seeds/plants/lotus-data.yml`
Scientific: *Nelumbo nucifera*
Zone: 4-11 | Layer: Aquatic
Functions: Edible, Ornamental, Water Purifier, Wildlife Attractor

### Lovage
File: `src/seeds/plants/lovage-data.yml`
Scientific: *Levisticum officinale*
Zone: 4-9 | Layer: Herbaceous
Functions: Edible, Medicinal, Pollinator, Wildlife Attractor, Border Plant, Dynamic Accumulator

### Luffa
File: `src/seeds/plants/luffa-data.yml`
Scientific: *Luffa aegyptiaca*
Zone: 3-11 | Layer: Vine
Functions: Edible, Fiber, Ornamental

### Lupine
File: `src/seeds/plants/lupine-data.yml`
Scientific: *Lupinus spp.*
Zone: 3-8 | Layer: Sub-Canopy, Shrub, Ground Cover
Functions: Edible, Nitrogen Fixer, Pollinator, Wildlife Attractor, Erosion Control, Ornamental

### Lychee
File: `src/seeds/plants/lychee-data.yml`
Scientific: *Litchi chinensis*
Zone: 10-11 | Layer: Tree
Functions: Edible, Ornamental, Wildlife Attractor

### Madagascar Vanilla
File: `src/seeds/plants/madagascar-vanilla-data.yml`
Scientific: *Vanilla planifolia*
Zone: 10-11 | Layer: Vine
Functions: Edible, Medicinal, Pollinator

### Maidenhair Fern
File: `src/seeds/plants/maidenhair-fern-data.yml`
Scientific: *Adiantum capillus-veneris*
Zone: 6-11 | Layer: Herbaceous, Ground Cover
Functions: Ornamental, Erosion Control, Wildlife Attractor

### Maitake Host
File: `src/seeds/plants/maitake-host-data.yml`
Scientific: *Grifola frondosa*
Zone: 4-9 | Layer: Tree
Functions: Edible, Medicinal, Mulcher


---

## When Done

```bash
python3 validate.py --since 2h
./sync.sh --check
./sync.sh
rm review/practitioner_notes_18_of_34.md
```

Then open `practitioner_notes_19_of_34.md`
