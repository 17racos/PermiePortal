# PermiePortal — Description Quality Pass Batch 3 of 3

## YOUR TASK
You are Cursor Agent in Agent mode. Each plant YAML listed below has a description
missing one or more required sections. Add the missing sections to the existing
description — do NOT rewrite the whole description, just append the missing parts.

## Required Description Sections (all 4 must be present)
1. What the plant is, origin, appearance, mature size
2. ☀️💧 Sun and Water Requirements
3. ✂️ Propagation (2+ methods with timing)
4. 🌾 Harvest / Best Use Timing

## Rules
- Use `src/seeds/plants/moringa-data.yml` as the gold standard
- Geographic context: Americas-wide, temperate/subtropical/tropical
- Temperatures in Fahrenheit with Celsius in parentheses
- Use ' -- ' not em dashes (—)
- Only add missing sections — do not change existing content
- Do NOT change any fields other than `description`

## Files to Fix

- `src/seeds/plants/roselle-data.yml` (missing: harvest)
- `src/seeds/plants/rumberry-data.yml` (missing: harvest)
- `src/seeds/plants/scorpion-weed-data.yml` (missing: harvest)
- `src/seeds/plants/sea-plantain-data.yml` (missing: harvest)
- `src/seeds/plants/shiitake-data.yml` (missing: harvest)
- `src/seeds/plants/shiny-blueberry-data.yml` (missing: harvest)
- `src/seeds/plants/shiso-data.yml` (missing: harvest)
- `src/seeds/plants/skullcap-data.yml` (missing: harvest)
- `src/seeds/plants/sour-orange-data.yml` (missing: harvest)
- `src/seeds/plants/soursop-data.yml` (missing: harvest)
- `src/seeds/plants/southern-magnolia-data.yml` (missing: harvest)
- `src/seeds/plants/sparkleberry-data.yml` (missing: harvest)
- `src/seeds/plants/spatterdock-data.yml` (missing: harvest)
- `src/seeds/plants/stinging-tree-data.yml` (missing: harvest)
- `src/seeds/plants/sugar-apple-data.yml` (missing: harvest)
- `src/seeds/plants/sweet-cicely-data.yml` (missing: harvest)
- `src/seeds/plants/tannia-data.yml` (missing: harvest)
- `src/seeds/plants/tree-spinach-data.yml` (missing: harvest)
- `src/seeds/plants/turkey-tail-data.yml` (missing: harvest)
- `src/seeds/plants/ulluco-data.yml` (missing: harvest)
- `src/seeds/plants/uvaia-data.yml` (missing: harvest)
- `src/seeds/plants/vietnamese-coriander-data.yml` (missing: harvest)
- `src/seeds/plants/vines-data.yml` (missing: harvest)
- `src/seeds/plants/viper-bugloss-data.yml` (missing: harvest)
- `src/seeds/plants/water-aquatic-data.yml` (missing: harvest)
- `src/seeds/plants/water-lettuce-data.yml` (missing: harvest)
- `src/seeds/plants/water-plantain-data.yml` (missing: harvest)
- `src/seeds/plants/watershield-data.yml` (missing: harvest)
- `src/seeds/plants/wild-anise-data.yml` (missing: harvest)
- `src/seeds/plants/wild-caraway-data.yml` (missing: harvest)
- `src/seeds/plants/wild-carrot-data.yml` (missing: harvest)
- `src/seeds/plants/wild-chervil-data.yml` (missing: harvest)
- `src/seeds/plants/wild-coffee-data.yml` (missing: harvest)
- `src/seeds/plants/wild-cumin-data.yml` (missing: harvest)
- `src/seeds/plants/wild-ginger-data.yml` (missing: harvest)
- `src/seeds/plants/wild-indigo-data.yml` (missing: harvest)
- `src/seeds/plants/wine-cap-data.yml` (missing: harvest)
- `src/seeds/plants/wood-sorrel-data.yml` (missing: harvest)
- `src/seeds/plants/yacon-data.yml` (missing: harvest)
- `src/seeds/plants/yaupon-holly-data.yml` (missing: harvest)
- `src/seeds/plants/yellow-yam-data.yml` (missing: harvest)
- `src/seeds/plants/yuzu-data.yml` (missing: harvest)

## When ALL Files Are Done

```bash
python3 validate.py --since 2h
python3 validate.py --fix --since 2h
./sync.sh --check
./sync.sh
git add -A
git commit -m "Description quality pass batch 3 -- add missing harvest/sun/propagation sections"
git push origin v2
rm review/description_quality_3_of_3.md
```
