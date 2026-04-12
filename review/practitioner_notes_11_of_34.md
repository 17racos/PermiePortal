# Practitioner Notes — Batch 11 of 34

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

### Cuban Oregano
File: `src/seeds/plants/cuban-oregano-data.yml`
Scientific: *Coleus amboinicus*
Zone: 8-11 | Layer: Herbaceous
Functions: Edible, Medicinal, Pollinator, Ground Cover

### Cucamelon
File: `src/seeds/plants/cucamelon-data.yml`
Scientific: *Melothria scabra*
Zone: 7-11 | Layer: Herbaceous, Vine
Functions: Edible, Wildlife Attractor, Ground Cover

### Culantro
File: `src/seeds/plants/culantro-data.yml`
Scientific: *Eryngium foetidum*
Zone: 9-12 | Layer: Herbaceous
Functions: Edible, Medicinal, Pest Management

### Cupuacu
File: `src/seeds/plants/cupuacu-data.yml`
Scientific: *Theobroma grandiflorum*
Zone: 11-12 | Layer: Tree
Functions: Edible, Wildlife Attractor, Shade Provider

### Custard Apple
File: `src/seeds/plants/custard-apple-data.yml`
Scientific: *Annona reticulata*
Zone: 10-11 | Layer: Tree
Functions: Edible, Wildlife Attractor, Mulcher, Shade Provider

### Dahoon Holly
File: `src/seeds/plants/dahoon-holly-data.yml`
Scientific: *Ilex cassine*
Zone: 7-11 | Layer: Tree, Shrub
Functions: Wildlife Attractor, Ornamental, Windbreaker

### Daikon Radish
File: `src/seeds/plants/daikon-radish-data.yml`
Scientific: *Raphanus sativus var. longipinnatus*
Zone: 2-11 | Layer: Root
Functions: Edible, Medicinal, Dynamic Accumulator, Erosion Control, Animal Fodder, Pest Management

### Damiana
File: `src/seeds/plants/damiana-data.yml`
Scientific: *Turnera diffusa*
Zone: 9-11 | Layer: Shrub, Herbaceous
Functions: Medicinal, Pollinator, Drought Tolerant, Wildlife Attractor

### Dandelion
File: `src/seeds/plants/dandelion-data.yml`
Scientific: *Taraxacum officinale*
Zone: 3-10 | Layer: Herbaceous
Functions: Edible, Medicinal, Dynamic Accumulator, Pollinator, Ground Cover

### Darrow Blueberry
File: `src/seeds/plants/darrow-blueberry-data.yml`
Scientific: *Vaccinium corymbosum 'Darrow'*
Zone: 7-9 | Layer: Shrub
Functions: Edible, Pollinator, Wildlife Attractor, Ornamental

### Dasheen
File: `src/seeds/plants/dasheen-data.yml`
Scientific: *Colocasia esculenta*
Zone: 8-11 | Layer: Herbaceous, Root, Aquatic
Functions: Edible, Aquatic, Erosion Control, Mulcher

### Desert Date
File: `src/seeds/plants/desert-date-data.yml`
Scientific: *Balanites aegyptiaca*
Zone: 10-12 | Layer: Tree
Functions: Edible, Animal Fodder, Erosion Control, Windbreaker

### Desert Hackberry
File: `src/seeds/plants/desert-hackberry-data.yml`
Scientific: *Celtis pallida*
Zone: 7-11 | Layer: Shrub
Functions: Edible, Wildlife Attractor, Erosion Control, Border Plant, Shade Provider

### Desert Ironwood
File: `src/seeds/plants/desert-ironwood-data.yml`
Scientific: *Olneya tesota*
Zone: 9-11 | Layer: Tree
Functions: Nitrogen Fixer, Wildlife Attractor, Shade Provider, Windbreaker, Erosion Control, Mulcher

### Desert Marigold
File: `src/seeds/plants/desert-marigold-data.yml`
Scientific: *Baileya multiradiata*
Zone: 7-11 | Layer: Herbaceous
Functions: Ornamental, Pollinator, Ground Cover, Erosion Control, Wildlife Attractor

### Desert Sage
File: `src/seeds/plants/desert-sage-data.yml`
Scientific: *Salvia dorrii*
Zone: 5-9 | Layer: Shrub
Functions: Pollinator, Wildlife Attractor, Border Plant, Medicinal

### Desert Willow
File: `src/seeds/plants/desert-willow-data.yml`
Scientific: *Chilopsis linearis*
Zone: 7-11 | Layer: Tree
Functions: Ornamental, Pollinator, Wildlife Attractor, Shade Provider, Erosion Control, Border Plant

### Desert Yam
File: `src/seeds/plants/desert-yam-data.yml`
Scientific: *Ipomoea costata*
Zone: 10-12 | Layer: Vine
Functions: Edible, Ground Cover, Erosion Control, Ornamental

### Devil's Trumpet
File: `src/seeds/plants/devils-trumpet-data.yml`
Scientific: *Datura metel*
Zone: 9-11 | Layer: Shrub
Functions: Ornamental, Medicinal, Pest Management

### Dichondra
File: `src/seeds/plants/dichondra-data.yml`
Scientific: *Dichondra repens*
Zone: 8-11 | Layer: Ground Cover
Functions: Ground Cover, Ornamental, Erosion Control, Drought Tolerant


---

## When Done

```bash
python3 validate.py --since 2h
./sync.sh --check
./sync.sh
rm review/practitioner_notes_11_of_34.md
```

Then open `practitioner_notes_12_of_34.md`
