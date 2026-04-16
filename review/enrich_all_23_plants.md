# PermiePortal — Enrich 23 Plant Stubs

## YOUR TASK
You are Cursor Agent in Agent mode. Enrich all 23 plant YAML files listed below.
Replace every NEEDS_DATA field with accurate botanical data.
Do NOT ask questions. Start editing immediately. Work through all 23 files before running any commands.

---

## Reference
Use `src/seeds/plants/moringa-data.yml` as the gold standard for structure and voice.

---

## Geographic Context
- Audience: All of the Americas — zones 3–13
- Do NOT write North Florida or any single-state framing
- Universal climate language: temperate, subtropical, tropical
- Temperatures: Fahrenheit with Celsius in parentheses

---

## Standards
**description** (min 400 chars) must include in order:
1. What the plant is, origin, appearance, mature size
2. ☀️💧 Sun and Water Requirements
3. ✂️ Propagation (2+ methods with timing)
4. 🌾 Harvest / Best Use Timing

**companions** — min 3 specific species with reason WHY (not categories)
**pests** — ONLY names that exactly match entries in src/seeds/pests/ files
**plant_function** — min 3 from the existing values in other seed files
**cautions** — real antagonists or growing warnings, or "None documented"

---

## All 23 Files to Enrich

- `src/seeds/plants/arugula-data.yml`
- `src/seeds/plants/broom-data.yml`
- `src/seeds/plants/brussels-sprouts-data.yml`
- `src/seeds/plants/cabbage-data.yml`
- `src/seeds/plants/cauliflower-data.yml`
- `src/seeds/plants/chinkapin-oak-data.yml`
- `src/seeds/plants/crabapple-data.yml`
- `src/seeds/plants/gorse-data.yml`
- `src/seeds/plants/honeyberry-data.yml`
- `src/seeds/plants/jostaberry-data.yml`
- `src/seeds/plants/mexican-oregano-data.yml`
- `src/seeds/plants/mizuna-data.yml`
- `src/seeds/plants/mockernut-hickory-data.yml`
- `src/seeds/plants/perilla-data.yml`
- `src/seeds/plants/pignut-hickory-data.yml`
- `src/seeds/plants/red-bay-data.yml`
- `src/seeds/plants/saskatoon-data.yml`
- `src/seeds/plants/scorzonera-data.yml`
- `src/seeds/plants/shagbark-hickory-data.yml`
- `src/seeds/plants/swamp-bay-data.yml`
- `src/seeds/plants/vietnamese-mint-data.yml`
- `src/seeds/plants/water-hickory-data.yml`
- `src/seeds/plants/wild-rice-data.yml`

---

## When ALL 23 Files Are Done

Run these commands in order:
```bash
python3 validate.py --since 2h
python3 validate.py --fix --since 2h
./sync.sh --check
./sync.sh
git add -A
git commit -m "Enrich 23 new plants -- arugula, cabbages, hickories, rare herbs"
git push origin v2
rm review/cursor_enrich_1_of_2.md
rm review/cursor_enrich_2_of_2.md
rm review/enrich_all_23_plants.md
```
