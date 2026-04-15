# PermiePortal — Cursor Agent Enrichment Task

Paste this entire prompt into Cursor Agent (not chat — Agent mode).

---

## Plants to Enrich

The following plant YAML files were manually created with minimal stub data.
For each file, replace all fields with accurate, detailed botanical information.
Use `src/seeds/plants/moringa-data.yml` as the exact structure reference.

## Requirements

- Zones and temperatures in Fahrenheit (Celsius in parentheses)
- Layers must be one of: Tree, Shrub, Herbaceous, Vine, Ground Cover, Root, Aquatic, Canopy
- plant_function values must match existing entries in other seed files
- Pest slugs must exactly match slugs in `src/seeds/pests/pests-data.yml`
- Companions must be real plants with documented beneficial relationships
- Description should be 3-5 sentences — informative but not corporate
- Focus on North Florida / Zone 9b subtropical context where relevant
- Voice: informative, practical, PermieBro tone where appropriate
- After each file is enriched, do NOT run sync — complete all files first

## Files to Enrich

- `src/seeds/plants/grapefruit-data.yml`
- `src/seeds/plants/key-lime-data.yml`
- `src/seeds/plants/persian-lime-data.yml`
- `src/seeds/plants/blood-orange-data.yml`
- `src/seeds/plants/navel-orange-data.yml`
- `src/seeds/plants/valencia-orange-data.yml`
- `src/seeds/plants/tangelo-data.yml`
- `src/seeds/plants/muscadine-grape-data.yml`
- `src/seeds/plants/stevia-data.yml`
- `src/seeds/plants/vitex-data.yml`
- `src/seeds/plants/yerba-mate-data.yml`
- `src/seeds/plants/eastern-redbud-data.yml`
- `src/seeds/plants/bottlebrush-data.yml`
- `src/seeds/plants/butterfly-cassia-data.yml`
- `src/seeds/plants/tea-olive-data.yml`
- `src/seeds/plants/opuntia-data.yml`
- `src/seeds/plants/blue-porterweed-data.yml`
- `src/seeds/plants/stokes-aster-data.yml`
- `src/seeds/plants/tilo-data.yml`

## After Enriching All Files

Run:
./sync.sh 2>&1 | grep -E "Plants:|Warnings:"

Fix any warnings about unmatched pest references or missing fields, then run:
./sync.sh
git add -A
git commit -m "Enrich 20 new nursery plants — citrus subtypes, muscadine, stevia, vitex and more"
git push origin v2

## Reference File Structure

Use `src/seeds/plants/moringa-data.yml` as the gold standard for field
completeness and voice. Cross-reference `src/seeds/plants/lemongrass-data.yml`
for a Florida-native subtropical example and `src/seeds/plants/elderberry-data.yml`
for a shrub layer example.
