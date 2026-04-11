# PermiePortal — Targeted Data Enrichment

> **Agent mode only.** Small focused task — do not touch anything not listed.

---

## Task

Improve companion and pest data for specific plants.
Edit only the listed YAML files in `src/seeds/plants/`.

**Rules:**
- Companions must be real plants with documented beneficial relationships
- Pest names must exactly match slugs in `src/seeds/pests/pests-data.yml`
- Do NOT change any other fields — only `companions:`, `avoid:`, and `pests:`
- After edits run: `./sync.sh --check`

---

## Plants Needing Better Companion Data

These have vague or empty companion lists worth improving:

- `src/seeds/plants/buriti-palm-data.yml`
  Current: `['Other native Amazonian wetland trees (in range)']`
  Goal: Add 3-5 specific companion species appropriate for wetland/tropical systems

- `src/seeds/plants/cattley-guava-data.yml`
  Current: `['None documented']`
  Goal: Add real companions — guavas do well with nitrogen fixers, dynamic accumulators

- `src/seeds/plants/cinnamon-vine-data.yml`
  Current: `['None documented']`
  Goal: Add companions appropriate for a climbing vine in subtropical systems

- `src/seeds/plants/mimosa-data.yml`
  Current: `['None documented']`
  Goal: Mimosa is a nitrogen fixer — add plants that benefit from nitrogen

- `src/seeds/plants/sea-buckthorn-data.yml`
  Current: `['Nitrogen-loving plants']`
  Goal: Replace vague entry with 3-5 specific species

- `src/seeds/plants/surinam-cherry-data.yml`
  Current: `['None documented']`
  Goal: Add companions for a subtropical fruit shrub

- `src/seeds/plants/wild-parsnip-data.yml`
  Current: `[]`
  Goal: Add companions and avoid list

---

## Plants Needing More Pest Links

These have only 1 pest — add 2-4 more that are botanically accurate:

- `src/seeds/plants/chaya-data.yml`
  Current pests: `['Iguana']`
  Note: Chaya in Florida also gets aphids, whiteflies, spider mites

- `src/seeds/plants/pineapple-guava-data.yml`
  Current pests: `['Iguana']`
  Note: Pineapple guava also gets scale insects, aphids, fruit flies

---

## Leave These Alone — They Are Botanically Correct

- Fennel (allelopathic, grows alone)
- Air Potato (invasive, no companions recommended)
- Singapore Daisy (invasive)
- Water Hyacinth (contained system)
- Chaga Host / Turkey Tail Host (mushroom hosts, minimal pest pressure)
- Stinging Tree (naturally pest-resistant)

---

## When Done

```bash
./sync.sh --check
```
Fix any warnings, then:
```bash
./sync.sh
```
