# Pest Enrichment — Batch 4 of 5

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

- **Leaf Curl** (slug: `leaf-curl`)
- **Brown Rot** (slug: `brown-rot`)
- **Andean Potato Weevil** (slug: `andean-potato-weevil`)
- **Ulluco Weevil** (slug: `ulluco-weevil`)
- **Onion Fly** (slug: `onion-fly`)
- **Gall Mite** (slug: `gall-mite`)
- **Palm Weevil** (slug: `palm-weevil`)
- **Ganoderma Butt Rot** (slug: `ganoderma-butt-rot`)
- **Papaya Ringspot Virus** (slug: `papaya-ringspot-virus`)
- **Pea Weevil** (slug: `pea-weevil`)
- **Pecan Weevil** (slug: `pecan-weevil`)
- **Hickory Shuckworm** (slug: `hickory-shuckworm`)
- **Pecan Scab** (slug: `pecan-scab`)
- **Persimmon Borer** (slug: `persimmon-borer`)
- **Colorado Potato Beetle** (slug: `colorado-potato-beetle`)
- **Potato Scab** (slug: `potato-scab`)
- **Late Blight** (slug: `late-blight`)
- **Rhubarb Curculio** (slug: `rhubarb-curculio`)
- **Rice Water Weevil** (slug: `rice-water-weevil`)
- **Rice Blast Fungus** (slug: `rice-blast-fungus`)
- **Cranberry Fruitworm** (slug: `cranberry-fruitworm`)
- **Cranberry Tipworm** (slug: `cranberry-tipworm`)
- **Sparganothis Fruitworm** (slug: `sparganothis-fruitworm`)
- **Bean Weevil** (slug: `bean-weevil`)
- **Swallowtail Caterpillar** (slug: `swallowtail-caterpillar`)

## When Done

```bash
./sync.sh --check
```

Then open `pest_enrich_5_of_5.md`
