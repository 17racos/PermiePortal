# Pest Enrichment — Batch 3 of 5

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

- **Serpentine Leafminer** (slug: `serpentine-leafminer`)
- **Vegetable Leafminer** (slug: `vegetable-leafminer`)
- **Shore Fly** (slug: `shore-fly`)
- **Fungus Gnat** (slug: `fungus-gnat`)
- **Citrus Red Mite** (slug: `citrus-red-mite`)
- **Texas Citrus Mite** (slug: `texas-citrus-mite`)
- **Broad Mite** (slug: `broad-mite`)
- **Cyclamen Mite** (slug: `cyclamen-mite`)
- **Rust Mite** (slug: `rust-mite`)
- **Citrus Rust Mite** (slug: `citrus-rust-mite`)
- **Citrus Greening** (slug: `citrus-greening`)
- **Fusarium Wilt** (slug: `fusarium-wilt`)
- **Pythium Root Rot** (slug: `pythium-root-rot`)
- **Phytophthora Root Rot** (slug: `phytophthora-root-rot`)
- **Sooty Mold** (slug: `sooty-mold`)
- **Anthracnose** (slug: `anthracnose`)
- **Cercospora Leaf Spot** (slug: `cercospora-leaf-spot`)
- **Alternaria Leaf Spot** (slug: `alternaria-leaf-spot`)
- **Bacterial Leaf Spot** (slug: `bacterial-leaf-spot`)
- **Reniform Nematode** (slug: `reniform-nematode`)
- **Sunflower Moth** (slug: `sunflower-moth`)
- **Walnut Husk Fly** (slug: `walnut-husk-fly`)
- **Mango Seed Weevil** (slug: `mango-seed-weevil`)
- **Grasshopper** (slug: `grasshopper`)
- **Oriental Fruit Moth** (slug: `oriental-fruit-moth`)

## When Done

```bash
./sync.sh --check
```

Then open `pest_enrich_4_of_5.md`
