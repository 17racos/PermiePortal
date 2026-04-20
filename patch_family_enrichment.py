#!/usr/bin/env python3
"""
patch_family_enrichment.py
==========================
Adds enrich_family_nodes() to convert_permie_data.py.
Runs automatically after build_family_nodes() on every sync.
Adds to each family node:
  - pest_pressure: {plant_count, total_pest_associations, unique_pests,
                    avg_pests_per_plant, top_pests}
  - trait_profile: {top_functions, top_layers, perennial_ratio, nitrogen_fixers}
Also writes pest_family_index as top-level key in families.json.
"""
from pathlib import Path

f = Path("convert_permie_data.py")
text = f.read_text()

# ── PATCH 1: Add enrich_family_nodes() before build_family_nodes() ───────────
ANCHOR = "def build_family_nodes(plants, warnings):"

NEW_FUNC = '''def enrich_family_nodes(family_nodes, plants, relationships):
    """
    Enrich family nodes with pest pressure and trait profiles.
    Runs after build_family_nodes() and build_plant_family_edges().
    Modifies family_nodes in place. Returns pest_family_index.
    """
    from collections import defaultdict, Counter as _Counter

    plant_by_slug = {p["slug"]: p for p in plants}

    # plant → family
    plant_to_family = {}
    for r in relationships:
        if r.get("type") == "plant_family":
            plant_to_family[r["source_slug"]] = r["target_slug"]

    # family → plants
    family_to_plants = defaultdict(list)
    for slug, fam in plant_to_family.items():
        family_to_plants[fam].append(slug)

    # plant → pests (plant_pest edges only)
    plant_to_pests = defaultdict(set)
    for r in relationships:
        if r.get("type") == "plant_pest":
            plant_to_pests[r["source_slug"]].add(r.get("pest_name", ""))

    # ── Pest pressure per family ──────────────────────────────────────────────
    family_pest_pressure = {}
    for fam_slug, plant_slugs in family_to_plants.items():
        all_pests = []
        for ps in plant_slugs:
            all_pests.extend(p for p in plant_to_pests.get(ps, set()) if p)
        pest_counter = _Counter(all_pests)
        family_pest_pressure[fam_slug] = {
            "plant_count":             len(plant_slugs),
            "total_pest_associations": len(all_pests),
            "unique_pests":            len(pest_counter),
            "avg_pests_per_plant":     round(len(all_pests) / len(plant_slugs), 2)
                                       if plant_slugs else 0,
            "top_pests":               [{"name": n, "count": c}
                                        for n, c in pest_counter.most_common(5)],
        }

    # ── Trait profiles per family ─────────────────────────────────────────────
    family_traits = {}
    for fam_slug, plant_slugs in family_to_plants.items():
        fam_plants = [plant_by_slug[ps] for ps in plant_slugs if ps in plant_by_slug]
        functions_all = []
        layers_all    = []
        perennial_count = 0
        for p in fam_plants:
            functions_all.extend(p.get("plant_function", []) or [])
            layers_all.extend(p.get("layers", []) or [])
            if p.get("perennial"):
                perennial_count += 1
        fn_counter  = _Counter(functions_all)
        lay_counter = _Counter(layers_all)
        family_traits[fam_slug] = {
            "top_functions":  [{"name": n, "count": c}
                                for n, c in fn_counter.most_common(5)],
            "top_layers":     [{"name": n, "count": c}
                                for n, c in lay_counter.most_common(3)],
            "perennial_ratio": round(perennial_count / len(fam_plants), 2)
                               if fam_plants else 0,
            "nitrogen_fixers": fn_counter.get("Nitrogen Fixer", 0),
        }

    # ── Pest → family reverse index ───────────────────────────────────────────
    pest_to_families = defaultdict(lambda: defaultdict(int))
    for r in relationships:
        if r.get("type") == "plant_pest":
            fam_slug = plant_to_family.get(r["source_slug"])
            if fam_slug:
                pest_to_families[r.get("pest_name", "")][fam_slug] += 1

    pest_family_index = {}
    for pest_name, fam_counts in pest_to_families.items():
        if not pest_name:
            continue
        total = sum(fam_counts.values())
        pest_family_index[pest_name] = {
            "total_plants_affected": total,
            "families": [
                {
                    "family_slug": fs,
                    "plant_count": c,
                    "exposure": round(
                        c / family_pest_pressure[fs]["plant_count"], 2
                    ) if fs in family_pest_pressure else 0,
                }
                for fs, c in sorted(fam_counts.items(), key=lambda x: -x[1])
            ],
        }

    # ── Merge into family nodes in place ──────────────────────────────────────
    for node in family_nodes:
        slug = node["slug"]
        node["pest_pressure"] = family_pest_pressure.get(slug, {
            "plant_count": node.get("plant_count", 0),
            "total_pest_associations": 0,
            "unique_pests": 0,
            "avg_pests_per_plant": 0,
            "top_pests": [],
        })
        node["trait_profile"] = family_traits.get(slug, {
            "top_functions": [],
            "top_layers": [],
            "perennial_ratio": 0,
            "nitrogen_fixers": 0,
        })

    return pest_family_index


def build_family_nodes(plants, warnings):'''

if ANCHOR in text and "enrich_family_nodes" not in text:
    text = text.replace(ANCHOR, NEW_FUNC)
    print("✅ Patch 1: enrich_family_nodes() added")
else:
    if "enrich_family_nodes" in text:
        print("⏭️  Patch 1: already applied")
    else:
        print("❌ Patch 1: anchor not found")

# ── PATCH 2: Call enrich_family_nodes() after family graph is built ──────────
OLD_CALL = '''    relationships = relationships + plant_family_edges
    print(f"  ✅ {len(plant_family_edges)} plant_family edges")
    print(f"  ✅ {len(family_nodes)} family nodes")'''

NEW_CALL = '''    relationships = relationships + plant_family_edges
    print(f"  ✅ {len(plant_family_edges)} plant_family edges")
    print(f"  ✅ {len(family_nodes)} family nodes")
    pest_family_index = enrich_family_nodes(family_nodes, plants, relationships)
    print(f"  ✅ Family nodes enriched with pest pressure + trait profiles")'''

if OLD_CALL in text:
    text = text.replace(OLD_CALL, NEW_CALL)
    print("✅ Patch 2: enrich_family_nodes() called in pipeline")
else:
    print("❌ Patch 2: anchor not found")

# ── PATCH 3: Write enriched families.json with pest_family_index ─────────────
OLD_WRITE = '    write_json("families.json", family_nodes)'
NEW_WRITE = '''    write_json("families.json", {
        "families":          family_nodes,
        "pest_family_index": pest_family_index,
    })'''

if OLD_WRITE in text:
    text = text.replace(OLD_WRITE, NEW_WRITE)
    print("✅ Patch 3: families.json includes pest_family_index")
else:
    print("❌ Patch 3: anchor not found")

f.write_text(text)
print("\nDone — run ./sync.sh to verify")
