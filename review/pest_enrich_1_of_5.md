# Pest Enrichment — Batch 1 of 5

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

- **Squash Vine Borer** (slug: `squash-vine-borer`)
- **Stink Bug** (slug: `stink-bug`)
- **Fungus Gnats** (slug: `fungus-gnats`)
- **Whitefly** (slug: `whitefly`)
- **Citrus Leafminer** (slug: `citrus-leafminer`)
- **Asian Citrus Psyllid** (slug: `asian-citrus-psyllid`)
- **Citrus Canker** (slug: `citrus-canker`)
- **Root Rot** (slug: `root-rot`)
- **Downy Mildew** (slug: `downy-mildew`)
- **Gray Mold** (slug: `gray-mold`)
- **Harlequin Bug** (slug: `harlequin-bug`)
- **Kudzu Bug** (slug: `kudzu-bug`)
- **Fall Armyworm** (slug: `fall-armyworm`)
- **Southern Green Stink Bug** (slug: `southern-green-stink-bug`)
- **Lubber Grasshopper** (slug: `lubber-grasshopper`)
- **Cuban Laurel Thrips** (slug: `cuban-laurel-thrips`)
- **Banded Cucumber Beetle** (slug: `banded-cucumber-beetle`)
- **Pickleworm** (slug: `pickleworm`)
- **Melonworm** (slug: `melonworm`)
- **Caribbean Fruit Fly** (slug: `caribbean-fruit-fly`)
- **Brown Citrus Aphid** (slug: `brown-citrus-aphid`)
- **Citrus Mealybug** (slug: `citrus-mealybug`)
- **Longtailed Mealybug** (slug: `longtailed-mealybug`)
- **Citrus Whitefly** (slug: `citrus-whitefly`)
- **Silverleaf Whitefly** (slug: `silverleaf-whitefly`)

## When Done

```bash
./sync.sh --check
```

Then open `pest_enrich_2_of_5.md`
