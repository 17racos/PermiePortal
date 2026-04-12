# Practitioner Notes — Batch 16 of 34

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

### Ice Cream Bean Tree
File: `src/seeds/plants/ice-cream-bean-tree-data.yml`
Scientific: *Inga edulis*
Zone: 9-11 | Layer: Canopy
Functions: Edible, Nitrogen Fixer, Shade Provider, Soil Improver

### Iceberg Lettuce
File: `src/seeds/plants/iceberg-lettuce-data.yml`
Scientific: *Lactuca sativa var. capitata*
Zone: 2-11 | Layer: Ground Cover
Functions: Edible, Ground Cover, Biomass

### Ilama
File: `src/seeds/plants/ilama-data.yml`
Scientific: *Annona diversifolia*
Zone: 10-11 | Layer: Tree
Functions: Edible, Wildlife Attractor, Shade Provider

### Illawarra Plum
File: `src/seeds/plants/illawarra-plum-data.yml`
Scientific: *Podocarpus elatus*
Zone: 9-11 | Layer: Tree, Shrub
Functions: Edible, Shade Provider, Windbreaker, Wildlife Attractor

### Illinois Bundleflower
File: `src/seeds/plants/illinois-bundleflower-data.yml`
Scientific: *Desmanthus illinoensis*
Zone: 5-10 | Layer: Herb, Ground Cover
Functions: Nitrogen Fixer, Animal Fodder, Biomass, Pollinator

### Imbe
File: `src/seeds/plants/imbe-data.yml`
Scientific: *Garcinia livingstonei*
Zone: 10-11 | Layer: Shrub
Functions: Edible, Ornamental, Wildlife Attractor

### Indian Almond
File: `src/seeds/plants/indian-almond-data.yml`
Scientific: *Terminalia catappa*
Zone: 10b-12 | Layer: Tree
Functions: Edible, Shade Provider, Windbreaker, Erosion Control

### Indigofera tinctoria
File: `src/seeds/plants/indigofera-tinctoria-data.yml`
Scientific: *Indigofera tinctoria*
Zone: 9-12 | Layer: Shrub, Herb
Functions: Nitrogen Fixer, Medicinal, Biomass, Border Plant

### Italian oregano
File: `src/seeds/plants/italian-oregano-data.yml`
Scientific: *Origanum x majoricum*
Zone: 5-10 | Layer: Herbaceous
Functions: Edible, Medicinal, Pollinator, Wildlife Attractor, Border Plant -Ground Cover

### Ivy Gourd
File: `src/seeds/plants/ivy-gourd-data.yml`
Scientific: *Coccinia grandis*
Zone: 9-11 | Layer: Vine
Functions: Edible, Ground Cover, Wildlife Attractor

### Jaboticaba
File: `src/seeds/plants/jaboticaba-data.yml`
Scientific: *Plinia cauliflora*
Zone: 9-11 | Layer: Sub-Canopy, Shrub
Functions: Edible, Medicinal, Wildlife Attractor, Pollinator

### Jackfruit
File: `src/seeds/plants/jackfruit-data.yml`
Scientific: *Artocarpus heterophyllus*
Zone: 10-11 | Layer: Tree, Canopy
Functions: Edible, Animal Fodder, Windbreaker, Mulcher

### Jambolan
File: `src/seeds/plants/jambolan-data.yml`
Scientific: *Syzygium cumini*
Zone: 9-11 | Layer: Tree
Functions: Edible, Wildlife Attractor, Shade Provider

### Jamelao
File: `src/seeds/plants/jamelao-data.yml`
Scientific: *Syzygium cumini*
Zone: 9b-11 | Layer: Tree
Functions: Edible, Wildlife Attractor, Ornamental

### Jatoba
File: `src/seeds/plants/jatoba-data.yml`
Scientific: *Hymenaea courbaril*
Zone: 10b-12 | Layer: Tree, Canopy
Functions: Edible, Timber, Wildlife Attractor, Nitrogen Fixer

### Jelly Palm
File: `src/seeds/plants/jelly-palm-data.yml`
Scientific: *Butia odorata*
Zone: 8b-11 | Layer: Tree
Functions: Edible, Ornamental, Wildlife Attractor, Windbreaker

### Jerusalem Artichoke
File: `src/seeds/plants/jerusalem-artichoke-data.yml`
Scientific: *Helianthus tuberosus*
Zone: 3-9 | Layer: Herbaceous, Root
Functions: Edible, Animal Fodder, Mulcher, Wildlife Attractor, Dynamic Accumulator

### Jicama
File: `src/seeds/plants/jicama-data.yml`
Scientific: *Pachyrhizus erosus*
Zone: 9-11 | Layer: Vine, Root
Functions: Edible, Nitrogen Fixer, Ground Cover

### Joe Pye Weed
File: `src/seeds/plants/joe-pye-weed-data.yml`
Scientific: *Eutrochium purpureum*
Zone: 4-9 | Layer: Sub-Canopy
Functions: Medicinal, Pollinator, Wildlife Attractor, Border Plant

### Jojoba
File: `src/seeds/plants/jojoba-data.yml`
Scientific: *Simmondsia chinensis*
Zone: 9-11 | Layer: Shrub
Functions: Edible, Border Plant, Erosion Control, Windbreaker


---

## When Done

```bash
python3 validate.py --since 2h
./sync.sh --check
./sync.sh
rm review/practitioner_notes_16_of_34.md
```

Then open `practitioner_notes_17_of_34.md`
