# PermiePortal — Relationship Backfill

> **Agent mode only.** This is a data quality task.

---

## Context

The database has two relationship gaps to fix:

1. **Pests with no affected plants** — these pests exist but no plant files reference them
2. **Plants with no pest links** — these plants have empty pest lists

Both are fixed by editing plant YAML files in `src/seeds/plants/`.

**Rules:**
- Only add relationships that are botanically accurate
- Pest names must exactly match names in `src/seeds/pests/pests-data.yml`
- Add pests to the `pests:` list in plant YAML files
- Do NOT create new files — only edit existing plant YAML files
- After all edits run: `./sync.sh --check`

---

## Part 1 — Pests Needing Plant Connections

For each pest below, find the plant YAML files in `src/seeds/plants/` that should be affected by this pest and add it to their `pests:` list.

- **Alternaria Leaf Spot** (`alternaria-leaf-spot`)
- **Bacterial Leaf Spot** (`bacterial-leaf-spot`)
- **Banded Winged Whitefly** (`banded-winged-whitefly`)
- **Beet Armyworm** (`beet-armyworm`)
- **Broad Mite** (`broad-mite`)
- **Brown Citrus Aphid** (`brown-citrus-aphid`)
- **Cabbage Root Fly** (`cabbage-root-fly`)
- **Cabbage White Butterflies** (`cabbage-white-butterflies`)
- **Carrot Weevil** (`carrot-weevil`)
- **Cercospora Leaf Spot** (`cercospora-leaf-spot`)
- **Citrus Root Weevil** (`citrus-root-weevil`)
- **Citrus Rust Mite** (`citrus-rust-mite`)
- **Citrus Whitefly** (`citrus-whitefly`)
- **Cross-striped Cabbageworm** (`cross-striped-cabbageworm`)
- **Cuban Laurel Thrips** (`cuban-laurel-thrips`)
- **Cyclamen Mite** (`cyclamen-mite`)
- **Cytospora Canker** (`cytospora-canker`)
- **Diamondback Moth** (`diamondback-moth`)
- **Diaprepes Root Weevil** (`diaprepes-root-weevil`)
- **Fungus Gnats** (`fungus-gnats`)
- **Gray Mold** (`gray-mold`)
- **Greenhouse Whitefly** (`greenhouse-whitefly`)
- **Harlequin Bug** (`harlequin-bug`)
- **Imported Cabbageworm** (`imported-cabbageworm`)
- **Kudzu Bug** (`kudzu-bug`)
- **Leek Moth** (`leek-moth`)
- **Longtailed Mealybug** (`longtailed-mealybug`)
- **Lubber Grasshopper** (`lubber-grasshopper`)
- **Phytophthora Root Rot** (`phytophthora-root-rot`)
- **Pythium Root Rot** (`pythium-root-rot`)
- **Raspberry Beetle** (`raspberry-beetle`)
- **Rugose Spiraling Whitefly** (`rugose-spiraling-whitefly`)
- **Rust Mite** (`rust-mite`)
- **Serpentine Leafminer** (`serpentine-leafminer`)
- **Shore Fly** (`shore-fly`)
- **Silverleaf Whitefly** (`silverleaf-whitefly`)
- **Sooty Mold** (`sooty-mold`)
- **Southern Armyworm** (`southern-armyworm`)
- **Southern Green Stink Bug** (`southern-green-stink-bug`)
- **Soybean Looper** (`soybean-looper`)
- **Spiraling Whitefly** (`spiraling-whitefly`)
- **Swede Midge** (`swede-midge`)
- **Texas Citrus Mite** (`texas-citrus-mite`)
- **Tobacco Budworm** (`tobacco-budworm`)
- **Tomato Hornworms** (`tomato-hornworms`)
- **Twig Girdlers** (`twig-girdlers`)
- **Velvetbean Caterpillar** (`velvetbean-caterpillar`)
- **Whitefly** (`whitefly`)

---

## Part 2 — Plants Needing Pest Links

For each plant below, open its YAML file and add appropriate pests from `src/seeds/pests/pests-data.yml` to its `pests:` list.

- **Beautyberry** → `src/seeds/plants/beautyberry-data.yml`
- **Bee Bush** → `src/seeds/plants/bee-bush-data.yml`
- **Bladderwort** → `src/seeds/plants/bladderwort-data.yml`
- **Chia** → `src/seeds/plants/chia-data.yml`
- **Coral Bean** → `src/seeds/plants/coral-bean-data.yml`
- **Dandelion** → `src/seeds/plants/dandelion-data.yml`
- **Duckweed** → `src/seeds/plants/duckweed-data.yml`
- **Fish Mint** → `src/seeds/plants/fish-mint-data.yml`
- **Katuk** → `src/seeds/plants/katuk-data.yml`
- **Muhly Grass** → `src/seeds/plants/muhly-grass-data.yml`
- **Perennial Peanut** → `src/seeds/plants/perennial-peanut-data.yml`
- **Rattlebox** → `src/seeds/plants/rattlebox-data.yml`
- **Saw Palmetto** → `src/seeds/plants/saw-palmetto-data.yml`
- **Sea Buckthorn** → `src/seeds/plants/sea-buckthorn-data.yml`
- **Siberian Pea Shrub** → `src/seeds/plants/siberian-pea-shrub-data.yml`
- **Singapore Daisy** → `src/seeds/plants/singapore-daisy-data.yml`
- **Vetiver Grass** → `src/seeds/plants/vetiver-grass-data.yml`

---

## When Done

```bash
./sync.sh --check
```
Fix any warnings, then:
```bash
./sync.sh
```
Report: plants with no pests, pests with no affected plants.
