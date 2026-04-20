#!/bin/bash
set -e
echo "📦 Installing Python dependencies..."
pip install -r requirements.txt --quiet --break-system-packages 2>/dev/null \
  || pip install -r requirements.txt --quiet

echo "🌱 Building data pipeline..."
python3 convert_permie_data.py

echo "🚀 Building Astro site..."
npx astro build
