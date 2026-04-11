#!/usr/bin/env python3
"""
PermiePortal Cleanup Script
============================
1. Removes duplicate plant YAML files (keeps most complete entry)
2. Fetches missing images from Wikimedia / iNaturalist
3. Clears broken picture fields so placeholders render instead of 404s
4. Reports everything still needing Cursor Agent enrichment

Usage:
  python3 cleanup.py              # fix everything
  python3 cleanup.py --dry-run    # report only, no changes
  python3 cleanup.py --images     # only fix missing images
  python3 cleanup.py --dupes      # only fix duplicates
"""

import json
import re
import sys
import time
import argparse
import urllib.request
import urllib.parse
from pathlib import Path
from collections import defaultdict

# ── CONFIG ────────────────────────────────────────────────────────────────────
PROJECT      = Path(__file__).parent
SEEDS_PLANTS = PROJECT / "src/seeds/plants"
SEEDS_PESTS  = PROJECT / "src/seeds/pests/pests-data.yml"
PLANT_IMAGES = PROJECT / "public/assets/plants"
PEST_IMAGES  = PROJECT / "public/assets/pests"
DATA_DIR     = PROJECT / "src/data"
# ─────────────────────────────────────────────────────────────────────────────


def slugify(text):
    text = str(text).lower().strip()
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[\s_]+', '-', text)
    return re.sub(r'-+', '-', text).strip('-')


def fetch_json(url, timeout=10):
    req = urllib.request.Request(
        url,
        headers={'User-Agent': 'PermiePortal/2.0 (permieportal.com)'}
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return json.loads(resp.read().decode('utf-8'))
    except Exception:
        return None


def download_image(url, dest_path, dry_run=False):
    if dry_run:
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
        return False


def wikimedia_image(query):
    search_url = (
        "https://commons.wikimedia.org/w/api.php?"
        "action=query&format=json&list=search"
        f"&srsearch={urllib.parse.quote(query + ' plant')}"
        "&srnamespace=6&srlimit=5"
    )
    data = fetch_json(search_url)
    if not data:
        return None

    results = data.get('query', {}).get('search', [])
    for result in results:
        title = result.get('title', '')
        if not title.startswith('File:'):
            continue
        info_url = (
            "https://commons.wikimedia.org/w/api.php?"
            "action=query&format=json&prop=imageinfo"
            "&iiprop=url|mime"
            f"&titles={urllib.parse.quote(title)}"
        )
        info = fetch_json(info_url)
        if not info:
            continue
        pages = info.get('query', {}).get('pages', {})
        for page in pages.values():
            ii = page.get('imageinfo', [{}])[0]
            if ii.get('mime', '') in ('image/jpeg', 'image/png', 'image/webp'):
                url = ii.get('url', '')
                if url:
                    return url
    return None


def inaturalist_image(query):
    url = (
        f"https://api.inaturalist.org/v1/taxa?"
        f"q={urllib.parse.quote(query)}&per_page=3"
    )
    data = fetch_json(url)
    if not data:
        return None
    for taxon in data.get('results', []):
        photo = taxon.get('default_photo')
        if photo:
            return photo.get('medium_url') or photo.get('url')
    return None


def get_image(name, mode='plant'):
    url = wikimedia_image(name)
    if url:
        return url, 'wikimedia'
    query = name
    url = inaturalist_image(query)
    if url:
        return url, 'inaturalist'
    return None, None


# ── COMPLETENESS SCORE ───────────────────────────────────────────────────────

def completeness_score(filepath):
    """
    Score a YAML file by how complete it is.
    Higher = more data filled in, fewer NEEDS_DATA fields.
    """
    try:
        content = filepath.read_text(encoding='utf-8')
        needs_data_count = content.count('NEEDS_DATA')
        total_lines = len(content.splitlines())
        # More lines + fewer NEEDS_DATA = better
        return total_lines - (needs_data_count * 10)
    except Exception:
        return -999


# ── DUPLICATE FINDER ─────────────────────────────────────────────────────────

def find_duplicates():
    """
    Find plant YAML files that produce the same slug.
    Returns dict of slug -> [list of files]
    """
    slug_map = defaultdict(list)

    for yml_file in SEEDS_PLANTS.glob("*.yml"):
        if yml_file.suffix == '.bak':
            continue
        try:
            content = yml_file.read_text(encoding='utf-8')
            # Extract common_name
            match = re.search(r'common_name:\s*(.+)', content)
            if match:
                name = match.group(1).strip().strip('"\'')
                slug = slugify(name)
                slug_map[slug].append(yml_file)
        except Exception:
            continue

    return {slug: files for slug, files in slug_map.items() if len(files) > 1}


def fix_duplicates(dry_run=False):
    """Keep most complete file, archive the rest."""
    dupes = find_duplicates()

    if not dupes:
        print("  ✅ No duplicates found")
        return 0

    fixed = 0
    archive_dir = SEEDS_PLANTS / "_archived_duplicates"

    for slug, files in dupes.items():
        # Score each file
        scored = sorted(files, key=completeness_score, reverse=True)
        keeper = scored[0]
        losers = scored[1:]

        print(f"\n  Duplicate: {slug}")
        print(f"    Keeping:  {keeper.name} (score: {completeness_score(keeper)})")

        for loser in losers:
            print(f"    Archiving: {loser.name} (score: {completeness_score(loser)})")
            if not dry_run:
                archive_dir.mkdir(exist_ok=True)
                dest = archive_dir / loser.name
                # Avoid overwriting archive
                if dest.exists():
                    dest = archive_dir / (loser.stem + '_2' + loser.suffix)
                loser.rename(dest)
            fixed += 1

    return fixed


# ── IMAGE FIXER ──────────────────────────────────────────────────────────────

def get_missing_images(dry_run=False):
    """
    Find plants with missing images and fetch them.
    Also clears broken picture fields in YAML when no image can be found.
    """
    if not DATA_DIR.joinpath('plants.json').exists():
        print("  ⚠️  src/data/plants.json not found — run ./sync.sh first")
        return 0, 0

    plants = json.loads(DATA_DIR.joinpath('plants.json').read_text())

    missing = []
    for p in plants:
        pic = p.get('picture', '')
        if pic and pic not in ('', 'NEEDS_DATA', 'NEEDS_IMAGE'):
            img_path = PLANT_IMAGES / pic
            if not img_path.exists():
                missing.append((p['common_name'], p['slug'], pic))

    print(f"  Found {len(missing)} missing plant images")

    fetched = 0
    failed = []

    for name, slug, pic in missing:
        print(f"  🔍 {name}...", end=' ', flush=True)
        img_url, source = get_image(name, mode='plant')

        if img_url:
            dest = PLANT_IMAGES / pic
            ok = download_image(img_url, dest, dry_run=dry_run)
            if ok:
                print(f"✅ ({source})")
                fetched += 1
            else:
                print(f"⚠️  download failed")
                failed.append((name, slug, pic))
        else:
            print(f"❌ not found")
            failed.append((name, slug, pic))

        time.sleep(0.4)

    # For images we couldn't find, clear the picture field in YAML
    # so the placeholder renders instead of a 404
    if failed and not dry_run:
        print(f"\n  Clearing {len(failed)} unfindable picture fields in YAML...")
        for name, slug, pic in failed:
            # Find the YAML file for this plant
            yml_candidates = list(SEEDS_PLANTS.glob(f"{slug}-data.yml"))
            if not yml_candidates:
                yml_candidates = list(SEEDS_PLANTS.glob(f"*{slug}*.yml"))

            for yml_file in yml_candidates:
                try:
                    content = yml_file.read_text(encoding='utf-8')
                    # Replace picture field with empty string
                    new_content = re.sub(
                        r'(  picture:\s*)' + re.escape(pic),
                        r'\1""',
                        content
                    )
                    if new_content != content:
                        yml_file.write_text(new_content, encoding='utf-8')
                        print(f"    Cleared picture field: {yml_file.name}")
                except Exception as e:
                    print(f"    ⚠️  Could not update {yml_file.name}: {e}")

    return fetched, len(failed)


# ── NEEDS_DATA REPORT ────────────────────────────────────────────────────────

def report_needs_data():
    """Report files still needing Cursor Agent enrichment."""
    plant_files = list(SEEDS_PLANTS.glob("*.yml"))
    plant_files = [f for f in plant_files
                   if not str(f).endswith('.bak')
                   and '_archived' not in str(f)]

    needs_enrichment = []
    complete = []

    for f in plant_files:
        try:
            content = f.read_text(encoding='utf-8')
            count = content.count('NEEDS_DATA')
            if count > 0:
                needs_enrichment.append((f.name, count))
            else:
                complete.append(f.name)
        except Exception:
            continue

    # Check pests file
    pest_needs = 0
    if SEEDS_PESTS.exists():
        pest_content = SEEDS_PESTS.read_text(encoding='utf-8')
        pest_needs = pest_content.count('NEEDS_DATA')

    return needs_enrichment, complete, pest_needs


def write_enrichment_prompt(needs_enrichment, pest_needs):
    """Write a Cursor Agent prompt for all remaining NEEDS_DATA entries."""
    review_dir = PROJECT / "review"
    review_dir.mkdir(exist_ok=True)

    # Split into chunks of 30 for manageable Agent sessions
    chunk_size = 30
    chunks = [needs_enrichment[i:i+chunk_size]
              for i in range(0, len(needs_enrichment), chunk_size)]

    prompt_files = []
    for i, chunk in enumerate(chunks, 1):
        prompt_path = review_dir / f"cursor_enrich_{i}_of_{len(chunks)}.md"

        lines = [
            f"# PermiePortal — Cursor Agent Enrichment Batch {i} of {len(chunks)}\n\n",
            "Switch to **Agent mode** before pasting this prompt.\n\n",
            "---\n\n",
            "## Task\n\n",
            "Enrich the following plant YAML files. Replace every `NEEDS_DATA` "
            "value with accurate botanical information.\n\n",
            "**Rules:**\n",
            "- Use `src/seeds/plants/moringa-data.yml` as the structure reference\n",
            "- Temperatures in Fahrenheit\n",
            "- Zones as strings like `\"9-11\"`\n",
            "- `layers` must be one of: Tree, Shrub, Herbaceous, Vine, "
            "Ground Cover, Root, Aquatic, Canopy\n",
            "- `plant_function` values must match existing entries in other seed files\n",
            "- `pests` must match slugs in `src/seeds/pests/pests-data.yml` exactly\n",
            "- Description must include propagation methods and sun/water requirements\n",
            "- North Florida / subtropical context where relevant\n",
            "- No corporate language. PermieBro voice where appropriate.\n\n",
            "## Files to Enrich\n\n",
        ]

        for fname, count in chunk:
            lines.append(f"- `src/seeds/plants/{fname}` ({count} fields need data)\n")

        if i == len(chunks) and pest_needs > 0:
            lines.append(f"\n## Also Enrich Pests\n\n")
            lines.append(
                f"`src/seeds/pests/pests-data.yml` has {pest_needs} `NEEDS_DATA` "
                f"fields. Find each entry containing `NEEDS_DATA` and replace with "
                f"accurate organic-only pest management information.\n\n"
                "**Rules for pests:**\n"
                "- Organic control methods ONLY — absolutely no synthetic pesticides\n"
                "- `control_methods` keys: organic_sprays, biological_controls, "
                "cultural_practices, mechanical_physical, preventive_methods\n"
                "- `natural_enemies` should be real biological predators\n"
                "- Descriptions should help identify the pest in the field\n\n"
            )

        lines.append("\n## When Done\n\n")
        lines.append("```bash\n./sync.sh --check\n```\n")
        lines.append("Fix any warnings, then:\n")
        lines.append("```bash\n./sync.sh\n```\n")

        prompt_path.write_text(''.join(lines))
        prompt_files.append(prompt_path)
        print(f"  📋 {prompt_path.name} ({len(chunk)} plants)")

    return prompt_files


# ── MAIN ─────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description='PermiePortal Cleanup')
    parser.add_argument('--dry-run', action='store_true',
                        help='Report only — no changes made')
    parser.add_argument('--images', action='store_true',
                        help='Only fix missing images')
    parser.add_argument('--dupes', action='store_true',
                        help='Only fix duplicates')
    args = parser.parse_args()

    do_all = not args.images and not args.dupes

    print("\n🧹 PermiePortal Cleanup")
    print("=" * 50)

    if args.dry_run:
        print("DRY RUN — no files will be changed\n")

    # ── DUPLICATES ───────────────────────────────────────────────
    if do_all or args.dupes:
        print("\n📋 Checking for duplicates...")
        fixed = fix_duplicates(dry_run=args.dry_run)
        if fixed:
            action = "Would archive" if args.dry_run else "Archived"
            print(f"\n  {action} {fixed} duplicate files")

    # ── MISSING IMAGES ───────────────────────────────────────────
    if do_all or args.images:
        print("\n🖼️  Fetching missing images...")
        fetched, failed = get_missing_images(dry_run=args.dry_run)
        print(f"\n  Fetched: {fetched}")
        print(f"  Still missing (picture field cleared): {failed}")

    # ── NEEDS_DATA REPORT ────────────────────────────────────────
    print("\n📊 Enrichment status...")
    needs_enrichment, complete, pest_needs = report_needs_data()

    print(f"  Complete plant files:     {len(complete)}")
    print(f"  Need enrichment:          {len(needs_enrichment)}")
    print(f"  Pest NEEDS_DATA fields:   {pest_needs}")

    if needs_enrichment and not args.dry_run:
        print(f"\n📋 Writing Cursor Agent prompts (batches of 30)...")
        prompt_files = write_enrichment_prompt(needs_enrichment, pest_needs)
        print(f"\n  {len(prompt_files)} prompt file(s) written to review/")

    # ── REBUILD ──────────────────────────────────────────────────
    if not args.dry_run and (do_all or args.dupes):
        print("\n🔄 Rebuilding JSON...")
        import subprocess
        result = subprocess.run(
            ['python3', 'convert_permie_data.py'],
            cwd=PROJECT,
            capture_output=True, text=True
        )
        if result.returncode == 0:
            print("  ✅ JSON rebuilt successfully")
        else:
            print(f"  ⚠️  Converter error:\n{result.stderr[:500]}")

    # ── SUMMARY ──────────────────────────────────────────────────
    print(f"\n{'='*50}")
    print("✅ Cleanup complete")
    print(f"{'='*50}")

    if needs_enrichment and not args.dry_run:
        print(f"""
Next steps:
  1. Open Cursor in Agent mode
  2. Work through review/cursor_enrich_1_of_*.md first
  3. Run each subsequent batch after the previous completes
  4. Final: ./sync.sh to rebuild everything
""")
    elif not needs_enrichment:
        print("\n🎉 All plant files are fully enriched!")
        print("   Run ./sync.sh to rebuild JSON\n")


if __name__ == '__main__':
    main()
