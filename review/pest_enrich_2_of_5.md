# Pest Enrichment — Batch 2 of 5

> **Agent mode only.** Run sequentially, one batch at a time.

## Task

File: `src/seeds/pests/pests-data.yml`

Find each pest listed below and replace ALL `NEEDS_DATA` values with accurate information.

**Rules:**
- Organic controls ONLY — no synthetic pesticides ever
- `control_methods` keys: organic_sprays, biological_controls, cultural_practices, mechanical_physical, preventive_methods
- `natural_enemies`: real predators/parasitoids only
- `scientific_name`: accurate binomial nomenclature
- Descriptions help identify the pest in the field
- Do NOT change entries that already have real data

## Pests to Enrich

- **Greenhouse Whitefly** (slug: `greenhouse-whitefly`)
- **Banded Winged Whitefly** (slug: `banded-winged-whitefly`)
- **Spiraling Whitefly** (slug: `spiraling-whitefly`)
- **Rugose Spiraling Whitefly** (slug: `rugose-spiraling-whitefly`)
- **Corn Earworm** (slug: `corn-earworm`)
- **Tobacco Budworm** (slug: `tobacco-budworm`)
- **Beet Armyworm** (slug: `beet-armyworm`)
- **Southern Armyworm** (slug: `southern-armyworm`)
- **Velvetbean Caterpillar** (slug: `velvetbean-caterpillar`)
- **Soybean Looper** (slug: `soybean-looper`)
- **Cabbage Looper** (slug: `cabbage-looper`)
- **Diamondback Moth** (slug: `diamondback-moth`)
- **Imported Cabbageworm** (slug: `imported-cabbageworm`)
- **Cross-striped Cabbageworm** (slug: `cross-striped-cabbageworm`)
- **Spotted Cucumber Beetle** (slug: `spotted-cucumber-beetle`)
- **Striped Cucumber Beetle** (slug: `striped-cucumber-beetle`)
- **Bean Leaf Beetle** (slug: `bean-leaf-beetle`)
- **Cowpea Curculio** (slug: `cowpea-curculio`)
- **Sweet Potato Weevil** (slug: `sweet-potato-weevil`)
- **Citrus Root Weevil** (slug: `citrus-root-weevil`)
- **Diaprepes Root Weevil** (slug: `diaprepes-root-weevil`)
- **Palmetto Weevil** (slug: `palmetto-weevil`)
- **Red Palm Weevil** (slug: `red-palm-weevil`)
- **Oriental Fruit Fly** (slug: `oriental-fruit-fly`)
- **Mediterranean Fruit Fly** (slug: `mediterranean-fruit-fly`)

## When Done

```bash
./sync.sh --check
```

Then open `pest_enrich_3_of_5.md`
