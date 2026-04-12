# Practitioner Notes — Batch 34 of 34

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

## Plants (10 total in this batch)

### Yam Bean
File: `src/seeds/plants/yam-bean-data.yml`
Scientific: *Pachyrhizus erosus*
Zone: 9-11 | Layer: Vine, Root
Functions: Edible, Nitrogen Fixer, Ground Cover

### Yam Daisy
File: `src/seeds/plants/yam-daisy-data.yml`
Scientific: *Microseris walteri*
Zone: 8-11 | Layer: Herb, Root
Functions: Edible, Ground Cover, Pollinator, Ornamental

### Yarrow
File: `src/seeds/plants/yarrow-data.yml`
Scientific: *Achillea millefolium*
Zone: 3-9 | Layer: Herbaceous
Functions: Medicinal, Pollinator, Wildlife Attractor, Mulcher, Dynamic Accumulator, Erosion Control, Border Plant, Water Purifier

### Yaupon Holly
File: `src/seeds/plants/yaupon-holly-data.yml`
Scientific: *Ilex vomitoria*
Zone: 7-10 | Layer: Shrub, Tree
Functions: Edible, Wildlife Attractor, Windbreaker, Erosion Control

### Yellow Dock
File: `src/seeds/plants/yellow-dock-data.yml`
Scientific: *Rumex crispus*
Zone: 4-9 | Layer: Herbaceous
Functions: Edible, Medicinal, Dynamic Accumulator, Wildlife Attractor

### Yellow Sweet Clover
File: `src/seeds/plants/yellow-sweet-clover-data.yml`
Scientific: *Melilotus officinalis*
Zone: 3-9 | Layer: Herb, Ground Cover
Functions: Nitrogen Fixer, Biomass, Wildlife Attractor, Animal Fodder

### Yellow Yam
File: `src/seeds/plants/yellow-yam-data.yml`
Scientific: *Dioscorea cayenensis*
Zone: 10-11 | Layer: Vine, Root
Functions: Edible, Ground Cover, Mulcher

### Yellowhorn Tree
File: `src/seeds/plants/yellowhorn-tree-data.yml`
Scientific: *Xanthoceras sorbifolium*
Zone: 4-8 | Layer: Tree
Functions: Edible, Ornamental, Wildlife Attractor, Windbreaker

### Yerba Santa
File: `src/seeds/plants/yerba-santa-data.yml`
Scientific: *Eriodictyon californicum*
Zone: 7-10 | Layer: Shrub
Functions: Medicinal, Wildlife Attractor, Erosion Control, Border Plant

### Yuzu
File: `src/seeds/plants/yuzu-data.yml`
Scientific: *Citrus junos*
Zone: 8-10 | Layer: Tree, Shrub
Functions: Edible, Medicinal, Ornamental


---

## When Done

```bash
python3 validate.py --since 2h
./sync.sh --check
./sync.sh
rm review/practitioner_notes_34_of_34.md
```

✅ Final batch — commit:
```bash
git add -A && git commit -m 'add practitioner_notes to all plants'
```
