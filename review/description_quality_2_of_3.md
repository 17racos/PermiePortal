# PermiePortal — Description Quality Pass Batch 2 of 3

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

- `src/seeds/plants/gopher-apple-data.yml` (missing: harvest)
- `src/seeds/plants/grumichama-data.yml` (missing: harvest)
- `src/seeds/plants/hairy-indigo-data.yml` (missing: harvest)
- `src/seeds/plants/hemp-data.yml` (missing: harvest)
- `src/seeds/plants/henequen-data.yml` (missing: harvest)
- `src/seeds/plants/hoary-plantain-data.yml` (missing: harvest)
- `src/seeds/plants/honey-locust-data.yml` (missing: harvest)
- `src/seeds/plants/honey-melon-sage-data.yml` (missing: harvest)
- `src/seeds/plants/hyacinth-bean-data.yml` (missing: harvest)
- `src/seeds/plants/ilama-data.yml` (missing: harvest)
- `src/seeds/plants/jelly-palm-data.yml` (missing: harvest)
- `src/seeds/plants/jerusalem-artichoke-data.yml` (missing: harvest)
- `src/seeds/plants/kava-data.yml` (missing: harvest)
- `src/seeds/plants/konjac-data.yml` (missing: harvest)
- `src/seeds/plants/kratom-data.yml` (missing: harvest)
- `src/seeds/plants/lead-plant-data.yml` (missing: harvest)
- `src/seeds/plants/lemon-eucalyptus-data.yml` (missing: harvest)
- `src/seeds/plants/lemon-verbena-data.yml` (missing: harvest)
- `src/seeds/plants/lions-mane-data.yml` (missing: harvest)
- `src/seeds/plants/lovage-data.yml` (missing: harvest)
- `src/seeds/plants/luffa-data.yml` (missing: harvest)
- `src/seeds/plants/maidenhair-fern-data.yml` (missing: harvest)
- `src/seeds/plants/maitake-data.yml` (missing: harvest)
- `src/seeds/plants/malabar-chestnut-data.yml` (missing: harvest)
- `src/seeds/plants/mamey-sapote-data.yml` (missing: harvest)
- `src/seeds/plants/marlberry-data.yml` (missing: harvest)
- `src/seeds/plants/mashua-data.yml` (missing: harvest)
- `src/seeds/plants/mayhaw-data.yml` (missing: harvest)
- `src/seeds/plants/mexican-tarragon-data.yml` (missing: harvest)
- `src/seeds/plants/mud-plantain-data.yml` (missing: harvest)
- `src/seeds/plants/murici-data.yml` (missing: harvest)
- `src/seeds/plants/myrsine-data.yml` (missing: harvest)
- `src/seeds/plants/natal-plum-data.yml` (missing: harvest)
- `src/seeds/plants/oyster-mushroom-data.yml` (missing: harvest)
- `src/seeds/plants/pawpaw-data.yml` (missing: harvest)
- `src/seeds/plants/pennyroyal-data.yml` (missing: harvest)
- `src/seeds/plants/perennial-basil-data.yml` (missing: harvest)
- `src/seeds/plants/pickerelweed-data.yml` (missing: harvest)
- `src/seeds/plants/pindo-palm-data.yml` (missing: harvest)
- `src/seeds/plants/pollinator-support-data.yml` (missing: harvest)
- `src/seeds/plants/ramps-data.yml` (missing: harvest)
- `src/seeds/plants/reishi-data.yml` (missing: harvest)
- `src/seeds/plants/ribwort-plantain-data.yml` (missing: harvest)

## When ALL Files Are Done

```bash
python3 validate.py --since 2h
python3 validate.py --fix --since 2h
./sync.sh --check
./sync.sh
git add -A
git commit -m "Description quality pass batch 2 -- add missing harvest/sun/propagation sections"
git push origin v2
rm review/description_quality_2_of_3.md
```
