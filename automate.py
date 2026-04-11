#!/usr/bin/env python3
"""
PermiePortal Plant & Pest Automation
=====================================
Fetches images from Wikimedia Commons / iNaturalist,
generates YAML stubs, and queues them for Cursor Agent to enrich.

Usage:
  python3 automate.py plants "Chaya" "Lemon Verbena" "Cranberry Hibiscus"
  python3 automate.py pests "Squash Vine Borer" "Stink Bug" "Fungus Gnats"
  python3 automate.py plants --file plant_queue.txt
  python3 automate.py pests --file pest_queue.txt
  python3 automate.py --daily          # runs full daily batch from queue files
  python3 automate.py --dry-run plants "Moringa"  # test without downloading
"""

import json
import re
import sys
import time
import argparse
import urllib.request
import urllib.parse
import urllib.error
from pathlib import Path

# ── CONFIG ────────────────────────────────────────────────────────────────────
PROJECT         = Path(__file__).parent
SEEDS_PLANTS    = PROJECT / "src/seeds/plants"
SEEDS_PESTS     = PROJECT / "src/seeds/pests"
PESTS_FILE      = SEEDS_PESTS / "pests-data.yml"
PLANT_IMAGES    = PROJECT / "public/assets/plants"
PEST_IMAGES     = PROJECT / "public/assets/pests"
QUEUE_PLANTS    = PROJECT / "queue_plants.txt"
QUEUE_PESTS     = PROJECT / "queue_pests.txt"
REVIEW_DIR      = PROJECT / "review"
DAILY_PLANTS    = 20
DAILY_PESTS     = 10
# ──────────────────────────────────────────────────────────────────────────────

def slugify(text):
    text = str(text).lower().strip()
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[\s_]+', '-', text)
    return re.sub(r'-+', '-', text).strip('-')


def picture_name(name):
    """Convert display name to image filename."""
    return slugify(name).replace('-', '_') + '.jpg'


def fetch_json(url, timeout=10):
    """Simple JSON fetch with user agent."""
    req = urllib.request.Request(
        url,
        headers={'User-Agent': 'PermiePortal/2.0 (permieportal.com; botanical database)'}
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return json.loads(resp.read().decode('utf-8'))
    except Exception as e:
        return None


def download_image(url, dest_path, dry_run=False):
    """Download an image to dest_path."""
    if dry_run:
        print(f"    [DRY RUN] Would download: {url}")
        return True
    try:
        req = urllib.request.Request(
            url,
            headers={'User-Agent': 'PermiePortal/2.0 (permieportal.com)'}
        )
        with urllib.request.urlopen(req, timeout=15) as resp:
            dest_path.parent.mkdir(parents=True, exist_ok=True)
            dest_path.write_bytes(resp.read())
        return True
    except Exception as e:
        print(f"    ⚠️  Download failed: {e}")
        return False


# ── IMAGE SOURCES ─────────────────────────────────────────────────────────────

def wikimedia_image(query, prefer_botanical=True):
    """
    Search Wikimedia Commons for a plant/pest image.
    Returns (image_url, attribution) or (None, None).
    """
    # Search Commons
    search_url = (
        "https://commons.wikimedia.org/w/api.php?"
        "action=query&format=json&list=search"
        f"&srsearch={urllib.parse.quote(query + ' plant')}"
        "&srnamespace=6&srlimit=5"
    )
    data = fetch_json(search_url)
    if not data:
        return None, None

    results = data.get('query', {}).get('search', [])
    if not results:
        return None, None

    # Try each result until we get a usable image
    for result in results:
        title = result.get('title', '')
        if not title.startswith('File:'):
            continue

        # Get image info
        info_url = (
            "https://commons.wikimedia.org/w/api.php?"
            "action=query&format=json&prop=imageinfo"
            "&iiprop=url|extmetadata|mime"
            f"&titles={urllib.parse.quote(title)}"
        )
        info = fetch_json(info_url)
        if not info:
            continue

        pages = info.get('query', {}).get('pages', {})
        for page in pages.values():
            ii = page.get('imageinfo', [{}])[0]
            mime = ii.get('mime', '')
            if mime not in ('image/jpeg', 'image/png', 'image/webp'):
                continue

            url = ii.get('url', '')
            if not url:
                continue

            meta = ii.get('extmetadata', {})
            license_short = meta.get('LicenseShortName', {}).get('value', 'Unknown')
            artist = meta.get('Artist', {}).get('value', 'Unknown')
            # Strip HTML from artist
            artist = re.sub(r'<[^>]+>', '', artist).strip()

            attribution = f"{artist} / Wikimedia Commons / {license_short}"
            return url, attribution

    return None, None


def inaturalist_image(query, taxon_type='Plantae'):
    """
    Search iNaturalist for a plant or insect image.
    Returns (image_url, attribution) or (None, None).
    """
    search_url = (
        f"https://api.inaturalist.org/v1/taxa?"
        f"q={urllib.parse.quote(query)}&per_page=3"
    )
    data = fetch_json(search_url)
    if not data:
        return None, None

    results = data.get('results', [])
    for taxon in results:
        photo = taxon.get('default_photo')
        if not photo:
            continue
        url = photo.get('medium_url') or photo.get('url')
        if not url:
            continue
        attribution = photo.get('attribution', 'iNaturalist')
        return url, attribution

    return None, None


def get_best_image(name, mode='plant', dry_run=False):
    """
    Try Wikimedia first, fall back to iNaturalist.
    Returns (url, attribution, source) or (None, None, None).
    """
    print(f"  🔍 Searching images for: {name}")

    # Wikimedia first
    url, attr = wikimedia_image(name)
    if url:
        print(f"    ✅ Found on Wikimedia Commons")
        return url, attr, 'wikimedia'

    # iNaturalist fallback
    taxon = 'Insecta' if mode == 'pest' else 'Plantae'
    url, attr = inaturalist_image(name, taxon)
    if url:
        print(f"    ✅ Found on iNaturalist")
        return url, attr, 'inaturalist'

    print(f"    ⚠️  No image found — placeholder will be used")
    return None, None, None


# ── YAML GENERATORS ───────────────────────────────────────────────────────────

PLANT_STUB = '''---
- common_name: {common_name}
  picture: {picture}
  scientific_name: "NEEDS_DATA"
  aka: []
  family: "NEEDS_DATA"
  zone: "NEEDS_DATA"
  ideal_temp_min: 0
  ideal_temp_max: 0
  min_temp: 0
  max_temp: 0
  perennial: true
  layers:
  - NEEDS_DATA
  plant_function:
  - NEEDS_DATA
  description: "NEEDS_DATA — Cursor Agent will enrich this entry."
  purpose: "NEEDS_DATA"
  companions:
  - NEEDS_DATA
  avoid:
  - NEEDS_DATA
  pests:
  - NEEDS_DATA
  # Image attribution: {attribution}
  # Image source: {source}
  # AUTO-GENERATED STUB — requires Cursor Agent enrichment
'''

PEST_STUB = '''- name: "{name}"
  slug: "{slug}"
  picture: "{picture}"
  scientific_name: "NEEDS_DATA"
  description: "NEEDS_DATA — Cursor Agent will enrich this entry."
  characteristics: "NEEDS_DATA"
  control_methods:
    organic_sprays: "NEEDS_DATA"
    biological_controls: "NEEDS_DATA"
    cultural_practices: "NEEDS_DATA"
    mechanical_physical: "NEEDS_DATA"
    preventive_methods: "NEEDS_DATA"
  natural_enemies:
  - NEEDS_DATA
  # Image attribution: {attribution}
  # Image source: {source}
  # AUTO-GENERATED STUB — requires Cursor Agent enrichment
'''


def generate_plant_stub(name, attribution, source):
    pic = picture_name(name)
    slug = slugify(name)
    filepath = SEEDS_PLANTS / f"{slug}-data.yml"

    if filepath.exists():
        print(f"  ⏭️  Skipping {name} — YAML already exists")
        return None

    content = PLANT_STUB.format(
        common_name=name,
        picture=pic,
        attribution=attribution or 'No image found',
        source=source or 'none',
    )
    return filepath, content


def generate_pest_stub(name, attribution, source):
    pic = picture_name(name)
    slug = slugify(name)

    # Check if pest already exists in pests-data.yml
    if PESTS_FILE.exists():
        existing = PESTS_FILE.read_text()
        if f'name: "{name}"' in existing or f"name: '{name}'" in existing:
            print(f"  ⏭️  Skipping {name} — pest already exists")
            return None

    content = PEST_STUB.format(
        name=name,
        slug=slug,
        picture=pic,
        attribution=attribution or 'No image found',
        source=source or 'none',
    )
    return content


# ── CURSOR AGENT PROMPT GENERATOR ────────────────────────────────────────────

def write_cursor_prompt(plant_names, pest_names, output_path):
    """Write a ready-to-paste Cursor Agent prompt."""
    lines = ["# PermiePortal — Cursor Agent Enrichment Task\n"]
    lines.append("Paste this entire prompt into Cursor Agent (not chat — Agent mode).\n")
    lines.append("---\n")

    if plant_names:
        lines.append("## Plants to Enrich\n")
        lines.append(
            "The following plant YAML files have been created with stub data. "
            "For each file, replace every `NEEDS_DATA` field with accurate botanical "
            "information. Use `src/seeds/plants/moringa-data.yml` as the exact structure "
            "reference. Requirements:\n"
            "- Zones and temperatures in Fahrenheit\n"
            "- Layers must be one of: Tree, Shrub, Herbaceous, Vine, Ground Cover, "
            "Root, Aquatic, Canopy\n"
            "- plant_function values must match existing entries in other seed files\n"
            "- Pests must exactly match slugs in src/seeds/pests/pests-data.yml\n"
            "- Description should include propagation methods and sun/water requirements\n"
            "- Focus on North Florida / subtropical context where relevant\n"
            "- Voice: informative but not corporate. PermieBro tone where appropriate.\n\n"
        )
        for name in plant_names:
            slug = slugify(name)
            lines.append(f"- `src/seeds/plants/{slug}-data.yml`\n")

        lines.append("\n")

    if pest_names:
        lines.append("## Pests to Enrich\n")
        lines.append(
            "The following pest stubs have been appended to "
            "`src/seeds/pests/pests-data.yml`. Find each entry with `NEEDS_DATA` "
            "and replace with accurate information. Requirements:\n"
            "- Organic control methods ONLY — no synthetic pesticides ever\n"
            "- control_methods keys: organic_sprays, biological_controls, "
            "cultural_practices, mechanical_physical, preventive_methods\n"
            "- natural_enemies should be real biological predators/parasites\n"
            "- Description should help identify the pest in the field\n\n"
        )
        for name in pest_names:
            lines.append(f"- {name}\n")
        lines.append("\n")

    lines.append("## After Enriching\n")
    lines.append(
        "When all entries are filled in, run:\n"
        "```\n./sync.sh --check\n```\n"
        "Fix any warnings about unmatched pest references, then run:\n"
        "```\n./sync.sh\n```\n"
        "Report the final summary (plants, pests, relationships count).\n"
    )

    output_path.write_text(''.join(lines))
    print(f"\n📋 Cursor Agent prompt saved to: {output_path}")


# ── MAIN PROCESSORS ──────────────────────────────────────────────────────────

def process_plants(names, dry_run=False):
    """Process a list of plant names."""
    SEEDS_PLANTS.mkdir(parents=True, exist_ok=True)
    PLANT_IMAGES.mkdir(parents=True, exist_ok=True)

    processed = []
    for name in names:
        name = name.strip()
        if not name:
            continue

        print(f"\n🌱 Processing plant: {name}")

        # Get image
        img_url, attribution, source = get_best_image(name, mode='plant', dry_run=dry_run)

        # Download image
        pic = picture_name(name)
        img_dest = PLANT_IMAGES / pic
        if img_url and not img_dest.exists():
            ok = download_image(img_url, img_dest, dry_run=dry_run)
            if ok and not dry_run:
                print(f"    💾 Saved: public/assets/plants/{pic}")
        elif img_dest.exists():
            print(f"    ⏭️  Image already exists: {pic}")

        # Generate YAML stub
        result = generate_plant_stub(name, attribution, source)
        if result:
            filepath, content = result
            if not dry_run:
                filepath.write_text(content)
                print(f"    📝 Created: src/seeds/plants/{filepath.name}")
            else:
                print(f"    [DRY RUN] Would create: src/seeds/plants/{filepath.name}")
            processed.append(name)

        time.sleep(0.5)  # Be polite to APIs

    return processed


def process_pests(names, dry_run=False):
    """Process a list of pest names — appends to pests-data.yml."""
    SEEDS_PESTS.mkdir(parents=True, exist_ok=True)
    PEST_IMAGES.mkdir(parents=True, exist_ok=True)

    processed = []
    new_stubs = []

    for name in names:
        name = name.strip()
        if not name:
            continue

        print(f"\n🐛 Processing pest: {name}")

        # Get image
        img_url, attribution, source = get_best_image(name, mode='pest', dry_run=dry_run)

        # Download image
        pic = picture_name(name)
        img_dest = PEST_IMAGES / pic
        if img_url and not img_dest.exists():
            ok = download_image(img_url, img_dest, dry_run=dry_run)
            if ok and not dry_run:
                print(f"    💾 Saved: public/assets/pests/{pic}")
        elif img_dest.exists():
            print(f"    ⏭️  Image already exists: {pic}")

        # Generate pest stub
        result = generate_pest_stub(name, attribution, source)
        if result:
            new_stubs.append(result)
            processed.append(name)
            if dry_run:
                print(f"    [DRY RUN] Would append {name} to pests-data.yml")
            else:
                print(f"    📝 Queued: {name}")

        time.sleep(0.5)

    # Append all new stubs to pests-data.yml at once
    if new_stubs and not dry_run:
        with open(PESTS_FILE, 'a', encoding='utf-8') as f:
            f.write('\n')
            for stub in new_stubs:
                f.write(stub)
        print(f"\n  ✅ Appended {len(new_stubs)} pest stubs to pests-data.yml")

    return processed


def load_queue(filepath, limit):
    """Load names from a queue file, return first N, rewrite remainder."""
    if not filepath.exists():
        return []
    lines = [l.strip() for l in filepath.read_text().splitlines() if l.strip()]
    batch = lines[:limit]
    remaining = lines[limit:]
    filepath.write_text('\n'.join(remaining) + ('\n' if remaining else ''))
    return batch


# ── CLI ───────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description='PermiePortal Automation')
    parser.add_argument('mode', nargs='?', choices=['plants', 'pests'],
                        help='What to process')
    parser.add_argument('names', nargs='*', help='Names to process')
    parser.add_argument('--file', '-f', help='Read names from a text file (one per line)')
    parser.add_argument('--daily', action='store_true',
                        help=f'Run daily batch: {DAILY_PLANTS} plants + {DAILY_PESTS} pests from queue files')
    parser.add_argument('--dry-run', action='store_true',
                        help='Test run — no files downloaded or created')
    args = parser.parse_args()

    REVIEW_DIR.mkdir(exist_ok=True)
    prompt_path = REVIEW_DIR / "cursor_agent_prompt.md"

    plant_names = []
    pest_names = []

    # ── DAILY MODE ────────────────────────────────────────────────────────────
    if args.daily:
        print(f"\n📅 Daily batch mode")
        print(f"   Plants: up to {DAILY_PLANTS} from {QUEUE_PLANTS.name}")
        print(f"   Pests:  up to {DAILY_PESTS} from {QUEUE_PESTS.name}")

        plant_names = load_queue(QUEUE_PLANTS, DAILY_PLANTS)
        pest_names  = load_queue(QUEUE_PESTS, DAILY_PESTS)

        if not plant_names and not pest_names:
            print("\n  ℹ️  Both queues are empty.")
            print(f"  Add plant names to: {QUEUE_PLANTS}")
            print(f"  Add pest names to:  {QUEUE_PESTS}")
            return

        print(f"\n  Plants queued: {len(plant_names)}")
        print(f"  Pests queued:  {len(pest_names)}")

    # ── SINGLE MODE ───────────────────────────────────────────────────────────
    else:
        if not args.mode:
            parser.print_help()
            return

        # Collect names from args or file
        names = list(args.names)
        if args.file:
            fpath = Path(args.file)
            if fpath.exists():
                names += [l.strip() for l in fpath.read_text().splitlines() if l.strip()]
            else:
                print(f"❌ File not found: {args.file}")
                return

        if not names:
            print("❌ No names provided. Pass names as arguments or use --file")
            return

        if args.mode == 'plants':
            plant_names = names
        else:
            pest_names = names

    # ── PROCESS ───────────────────────────────────────────────────────────────
    if args.dry_run:
        print("\n🔍 DRY RUN — no files will be created or downloaded\n")

    done_plants = []
    done_pests = []

    if plant_names:
        print(f"\n{'='*50}")
        print(f"🌱 Processing {len(plant_names)} plants")
        print('='*50)
        done_plants = process_plants(plant_names, dry_run=args.dry_run)

    if pest_names:
        print(f"\n{'='*50}")
        print(f"🐛 Processing {len(pest_names)} pests")
        print('='*50)
        done_pests = process_pests(pest_names, dry_run=args.dry_run)

    # ── SUMMARY ───────────────────────────────────────────────────────────────
    total = len(done_plants) + len(done_pests)
    print(f"\n{'='*50}")
    print(f"✅ Done — {total} items processed")
    if done_plants:
        print(f"  Plants: {', '.join(done_plants)}")
    if done_pests:
        print(f"  Pests:  {', '.join(done_pests)}")

    if total > 0 and not args.dry_run:
        # Write Cursor Agent prompt
        write_cursor_prompt(done_plants, done_pests, prompt_path)

        print(f"""
{'='*50}
📋 NEXT STEPS
{'='*50}
1. Open Cursor in this project
2. Switch to Agent mode (not chat)
3. Paste contents of: review/cursor_agent_prompt.md
4. Let Agent enrich all NEEDS_DATA fields
5. When done, Agent will run ./sync.sh automatically
6. Review at http://localhost:4321/plants and /pests
7. Commit when satisfied:
   git add -A && git commit -m "add {total} new entries"
""")

        # Show remaining queue counts
        if QUEUE_PLANTS.exists():
            remaining = len([l for l in QUEUE_PLANTS.read_text().splitlines() if l.strip()])
            if remaining:
                print(f"  📋 {remaining} plants still in queue ({QUEUE_PLANTS.name})")
        if QUEUE_PESTS.exists():
            remaining = len([l for l in QUEUE_PESTS.read_text().splitlines() if l.strip()])
            if remaining:
                print(f"  📋 {remaining} pests still in queue ({QUEUE_PESTS.name})")


if __name__ == '__main__':
    main()
