# PermiePortal — Description Quality Pass Batch 1 of 3

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

- `src/seeds/plants/abiu-data.yml` (missing: harvest)
- `src/seeds/plants/ahipa-data.yml` (missing: harvest)
- `src/seeds/plants/air-potato-data.yml` (missing: harvest)
- `src/seeds/plants/alder-data.yml` (missing: harvest)
- `src/seeds/plants/alexanders-data.yml` (missing: harvest)
- `src/seeds/plants/american-persimmon-data.yml` (missing: harvest)
- `src/seeds/plants/angelica-data.yml` (missing: harvest)
- `src/seeds/plants/angled-loofah-data.yml` (missing: harvest)
- `src/seeds/plants/arrowhead-data.yml` (missing: harvest)
- `src/seeds/plants/atemoya-data.yml` (missing: harvest)
- `src/seeds/plants/bilimbi-data.yml` (missing: harvest)
- `src/seeds/plants/bitter-orange-data.yml` (missing: harvest)
- `src/seeds/plants/bitter-yam-data.yml` (missing: harvest)
- `src/seeds/plants/blue-agave-data.yml` (missing: harvest)
- `src/seeds/plants/blue-woodruff-data.yml` (missing: harvest)
- `src/seeds/plants/buck-plantain-data.yml` (missing: harvest)
- `src/seeds/plants/buffalo-gourd-data.yml` (missing: harvest)
- `src/seeds/plants/burdock-data.yml` (missing: harvest)
- `src/seeds/plants/buriti-palm-data.yml` (missing: harvest)
- `src/seeds/plants/calabaza-data.yml` (missing: harvest)
- `src/seeds/plants/canistel-data.yml` (missing: harvest)
- `src/seeds/plants/canna-lily-data.yml` (missing: harvest)
- `src/seeds/plants/century-plant-data.yml` (missing: harvest)
- `src/seeds/plants/chaga-data.yml` (missing: harvest)
- `src/seeds/plants/chickasaw-plum-data.yml` (missing: harvest)
- `src/seeds/plants/chicken-of-the-woods-data.yml` (missing: harvest)
- `src/seeds/plants/chicory-data.yml` (missing: harvest)
- `src/seeds/plants/cinnamon-basil-data.yml` (missing: harvest)
- `src/seeds/plants/citron-data.yml` (missing: harvest)
- `src/seeds/plants/clary-sage-data.yml` (missing: harvest)
- `src/seeds/plants/coco-plum-data.yml` (missing: harvest)
- `src/seeds/plants/cordyceps-data.yml` (missing: harvest)
- `src/seeds/plants/corsican-mint-data.yml` (missing: harvest)
- `src/seeds/plants/cupuacu-data.yml` (missing: harvest)
- `src/seeds/plants/dahoon-holly-data.yml` (missing: harvest)
- `src/seeds/plants/darrow-blueberry-data.yml` (missing: harvest)
- `src/seeds/plants/elderflower-data.yml` (missing: harvest)
- `src/seeds/plants/elliott-blueberry-data.yml` (missing: harvest)
- `src/seeds/plants/fever-few-data.yml` (missing: harvest)
- `src/seeds/plants/fiber-and-industrial-data.yml` (missing: harvest)
- `src/seeds/plants/floating-heart-data.yml` (missing: harvest)
- `src/seeds/plants/fruit-sage-data.yml` (missing: harvest)
- `src/seeds/plants/giant-bulrush-data.yml` (missing: harvest)

## When ALL Files Are Done

```bash
python3 validate.py --since 2h
python3 validate.py --fix --since 2h
./sync.sh --check
./sync.sh
git add -A
git commit -m "Description quality pass batch 1 -- add missing harvest/sun/propagation sections"
git push origin v2
rm review/description_quality_1_of_3.md
```
