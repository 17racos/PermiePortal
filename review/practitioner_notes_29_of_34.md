# Practitioner Notes — Batch 29 of 34

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

### Sunrose
File: `src/seeds/plants/sunrose-data.yml`
Scientific: *Helianthemum nummularium*
Zone: 5-9 | Layer: Ground Cover
Functions: Ornamental, Pollinator, Ground Cover

### Sunset Muskmallow
File: `src/seeds/plants/sunset-muskmallow-data.yml`
Scientific: *Abelmoschus manihot*
Zone: 8-11 | Layer: Herbaceous, Shrub
Functions: Edible, Pollinator, Ornamental, Mulcher

### Sunshine Mimosa
File: `src/seeds/plants/sunshine-mimosa-data.yml`
Scientific: *Mimosa strigillosa*
Zone: 8-11 | Layer: Ground Cover
Functions: Ground Cover, Erosion Control, Nitrogen Fixer, Pollinator

### Suran
File: `src/seeds/plants/suran-data.yml`
Scientific: *Amorphophallus paeoniifolius*
Zone: 9-11 | Layer: Herbaceous, Root
Functions: Edible, Ornamental, Mulcher

### Surinam Cherry
File: `src/seeds/plants/surinam-cherry-data.yml`
Scientific: *Eugenia uniflora*
Zone: 9-11 | Layer: Shrub
Functions: Edible, Wildlife Attractor, Ornamental, Border Plant

### Swamp Milkweed
File: `src/seeds/plants/swamp-milkweed-data.yml`
Scientific: *Asclepias incarnata*
Zone: 3-9 | Layer: Herb
Functions: Pollinator, Wildlife Attractor, Water Retention

### Sweet Alyssum
File: `src/seeds/plants/sweet-alyssum-data.yml`
Scientific: *Lobularia maritima*
Zone: 5-11 | Layer: Ground Cover
Functions: Pollinator, Ground Cover, Pest Management

### Sweet Cassava variants
File: `src/seeds/plants/sweet-cassava-variants-data.yml`
Scientific: *Manihot esculenta*
Zone: 9-12 | Layer: Shrub
Functions: Edible, Biomass, Erosion Control

### Sweet Cicely
File: `src/seeds/plants/sweet-cicely-data.yml`
Scientific: *Myrrhis odorata*
Zone: 4-9 | Layer: Herbaceous
Functions: Edible, Medicinal, Pollinator, Wildlife Attractor, Border Plant

### Sweet Coltsfoot
File: `src/seeds/plants/sweet-coltsfoot-data.yml`
Scientific: *Petasites japonicus*
Zone: 5-9 | Layer: Herb
Functions: Edible, Ground Cover, Water Retention

### Sweet Flag
File: `src/seeds/plants/sweet-flag-data.yml`
Scientific: *Acorus calamus*
Zone: 4-11 | Layer: Aquatic
Functions: Medicinal, Water Retention, Ornamental

### Sweet Gale
File: `src/seeds/plants/sweet-gale-data.yml`
Scientific: *Myrica gale*
Zone: 2-6 | Layer: Shrub
Functions: Nitrogen Fixer, Wildlife Attractor, Border Plant

### Sweet Granadilla
File: `src/seeds/plants/sweet-granadilla-data.yml`
Scientific: *Passiflora ligularis*
Zone: 10-11 | Layer: Vine
Functions: Edible, Wildlife Attractor, Erosion Control, Shade Provider

### Sweet Leaf
File: `src/seeds/plants/sweet-leaf-data.yml`
Scientific: *Stevia rebaudiana*
Zone: 9-11 | Layer: Herbaceous
Functions: Edible, Medicinal, Border Plant

### Sweet Woodruff
File: `src/seeds/plants/sweet-woodruff-data.yml`
Scientific: *Galium odoratum*
Zone: 4-9 | Layer: Ground Cover
Functions: Edible, Ground Cover, Ornamental

### Sweet Potato
File: `src/seeds/plants/sweet-potato-data.yml`
Scientific: *Ipomoea batatas*
Zone: 8-11 | Layer: Ground Cover
Functions: Edible, Ground Cover, Animal Fodder

### Tagasaste
File: `src/seeds/plants/tagasaste-data.yml`
Scientific: *Chamaecytisus palmensis*
Zone: 8-10 | Layer: Shrub, Sub-Canopy
Functions: Nitrogen Fixer, Animal Fodder, Erosion Control, Windbreaker, Wildlife Attractor, Pollinator, Soil Improvement, Ornamental

### Tamarisk
File: `src/seeds/plants/tamarisk-data.yml`
Scientific: *Tamarix ramosissima*
Zone: 2-10 | Layer: Tree
Functions: Windbreaker, Erosion Control, Wildlife Attractor

### Tangerine
File: `src/seeds/plants/tangerine-data.yml`
Scientific: *Citrus reticulata*
Zone: 9-11 | Layer: Canopy
Functions: Edible, Pollinator, Wildlife Attractor

### Tannia
File: `src/seeds/plants/tannia-data.yml`
Scientific: *Xanthosoma sagittifolium*
Zone: 9-11 | Layer: Herbaceous, Root
Functions: Edible, Mulcher, Ornamental


---

## When Done

```bash
python3 validate.py --since 2h
./sync.sh --check
./sync.sh
rm review/practitioner_notes_29_of_34.md
```

Then open `practitioner_notes_30_of_34.md`
