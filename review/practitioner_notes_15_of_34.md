# Practitioner Notes — Batch 15 of 34

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

### Guanabana
File: `src/seeds/plants/guanabana-data.yml`
Scientific: *Annona muricata*
Zone: 10-11 | Layer: Tree
Functions: Edible, Medicinal, Wildlife Attractor

### Guava
File: `src/seeds/plants/guava-data.yml`
Scientific: *Psidium guajava*
Zone: 9-11 | Layer: Tree, Shrub
Functions: Edible, Wildlife Attractor, Windbreaker, Mulcher

### Guayule
File: `src/seeds/plants/guayule-data.yml`
Scientific: *Parthenium argentatum*
Zone: 8-11 | Layer: Shrub, Herb
Functions: Fiber, Biomass, Erosion Control, Border Plant

### Guinea Yam
File: `src/seeds/plants/guinea-yam-data.yml`
Scientific: *Dioscorea rotundata*
Zone: 10-12 | Layer: Vine, Root
Functions: Edible, Mulcher, Biomass

### Gynura
File: `src/seeds/plants/gynura-data.yml`
Scientific: *Gynura procumbens*
Zone: 9-11 | Layer: Herbaceous, Ground Cover
Functions: Edible, Medicinal, Mulcher

### Hairy Indigo
File: `src/seeds/plants/hairy-indigo-data.yml`
Scientific: *Indigofera hirsuta*
Zone: 5-11 | Layer: Herbaceous, Ground Cover
Functions: Nitrogen Fixer, Green Manure, Animal Fodder, Cover Crop, Wildlife Attractor

### Hemp
File: `src/seeds/plants/hemp-data.yml`
Scientific: *Cannabis sativa*
Zone: 3-11 | Layer: Herbaceous
Functions: Fiber, Edible, Cover Crop, Dynamic Accumulator

### Henequen
File: `src/seeds/plants/henequen-data.yml`
Scientific: *Agave fourcroydes*
Zone: 9-11 | Layer: Herbaceous
Functions: Mulcher, Erosion Control, Animal Fodder

### Highbush Blueberry
File: `src/seeds/plants/highbush-blueberry-data.yml`
Scientific: *Vaccinium corymbosum*
Zone: 3-10 | Layer: Shrub
Functions: Edible, Pollinator, Wildlife Attractor, Ornamental

### Hoary Plantain
File: `src/seeds/plants/hoary-plantain-data.yml`
Scientific: *Plantago media*
Zone: 3-9 | Layer: Herbaceous, Ground Cover
Functions: Edible, Medicinal, Wildlife Attractor, Ground Cover

### Holy Basil
File: `src/seeds/plants/holy-basil-data.yml`
Scientific: *Ocimum tenuiflorum*
Zone: 9-12 | Layer: Herbaceous
Functions: Edible, Medicinal, Pollinator, Wildlife Attractor, Dynamic Accumulator, Border Plant, Pest Management

### Honey Locust
File: `src/seeds/plants/honey-locust-data.yml`
Scientific: *Gleditsia triacanthos*
Zone: 4-9 | Layer: Canopy, Tree
Functions: Nitrogen Fixer, Animal Fodder, Wildlife Attractor, Timber, Shade Provider

### Honey Melon Sage
File: `src/seeds/plants/honey-melon-sage-data.yml`
Scientific: *Salvia elegans*
Zone: 8-11 | Layer: Herbaceous
Functions: Edible, Pollinator, Ornamental, Wildlife Attractor

### Hop Shoots
File: `src/seeds/plants/hop-shoots-data.yml`
Scientific: *Humulus lupulus*
Zone: 5-9 | Layer: Vine, Herb
Functions: Edible, Pollinator, Windbreaker, Ornamental

### Hopniss
File: `src/seeds/plants/hopniss-data.yml`
Scientific: *Apios americana*
Zone: 3-9 | Layer: Vine, Root
Functions: Edible, Nitrogen Fixer, Wildlife Attractor

### Horehound
File: `src/seeds/plants/horehound-data.yml`
Scientific: *Marrubium vulgare*
Zone: 4-9 | Layer: Herb, Ground Cover
Functions: Medicinal, Pollinator, Pest Management, Animal Fodder

### Huacatay
File: `src/seeds/plants/huacatay-data.yml`
Scientific: *Tagetes minuta*
Zone: 9-11 | Layer: Herbaceous
Functions: Edible, Pest Management, Soil Improvement, Border Plant

### Hyacinth Bean
File: `src/seeds/plants/hyacinth-bean-data.yml`
Scientific: *Lablab purpureus*
Zone: 9-11 | Layer: Vine
Functions: Edible, Nitrogen Fixer, Animal Fodder, Ornamental, Pollinator

### Hyssop officinalis
File: `src/seeds/plants/hyssop-officinalis-data.yml`
Scientific: *Hyssopus officinalis*
Zone: 4-9 | Layer: Herb, Shrub
Functions: Edible, Medicinal, Pollinator, Ornamental

### Ice plant
File: `src/seeds/plants/ice-plant-data.yml`
Scientific: *Delosperma cooperi*
Zone: 5-11 | Layer: Ground Cover
Functions: Edible, Medicinal, Ground Cover, Erosion Control, Border Plant


---

## When Done

```bash
python3 validate.py --since 2h
./sync.sh --check
./sync.sh
rm review/practitioner_notes_15_of_34.md
```

Then open `practitioner_notes_16_of_34.md`
