import os
import re
import yaml
from glob import glob

VALID_FUNCTIONS = {
    "Edible","Medicinal","Nitrogen Fixer","Dynamic Accumulator","Mulcher",
    "Pollinator","Wildlife Attractor","Erosion Control","Animal Fodder",
    "Windbreaker","Border Plant","Pest Management","Ground Cover",
    "Shade Provider","Water Retention","Fiber","Biomass","Aquatic",
    "Ornamental","Water Purification","Plant Growth Stimulant","Biofuel"
}

FUNCTION_MAP = {
    "Pest Repellent": "Pest Management",
    "Water Purifier": "Water Purification",
}

INVALID_COMPANIONS = {
    "plants","trees","vegetables","crops","flowers","shrubs"
}

GENERIC_BAD = {
    "beans","grasses","vegetables","plants","trees"
}

def clean_geo(text):
    if not text:
        return text
    text = re.sub(r'\b(North Florida|Midwest|Southeast US|United States)\b', '', text, flags=re.I)
    text = re.sub(r'\bspring\b|\bfall\b', 'wet season', text, flags=re.I)
    return text

def fix_functions(data):
    pf = data.get("plant_function", [])
    new_pf = []

    for f in pf:
        if f in VALID_FUNCTIONS:
            new_pf.append(f)
        elif f in FUNCTION_MAP:
            new_pf.append(FUNCTION_MAP[f])
        # else drop

    data["plant_function"] = list(dict.fromkeys(new_pf))  # dedupe
    return data

def parse_purpose(purpose_text):
    lines = []
    for line in (purpose_text or "").split("\n"):
        if ":" in line and " -- " in line:
            fn = line.split(":",1)[0].strip()
            lines.append((fn, line))
    return lines

def fix_purpose(data):
    pf = set(data.get("plant_function", []))
    purpose = data.get("purpose","")

    parsed = parse_purpose(purpose)

    # keep only lines that match plant_function
    new_lines = []
    for fn, line in parsed:
        if fn in pf:
            new_lines.append(line)

    data["purpose"] = "\n".join(new_lines)
    return data

def clean_companions(data):
    seen = set()

    def normalize_name(n):
        return n.strip().lower()

    # companions (resolved)
    comps = data.get("companions", [])
    new_comps = []
    for c in comps:
        slug = c.get("slug")
        if slug and slug not in seen:
            seen.add(slug)
            new_comps.append(c)

    data["companions"] = new_comps

    # unresolved
    unresolved = data.get("companions_unresolved", [])
    new_unresolved = []
    for c in unresolved:
        name = c.get("name","").strip()
        key = normalize_name(name)

        if key in seen:
            continue
        if key in INVALID_COMPANIONS or key in GENERIC_BAD:
            continue
        if not name:
            continue

        seen.add(key)
        new_unresolved.append({
            "name": name,
            "original": c.get("original", name)
        })

    data["companions_unresolved"] = new_unresolved[:5]

    # categories
    cats = data.get("companion_categories", [])
    new_cats = []
    for c in cats:
        name = c.get("name","").strip()
        key = normalize_name(name)

        if key in seen:
            continue

        seen.add(key)
        new_cats.append(c)

    data["companion_categories"] = new_cats[:4]

    return data

def process_file(path):
    with open(path) as f:
        data = yaml.safe_load(f)

    # geo cleanup
    if "description" in data:
        data["description"] = clean_geo(data["description"])

    # functions
    data = fix_functions(data)

    # purpose alignment
    data = fix_purpose(data)

    # companions cleanup
    data = clean_companions(data)

    # field_observations enforcement
    if "field_observations" in data and data["field_observations"] not in ["", None]:
        data["field_observations"] = ""

    with open(path, "w") as f:
        yaml.dump(data, f, sort_keys=False)

def main():
    files = glob("src/seeds/plants/*-data.yml")
    for f in files:
        process_file(f)
        print(f"Fixed: {f}")

if __name__ == "__main__":
    main()