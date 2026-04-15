#!/usr/bin/env python3
"""One-off: insert standardized symptoms into individual pest YAML seeds."""
from __future__ import annotations

import re
import sys
from pathlib import Path

import yaml

PESTS_DIR = Path(__file__).resolve().parents[1] / "src" / "seeds" / "pests"
SKIP = {"pests-data.yml", "pests-data.yml.bak"}


def infer_symptoms(slug: str) -> list[str]:
    """Return 2-5 taxonomy tags appropriate to the pest slug."""
    s = slug.lower()

    def pick(xs: list[str]) -> list[str]:
        assert 2 <= len(xs) <= 5, xs
        return xs

    # --- Diseases & disorders (specific first) ---
    if s == "powdery-mildew":
        return pick(
            ["white-powder", "distorted-growth", "yellowing-leaves", "dropping-leaves"]
        )
    if s == "downy-mildew":
        return pick(
            ["leaf-spots", "yellowing-leaves", "wilting", "distorted-growth"]
        )
    if s == "sooty-mold":
        return pick(
            ["black-coating", "sticky-residue", "yellowing-leaves", "dropping-leaves"]
        )
    if s in (
        "phytophthora-root-rot",
        "pythium-root-rot",
        "root-rot",
        "ganoderma-butt-rot",
        "heart-rot",
    ) or s.endswith("-root-rot"):
        return pick(
            [
                "wilting",
                "root-damage",
                "yellowing-leaves",
                "dropping-leaves",
                "crown-damage",
            ]
        )
    if s == "fusarium-wilt":
        return pick(
            ["wilting", "yellowing-leaves", "die-back", "dropping-leaves", "brown-edges"]
        )
    if "virus" in s or s in ("cucumber-mosaic-virus", "papaya-ringspot-virus"):
        return pick(
            ["distorted-growth", "yellowing-leaves", "leaf-spots", "dropping-leaves"]
        )
    if s == "citrus-greening":
        return pick(["yellowing-leaves", "distorted-growth", "dropping-leaves", "die-back"])
    if s == "leaf-curl":
        return pick(
            ["distorted-growth", "leaf-spots", "curling-leaves", "dropping-leaves"]
        )
    if "blight" in s:
        return pick(
            ["wilting", "die-back", "leaf-spots", "brown-edges", "fruit-damage"]
        )
    if s in (
        "bacterial-leaf-spot",
        "alternaria-leaf-spot",
        "cercospora-leaf-spot",
        "leaf-spot",
    ):
        return pick(["leaf-spots", "yellowing-leaves", "dropping-leaves", "wilting"])
    if s == "anthracnose":
        return pick(["leaf-spots", "fruit-damage", "die-back", "wilting"])
    if s in ("apple-scab", "pecan-scab", "citrus-canker"):
        return pick(["leaf-spots", "fruit-damage", "dropping-leaves", "die-back"])
    if s == "potato-scab":
        return pick(["root-damage", "distorted-growth", "yellowing-leaves", "wilting"])
    if s == "parsnip-canker":
        return pick(["root-damage", "wilting", "yellowing-leaves", "distorted-growth"])
    if s in ("gray-mold", "rice-blast-fungus"):
        return pick(["leaf-spots", "wilting", "fruit-damage", "dropping-leaves"])
    if s == "brown-rot":
        return pick(["fruit-damage", "wilting", "die-back", "leaf-spots"])
    if s == "white-rot":
        return pick(["wilting", "crown-damage", "root-damage", "yellowing-leaves"])
    if s == "cytospora-canker":
        return pick(["die-back", "bark-damage", "wilting", "dropping-leaves"])
    if s == "late-blight":
        return pick(["leaf-spots", "wilting", "die-back", "fruit-damage", "brown-edges"])

    # --- Nematodes ---
    if "nematode" in s:
        return pick(
            ["galls", "root-damage", "wilting", "yellowing-leaves", "distorted-growth"]
        )

    # --- Vertebrate / mollusk ---
    if s in ("deer", "iguana"):
        return pick(["chewed-stems", "bark-damage", "fruit-damage", "wilting"])
    if s == "armadillo":
        return pick(["root-damage", "tunneling", "wilting", "chewed-stems"])
    if s in ("snails", "slugs"):
        return pick(["slime-trails", "holes-in-leaves", "chewed-stems", "fruit-damage"])

    # --- Mites (gall before generic mite) ---
    if s == "gall-mite":
        return pick(["galls", "distorted-growth", "yellowing-leaves", "dropping-leaves"])
    if s in ("spider-mites", "mites") or "mite" in s:
        return pick(
            ["yellowing-leaves", "webbing", "silvery-streaking", "brown-edges"]
        )

    # --- Sap feeders ---
    if "aphid" in s:
        return pick(
            ["sticky-residue", "curling-leaves", "yellowing-leaves", "distorted-growth"]
        )
    if "whitefly" in s or s == "whiteflies":
        return pick(
            ["sticky-residue", "yellowing-leaves", "curling-leaves", "sooty-deposits"]
        )
    if "mealybug" in s:
        return pick(
            ["sticky-residue", "yellowing-leaves", "distorted-growth", "sooty-deposits"]
        )
    if s == "scale-insects":
        return pick(
            ["sticky-residue", "yellowing-leaves", "die-back", "sooty-deposits"]
        )
    if "thrips" in s:
        return pick(
            ["silvery-streaking", "distorted-growth", "brown-edges", "dropping-leaves"]
        )
    if "psyllid" in s or "psylla" in s:
        return pick(
            ["sticky-residue", "curling-leaves", "yellowing-leaves", "distorted-growth"]
        )
    if s in ("leafhoppers",) or s == "spotted-lanternfly":
        return pick(
            ["yellowing-leaves", "brown-edges", "distorted-growth", "wilting"]
        )

    # --- True bugs ---
    if (
        "stink-bug" in s
        or s in ("squash-bug", "kudzu-bug", "harlequin-bug", "boxelder-bug")
    ):
        return pick(
            ["fruit-damage", "wilting", "yellowing-leaves", "distorted-growth"]
        )

    # --- Borers & trunk injury ---
    if "borer" in s or s == "borers":
        return pick(
            ["tunneling", "stem-damage", "wilting", "die-back", "bark-damage"]
        )
    if s == "twig-girdlers":
        return pick(["bark-damage", "die-back", "wilting", "stem-damage"])

    # --- Locusts / grasshoppers (exclude locust-borer, locust-leaf-miner) ---
    if s in ("grasshopper", "lubber-grasshopper") or (
        "locust" in s and "borer" not in s and "miner" not in s and "leaf-miner" not in s
    ):
        return pick(
            ["holes-in-leaves", "skeletonized-leaves", "chewed-stems", "fruit-damage"]
        )

    # --- Leaf miners ---
    if "leafminer" in s or "leaf-miner" in s:
        return pick(
            ["tunneling", "distorted-growth", "leaf-spots", "dropping-leaves"]
        )
    if "leaf-miner" in s or ("miner" in s and "mite" not in s):
        return pick(
            ["tunneling", "distorted-growth", "dropping-leaves", "brown-edges"]
        )

    # --- Bagworm (not general "worm" caterpillars) ---
    if s == "bagworm":
        return pick(
            ["skeletonized-leaves", "chewed-stems", "dropping-leaves", "wilting"]
        )

    # --- Caterpillars & chewing larvae ---
    is_caterpillar_like = any(
        k in s
        for k in (
            "caterpillar",
            "armyworm",
            "cutworm",
            "looper",
            "hornworm",
            "webworm",
            "sawfly",
            "cabbageworm",
            "moth",
            "swallowtail",
            "velvetbean",
            "melonworm",
            "pickleworm",
            "butterfly",
            "budworm",
        )
    ) or ("worm" in s and s != "wireworm") or s in (
        "armyworms",
        "caterpillars",
        "cabbage-worms",
        "parsley-worms",
        "dill-worms",
    )
    if is_caterpillar_like:
        return pick(
            [
                "holes-in-leaves",
                "chewed-stems",
                "fruit-damage",
                "skeletonized-leaves",
            ]
        )

    # --- Beetles (chewing) ---
    if "beetle" in s and "ladybird" not in s:
        return pick(
            ["holes-in-leaves", "skeletonized-leaves", "chewed-stems", "wilting"]
        )

    # --- Fruit flies (Tephritidae and similar) ---
    if "fruit-fly" in s or s in ("walnut-husk-fly", "mediterranean-fruit-fly"):
        return pick(["fruit-damage", "wilting", "distorted-growth", "leaf-spots"])

    # --- Maggots & root-feeding flies ---
    if "maggot" in s or s in ("carrot-fly", "onion-fly", "cabbage-root-fly", "onion-maggot"):
        return pick(["root-damage", "wilting", "yellowing-leaves", "holes-in-leaves"])

    # --- Weevils & curculios ---
    if "weevil" in s or "curculio" in s:
        if s == "rice-water-weevil":
            return pick(
                ["holes-in-leaves", "wilting", "yellowing-leaves", "chewed-stems"]
            )
        if "root" in s or "vine-weevil" in s or "strawberry-root-weevil" in s:
            return pick(
                ["root-damage", "wilting", "chewed-stems", "holes-in-leaves"]
            )
        return pick(
            ["chewed-stems", "stem-damage", "fruit-damage", "holes-in-leaves"]
        )

    if "flea" in s and "beetle" in s:
        return pick(["holes-in-leaves", "skeletonized-leaves", "wilting", "leaf-spots"])

    # --- Wireworm ---
    if s == "wireworm":
        return pick(["root-damage", "wilting", "holes-in-leaves", "stem-damage"])

    # --- Fungus gnats / shore flies ---
    if "fungus-gnat" in s or s == "shore-fly":
        return pick(["wilting", "root-damage", "yellowing-leaves", "dropping-leaves"])

    # --- Ants, earwigs, etc. ---
    if s == "fire-ant":
        return pick(
            ["sticky-residue", "wilting", "yellowing-leaves", "chewed-stems"]
        )
    if s == "earwig":
        return pick(["holes-in-leaves", "chewed-stems", "fruit-damage", "wilting"])

    # --- Rollers & web spinners ---
    if s == "leafrollers":
        return pick(
            ["curling-leaves", "holes-in-leaves", "chewed-stems", "webbing"]
        )
    if s in ("tent-caterpillar", "eastern-tent-caterpillar", "fall-webworm"):
        return pick(
            ["webbing", "holes-in-leaves", "skeletonized-leaves", "chewed-stems"]
        )

    # --- Miscellaneous sucking / hopping ---
    if s == "spittlebugs":
        return pick(["wilting", "distorted-growth", "yellowing-leaves", "leaf-spots"])

    # --- Beneficial-turned-problem ---
    if s == "harlequin-ladybird":
        return pick(["yellowing-leaves", "distorted-growth", "dropping-leaves", "holes-in-leaves"])

    # --- Fallback ---
    return pick(["yellowing-leaves", "wilting", "leaf-spots", "dropping-leaves"])


SYMPTOM_LINE = re.compile(r"^  - [a-z0-9-]+$", re.M)
ALLOWED = frozenset(
    """
    holes-in-leaves yellowing-leaves wilting sticky-residue white-powder leaf-spots
    curling-leaves webbing chewed-stems stem-damage root-damage fruit-damage
    black-coating distorted-growth tunneling galls dropping-leaves silvery-streaking
    brown-edges die-back sooty-deposits slime-trails skeletonized-leaves bark-damage
    crown-damage
    """.split()
)


def format_block(symptoms: list[str]) -> str:
    lines = ["  symptoms:"]
    for t in symptoms:
        if t not in ALLOWED:
            raise ValueError(f"invalid symptom tag: {t!r}")
        lines.append(f"  - {t}")
    return "\n".join(lines) + "\n"


def main() -> int:
    changed = 0
    for path in sorted(PESTS_DIR.glob("*-data.yml")):
        if path.name in SKIP:
            continue
        text = path.read_text(encoding="utf-8")
        if re.search(r"(?m)^  symptoms:$", text):
            continue
        if "\n  control_methods:\n" not in text and "\r\n  control_methods:\r\n" not in text:
            print(f"ERR: missing control_methods anchor: {path}", file=sys.stderr)
            return 1
        data = yaml.safe_load(text)
        if not isinstance(data, list) or not data:
            print(f"ERR: unexpected YAML shape: {path}", file=sys.stderr)
            return 1
        slug = (data[0] or {}).get("slug")
        if not slug:
            print(f"ERR: missing slug: {path}", file=sys.stderr)
            return 1
        syms = infer_symptoms(slug)
        block = format_block(syms)
        new_text = text.replace("\n  control_methods:\n", "\n" + block + "  control_methods:\n", 1)
        if new_text == text:
            print(f"ERR: insert failed: {path}", file=sys.stderr)
            return 1
        path.write_text(new_text, encoding="utf-8")
        changed += 1
    print(f"Updated {changed} pest files under {PESTS_DIR}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
