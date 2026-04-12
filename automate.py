#!/usr/bin/env python3
"""
PermiePortal Plant & Pest Automation v4
========================================
Changes in v4:
- Americas-wide geographic framing (zones 3-13)
- Cursor prompts include validate.py mandatory workflow
- Prompt files include rm cleanup instruction for Agent
- Temperatures: Fahrenheit with Celsius in parentheses
- cautions field in stubs (not avoid)

Usage:
  python3 automate.py plants "Chaya" "Lemon Verbena"
  python3 automate.py pests "Squash Vine Borer" "Stink Bug"
  python3 automate.py plants --file queue_plants.txt
  python3 automate.py pests --file queue_pests.txt
  python3 automate.py --daily
  python3 automate.py --dry-run plants "Moringa"
  python3 automate.py --prompt-only
"""

import json
import re
import sys
import time
import argparse
import urllib.request
import urllib.parse
from pathlib import Path

# ── CONFIG ────────────────────────────────────────────────────────────────────
PROJECT      = Path(__file__).parent
SEEDS_PLANTS = PROJECT / "src/seeds/plants"
SEEDS_PESTS  = PROJECT / "src/seeds/pests"
PESTS_FILE   = SEEDS_PESTS / "pests-data.yml"
PLANT_IMAGES = PROJECT / "public/assets/plants"
PEST_IMAGES  = PROJECT / "public/assets/pests"
QUEUE_PLANTS = PROJECT / "queue_plants.txt"
QUEUE_PESTS  = PROJECT / "queue_pests.txt"
REVIEW_DIR   = PROJECT / "review"
DAILY_PLANTS = 20
DAILY_PESTS  = 999
PROMPT_CHUNK = 20
# ─────────────────────────────────────────────────────────────────────────────


# ── NAME VALIDATION ──────────────────────────────────────────────────────────

INVALID_PATTERNS = [
    r'^#',
    r'^-{2,}',
    r'──',
    r'^Add to',
    r'^\d{2,}',
    r'queue_plants',
    r'queue_pests',
    r'\.txt$',
    r'\.yml$',
    r'\.py$',
    r'Focus$',
    r'^(Canopy Trees|Shrubs|Herbaceous|Vines|Ground Covers|Roots|'
    r'Nitrogen Fix|Dynamic Acc|Pollinator|Mushroom|Fiber|Medicinal|'
    r'Rare Tropical|Native|Subtropical|Water|Understud|Industrial)',
]

VALID_NAME_RE = re.compile(r"^[A-Z][a-zA-Z\s\-\'\.]{1,49}$")


def is_valid_name(line):
    line = line.strip()
    if not line:
        return False
    for pattern in INVALID_PATTERNS:
        if re.search(pattern, line, re.IGNORECASE):
            return False
    if not VALID_NAME_RE.match(line):
        return False
    if len(line) > 50:
        return False
    return True


def validate_names(names, source="input"):
    valid, rejected = [], []
    for name in names:
        name = name.strip()
        if is_valid_name(name):
            valid.append(name)
        elif name:
            rejected.append(name)
    if rejected:
        print(f"  ⚠️  Rejected {len(rejected)} invalid entries from {source}:")
        for r in rejected[:10]:
            print(f"    ✗ {r!r}")
        if len(rejected) > 10:
            print(f"    ... and {len(rejected) - 10} more")
    return valid


# ── HELPERS ──────────────────────────────────────────────────────────────────

def slugify(text):
    text = str(text).lower().strip()
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[\s_]+', '-', text)
    return re.sub(r'-+', '-', text).strip('-')


def picture_name(name):
    return slugify(name).replace('-', '_') + '.jpg'


def fetch_json(url, timeout=10):
    req = urllib.request.Request(
        url,
        headers={'User-Agent': 'PermiePortal/2.0 (permieportal.com; botanical database)'}
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return json.loads(resp.read().decode('utf-8'))
    except Exception:
        return None


def download_image(url, dest_path, dry_run=False):
    if dry_run:
        print(f"    [DRY RUN] Would download: {url}")
        return True
    try:
        req = urllib.request.Request(
            url, headers={'User-Agent': 'PermiePortal/2.0 (permieportal.com)'}
        )
        with urllib.request.urlopen(req, timeout=15) as resp:
            dest_path.parent.mkdir(parents=True, exist_ok=True)
            dest_path.write_bytes(resp.read())
        return True
    except Exception as e:
        print(f"    ⚠️  Download failed: {e}")
        return False


# ── IMAGE SOURCES ─────────────────────────────────────────────────────────────

def wikimedia_image(query):
    search_url = (
        "https://commons.wikimedia.org/w/api.php?"
        "action=query&format=json&list=search"
        f"&srsearch={urllib.parse.quote(query + ' plant')}"
        "&srnamespace=6&srlimit=5"
    )
    data = fetch_json(search_url)
    if not data:
        return None, None
    for result in data.get('query', {}).get('search', []):
        title = result.get('title', '')
        if not title.startswith('File:'):
            continue
        info_url = (
            "https://commons.wikimedia.org/w/api.php?"
            "action=query&format=json&prop=imageinfo"
            "&iiprop=url|extmetadata|mime"
            f"&titles={urllib.parse.quote(title)}"
        )
        info = fetch_json(info_url)
        if not info:
            continue
        for page in info.get('query', {}).get('pages', {}).values():
            ii = page.get('imageinfo', [{}])[0]
            if ii.get('mime', '') not in ('image/jpeg', 'image/png', 'image/webp'):
                continue
            url = ii.get('url', '')
            if not url:
                continue
            meta = ii.get('extmetadata', {})
            license_short = meta.get('LicenseShortName', {}).get('value', 'Unknown')
            artist = re.sub(
                r'<[^>]+>', '',
                meta.get('Artist', {}).get('value', 'Unknown')
            ).strip()
            return url, f"{artist} / Wikimedia Commons / {license_short}"
    return None, None


def inaturalist_image(query):
    data = fetch_json(
        f"https://api.inaturalist.org/v1/taxa?"
        f"q={urllib.parse.quote(query)}&per_page=3"
    )
    if not data:
        return None, None
    for taxon in data.get('results', []):
        photo = taxon.get('default_photo')
        if photo:
            url = photo.get('medium_url') or photo.get('url')
            if url:
                return url, photo.get('attribution', 'iNaturalist')
    return None, None


def get_best_image(name, mode='plant', dry_run=False):
    print(f"  🔍 {name}...", end=' ', flush=True)
    url, attr = wikimedia_image(name)
    if url:
        print("✅ Wikimedia")
        return url, attr, 'wikimedia'
    url, attr = inaturalist_image(name)
    if url:
        print("✅ iNaturalist")
        return url, attr, 'inaturalist'
    print("⚠️  no image found")
    return None, None, None


# ── YAML STUBS ────────────────────────────────────────────────────────────────

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
  cautions:
  - NEEDS_DATA
  practitioner_notes: "NEEDS_DATA — unique facts, real-world observations, surprising uses"
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


def plant_slug_exists(slug):
    for pattern in [f"{slug}-data.yml", f"{slug}.yml"]:
        if (SEEDS_PLANTS / pattern).exists():
            return True
    archived = SEEDS_PLANTS / "_archived_duplicates"
    if archived.exists():
        for pattern in [f"{slug}-data.yml", f"{slug}.yml"]:
            if (archived / pattern).exists():
                return True
    return False


def generate_plant_stub(name, attribution, source):
    slug = slugify(name)
    if plant_slug_exists(slug):
        print(f"  ⏭️  Skipping {name} — already exists")
        return None
    pic = picture_name(name)
    filepath = SEEDS_PLANTS / f"{slug}-data.yml"
    content = PLANT_STUB.format(
        common_name=name, picture=pic,
        attribution=attribution or 'No image found',
        source=source or 'none',
    )
    return filepath, content


def generate_pest_stub(name, attribution, source):
    if PESTS_FILE.exists():
        existing = PESTS_FILE.read_text()
        if f'name: "{name}"' in existing or f"name: '{name}'" in existing:
            print(f"  ⏭️  Skipping {name} — already exists")
            return None
    slug = slugify(name)
    pic = picture_name(name)
    return PEST_STUB.format(
        name=name, slug=slug, picture=pic,
        attribution=attribution or 'No image found',
        source=source or 'none',
    )


# ── CURSOR PROMPT GENERATOR ──────────────────────────────────────────────────

def scan_all_needs_data():
    needs = []
    if SEEDS_PLANTS.exists():
        for yml in sorted(SEEDS_PLANTS.glob("*.yml")):
            if '_archived' in str(yml):
                continue
            try:
                content = yml.read_text(encoding='utf-8')
                count = content.count('NEEDS_DATA')
                if count > 0:
                    needs.append((yml.name, count))
            except Exception:
                continue

    pest_count = 0
    if PESTS_FILE.exists():
        pest_count = PESTS_FILE.read_text(encoding='utf-8').count('NEEDS_DATA')

    return sorted(needs, key=lambda x: x[1], reverse=True), pest_count


def write_cursor_prompts():
    REVIEW_DIR.mkdir(exist_ok=True)

    for f in REVIEW_DIR.glob("cursor_enrich_*.md"):
        f.unlink()

    needs, pest_needs = scan_all_needs_data()

    if not needs and pest_needs == 0:
        print("  ✅ All seeds fully enriched — no NEEDS_DATA found")
        return []

    total_plants = len(needs)
    chunks = [needs[i:i+PROMPT_CHUNK] for i in range(0, len(needs), PROMPT_CHUNK)]
    num_chunks = len(chunks)

    prompt_files = []
    for i, chunk in enumerate(chunks, 1):
        filename = f"cursor_enrich_{i}_of_{num_chunks}.md"
        prompt_path = REVIEW_DIR / filename

        lines = [
            f"# PermiePortal — Enrichment Batch {i} of {num_chunks}\n\n",
            "> **Agent mode only.** ONE session at a time.\n",
            f"> This batch: {len(chunk)} plants. ",
            f"Total remaining: {total_plants} plants + {pest_needs} pest fields.\n\n",
            "---\n\n",
            "## Reference\n\n",
            "Use `src/seeds/plants/moringa-data.yml` as the quality standard.\n\n",
            "---\n\n",
            "## Geographic Context\n\n",
            "**Audience: All of the Americas — zones 3–13**\n",
            "- Do NOT write 'North Florida' or any single state/region framing\n",
            "- Use universal climate language: 'temperate', 'subtropical', 'tropical'\n",
            "- Use 'wet season / dry season' not 'spring / fall' where relevant\n",
            "- Temperatures: Fahrenheit with Celsius in parentheses — 32°F (0°C)\n\n",
            "---\n\n",
            "## Standards\n\n",
            "**description** (min 400 chars):\n",
            "1. What the plant is, origin, appearance, mature size\n",
            "2. ☀️💧 Sun and Water Requirements\n",
            "3. ✂️ Propagation (2+ methods with timing)\n",
            "4. 🌾 Harvest / Best Use Timing\n\n",
            "**purpose** — explain HOW each function works in a permaculture system\n\n",
            "**companions** — min 3 specific species with reason WHY\n",
            "NOT categories like 'nitrogen-fixing plants' or 'legumes'\n\n",
            "**cautions** — antagonistic plants OR growing condition warnings (both valid)\n",
            "'None documented' acceptable if genuinely true\n\n",
            "**plant_function** — min 3 from:\n",
            "Edible, Medicinal, Nitrogen Fixer, Dynamic Accumulator, Mulcher,\n",
            "Pollinator, Wildlife Attractor, Erosion Control, Animal Fodder,\n",
            "Windbreaker, Border Plant, Pest Management, Ground Cover,\n",
            "Shade Provider, Water Retention, Fiber, Biomass, Aquatic, Ornamental\n\n",
            "**pests** — ONLY names verbatim from `src/seeds/pests/pests-data.yml`\n",
            "grep to confirm before adding. Min 2 cultivated plants. [] for specialists.\n",
            "NEVER: None, NEEDS_DATA, or animals without pest profiles\n\n",
            "---\n\n",
            "## Plants to Enrich\n\n",
        ]

        for fname, count in chunk:
            lines.append(f"- `src/seeds/plants/{fname}` ({count} fields)\n")

        if i == num_chunks and pest_needs > 0:
            lines.append(f"\n## Pests to Enrich\n\n")
            lines.append(
                f"`src/seeds/pests/pests-data.yml` — {pest_needs} NEEDS_DATA fields\n\n"
                "Find every entry with NEEDS_DATA and replace with accurate data.\n\n"
                "Pest rules:\n"
                "- Organic controls ONLY — no synthetic pesticides ever\n"
                "- control_methods: organic_sprays, biological_controls,\n"
                "  cultural_practices, mechanical_physical, preventive_methods\n"
                "- natural_enemies: real predators/parasitoids only\n\n"
            )

        lines.append("---\n\n## When Done\n\n```bash\n")
        lines.append("python3 validate.py --since 2h\n")
        lines.append("python3 validate.py --fix --since 2h\n")
        lines.append("./sync.sh --check\n")
        lines.append("./sync.sh\n")
        lines.append(f"rm review/{filename}\n")
        lines.append("```\n\n")
        lines.append("Zero warnings required before the next batch.\n\n")

        if i < num_chunks:
            lines.append(f"Next: `cursor_enrich_{i+1}_of_{num_chunks}.md`\n")
        else:
            lines.append("✅ Final batch — commit:\n")
            lines.append("```bash\ngit add -A && git commit -m 'enrichment complete'\n```\n")

        prompt_path.write_text(''.join(lines))
        prompt_files.append(prompt_path)

    print(f"\n📋 {num_chunks} prompt file(s) in review/")
    print(f"   {total_plants} plants + {pest_needs} pest fields need enrichment")
    print(f"   Start: review/cursor_enrich_1_of_{num_chunks}.md")
    print(f"   Sequential only — one Agent session per file\n")

    return prompt_files


# ── PROCESSORS ────────────────────────────────────────────────────────────────

def process_plants(names, dry_run=False):
    SEEDS_PLANTS.mkdir(parents=True, exist_ok=True)
    PLANT_IMAGES.mkdir(parents=True, exist_ok=True)
    processed = []
    for name in names:
        name = name.strip()
        if not name:
            continue
        print(f"\n🌱 {name}")
        img_url, attribution, source = get_best_image(name, dry_run=dry_run)
        pic = picture_name(name)
        img_dest = PLANT_IMAGES / pic
        if img_url and not img_dest.exists():
            ok = download_image(img_url, img_dest, dry_run=dry_run)
            if ok and not dry_run:
                print(f"    💾 {pic}")
        elif img_dest.exists():
            print(f"    ⏭️  image exists")
        result = generate_plant_stub(name, attribution, source)
        if result:
            filepath, content = result
            if not dry_run:
                filepath.write_text(content)
                print(f"    📝 {filepath.name}")
            else:
                print(f"    [DRY RUN] would create {filepath.name}")
            processed.append(name)
        time.sleep(0.5)
    return processed


def process_pests(names, dry_run=False):
    SEEDS_PESTS.mkdir(parents=True, exist_ok=True)
    PEST_IMAGES.mkdir(parents=True, exist_ok=True)
    processed = []
    new_stubs = []
    for name in names:
        name = name.strip()
        if not name:
            continue
        print(f"\n🐛 {name}")
        img_url, attribution, source = get_best_image(name, mode='pest', dry_run=dry_run)
        pic = picture_name(name)
        img_dest = PEST_IMAGES / pic
        if img_url and not img_dest.exists():
            ok = download_image(img_url, img_dest, dry_run=dry_run)
            if ok and not dry_run:
                print(f"    💾 {pic}")
        elif img_dest.exists():
            print(f"    ⏭️  image exists")
        result = generate_pest_stub(name, attribution, source)
        if result:
            new_stubs.append(result)
            processed.append(name)
            if not dry_run:
                print(f"    📝 queued")
        time.sleep(0.5)
    if new_stubs and not dry_run:
        with open(PESTS_FILE, 'a', encoding='utf-8') as f:
            f.write('\n')
            for stub in new_stubs:
                f.write(stub)
        print(f"\n  ✅ Appended {len(new_stubs)} pest stubs")
    return processed


def load_queue(filepath, limit):
    if not filepath.exists():
        return []
    raw = [l.strip() for l in filepath.read_text().splitlines()]
    valid = validate_names(raw, source=filepath.name)
    batch = valid[:limit]
    remaining = valid[limit:]
    filepath.write_text('\n'.join(remaining) + ('\n' if remaining else ''))
    return batch


# ── MAIN ─────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description='PermiePortal Automation v4')
    parser.add_argument('mode', nargs='?', choices=['plants', 'pests'])
    parser.add_argument('names', nargs='*')
    parser.add_argument('--file', '-f')
    parser.add_argument('--daily', action='store_true')
    parser.add_argument('--dry-run', action='store_true')
    parser.add_argument('--prompt-only', action='store_true',
                        help='Regenerate Cursor Agent prompts without processing')
    args = parser.parse_args()

    REVIEW_DIR.mkdir(exist_ok=True)

    if args.prompt_only:
        print("\n📋 Scanning all seeds for NEEDS_DATA...")
        write_cursor_prompts()
        return

    plant_names = []
    pest_names = []

    if args.daily:
        print(f"\n📅 Daily batch ({DAILY_PLANTS} plants / {DAILY_PESTS} pests)")
        plant_names = load_queue(QUEUE_PLANTS, DAILY_PLANTS)
        pest_names  = load_queue(QUEUE_PESTS, DAILY_PESTS)
        if not plant_names and not pest_names:
            print("\n  ℹ️  Queues empty.")
            write_cursor_prompts()
            return
        print(f"  Plants: {len(plant_names)}, Pests: {len(pest_names)}")
    else:
        if not args.mode:
            parser.print_help()
            return
        names = list(args.names)
        if args.file:
            fpath = Path(args.file)
            if fpath.exists():
                raw = [l.strip() for l in fpath.read_text().splitlines()]
                names += raw
            else:
                print(f"❌ File not found: {args.file}")
                return
        names = validate_names(names, source=args.file or "arguments")
        if not names:
            print("❌ No valid names provided.")
            return
        if args.mode == 'plants':
            plant_names = names
        else:
            pest_names = names

    if args.dry_run:
        print("\n🔍 DRY RUN — no files created\n")

    done_plants, done_pests = [], []

    if plant_names:
        print(f"\n{'='*50}\n🌱 {len(plant_names)} plants\n{'='*50}")
        done_plants = process_plants(plant_names, dry_run=args.dry_run)

    if pest_names:
        print(f"\n{'='*50}\n🐛 {len(pest_names)} pests\n{'='*50}")
        done_pests = process_pests(pest_names, dry_run=args.dry_run)

    total = len(done_plants) + len(done_pests)
    print(f"\n{'='*50}\n✅ {total} processed\n{'='*50}")

    if not args.dry_run:
        write_cursor_prompts()

        for label, qfile in [("plants", QUEUE_PLANTS), ("pests", QUEUE_PESTS)]:
            if qfile.exists():
                remaining = sum(
                    1 for l in qfile.read_text().splitlines()
                    if is_valid_name(l.strip())
                )
                if remaining:
                    print(f"  📋 {remaining} {label} still in queue")


if __name__ == '__main__':
    main()
