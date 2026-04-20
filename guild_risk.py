#!/usr/bin/env python3
"""
guild_risk.py
=============
compute_guild_risk(plant_slugs) — pure Python guild risk scorer.

Uses ONLY:
  - src/data/plants.json       (plant metadata)
  - src/data/relationships.json (plant_family + plant_pest edges)

No new files. No new edge types. No mutation of source data.
"""
from __future__ import annotations
from collections import Counter, defaultdict
from pathlib import Path
from typing import List
import json


# ── Data loader (lazy, cached at module level) ────────────────────────────────

_cache: dict = {}

def _load():
    if _cache:
        return _cache
    base = Path(__file__).parent / "src" / "data"
    _cache["rels"]   = json.loads((base / "relationships.json").read_text())
    _cache["plants"] = json.loads((base / "plants.json").read_text())
    return _cache


# ── Core function ─────────────────────────────────────────────────────────────

def compute_guild_risk(plant_slugs: List[str]) -> dict:
    """
    Compute ecological risk score for a guild of plants.

    Args:
        plant_slugs: list of plant slug strings (e.g. ["tomato", "basil"])

    Returns:
        {
            "family_diversity_score": float,   # unique_families / total_plants
            "dominant_families":      list,    # family slugs present in guild
            "shared_pests":           list,    # pest names affecting >1 plant
            "risk_score":             float,   # 0.0 (low) – 1.0 (high)
            "warnings":               list,    # human-readable risk flags
        }
    """
    data = _load()
    rels = data["rels"]

    # ── Dedup input ───────────────────────────────────────────────────────────
    slugs = list(dict.fromkeys(s.strip() for s in plant_slugs if s and s.strip()))
    n = len(slugs)

    if n == 0:
        return {
            "family_diversity_score": 0.0,
            "dominant_families":      [],
            "shared_pests":           [],
            "risk_score":             0.0,
            "warnings":               ["No valid plant slugs provided."],
        }

    # ── Build indexes (read-only views, no mutation) ──────────────────────────
    plant_to_family: dict[str, str] = {}
    plant_to_pests:  dict[str, set] = defaultdict(set)

    for r in rels:
        rtype = r.get("type")
        if rtype == "plant_family":
            plant_to_family[r["source_slug"]] = r["target_slug"]
        elif rtype == "plant_pest":
            plant_to_pests[r["source_slug"]].add(r["pest_name"])

    # ── Resolve families for this guild ───────────────────────────────────────
    guild_families = [
        plant_to_family[s] for s in slugs if s in plant_to_family
    ]
    family_counts  = Counter(guild_families)
    unique_families = len(family_counts)

    family_diversity_score = round(unique_families / n, 4)

    # Dominant families (sorted by frequency)
    dominant_families = [fam for fam, _ in family_counts.most_common()]

    # ── Gather pests ──────────────────────────────────────────────────────────
    pest_occurrence: Counter = Counter()
    for s in slugs:
        for pest in plant_to_pests.get(s, set()):
            pest_occurrence[pest] += 1

    total_pests  = len(pest_occurrence)
    shared_pests = [pest for pest, count in pest_occurrence.items() if count > 1]

    # ── Risk score ────────────────────────────────────────────────────────────
    shared_ratio = len(shared_pests) / total_pests if total_pests > 0 else 0.0
    risk_score   = round(
        (1 - family_diversity_score) * 0.5 + shared_ratio * 0.5,
        4,
    )

    # ── Warnings ──────────────────────────────────────────────────────────────
    warnings: list[str] = []

    # Family dominance warning (only meaningful for guilds of 3+ plants)
    if family_counts and n >= 3:
        top_family, top_count = family_counts.most_common(1)[0]
        if top_count / n > 0.6:
            warnings.append(
                f"Family dominance: {top_family} makes up "
                f"{round(top_count / n * 100)}% of guild — "
                f"consider adding plants from other families."
            )

    # Shared pest warning
    if total_pests > 0 and len(shared_pests) / total_pests > 0.5:
        warnings.append(
            f"High shared pest load: {len(shared_pests)} of {total_pests} pests "
            f"affect multiple guild members — pest outbreak risk is elevated."
        )

    # Unresolved slugs
    unresolved = [s for s in slugs if s not in plant_to_family]
    if unresolved:
        warnings.append(
            f"Slugs not found in plant_family edges: {unresolved} — "
            f"they were excluded from family analysis."
        )

    return {
        "family_diversity_score": family_diversity_score,
        "dominant_families":      dominant_families,
        "shared_pests":           sorted(shared_pests),
        "risk_score":             risk_score,
        "warnings":               warnings,
    }


# ── Inline test ───────────────────────────────────────────────────────────────

if __name__ == "__main__":
    import sys

    test_guilds = [
        {
            "label": "HIGH risk — Solanaceae monoculture",
            "slugs": ["tomato", "eggplant", "bell-pepper", "moringa", "basil"],
        },
        {
            "label": "LOW risk — diverse families",
            "slugs": ["moringa", "comfrey", "elderberry", "lemongrass", "sweet-potato"],
        },
        {
            "label": "HIGH risk — all Rosaceae",
            "slugs": ["strawberry", "raspberry", "peach-tree", "pear-tree"],
        },
        {
            "label": "EDGE — single plant",
            "slugs": ["moringa"],
        },
        {
            "label": "EDGE — empty guild",
            "slugs": [],
        },
    ]

    for guild in test_guilds:
        result = compute_guild_risk(guild["slugs"])
        print(f"\n{'='*60}")
        print(f"Guild: {guild['label']}")
        print(f"  Plants:             {guild['slugs']}")
        print(f"  Family diversity:   {result['family_diversity_score']}")
        print(f"  Dominant families:  {result['dominant_families'][:4]}")
        print(f"  Shared pests:       {result['shared_pests'][:5]}")
        print(f"  Risk score:         {result['risk_score']}")
        if result["warnings"]:
            for w in result["warnings"]:
                print(f"  ⚠️  {w}")
