# Practitioner Notes — Batch 31 of 34

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

### Tulsi
File: `src/seeds/plants/tulsi-data.yml`
Scientific: *Ocimum tenuiflorum*
Zone: 10-11 | Layer: Herbaceous
Functions: Medicinal, Edible, Pollinator, Pest Management

### Turkey Tail Host
File: `src/seeds/plants/turkey-tail-host-data.yml`
Scientific: *Trametes versicolor*
Zone: 3-11 | Layer: Tree
Functions: Medicinal, Mulcher, Soil Improvement

### Turkish Rocket
File: `src/seeds/plants/turkish-rocket-data.yml`
Scientific: *Bunias orientalis*
Zone: 4-9 | Layer: Herb, Ground Cover
Functions: Edible, Biomass, Wildlife Attractor, Border Plant, Dynamic Accumulator

### Turmeric
File: `src/seeds/plants/turmeric-data.yml`
Scientific: *Curcuma longa*
Zone: 8-11 | Layer: Herbaceous, Root
Functions: Edible, Medicinal, Mulcher, Dynamic Accumulator

### Twinflower
File: `src/seeds/plants/twinflower-data.yml`
Scientific: *Linnaea borealis*
Zone: 2-7 | Layer: Ground Cover, Herb
Functions: Ground Cover, Wildlife Attractor, Ornamental, Medicinal

### Ulluco
File: `src/seeds/plants/ulluco-data.yml`
Scientific: *Ullucus tuberosus*
Zone: 8-10 | Layer: Herbaceous, Root
Functions: Edible, Ground Cover, Dynamic Accumulator

### Uvaia
File: `src/seeds/plants/uvaia-data.yml`
Scientific: *Eugenia pyriformis*
Zone: 9b-11 | Layer: Tree, Shrub
Functions: Edible, Wildlife Attractor, Ornamental

### Valerian
File: `src/seeds/plants/valerian-data.yml`
Scientific: *Valeriana officinalis*
Zone: 4-9 | Layer: Herbaceous
Functions: Medicinal, Pollinator, Wildlife Attractor

### Venus Flytrap
File: `src/seeds/plants/venus-flytrap-data.yml`
Scientific: *Dionaea muscipula*
Zone: 5-8 | Layer: Ground Cover
Functions: Pest Management, Wildlife Attractor

### Verbena bonariensis
File: `src/seeds/plants/verbena-bonariensis-data.yml`
Scientific: *Verbena bonariensis*
Zone: 7-11 | Layer: Herb
Functions: Pollinator, Wildlife Attractor, Ornamental, Border Plant, Biomass

### Vetiver Grass
File: `src/seeds/plants/vetiver-grass-data.yml`
Scientific: *Chrysopogon zizanioides*
Zone: 8-11 | Layer: Herbaceous
Functions: Erosion Control, Mulcher, Dynamic Accumulator, Windbreaker, Animal Fodder, Pest Management, Water Purifier

### Vietnamese Coriander
File: `src/seeds/plants/vietnamese-coriander-data.yml`
Scientific: *Persicaria odorata*
Zone: 9-11 | Layer: Herbaceous, Ground Cover
Functions: Edible, Medicinal, Wildlife Attractor

### Vines
File: `src/seeds/plants/vines-data.yml`
Scientific: *Polyculture (multiple species)*
Zone: 8-11 | Layer: Vine
Functions: Shade Provider, Edible, Wildlife Attractor, Pollinator, Erosion Control

### Viper Bugloss
File: `src/seeds/plants/viper-bugloss-data.yml`
Scientific: *Echium vulgare*
Zone: 3-8 | Layer: Herbaceous
Functions: Pollinator, Wildlife Attractor, Border Plant, Animal Fodder

### Walking Onion
File: `src/seeds/plants/walking-onion-data.yml`
Scientific: *Allium × proliferum*
Zone: 3-10 | Layer: Herb, Ground Cover
Functions: Edible, Pest Management, Border Plant, Biomass

### Walnut Tree
File: `src/seeds/plants/walnut-tree-data.yml`
Scientific: *Juglans regia*
Zone: 4-9 | Layer: Canopy
Functions: Edible, Medicinal, Wildlife Attractor, Timber

### Walter Viburnum
File: `src/seeds/plants/walter-viburnum-data.yml`
Scientific: *Viburnum obovatum*
Zone: 8-10 | Layer: Shrub
Functions: Wildlife Attractor, Border Plant, Erosion Control, Ornamental

### Walter's Viburnum
File: `src/seeds/plants/walters-viburnum-data.yml`
Scientific: *Viburnum obovatum*
Zone: 7-10 | Layer: Shrub
Functions: Edible, Wildlife Attractor, Ornamental, Erosion Control

### Warrigal Greens
File: `src/seeds/plants/warrigal-greens-data.yml`
Scientific: *Tetragonia tetragonoides*
Zone: 9-11 | Layer: Herbaceous, Ground Cover
Functions: Edible, Ground Cover, Drought Tolerant

### Water Aquatic
File: `src/seeds/plants/water-aquatic-data.yml`
Scientific: *Polyculture (multiple species)*
Zone: 8-11 | Layer: Aquatic
Functions: Water Purifier, Edible, Wildlife Attractor, Aquatic


---

## When Done

```bash
python3 validate.py --since 2h
./sync.sh --check
./sync.sh
rm review/practitioner_notes_31_of_34.md
```

Then open `practitioner_notes_32_of_34.md`
