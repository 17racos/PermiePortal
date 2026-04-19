#!/usr/bin/env python3
"""Append 🌾 Harvest / Best Use Timing to plant YAML descriptions (review batch)."""
from __future__ import annotations

import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
REVIEW = ROOT / "review"


def list_targets() -> list[Path]:
    paths: list[Path] = []
    for md in sorted(REVIEW.glob("description_quality_*_of_3.md")):
        for line in md.read_text(encoding="utf-8").splitlines():
            m = re.match(r"^- `(src/seeds/plants/[^`]+\.yml)`", line.strip())
            if m:
                paths.append(ROOT / m.group(1))
    return paths


def find_description_span(lines: list[str]) -> tuple[int, int] | None:
    """Return [start, end) line indices: start is `  description:` line, end is next sibling key."""
    for i, line in enumerate(lines):
        if re.match(r"^  description:\s", line):
            start = i
            break
    else:
        return None
    j = start + 1
    while j < len(lines):
        line = lines[j]
        if line.startswith("  #"):
            j += 1
            continue
        if len(line) >= 3 and line.startswith("  ") and line[2] not in (" ", "\t"):
            if re.match(r"^  [A-Za-z0-9_.]+:\s*$", line) or re.match(
                r"^  [A-Za-z0-9_.]+:\s", line
            ):
                return start, j
        j += 1
    return start, len(lines)


def has_harvest_section(desc: str) -> bool:
    d = desc.lower()
    return "🌾" in desc or "harvest / best use" in d or "when to harvest" in d


def join_harvest(bullets: list[str]) -> str:
    body = "\n".join(bullets)
    return f"\n\n🌾 Harvest / Best Use Timing:\n{body}"


def format_description_block(desc: str) -> str:
    out_lines = ["  description: |-"]
    for ln in desc.split("\n"):
        out_lines.append("    " + ln)
    return "\n".join(out_lines) + "\n"


def replace_description_block(raw: str, new_desc: str) -> str:
    lines = raw.splitlines()
    span = find_description_span(lines)
    if not span:
        raise ValueError("no description field")
    start, end = span
    new_block = format_description_block(new_desc).splitlines()
    # format_description_block ends with newline-only last empty? splitlines drops final empty
    out = lines[:start] + new_block + lines[end:]
    text = "\n".join(out)
    if raw.endswith("\n"):
        text += "\n"
    return text


def bullets_for(plant: dict, stem_fn: str) -> list[str]:
    """Return harvest bullet lines (without section header)."""
    custom = CUSTOM.get(stem_fn)
    if custom:
        return custom

    n = plant.get("common_name") or stem_fn
    layers = [str(x).lower() for x in (plant.get("layers") or [])]
    layer_blob = " ".join(layers)
    funcs = {str(x) for x in (plant.get("plant_function") or [])}

    if "fungal" in layer_blob:
        return fungal_bullets(stem_fn, n, funcs)

    if stem_fn in CLUSTER_TOPICS:
        return CLUSTER_TOPICS[stem_fn]

    if stem_fn in ("air-potato-data.yml",):
        return [
            "- In invaded range, timing is about removing bulbils before they drop -- not extending harvest season.",
            "- Where law and ecology intersect, bag and dispose per local invasive guidance instead of compost fantasies.",
            "- If you study processing in cultures where this yam is native, treat lineage and toxicity data as mandatory reading -- not a weekend forage thread.",
        ]

    if stem_fn == "stinging-tree-data.yml":
        return [
            "- There is no human-use harvest window -- contact is the hazard; photography uses long lenses and sense.",
            "- Management timing in native range is protective gear and trained response, not kitchen prep.",
            "- If you encounter unfamiliar large-leaved rainforest trees while traveling, identify before touch -- this species is the argument for that habit.",
        ]

    if "aquatic" in layer_blob and "Edible" in funcs:
        return [
            f"- Harvest {n} in warm active growth when leaves or shoots look crisp, before yellow water-stress marches in.",
            "- Morning picks ship better than wilted afternoon drama -- rinse grit in clean water, not pond soup.",
            "- Use quickly or blanch and freeze; aquatic tissues turn slimy faster than upland herbs in plastic bags.",
        ]

    if "aquatic" in layer_blob:
        return [
            f"- For {n}, value timing follows ecology -- thin or skim when biomass blocks flow or outcompetes natives per local guidance.",
            "- Floating mats: work cool mornings so fragments do not drift downstream and colonize new sins.",
            "- Compost hot active piles after any removal so wet tissues do not restart the invasion from your own yard.",
        ]

    if stem_fn in CITRUS_LIKE:
        return [
            f"- Pick {n} fruit when sugar-acid balance peaks for your use -- marmalade wants different timing than fresh slices.",
            "- Color is a hint, not a contract; sample one fruit from each sector of the canopy.",
            "- Store fresh citrus cool and dry; zest freezes well if you strip peel before shrivel sets in.",
        ]

    if stem_fn in PALMS:
        return [
            f"- {n}: harvest fruit when fully colored and aromatic -- underripe jelly fruit stays stubbornly starchy.",
            "- Use pole baskets or hooks on tall trunks; ripe heads bruise if they free-fall onto concrete morality plays.",
            "- Pulp ferments fast -- process within a day or two, or freeze puree in flat bags for later.",
        ]

    if stem_fn in AGAVE_PIÑA:
        return [
            "- Piña harvest is a years-long commitment -- mark planting dates and size targets before you commit tools.",
            "- Cut leaves close to the core with sharp pikes; sap irritates skin for many people -- gloves and eye sense.",
            "- After harvest, dry or cook processing lines matter as much as field timing; sweet agave work is not a midnight whim.",
        ]

    if "Edible" in funcs and "Tree" in (plant.get("layers") or []):
        # Do not substring-match zone digits (e.g. "11-12" contains "2").
        if stem_fn in TEMPERATE_FRUIT_TREES:
            return [
                f"- {n}: pick when full color, slight give, and aroma align -- early picks often ripen off-tree in a 65-72°F (18-22°C) room.",
                "- Taste-test one fruit per tree sector; sun-exposed shoulders ripen faster than shaded interiors.",
                "- Process windfalls within hours for jam or pulp; leaving them invites fruit fly internships.",
            ]
        return [
            f"- {n}: pick when color, aroma, and a gentle yield to pressure agree for that species -- impatient fruit keeps starch, latex, or both.",
            "- Clip clusters with clean tools; shallow trays beat deep piles that bruise the optimistic bottom layer.",
            "- Rain splits thin skins -- pick before monsoon weeks if weather apps cooperate.",
        ]

    if "Edible" in funcs and "Shrub" in (plant.get("layers") or []) and "Tree" not in (plant.get("layers") or []):
        if "blueberry" in stem_fn or "elder" in stem_fn or "sparkle" in stem_fn or "shiny-blueberry" in stem_fn:
            return [
                f"- {n}: pick berries when fully colored and detach with a gentle tug -- whitish bloom still present is fine.",
                "- Cool mornings beat hot afternoons for shelf life; chill soon if not eating the same day.",
                "- Freeze dry on trays before bagging so berries do not fuse into a single ice meteor.",
            ]
        return [
            f"- {n}: pick peak flavor when fruits soften slightly and detach easily -- birds are a parallel calendar.",
            "- Harvest after dew dries to reduce mold in baskets.",
            "- Jam batches same day if humidity is high; acid and sugar balance matter more than Instagram gloss.",
        ]

    if "Edible" in funcs and ("root" in layer_blob or stem_fn in ROOTY):
        return [
            f"- {n}: dig tubers or roots after tops senesce or frost signals storage shift -- curing a few days at 50-60°F (10-16°C) sweetens some starches.",
            "- Loosen soil wide first -- snapped necks invite rot in storage.",
            "- Brush-dry before long storage; plastic totes without airflow grow penicillin cosplay.",
        ]

    if "Edible" in funcs and "vine" in layer_blob:
        return [
            f"- {n}: pick fruits young for vegetable use or fully ripe for seed and sweetness goals -- one plant rarely serves both fantasies.",
            "- Cut stems morning; afternoon wilt reduces quality fast above 90°F (32°C).",
            "- Check trellis daily during peak set; hidden fruits split after rain.",
        ]

    if "Medicinal" in funcs and "Edible" not in funcs:
        return [
            f"- Harvest {n} aerial parts in early flowering for many mint-family uses -- oils shift after full bloom.",
            "- Dry in shade with airflow between 95-110°F (35-43°C) until crisp; mold invalidates the batch.",
            "- Label harvest date and plant part -- winter you will not remember which jar was optimism.",
        ]

    if "Edible" in funcs:
        return [
            f"- Snip tender {n} growth in cool mornings for best texture -- heat-stressed leaves taste like their day job.",
            "- Flowers at full color for peak volatiles; seeds when pods rattle but before they self-sow across paths.",
            "- Dry herbs in thin layers; deep piles steam themselves into compost.",
        ]

    return [
        f"- For {n}, harvest timing follows the primary function you planted for -- flowers, fodder, mulch, or structure.",
        "- Coppice or prune dormant windows where winters exist; subtropical plants often prefer dry-season cuts.",
        "- Always sanitize tools between diseased and clean plants -- drama spreads faster than newsletters.",
    ]


def fungal_bullets(stem_fn: str, n: str, funcs: set[str]) -> list[str]:
    if stem_fn in ("chaga-data.yml",):
        return [
            "- Conks are traditionally taken in cold months after hard freezes when tissue is firm -- never strip a live birch to bare wood.",
            "- Leave partial conk and respect land permissions; mail-order northern sources are the honest path in warm Americas.",
            "- Slice thin and dry completely before storage; rehydrate for slow decoctions, not crunchy salad cosplay.",
        ]
    if stem_fn in ("reishi-data.yml", "turkey-tail-data.yml"):
        return [
            "- Harvest mature brackets when still flexible -- chalky dry conks are past prime for tea quality.",
            "- Slice ribbons and air-dry with fan flow; finish crisp before jar sealing.",
            "- Long low simmers extract polysaccharide body; label batches with wood host and date.",
        ]
    if stem_fn == "cordyceps-data.yml":
        return [
            "- Wild cordyceps timing is a high-elevation specialist story -- ethical sourcing beats backyard fantasies in most Americas sites.",
            "- Lab-cultured mycelium products follow processor guidance, not field calendars.",
            "- If experimenting with insect-host models, containment and identification discipline come before marketing copy.",
        ]
    if stem_fn == "chicken-of-the-woods-data.yml":
        return [
            "- Harvest young overlapping shelves while still juicy -- old brackets toughen into shoe leather.",
            "- Trim close to wood, transport in paper, cook thoroughly day-of.",
            "- Never mix unknown brackets on the same skillet -- ID certainty first, brunch second.",
        ]
    if "Edible" in funcs:
        return [
            f"- Flush {n} before caps flatten and spores dust -- younger tissue holds better flavor for most logs and beds.",
            "- Twist or cut at base; second flushes often follow if humidity stays honest.",
            "- Refrigerate in paper bags and use within days; saute or pickle rather than letting slimy regret arrive.",
        ]
    return [
        f"- For {n}, harvest brackets at maturity for drying or tincture work -- woody zones mean slower drying, so slice thin.",
        "- Note host wood species on labels; chemistry varies by substrate.",
        "- Leave some fruiting bodies for spore banks and wildlife cycles.",
    ]


CLUSTER_TOPICS = {
    "fiber-and-industrial-data.yml": [
        "- Bast fibers: harvest stems at bloom or just before for best fiber length -- species sheets beat one rule.",
        "- Seed crops: combine or thresh when moisture hits the storage-safe window for that grain -- mold is not a preservative strategy.",
        "- Agave and bromeliad fiber: strip mature leaves after documented years in ground -- safety gear for sap is non-optional.",
    ],
    "vines-data.yml": [
        "- Fruiting vines: pick on flavor markers for each species -- color lies more often than smell.",
        "- Leaf and shoot vines: harvest tips during active growth; pause hard cuts during extreme heat or drought stress.",
        "- Mulch vines after major pruning so roots stay cool while new laterals form.",
    ],
    "water-aquatic-data.yml": [
        "- Edible aquatics: harvest young leaves and shoots in warm growth periods; grit removal matters more than garnish fantasies.",
        "- Water purifiers: thin mats when flow drops or dissolved oxygen complaints begin -- timing is ecological, not cosmetic.",
        "- Compost removed biomass hot and monitored so fragments cannot restart downstream.",
    ],
    "pollinator-support-data.yml": [
        "- For seed mixes and insectary strips, stagger bloom so something is open from frost-safe weeks through heat.",
        "- Cut spent flower heads before invasive self-sowers drop seed where you will regret diplomacy later.",
        "- Collect your own clean seed labeled by year; cheap mixes age out faster than hope.",
    ],
}

CITRUS_LIKE = {
    "bitter-orange-data.yml",
    "citron-data.yml",
    "sour-orange-data.yml",
    "yuzu-data.yml",
}

PALMS = {
    "buriti-palm-data.yml",
    "jelly-palm-data.yml",
    "pindo-palm-data.yml",
}

AGAVE_PIÑA = {"blue-agave-data.yml", "century-plant-data.yml", "henequen-data.yml"}

TEMPERATE_FRUIT_TREES = {
    "american-persimmon-data.yml",
    "chickasaw-plum-data.yml",
    "mayhaw-data.yml",
    "pawpaw-data.yml",
}

ROOTY = {
    "ahipa-data.yml",
    "jerusalem-artichoke-data.yml",
    "burdock-data.yml",
    "tannia-data.yml",
    "ulluco-data.yml",
    "yacon-data.yml",
    "mashua-data.yml",
    "konjac-data.yml",
    "bitter-yam-data.yml",
    "yellow-yam-data.yml",
    "chicory-data.yml",
    "arrowhead-data.yml",
    "canna-lily-data.yml",
}

CUSTOM: dict[str, list[str]] = {
    "fruit-sage-data.yml": [
        "- Snip leaves and tender tips before flowering for mildest tea flavor -- post-bloom foliage turns sharper.",
        "- Pick scarlet flower tubes at full color for syrups; use same day or refrigerate briefly.",
        "- Dry small bundles upside down in shade; strip when crisp and store airtight out of direct sun.",
    ],
    "dahoon-holly-data.yml": [
        "- Native wildlife timing matters more than human harvest -- berries support birds; leave plenty.",
        "- If collecting for restoration projects, take only from known-safe sites and legal permission contexts.",
        "- Prune for structure in cool months; hollies resent torn bark summer pruning.",
    ],
    "floating-heart-data.yml": [
        "- Thin floating mats when coverage blocks light for submersed plants you value.",
        "- Work in cool morning air so broken fragments drift less.",
        "- Compost removed biomass in active piles; do not toss live pieces into new water bodies.",
    ],
    "gopher-apple-data.yml": [
        "- Low apple-like fruits ripen summer into fall for wildlife -- human nibbling is curiosity, not calorie planning.",
        "- Leave groundcover intact; roots stabilize sandy soils for adjacent species.",
        "- Photograph for ID help instead of stripping every fruit for novelty.",
    ],
    "hemp-data.yml": [
        "- Fiber hemp: harvest at early to mid-bloom for long bast strips -- seed hemp follows combine moisture rules for that cultivar.",
        "- CBD-type fields follow regional compliance testing windows -- legal paperwork is part of the calendar.",
        "- Dry stalks in shocks with airflow; moldy hemp is landfill, not craft.",
    ],
    "kava-data.yml": [
        "- Harvest lateral roots after documented years in ground -- traditional timing is measured in seasons, not influencer weeks.",
        "- Dry roots slowly with airflow; powder when fully brittle and store labeled.",
        "- Respect local law and cultural sourcing ethics; this is not a stealth backyard pharma plot.",
    ],
    "kratom-data.yml": [
        "- Leaf harvest timing follows documented alkaloid curves in regions where cultivation is legal -- check jurisdiction before planting drama.",
        "- Pick mature leaves in dry weather; rapid wet piles compost themselves.",
        "- Dry flat with excellent airflow; label vein color and date for your own notes.",
    ],
    "lead-plant-data.yml": [
        "- For mulch and chop-and-drop, harvest leafy growth after flowering when biomass is high but before seed shatter if you want less spread.",
        "- Wildlife value peaks if you leave some stands uncut each year.",
        "- Never strip more than a third of canopy on small plants.",
    ],
    "honey-locust-data.yml": [
        "- Livestock pods: collect when pods rattle but before heavy worm damage -- taste-test livestock response in small increments.",
        "- Coppice wood on multi-year rotations for fence posts where thorns are acceptable.",
        "- Flowers feed pollinators -- avoid wholesale canopy removal during peak bloom.",
    ],
    "alder-data.yml": [
        "- For biomass and coppice, cut dormant season in temperate climates; avoid heavy sap-run windows if bark tears easily on your site.",
        "- Catkins feed early pollinators -- leave uncut blocks in rotation.",
        "- If tapping for dye experiments, mark trees and take modest volumes so crowns recover.",
    ],
    "wild-coffee-data.yml": [
        "- Berries ripen to glossy red on female plants -- coffee processing is a fermentation and drying discipline, not a five-minute hack.",
        "- Harvest for wildlife if you are not running clean processing lines.",
        "- Prune for shape after fruiting slows; shade-houseplants get repot timing instead of field frost.",
    ],
    "southern-magnolia-data.yml": [
        "- Pick mature cones when follicles open and scarlet seeds show -- air-dry seeds briefly before sowing or cold storage experiments.",
        "- Floral parts are ornamental use primarily -- fragrance peaks on freshly opened blooms.",
        "- Leaf drop is mulch timing -- rake into beds if scale insects are not part of the bundle.",
    ],
    "maidenhair-fern-data.yml": [
        "- Fronds are enjoyed in place -- sustainable harvest means photos for art, not stripping every leaflet.",
        "- If propagating divisions, take modest wedges from large clumps in cool wet weather.",
        "- Morning mist beats afternoon sun for transplant recovery.",
    ],
    "mud-plantain-data.yml": [
        "- Ecological value and subtle edible uses depend on correct ID -- harvest only where law and sanitation allow.",
        "- Thin dense stands if mosquito habitat becomes a managed-water issue.",
        "- Leave regenerating rhizome patches after any removal.",
    ],
    "scorpion-weed-data.yml": [
        "- Small flowers support native bees -- treat as support species, not salad bulk.",
        "- If managing in restoration, collect seed when capsules brown and before full shatter.",
        "- Avoid heavy grazing timing on restoration sites until stands establish.",
    ],
}


def process_file(path: Path) -> bool:
    raw = path.read_text(encoding="utf-8")
    data = yaml.safe_load(raw)
    if not data:
        return False
    plant = data[0]
    desc = plant.get("description") or ""
    if has_harvest_section(desc):
        return False
    stem_fn = path.name
    add = join_harvest(bullets_for(plant, stem_fn))
    new_desc = desc.rstrip() + add
    new_raw = replace_description_block(raw, new_desc)
    path.write_text(new_raw, encoding="utf-8")
    return True


def main() -> int:
    n_ok = 0
    for path in list_targets():
        if not path.exists():
            print("missing", path, file=sys.stderr)
            continue
        if process_file(path):
            print("updated", path.relative_to(ROOT))
            n_ok += 1
        else:
            print("skip", path.relative_to(ROOT))
    print("--- done, updated", n_ok)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
