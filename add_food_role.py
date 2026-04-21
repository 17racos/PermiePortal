#!/usr/bin/env python3
"""
add_food_role.py
================
Adds food_role: anchor | support | specialty to all edible plant YAMLs.
Only modifies plants where plant_function includes 'Edible'.
Non-edible plants are untouched.

Design:
- Rule-first classifier
- Tiny override map for true edge cases only
- Deterministic, no randomness
- Meant to support guild-builder anchor selection later

Run from: ~/apps/permieportal/
"""
import glob
from pathlib import Path
from collections import Counter

try:
    import ruamel.yaml
    USE_RUAMEL = True
except ImportError:
    import yaml as pyyaml
    USE_RUAMEL = False
    print("⚠️  ruamel.yaml not found, falling back to pyyaml (may alter formatting)")


# ── Tiny explicit overrides for true edge cases only ─────────────────────────

FOOD_ROLE_OVERRIDES = {
    # clearly not default food-guild anchors
    "shampoo-ginger": "specialty",
    "black-ginger": "specialty",
    "florida-pusley": "specialty",
    "wine-cap": "specialty",
    "cordyceps": "specialty",
    "reishi": "specialty",
    "turkey-tail": "specialty",
    "lion-s-mane": "specialty",
    "shiitake": "specialty",
    "oyster-mushroom": "specialty",
    "maitake": "specialty",
    "dollarweed": "specialty",
    "chaga": "specialty",
    "lion-s-mane": "specialty",
    "chicken-of-the-woods": "specialty",
    "florida-pusley": "specialty",
    "kratom": "specialty",
    "kava": "specialty",
    "miracle-berry": "specialty",
    "american-lotus": "specialty",
    "american-waterlily": "specialty",

    # obvious food anchors that heuristics might otherwise under-rank
    "mulberry-tree": "anchor",
    "red-mulberry": "anchor",
    "banana": "anchor",
    "papaya": "anchor",
    "cassava": "anchor",
    "sweet-potato": "anchor",
    "pigeon-pea": "anchor",
    "moringa": "anchor",
    "jackfruit": "anchor",
    "breadfruit": "anchor",
    "taro": "anchor",
    "yacon": "anchor",
    "jerusalem-artichoke": "anchor",
    "loquat": "anchor",
    "fig": "anchor",
    "avocado": "anchor",
    "mango": "anchor",
    "cacao": "anchor",
    "coconut-palm": "anchor",
    "peach-palm": "anchor",
    "elderberry": "anchor",
    "aronia": "anchor",
    "goumi": "anchor",
    "sea-buckthorn": "anchor",
    "autumn-olive": "anchor",
    "roselle": "anchor",
    "chaya": "anchor",
    "katuk": "anchor",
}

# Add Convolvulaceae to ANCHOR_FAMILIES (sweet potato family)


# ── Classifier knowledge ──────────────────────────────────────────────────────

SUPPORT_FUNCTIONS = {
    "Ground Cover",
    "Mulcher",
    "Dynamic Accumulator",
    "Erosion Control",
    "Pest Management",
    "Windbreaker",
    "Border Plant",
}

SPECIALTY_FAMILIES = {
    # fungi
    "Pleurotaceae",
    "Meripilaceae",
    "Omphalotaceae",
    "Polyporaceae",
    "Strophariaceae",
    "Ganodermataceae",
    "Hericiaceae",
    "Fomitopsidaceae",
    "Hymenochaetaceae",
    "Cordycipitaceae",
}

ANCHOR_FAMILIES = {
    # common food-guild backbone families
    "Rosaceae",
    "Myrtaceae",
    "Cucurbitaceae",
    "Solanaceae",
    "Fabaceae",
    "Brassicaceae",
    "Amaryllidaceae",
    "Arecaceae",
    "Araceae",
    "Annonaceae",
    "Rutaceae",
    "Moraceae",
    "Ericaceae",
    "Convolvulaceae",
    "Euphorbiaceae",
    "Moringaceae",
    "Elaeagnaceae",
    "Adoxaceae",
    "Malvaceae",
}

SUPPORT_BIASED_FAMILIES = {
    # commonly edible but often secondary / herb / support oriented
    "Lamiaceae",
    "Apiaceae",
    "Asteraceae",
    "Boraginaceae",
    "Polygonaceae",
    "Zingiberaceae",
    "Costaceae",
    "Marantaceae",
    "Cannaceae",
}

ANCHOR_SLUG_HINTS = {
    # broad food-pattern hints, not giant curated lists
    "banana", "papaya", "cassava", "sweet-potato", "potato", "yam", "taro",
    "oca", "yacon", "arrowroot", "leren", "jicama", "ahipa",
    "apple", "pear", "peach", "plum", "cherry", "fig", "mulberry", "avocado",
    "mango", "guava", "blueberry", "blackberry", "raspberry", "strawberry",
    "elderberry", "gooseberry", "currant", "serviceberry", "goumi",
    "broccoli", "cabbage", "cauliflower", "brussels", "kale", "bok-choy",
    "radish", "turnip", "carrot", "beet", "celery", "okra",
    "tomato", "pepper", "eggplant",
    "cucumber", "zucchini", "pumpkin", "squash", "watermelon", "cantaloupe",
    "garlic", "onion", "leek", "shallot", "chives",
    "bean", "pea", "lentil", "chickpea", "soybean", "mung", "adzuki",
    "corn", "maize", "rice", "wheat", "barley", "oat", "millet",
}

SPECIALTY_SLUG_HINTS = {
    # novelty, fungi, medicinal-leaning, oddballs
    "mushroom", "fungus", "fungi", "cordyceps", "reishi", "shiitake",
    "lotus", "waterlily", "duckweed", "water-lettuce", "water-hyacinth",
    "pitcher", "sundew", "nepenthes", "venus-flytrap", "cobra-lily",
    "miracle-berry", "kratom", "kava",
}


def slug_has_any_hint(slug: str, hints: set[str]) -> bool:
    return any(h in slug for h in hints)


def classify_food_role(slug: str, plant_functions: list[str], family: str) -> str:
    """
    Rule-first classifier for edible plants.

    Priority:
    1. explicit tiny overrides
    2. fungi / obvious specialty families
    3. support-heavy edible plants
    4. medicinal-dominant small-role edibles
    5. strong edible families / anchor-like patterns
    6. fallback: support
    """
    fns = set(plant_functions or [])
    family = (family or "").strip()

    # 1) explicit overrides
    if slug in FOOD_ROLE_OVERRIDES:
        return FOOD_ROLE_OVERRIDES[slug]

    # 2) specialty families / specialty slug patterns
    if family in SPECIALTY_FAMILIES:
        return "specialty"
    if slug_has_any_hint(slug, SPECIALTY_SLUG_HINTS):
        return "specialty"

    # 3) support-heavy edible plants should rarely anchor a food guild
    support_count = len(fns & SUPPORT_FUNCTIONS)
    if support_count >= 3:
        return "support"

    # 4) medicinal-dominant edibles are usually not default food anchors
    if "Medicinal" in fns and len(fns) <= 4 and support_count <= 1:
        return "specialty"

    # ornamental + edible + medicinal with low food signal → specialty
    if "Ornamental" in fns and "Medicinal" in fns and len(fns) <= 5:
        return "specialty"

    # 5a) strong food families → anchor
    if family in ANCHOR_FAMILIES and "Edible" in fns:
        return "anchor"

    # 5b) support-biased families → support unless very clearly anchor-like
    if family in SUPPORT_BIASED_FAMILIES:
        if slug_has_any_hint(slug, ANCHOR_SLUG_HINTS) and support_count <= 1:
            return "anchor"
        return "support"

    # 5c) grains / cereal-ish poaceae are anchors, most others support
    if family == "Poaceae":
        if slug_has_any_hint(slug, {"corn", "maize", "rice", "wheat", "barley", "oat", "millet", "sorghum"}):
            return "anchor"
        return "support"

    # 5d) obvious anchor name hints
    if slug_has_any_hint(slug, ANCHOR_SLUG_HINTS) and support_count <= 2:
        return "anchor"

    # 6) default edible fallback
    return "support"


def load_yaml(path: str):
    if USE_RUAMEL:
        y = ruamel.yaml.YAML()
        y.preserve_quotes = True
        y.width = 4096
        with open(path, "r", encoding="utf-8") as fh:
            return y.load(fh)
    else:
        with open(path, "r", encoding="utf-8") as fh:
            return pyyaml.safe_load(fh)


def dump_yaml(path: str, data):
    if USE_RUAMEL:
        y = ruamel.yaml.YAML()
        y.preserve_quotes = True
        y.width = 4096
        with open(path, "w", encoding="utf-8") as fh:
            y.dump(data, fh)
    else:
        # lightweight fallback append/replace to reduce full-file churn
        raw = Path(path).read_text(encoding="utf-8")
        lines = raw.splitlines()

        # replace if already exists
        for i, line in enumerate(lines):
            if line.startswith("food_role:"):
                lines[i] = f"food_role: {data['food_role']}"
                Path(path).write_text("\n".join(lines) + "\n", encoding="utf-8")
                return

        # insert after plant_function block if possible
        insert_at = None
        in_pf = False
        for i, line in enumerate(lines):
            if line.startswith("plant_function:"):
                in_pf = True
                continue
            if in_pf:
                if line.startswith("- "):
                    continue
                if line.startswith("  -"):
                    continue
                if line.strip():
                    insert_at = i
                    break

        if insert_at is None:
            lines.append(f"food_role: {data['food_role']}")
        else:
            lines.insert(insert_at, f"food_role: {data['food_role']}")

        Path(path).write_text("\n".join(lines) + "\n", encoding="utf-8")


def main():
    yaml_files = sorted(glob.glob("src/seeds/plants/*.yml"))
    counts = Counter()
    modified = 0
    skipped_non_edible = 0
    already_has = 0
    errors = []

    for path in yaml_files:
        try:
            data = load_yaml(path)
            if not isinstance(data, dict):
                continue

            fns = data.get("plant_function") or []
            if "Edible" not in fns:
                skipped_non_edible += 1
                continue

            if data.get("food_role"):
                already_has += 1
                counts[data["food_role"]] += 1
                continue

            slug = Path(path).stem.replace("-data", "")
            family = data.get("family", "") or ""
            role = classify_food_role(slug, fns, family)

            data["food_role"] = role
            dump_yaml(path, data)

            counts[role] += 1
            modified += 1

        except Exception as e:
            errors.append(f"{path}: {e}")

    print(f"\n{'=' * 50}")
    print("Food Role Audit Complete")
    print(f"{'=' * 50}")
    print(f"  Modified:          {modified}")
    print(f"  Already had field: {already_has}")
    print(f"  Non-edible (skip): {skipped_non_edible}")
    print("\nClassification breakdown:")
    for role in ("anchor", "support", "specialty"):
        print(f"  {role:12} {counts[role]}")
    print(f"\nTotal edible classified: {sum(counts.values())}")

    if errors:
        print(f"\n⚠️  Errors ({len(errors)}):")
        for e in errors[:10]:
            print(f"  {e}")


if __name__ == "__main__":
    main()