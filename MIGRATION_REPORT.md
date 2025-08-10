# Migration Report

Inventory built from `/home/dracos/apps/permieportal_old`.

## Inventory Table

| Source Path | Type | Suggested Slug | Tags (inferred) | Target |
|---|---|---|---|---|
| `docs/application.md` | article | application | permaculture, satire | `src/content/articles/application.mdx` |
| `docs/implementation_examples.md` | project | implementation-examples | florida, projects | `src/content/projects/implementation-examples.mdx` |
| `README.md` | article | readme | meta | `src/content/articles/readme.mdx` |
| `ENHANCED_PLANT_SYSTEM_GUIDE.md` | article | enhanced-plant-system-guide | plants, system | `src/content/articles/enhanced-plant-system-guide.mdx` |
| `ENHANCED_PLANT_MIGRATION_SUMMARY.md` | project | enhanced-plant-migration-summary | migration, plants | `src/content/projects/enhanced-plant-migration-summary.mdx` |

Excluded infra docs: Docker, Ollama, database, setup, schema, startup guides.

## Migrated
- `docs/application.md` → `src/content/articles/application.mdx`
- `README.md` → `src/content/articles/readme.mdx`
- `ENHANCED_PLANT_SYSTEM_GUIDE.md` → `src/content/articles/enhanced-plant-system-guide.mdx`
- `docs/implementation_examples.md` → `src/content/projects/implementation-examples.mdx`
- `ENHANCED_PLANT_MIGRATION_SUMMARY.md` → `src/content/projects/enhanced-plant-migration-summary.mdx`

## Skipped
- `DOCKER_SETUP.md`, `OLLAMA_SETUP_GUIDE.md`, `GPT_*`, `DATABASE_*`, `SCHEMA_*`, `STARTUP_TROUBLESHOOTING.md`, `APPLICATION_STARTUP_GUIDE.md` — Infra/engineering docs not aligned with the new site.

## Notes
- Dates fallback to today if no git history available.
- Internal links rewritten to `/articles/[slug]` or `/projects/[slug]` when applicable.
