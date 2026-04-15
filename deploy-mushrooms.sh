#!/bin/bash
# deploy-mushrooms.sh
# Run from: ~/apps/permieportal
# Usage: bash deploy-mushrooms.sh /path/to/new-ymls/

set -e

SEEDS="src/seeds/plants"
NEW_FILES="${1:-.}"  # pass the folder where you dropped the new ymls

echo "=== Mushroom YML Deploy ==="
echo "Seeds dir: $SEEDS"
echo "New files from: $NEW_FILES"
echo ""

# 1. Delete the meta-placeholder
if [ -f "$SEEDS/mushroom-hosts-data.yml" ]; then
  rm "$SEEDS/mushroom-hosts-data.yml"
  echo "✓ Deleted mushroom-hosts-data.yml"
else
  echo "- mushroom-hosts-data.yml already gone, skipping"
fi

# 2. Delete the old chicken-of-the-woods-host file (replaced by new name)
if [ -f "$SEEDS/chicken-of-the-woods-host-data.yml" ]; then
  rm "$SEEDS/chicken-of-the-woods-host-data.yml"
  echo "✓ Deleted chicken-of-the-woods-host-data.yml"
else
  echo "- chicken-of-the-woods-host-data.yml already gone, skipping"
fi

# 3. Copy all new yml files into seeds
for f in \
  chaga-data.yml \
  chicken-of-the-woods-data.yml \
  cordyceps-data.yml \
  lions-mane-data.yml \
  maitake-data.yml \
  oyster-mushroom-data.yml \
  reishi-data.yml \
  shiitake-data.yml \
  turkey-tail-data.yml \
  wine-cap-data.yml; do
  if [ -f "$NEW_FILES/$f" ]; then
    cp "$NEW_FILES/$f" "$SEEDS/$f"
    echo "✓ Deployed $f"
  else
    echo "✗ MISSING: $NEW_FILES/$f — skipped"
  fi
done

# 4. Rename the chicken-of-the-woods image if old name still exists
IMG_DIR="public/assets/plants"
if [ -f "$IMG_DIR/chicken_of_the_woods_host.webp" ] && [ ! -f "$IMG_DIR/chicken_of_the_woods.webp" ]; then
  mv "$IMG_DIR/chicken_of_the_woods_host.webp" "$IMG_DIR/chicken_of_the_woods.webp"
  echo "✓ Renamed chicken_of_the_woods_host.webp → chicken_of_the_woods.webp"
elif [ -f "$IMG_DIR/chicken_of_the_woods.webp" ]; then
  echo "- chicken_of_the_woods.webp already exists, skipping rename"
else
  echo "! chicken_of_the_woods_host.webp not found — check $IMG_DIR manually"
fi

# 5. Orphan the mushroom_hosts image (move to _archived or delete)
if [ -f "$IMG_DIR/mushroom_hosts.webp" ]; then
  mkdir -p "$IMG_DIR/_archived"
  mv "$IMG_DIR/mushroom_hosts.webp" "$IMG_DIR/_archived/mushroom_hosts.webp"
  echo "✓ Archived mushroom_hosts.webp → $IMG_DIR/_archived/"
else
  echo "- mushroom_hosts.webp already gone, skipping"
fi

echo ""
echo "=== Done. Run your sync/build pipeline next. ==="
