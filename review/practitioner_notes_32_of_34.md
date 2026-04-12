# Practitioner Notes — Batch 32 of 34

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

### Water Chestnut
File: `src/seeds/plants/water-chestnut-data.yml`
Scientific: *Eleocharis dulcis*
Zone: 8-11 | Layer: Aquatic
Functions: Edible, Water Purifier, Wildlife Attractor

### Water Hyacinth
File: `src/seeds/plants/water-hyacinth-data.yml`
Scientific: *Eichhornia crassipes*
Zone: 9-12 | Layer: Aquatic
Functions: Water Purifier, Animal Fodder, Mulcher, Green Manure

### Water Lettuce
File: `src/seeds/plants/water-lettuce-data.yml`
Scientific: *Pistia stratiotes*
Zone: 9-11 | Layer: Aquatic
Functions: Water Purifier, Animal Fodder

### Water Plantain
File: `src/seeds/plants/water-plantain-data.yml`
Scientific: *Alisma subcordatum*
Zone: 4-11 | Layer: Aquatic, Herbaceous
Functions: Edible, Wildlife Attractor, Erosion Control, Border Plant

### Water Spinach
File: `src/seeds/plants/water-spinach-data.yml`
Scientific: *Ipomoea aquatica*
Zone: 9-12 | Layer: Vine, Aquatic
Functions: Edible, Ground Cover, Water Purifier, Green Manure

### Water Yam
File: `src/seeds/plants/water-yam-data.yml`
Scientific: *Dioscorea alata*
Zone: 8-11 | Layer: Vine, Root
Functions: Edible, Ground Cover, Mulcher

### Watercress
File: `src/seeds/plants/watercress-data.yml`
Scientific: *Nasturtium officinale*
Zone: 6-9 | Layer: Herbaceous, Aquatic
Functions: Edible, Medicinal, Water Purifier, Ground Cover

### Watershield
File: `src/seeds/plants/watershield-data.yml`
Scientific: *Brasenia schreberi*
Zone: 4-11 | Layer: Aquatic
Functions: Edible, Wildlife Attractor, Border Plant

### Wax Gourd
File: `src/seeds/plants/wax-gourd-data.yml`
Scientific: *Benincasa hispida*
Zone: 3-11 | Layer: Vine, Ground Cover
Functions: Edible, Ground Cover, Pollinator

### Wax Jambu
File: `src/seeds/plants/wax-jambu-data.yml`
Scientific: *Syzygium samarangense*
Zone: 10-12 | Layer: Tree
Functions: Edible, Ornamental, Wildlife Attractor, Shade Provider

### Wax Myrtle
File: `src/seeds/plants/wax-myrtle-data.yml`
Scientific: *Morella cerifera*
Zone: 7-11 | Layer: Shrub, Tree
Functions: Nitrogen Fixer, Wildlife Attractor, Windbreaker, Erosion Control, Border Plant

### White Sage
File: `src/seeds/plants/white-sage-data.yml`
Scientific: *Salvia apiana*
Zone: 8-11 | Layer: Shrub
Functions: Medicinal, Pollinator, Drought Tolerant, Wildlife Attractor

### White Sapote
File: `src/seeds/plants/white-sapote-data.yml`
Scientific: *Casimiroa edulis*
Zone: 9-11 | Layer: Tree
Functions: Edible, Shade Provider, Wildlife Attractor

### White Yam
File: `src/seeds/plants/white-yam-data.yml`
Scientific: *Dioscorea rotundata*
Zone: 10-11 | Layer: Vine, Root
Functions: Edible, Ground Cover, Mulcher, Animal Fodder

### Wild Anise
File: `src/seeds/plants/wild-anise-data.yml`
Scientific: *Osmorhiza longistylis*
Zone: 4-9 | Layer: Herbaceous
Functions: Edible, Medicinal, Pollinator, Wildlife Attractor

### Wild Caraway
File: `src/seeds/plants/wild-caraway-data.yml`
Scientific: *Carum carvi*
Zone: 3-9 | Layer: Herbaceous
Functions: Edible, Medicinal, Pollinator, Border Plant

### Wild Carrot
File: `src/seeds/plants/wild-carrot-data.yml`
Scientific: *Daucus carota*
Zone: 3-11 | Layer: Herbaceous
Functions: Edible, Medicinal, Pollinator, Wildlife Attractor, Border Plant, Dynamic Accumulator

### Wild Celery
File: `src/seeds/plants/wild-celery-data.yml`
Scientific: *Apium graveolens*
Zone: 4-11 | Layer: Herbaceous
Functions: Edible, Wildlife Attractor, Border Plant, Dynamic Accumulator

### Wild Chervil
File: `src/seeds/plants/wild-chervil-data.yml`
Scientific: *Anthriscus sylvestris*
Zone: 4-9 | Layer: Herbaceous
Functions: Edible, Pollinator, Wildlife Attractor, Border Plant

### Wild Coffee
File: `src/seeds/plants/wild-coffee-data.yml`
Scientific: *Psychotria nervosa*
Zone: 9b-11 | Layer: Shrub
Functions: Wildlife Attractor, Shade Provider, Ornamental, Ground Cover


---

## When Done

```bash
python3 validate.py --since 2h
./sync.sh --check
./sync.sh
rm review/practitioner_notes_32_of_34.md
```

Then open `practitioner_notes_33_of_34.md`
