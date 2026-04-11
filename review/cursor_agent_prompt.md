# PermiePortal — Cursor Agent Enrichment Task
Paste this entire prompt into Cursor Agent (not chat — Agent mode).
---
## Plants to Enrich
The following plant YAML files have been created with stub data. For each file, replace every `NEEDS_DATA` field with accurate botanical information. Use `src/seeds/plants/moringa-data.yml` as the exact structure reference. Requirements:
- Zones and temperatures in Fahrenheit
- Layers must be one of: Tree, Shrub, Herbaceous, Vine, Ground Cover, Root, Aquatic, Canopy
- plant_function values must match existing entries in other seed files
- Pests must exactly match slugs in src/seeds/pests/pests-data.yml
- Description should include propagation methods and sun/water requirements
- Focus on North Florida / subtropical context where relevant
- Voice: informative but not corporate. PermieBro tone where appropriate.

- `src/seeds/plants/wild-dill-data.yml`
- `src/seeds/plants/wild-chervil-data.yml`
- `src/seeds/plants/wild-coriander-data.yml`
- `src/seeds/plants/wild-cumin-data.yml`
- `src/seeds/plants/wild-anise-data.yml`
- `src/seeds/plants/wild-caraway-data.yml`
- `src/seeds/plants/wild-tarragon-data.yml`
- `src/seeds/plants/mushroom-hosts-data.yml`
- `src/seeds/plants/wine-cap-substrate-data.yml`
- `src/seeds/plants/oyster-mushroom-host-data.yml`
- `src/seeds/plants/shiitake-oak-data.yml`
- `src/seeds/plants/maitake-host-data.yml`
- `src/seeds/plants/chicken-of-the-woods-host-data.yml`
- `src/seeds/plants/lions-mane-host-data.yml`
- `src/seeds/plants/turkey-tail-host-data.yml`
- `src/seeds/plants/reishi-host-data.yml`
- `src/seeds/plants/chaga-host-data.yml`
- `src/seeds/plants/cordyceps-host-data.yml`

## After Enriching
When all entries are filled in, run:
```
./sync.sh --check
```
Fix any warnings about unmatched pest references, then run:
```
./sync.sh
```
Report the final summary (plants, pests, relationships count).
