#!/usr/bin/env python3
"""
Rewrite purpose: blocks to Moringa-style quality (Function: detail -- system effect).
Only modifies text between `purpose:` and `companions:`. Skips files that already pass checks.
"""
from __future__ import annotations

import os
import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
PLANTS = ROOT / "src" / "seeds" / "plants"
# Reference gold file -- never auto-overwrite
SKIP_PURPOSE_AUTOGEN = frozenset({"moringa-data.yml"})


def flatten_description(desc) -> str:
    if not desc:
        return ""
    if not isinstance(desc, str):
        return ""
    t = desc.replace("\r\n", "\n")
    t = re.sub(r"[ \t]+", " ", t)
    t = re.sub(r"\n+", " ", t)
    return t.strip()


def desc_for_mining(desc_raw) -> str:
    """Opening / ecology paragraph only -- avoids pulling propagation or harvest bullets."""
    if not isinstance(desc_raw, str):
        return ""
    t = desc_raw.replace("\r\n", "\n")
    for cut in (
        "\n\n☀️",
        "\n☀️",
        "\n\n✂️",
        "\n✂️",
        "\n\n🌾",
        "\n🌾",
        "Sun and Water Requirements",
        "Methods to Propagate",
        "When to Harvest",
        "Harvest / Best Use Timing",
    ):
        if cut in t:
            t = t.split(cut, 1)[0]
    return flatten_description(t)


def no_em_dash(s: str) -> str:
    return (
        s.replace("\u2014", " -- ")
        .replace("\u2013", " - ")
        .replace("\u2212", "-")
    )


def mine_sentence(desc: str, keywords: tuple[str, ...], max_len: int = 320) -> str | None:
    if not desc:
        return None
    chunks = re.split(r"(?<=[.!?])\s+", desc)
    skip_substrings = (
        "propagation:",
        "harvest /",
        "when to harvest",
        "sun and water",
        "✂️",
        "🌾",
        "☀️",
    )
    for ch in chunks:
        low = ch.lower()
        if any(s in low for s in skip_substrings):
            continue
        if any(k.lower() in low for k in keywords):
            one = re.sub(r"\s+", " ", ch).strip()
            if len(one) < 25:
                continue
            return one[:max_len]
    return None


def already_good(purpose: str | None, funcs: list[str]) -> bool:
    if not purpose or not funcs:
        return False
    low = purpose.lower()
    if "serves multiple functions" in low:
        return False
    if "this species strengthens system function" in purpose:
        return False
    if "\n    - " in purpose:
        return False
    lines = [ln.strip() for ln in purpose.splitlines() if ln.strip()]
    if len(lines) < max(3, len(funcs)):
        return False
    for fn in funcs:
        if not any(L.startswith(fn + ":") for L in lines):
            return False
    dd = sum(1 for L in lines if " -- " in L)
    if dd < min(3, len(funcs)):
        return False
    return True


def closing_for(fn: str) -> str:
    """Second clause after ' -- ' for permaculture system behavior."""
    return {
        "Edible": "stacks calories and culinary diversity into guilds and annual rotations without leaning on imported fertility theater",
        "Medicinal": "keeps informed-adult herbal capacity on-site where drying, teas, and tinctures fit your actual risk tolerance",
        "Nitrogen Fixer": "feeds guild neighbors through root turnover, nodule decay, and leaf litter instead of bagged inputs",
        "Dynamic Accumulator": "moves minerals from deep or marginal horizons into chop-and-drop cycles your heavy feeders can bank on",
        "Mulcher": "turns fast leaf/stem turnover into mulch that feeds soil life and buffers moisture swings in mixed beds",
        "Animal Fodder": "cuts purchased feed pressure when offered fresh, wilted, or ensiled alongside your main forage plan",
        "Pollinator": "keeps nectar and pollen online through the heat when weaker flowers quit, stabilizing yields on adjacent crops",
        "Wildlife Attractor": "adds berries, seeds, cover, or insects so birds and beneficials treat your site like habitat, not a parking lot",
        "Windbreaker": "slows desiccating wind at edges and livestock lanes so understory crops keep turgor and transpiration sane",
        "Erosion Control": "binds slopes, banks, and disturbed cuts where bare soil would otherwise sheet during hard rains",
        "Shade Provider": "creates understory microclimate for shade-tolerant herbs and roots while cutting moisture loss below",
        "Water Retention": "adds living mulch, root channels, or canopy drip patterns that even out soil moisture between rains",
        "Ornamental": "gives structure, bloom timing, and texture you can design around while still pulling ecological weight",
        "Fiber": "supplies harvestable fiber for cordage, crafts, or mulch substitutes where woody biomass is scarce",
        "Dye Plant": "anchors natural-color workflows for cloth and craft without importing mystery chemistry",
        "Border Plant": "defines paths, hedgerows, and transition zones while tolerating the edge abuse most crops hate",
        "Ground Cover": "closes the soil surface against weeds and evaporation while feeding roots and arthropods at ground level",
        "Pest Management": "confuses or repels problem insects through scent, trap crops, or habitat for predators you actually want",
        "Biomass": "feeds compost, biochar feedstock, or bulk mulch systems where volume matters more than gourmet calories",
        "Aquatic": "does useful work in ponds, swales, or saturated margins where terrestrial guilds cannot reach",
        "Water Purifier": "supports water-polishing goals in constructed wetlands or settlement tanks when scaled realistically",
        "Timber": "delivers structural wood cycles in long-rotation zones without pretending every tree is dessert",
        "Biofuel": "can feed appropriate small-scale fuel or heat stacks where local law, safety, and storage are sorted",
        "Green Manure": "terminates into soil-covering residue that feeds biology before the next cash crop moves in",
        "Cover Crop": "fits tight rotations between main crops to protect soil structure and capture leaked nutrients",
        "Soil Improvement": "accelerates organic matter and biology gains in tired beds when managed as part of a rotation",
        "Soil Builder": "feeds fungal networks and aggregate stability through roots and residues you plan for, not hope for",
        "Soil Improver": "pulls marginal beds toward crumb structure and steady moisture when combined with mulch discipline",
        "Drought Tolerant": "carries the system through dry spells with less irrigation drama once roots find their depth",
        "Decomposer": "cycles lignin-rich residues into usable humus pathways when placed with the right moisture and airflow",
        "Indoor Plant": "extends propagation, culinary, or medicinal access in protected structures where outdoor extremes win",
        "Air Purifier": "adds living filtration and humidity buffering in enclosed spaces without promising miracle metrics",
    }.get(fn, "strengthens guild function through documented uses so your site needs fewer heroic rescues each season")


def opening_for(fn: str, name: str, sci: str, desc: str) -> str:
    """First clause before ' -- '."""
    d = desc_for_mining(desc) if len(desc) > 400 else flatten_description(desc)
    if len(d) < 40:
        d = flatten_description(desc)
    m = None
    if fn == "Edible":
        m = mine_sentence(d, ("harvest", "fruit", "berry", "leaf", "root", "seed", "pod", "nut", "eat", "culinar", "cook", "salad", "grain", "tuber"))
        if m:
            return f"{name} ({sci}) in the edible role draws on field reality: {m}"
        return f"{name} yields human food from the parts your description documents -- pods, fruits, leaves, roots, or seeds depending on variety and timing"
    if fn == "Medicinal":
        m = mine_sentence(d, ("medic", "herb", "tea", "tincture", "tradition", "oil", "bark", "flower", "immune", "digest"))
        if m:
            return f"Medicinal use stays grounded in what growers actually report: {m}"
        return f"{name} is kept as kitchen-level medicine where aerial parts, roots, or bark match references you trust before dosing"
    if fn == "Nitrogen Fixer":
        m = mine_sentence(d, ("nitrogen", "nodule", "legume", "fix", "rhizob"))
        if m:
            return f"Nitrogen fixation is the point on lean ground: {m}"
        return f"{name} hosts root-zone nitrogen partnerships typical of its family so neighboring feeders trade sugars for usable N"
    if fn == "Dynamic Accumulator":
        m = mine_sentence(d, ("mineral", "nutrient", "deep root", "taproot", "subsoil", "potassium", "calcium", "phosphorus"))
        if m:
            return f"Dynamic accumulation shows up where roots mine depth: {m}"
        return f"{name} pulls mobile nutrients into tissues you can chop-and-drop beside hungry crops"
    if fn == "Mulcher":
        m = mine_sentence(d, ("mulch", "biomass", "chop", "prune", "green manure", "cut back"))
        if m:
            return f"Mulch workflows love predictable biomass: {m}"
        return f"{name} tolerates periodic hard cuts that land leafy residue exactly where soil biology wants it"
    if fn == "Animal Fodder":
        m = mine_sentence(d, ("livestock", "cattle", "goat", "rabbit", "chicken", "forage", "hay", "silage", "graze"))
        if m:
            return f"Livestock integration stays evidence-led: {m}"
        return f"{name} offers palatable leaves, pods, or seeds for poultry and ruminants when introduced slowly like any new forage"
    if fn == "Pollinator":
        m = mine_sentence(d, ("flower", "nectar", "pollinat", "bee", "butterfly", "bloom"))
        if m:
            return f"Pollinator service is measurable at the flower: {m}"
        return f"{name} opens reliable nectar and pollen during the window your warm-season or early-spring crops are setting fruit"
    if fn == "Wildlife Attractor":
        m = mine_sentence(d, ("bird", "mammal", "wildlife", "fruit", "seed", "habitat", "cover"))
        if m:
            return f"Wildlife shows up for calories and cover: {m}"
        return f"{name} layers flowers, seeds, or thicket shelter so beneficial insects and small vertebrates find steady forage along hedgerows"
    if fn == "Windbreaker":
        m = mine_sentence(d, ("wind", "shelter", "hedge", "fence", "tall", "canopy"))
        if m:
            return f"Windbreak value is structural: {m}"
        return f"{name} builds a living wind-skin tall enough to protect tender crops and tunnel houses from desiccating gusts"
    if fn == "Erosion Control":
        m = mine_sentence(d, ("root", "slope", "bank", "soil", "erosion", "stabil"))
        if m:
            return f"Erosion control needs roots that grip: {m}"
        return f"{name} networks fibrous or deep roots through disturbed soil so rain energy meets biology instead of bare mud"
    if fn == "Shade Provider":
        m = mine_sentence(d, ("shade", "canopy", "understory", "sun", "forest"))
        if m:
            return f"Shade design leans on real canopy behavior: {m}"
        return f"{name} throws enough canopy to run ginger-class understory or to blunt afternoon heat on west-facing beds"
    if fn == "Water Retention":
        return f"{name} increases effective water security through mulch-form litter, dense roots, or slowed surface flow on your contour"
    if fn == "Ornamental":
        return f"{name} earns ornamental placement where bloom color, bark, or form matter in courtyard and border designs without abandoning ecology"
    if fn == "Fiber":
        m = mine_sentence(d, ("fiber", "fibre", "cordage", "bast", "weav"))
        if m:
            return f"Fiber harvests stay honest about processing labor: {m}"
        return f"{name} supplies harvestable fiber where small-scale cordage, crafts, or mulch substitutes beat buying plastic twine"
    if fn == "Dye Plant":
        return f"{name} contributes plant-based color from documented plant parts when extraction methods match safety expectations"
    if fn == "Border Plant":
        return f"{name} tolerates foot traffic, mower splash, and microclimate swings along paths and hedgerows where interior crops fail"
    if fn == "Ground Cover":
        m = mine_sentence(d, ("ground", "cover", "spreading", "mat", "creep"))
        if m:
            return f"Ground-cover behavior is the product: {m}"
        return f"{name} carpets soil fast enough to smother early weeds while feeding surface roots and arthropods"
    if fn == "Pest Management":
        return f"{name} supports IPM stacks through scent masking, trap-crop sacrifice, or predator habitat when rotated thoughtfully"
    if fn == "Biomass":
        return f"{name} prioritizes tons of organic matter for compost piles, deep mulch, or chop-and-drop under fruiting canopies"
    if fn == "Aquatic":
        m = mine_sentence(d, ("pond", "wetland", "aquatic", "water", "marginal", "floating"))
        if m:
            return f"Aquatic placement is non-negotiable: {m}"
        return f"{name} belongs in pond margins, tanks, or saturated swales where terrestrial guilds cannot survive full time"
    if fn == "Water Purifier":
        return f"{name} can sit inside constructed wetland edges or settlement plantings where roots and biofilm polish water before storage"
    if fn == "Timber":
        return f"{name} fits long-rotation timber lanes where straight stems or durable wood justify spacing that would starve annual beds"
    if fn == "Biofuel":
        return f"{name} can anchor legal, small-scale fuel or heat projects where dry storage and processing match local codes"
    if fn == "Green Manure":
        return f"{name} terminates on schedule into soil-covering green manure that feeds microbes before the next crop occupies the row"
    if fn == "Cover Crop":
        return f"{name} fills gaps between cash crops with living roots that intercept leaching and keep aggregates from collapsing"
    if fn in ("Soil Improvement", "Soil Builder", "Soil Improver"):
        return f"{name} accelerates tilth gains when residues and roots are planned into rotations instead of left as accidental thatch"
    if fn == "Drought Tolerant":
        return f"{name} carries marginal beds once established, buying time between irrigations in dry subtropical to temperate swings"
    if fn == "Decomposer":
        return f"{name} partners with fungal and bacterial decomposer networks when humidity, airflow, and substrate match its niche"
    if fn == "Indoor Plant":
        return f"{name} extends protected-culture value for propagation, aroma, or harvest where outdoor extremes would kill the stand"
    if fn == "Air Purifier":
        return f"{name} adds leaf surface area and transpiration buffering indoors without replacing real ventilation or filtration design"
    if fn == "Border Plant -Ground Cover":
        return f"{name} behaves as a walkable edge plant and low ground cover at once, tolerating compaction better than interior crops"
    return f"{name} delivers the {fn.lower()} role using the parts and timing your site description already implies"


def elaboration_line(fn: str, name: str, sci: str, desc: str, variant: int) -> str:
    """Extra purpose line when plant_function has fewer than three entries."""
    v = variant % 3
    if v == 0:
        op = f"{name} earns its keep on this axis through site-specific management described in your notes -- not through wishful thinking"
        cl = closing_for(fn)
    elif v == 1:
        op = mine_sentence(
            desc_for_mining(desc),
            ("avoid", "not", "illegal", "warn", "toxic", "caution", "control", "remove", "invasive"),
        ) or (
            f"Management reality for {name} matters as much as yield -- timing, disposal, and local rules decide whether the plant helps or hijacks the system"
        )
        cl = "keeps your design honest about edge cases instead of smuggling them into neighbor ecosystems"
    else:
        op = mine_sentence(
            desc_for_mining(desc),
            ("sun", "water", "soil", "shade", "drain", "humid", "dry", "frost"),
        ) or (
            f"{name} responds sharply to moisture, light, and temperature swings -- match spacing and mulch to the microclimate you measured, not the catalog fantasy"
        )
        cl = "reduces rescue irrigation and replanting drama once establishment rules are actually followed"
    return no_em_dash(f"{fn}: {op} -- {cl}")


def build_purpose(name: str, sci: str, desc_raw: str, funcs: list[str]) -> str:
    desc = desc_raw if isinstance(desc_raw, str) else ""
    if not sci:
        sci = "sp."
    lines: list[str] = []
    for fn in funcs:
        op = opening_for(fn, name, sci, desc or "")
        cl = closing_for(fn)
        line = no_em_dash(f"{fn}: {op} -- {cl}")
        lines.append(line)
    extra = 0
    while len(lines) < 3 and funcs:
        fn = funcs[min(extra, len(funcs) - 1)]
        lines.append(elaboration_line(fn, name, sci, desc or "", extra))
        extra += 1
    return "\n".join(lines) + "\n"


def replace_purpose_region(full: str, new_body: str) -> str:
    marker = "\n  companions:"
    if marker not in full:
        raise ValueError("companions marker missing")
    head, tail = full.split(marker, 1)
    idx = head.find("\n  purpose:")
    if idx == -1:
        idx = head.find("  purpose:")
    if idx == -1:
        raise ValueError("purpose missing")
    prefix = head[:idx].rstrip("\n")
    indented = []
    for ln in new_body.strip("\n").split("\n"):
        if not ln.strip():
            continue
        indented.append("    " + ln)
    # Preserve a newline before purpose: (splitting at idx drops the \n before purpose)
    block = prefix + "\n  purpose: |-\n" + "\n".join(indented) + "\n"
    return block + marker + tail


def iter_plant_files():
    for p in sorted(PLANTS.rglob("*-data.yml")):
        if "_archived_duplicates" in p.parts:
            continue
        yield p


def main() -> int:
    force = os.environ.get("PURPOSE_PASS_FORCE") == "1"
    updated = 0
    skipped = 0
    errors: list[str] = []
    for path in iter_plant_files():
        text = path.read_text(encoding="utf-8")
        try:
            data = yaml.safe_load(text)
        except Exception as e:
            errors.append(f"{path.name}: yaml {e}")
            continue
        if not data or not isinstance(data, list) or not isinstance(data[0], dict):
            errors.append(f"{path.name}: unexpected shape")
            continue
        entry = data[0]
        funcs = entry.get("plant_function") or []
        purpose = entry.get("purpose")
        if path.name in SKIP_PURPOSE_AUTOGEN:
            skipped += 1
            continue
        if not force and already_good(purpose, funcs):
            skipped += 1
            continue
        name = entry.get("common_name") or path.stem.replace("-data", "").replace("-", " ").title()
        sci = entry.get("scientific_name") or ""
        desc = entry.get("description") or ""
        if not funcs:
            errors.append(f"{path.name}: empty plant_function")
            continue
        new_body = build_purpose(name, sci, desc, funcs)
        try:
            new_text = replace_purpose_region(text, new_body)
        except Exception as e:
            errors.append(f"{path.name}: replace {e}")
            continue
        path.write_text(new_text, encoding="utf-8")
        updated += 1
    print(f"updated={updated} skipped_already_good={skipped} errors={len(errors)}")
    for e in errors[:40]:
        print("ERR", e)
    if len(errors) > 40:
        print(f"... {len(errors)-40} more errors")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
