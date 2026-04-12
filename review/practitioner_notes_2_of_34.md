# Practitioner Notes — Batch 2 of 34

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

### Aloe
File: `src/seeds/plants/aloe-data.yml`
Scientific: *Aloe vera*
Zone: 9-11 | Layer: Ground Cover
Functions: Medicinal, Ornamental, Ground Cover

### Alternanthera
File: `src/seeds/plants/alternanthera-data.yml`
Scientific: *Alternanthera spp.*
Zone: 10-11 | Layer: Herbaceous
Functions: Edible, Medicinal, Ground Cover, Border Plant, Wildlife Attractor

### Amaranth
File: `src/seeds/plants/amaranth-data.yml`
Scientific: *Amaranthus spp.*
Zone: 2-11 | Layer: Herbaceous
Functions: Edible, Medicinal, Dynamic Accumulator, Erosion Control, Animal Fodder, Ground Cover

### American Elderberry
File: `src/seeds/plants/american-elderberry-data.yml`
Scientific: *Sambucus canadensis*
Zone: 3-9 | Layer: Shrub
Functions: Edible, Medicinal, Wildlife Attractor, Mulcher

### American Hazelnut
File: `src/seeds/plants/american-hazelnut-data.yml`
Scientific: *Corylus americana*
Zone: 4-9 | Layer: Shrub
Functions: Edible, Wildlife Attractor, Windbreaker

### American Persimmon
File: `src/seeds/plants/american-persimmon-data.yml`
Scientific: *Diospyros virginiana*
Zone: 4-9 | Layer: Tree
Functions: Edible, Wildlife Attractor, Timber, Ornamental

### Amorphophallus
File: `src/seeds/plants/amorphophallus-data.yml`
Scientific: *Amorphophallus paeoniifolius*
Zone: 9-12 | Layer: Herbaceous
Functions: Edible, Ornamental, Mulcher

### Andrographis
File: `src/seeds/plants/andrographis-data.yml`
Scientific: *Andrographis paniculata*
Zone: 10-11 | Layer: Herbaceous
Functions: Medicinal, Pollinator, Ornamental

### Angelica
File: `src/seeds/plants/angelica-data.yml`
Scientific: *Angelica archangelica*
Zone: 4-9 | Layer: Herbaceous
Functions: Edible, Medicinal, Pollinator, Wildlife Attractor, Border Plant

### Angel's Trumpet
File: `src/seeds/plants/angels-trumpet-data.yml`
Scientific: *Brugmansia spp.*
Zone: 9-11 | Layer: Sub-Canopy
Functions: Ornamental, Medicinal, Wildlife Attractor

### Angled Loofah
File: `src/seeds/plants/angled-loofah-data.yml`
Scientific: *Luffa acutangula*
Zone: 3-11 | Layer: Vine
Functions: Edible, Fiber, Pollinator

### Anise Hyssop
File: `src/seeds/plants/anise-hyssop-data.yml`
Scientific: *Agastache foeniculum*
Zone: 4-9 | Layer: Herbaceous
Functions: Edible, Pollinator, Medicinal, Border Plant

### Apple Gourd
File: `src/seeds/plants/apple-gourd-data.yml`
Scientific: *Lagenaria siceraria*
Zone: 3-11 | Layer: Vine
Functions: Edible, Ornamental, Fiber

### Apple
File: `src/seeds/plants/apple-data.yml`
Scientific: *Malus domestica*
Zone: 3-9 | Layer: Canopy, Sub-Canopy
Functions: Edible, Medicinal, Pollinator, Wildlife Attractor, Mulcher, Dynamic Accumulator, Erosion Control, Border Plant

### Araza
File: `src/seeds/plants/araza-data.yml`
Scientific: *Eugenia stipitata*
Zone: 10-11 | Layer: Tree, Shrub
Functions: Edible, Wildlife Attractor, Ornamental

### Arracacha
File: `src/seeds/plants/arracacha-data.yml`
Scientific: *Arracacia xanthorrhiza*
Zone: 9-11 | Layer: Root, Herbaceous
Functions: Edible, Soil Improvement, Mulcher, Biomass

### Arrow Arum
File: `src/seeds/plants/arrow-arum-data.yml`
Scientific: *Peltandra virginica*
Zone: 5-11 | Layer: Aquatic, Herbaceous
Functions: Aquatic, Wildlife Attractor, Erosion Control, Ornamental

### Arrowhead
File: `src/seeds/plants/arrowhead-data.yml`
Scientific: *Sagittaria latifolia*
Zone: 5-11 | Layer: Herbaceous, Aquatic, Root
Functions: Edible, Wildlife Attractor, Water Purifier

### Arrowleaf Balsamroot
File: `src/seeds/plants/arrowleaf-balsamroot-data.yml`
Scientific: *Balsamorhiza sagittata*
Zone: 4-9 | Layer: Herbaceous
Functions: Edible, Pollinator, Wildlife Attractor, Erosion Control, Ornamental

### Arrowroot
File: `src/seeds/plants/arrowroot-data.yml`
Scientific: *Maranta arundinacea*
Zone: 10-12 | Layer: Herbaceous
Functions: Edible, Ground Cover, Mulcher


---

## When Done

```bash
python3 validate.py --since 2h
./sync.sh --check
./sync.sh
rm review/practitioner_notes_2_of_34.md
```

Then open `practitioner_notes_3_of_34.md`
