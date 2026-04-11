# Pest Enrichment — Batch 5 of 5

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

- **Fig Beetle** (slug: `fig-beetle`)
- **Gooseberry Sawfly** (slug: `gooseberry-sawfly`)
- **Azalea Caterpillar** (slug: `azalea-caterpillar`)
- **Bamboo Mite** (slug: `bamboo-mite`)
- **Banana Weevil** (slug: `banana-weevil`)
- **Locust Borer** (slug: `locust-borer`)
- **Locust Leaf Miner** (slug: `locust-leaf-miner`)
- **Leaf Spot** (slug: `leaf-spot`)
- **Heart Rot** (slug: `heart-rot`)
- **Cocoa Pod Borer** (slug: `cocoa-pod-borer`)
- **Carrot Fly** (slug: `carrot-fly`)
- **Wireworm** (slug: `wireworm`)
- **Cassava Mealybug** (slug: `cassava-mealybug`)
- **Cassava Green Mite** (slug: `cassava-green-mite`)
- **Pea Moth** (slug: `pea-moth`)
- **Onion Maggot** (slug: `onion-maggot`)
- **Coconut Mite** (slug: `coconut-mite`)
- **Rhinoceros Beetle** (slug: `rhinoceros-beetle`)

## When Done

```bash
./sync.sh --check
```

✅ All pests enriched! Run `./sync.sh` to rebuild.
