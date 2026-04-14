# Family Notes Generation

Add permaculture-focused notes for all remaining plant families in:
`src/pages/plants/family/[family].astro`

## Instructions

Find the `const FAMILY_NOTES` block in the file.
Add an entry for each family below using this exact format:

```typescript
  'FamilyName': {
    note: `2-3 sentence note here.`,
    wiki: `FamilyName`
  },
```

## Note Guidelines

- 2-3 sentences max
- Actionable for a grower or permaculture designer
- Focus on: guild role, soil behavior, pest pressure, companion planting, seed saving, or cautions
- No filler phrases like 'this fascinating family'
- Use backtick template literals for note values (not single quotes) to avoid apostrophe issues
- Wiki value should be the Wikipedia article slug (underscores for spaces)

## Families to Add

### Adoxaceae (16 plants)
Examples: American Elderberry, Arrowwood Viburnum, Black Elderberry

### Moraceae (15 plants)
Examples: African Breadfruit, Artocarpus species, Breadfruit

### Elaeagnaceae (15 plants)
Examples: Autumn Berry, Autumn Olive, Autumn Olive Seedless

### Annonaceae (14 plants)
Examples: Atemoya, Cherimoya, Custard Apple

### Rubiaceae (14 plants)
Examples: Blue Woodruff, Buttonbush, Firebush

### Anacardiaceae (10 plants)
Examples: Ambarella, Barbados Plum, Golden Apple

### Passifloraceae (10 plants)
Examples: Banana Passionfruit, Corkystem Passionflower, Damiana

### Fagaceae (9 plants)
Examples: Allegheny Chinquapin, Bluejack Oak, Bush Chinquapin

### Convolvulaceae (9 plants)
Examples: Beach Morning Glory, Carolina Ponysfoot, Desert Yam

### Polygonaceae (9 plants)
Examples: Buckwheat, Red Veined Sorrel, Rhubarb

### Asparagaceae (8 plants)
Examples: Agave Americana, Agave, Asparagus

### Dioscoreaceae (8 plants)
Examples: Air Potato, Bitter Yam, Chinese Yam

### Vitaceae (8 plants)
Examples: Catbird Grape, Frost Grape, Mustang Grape

### Sapindaceae (8 plants)
Examples: Chalk Maple, Florida Maple, Longan

### Amaryllidaceae (8 plants)
Examples: Chives, Garlic, Onion

### Sapotaceae (7 plants)
Examples: Abiu, Caimito, Canistel

### Amaranthaceae (7 plants)
Examples: Alternanthera, Amaranth, Brazilian Spinach

### Verbenaceae (7 plants)
Examples: Bee Bush, Blue Vervain, Frogfruit

### Oxalidaceae (7 plants)
Examples: Bilimbi, Bilimbi Tree, Carambola

### Zingiberaceae (7 plants)
Examples: Black Ginger, Butterfly Ginger, Cardamom

### Boraginaceae (7 plants)
Examples: Borage, Comfrey, Phacelia

### Crassulaceae (6 plants)
Examples: Allegheny Stonecrop, Broadleaf Stonecrop, Corsican Stonecrop

### Combretaceae (6 plants)
Examples: Beach Almond, Goat Plum, Indian Almond

### Plantaginaceae (6 plants)
Examples: Broadleaf Plantain, Buck Plantain, Hoary Plantain

### Euphorbiaceae (6 plants)
Examples: Candle Nut Tree, Cassava, Chaya

### Cannabaceae (6 plants)
Examples: Desert Hackberry, Hemp, Hop Shoots

### Pinaceae (6 plants)
Examples: Loblolly Pine, Longleaf Pine, Pond Pine

### Magnoliaceae (5 plants)
Examples: Ashe Magnolia, Bigleaf Magnolia, Southern Magnolia

### Ranunculaceae (5 plants)
Examples: Black Cohosh, Eastern Columbine, Goldenseal

### Cyperaceae (5 plants)
Examples: Chinese Water Chestnut, Giant Bulrush, Papyrus

### Caprifoliaceae (5 plants)
Examples: Coral Honeysuckle, Coralberry, Snowberry

### Aizoaceae (5 plants)
Examples: Ice plant, New Zealand Ice Plant, New Zealand Spinach

### Malpighiaceae (4 plants)
Examples: Acerola Cherry, Barbados Cherry, Murici

### Betulaceae (4 plants)
Examples: Alder, American Filbert, American Hazelnut

### Grossulariaceae (4 plants)
Examples: American Black Currant, Golden Currant, Gooseberry

### Ebenaceae (4 plants)
Examples: American Persimmon, Black Sapote, Persimmon Tree

### Nymphaeaceae (4 plants)
Examples: American Waterlily, Fragrant Waterlily, Spatterdock

### Acanthaceae (4 plants)
Examples: Andrographis, Hairy Wild Petunia, Prairie Wild Petunia

### Cupressaceae (4 plants)
Examples: Atlantic White Cedar, Bald Cypress, Pond Cypress

### Pontederiaceae (4 plants)
Examples: Blue Pickerelweed, Mud Plantain, Pickerelweed

### Campanulaceae (4 plants)
Examples: Blue Star Creeper, Cardinal Flower, Great Blue Lobelia

### Aquifoliaceae (4 plants)
Examples: Dahoon Holly, Gallberry, Inkberry

### Araliaceae (4 plants)
Examples: Marsh Pennywort, Prickly Elder, Spikenard

### Commelinaceae (4 plants)
Examples: Ohio Spiderwort, Spiderwort, Virginia Spiderwort

### Cannaceae (3 plants)
Examples: Achira, Canna Lily, Queensland Arrowroot

### Cornaceae (3 plants)
Examples: Alternate-leaf Dogwood, Roughleaf Dogwood, Swamp Dogwood

### Nelumbonaceae (3 plants)
Examples: American Lotus, Lotus, Nelumbo lutea

### Alismataceae (3 plants)
Examples: Arrowhead, Duck Potato, Water Plantain

### Marantaceae (3 plants)
Examples: Arrowroot, Calathea, Leren

### Lauraceae (3 plants)
Examples: Avocado, Sassafras, Spicebush

### Berberidaceae (3 plants)
Examples: Blue Cohosh, Mayapple, Oregon Grape

### Aristolochiaceae (3 plants)
Examples: Canadian Wild Ginger, Little Brown Jug, Wild Ginger

### Rhamnaceae (3 plants)
Examples: Carolina Buckthorn, Indian Cherry, New Jersey Tea

### Salicaceae (3 plants)
Examples: Ceylon Gooseberry Tree, Florida Willow, Osier Willow

### Meliaceae (3 plants)
Examples: Chinaberry, Neem, Neem Tree

### Cistaceae (3 plants)
Examples: Cistus, Rock Rose, Sunrose

### Zamiaceae (3 plants)
Examples: Coontie, Coontie Palm, Zamia integrifolia

### Primulaceae (3 plants)
Examples: Creeping Jenny, Marlberry, Myrsine

### Polemoniaceae (3 plants)
Examples: Creeping Phlox, Prairie Phlox, Wild Blue Phlox

### Bignoniaceae (3 plants)
Examples: Crossvine, Desert Willow, Panama Candle Tree

### Oleaceae (3 plants)
Examples: Fringe Tree, Persian Lilac, Wild Olive

### Piperaceae (3 plants)
Examples: Kava, Piper, Root Beer Plant

### Basellaceae (3 plants)
Examples: Malabar Spinach, Tropical Spinach, Ulluco

### Tropaeolaceae (3 plants)
Examples: Mashua, Nasturtium, Tuberous Nasturtium

### Apocynaceae (3 plants)
Examples: Milkweed, Natal Plum, Swamp Milkweed

### Juglandaceae (3 plants)
Examples: Pecan Tree, Scrub Hickory, Walnut Tree

### Urticaceae (3 plants)
Examples: Ramie, Stinging Nettle, Stinging Tree

### Asphodelaceae (2 plants)
Examples: Aloe, Bulbine

### Styracaceae (2 plants)
Examples: American Snowbell, Silverbell Tree

### Clusiaceae (2 plants)
Examples: Bacupari, Imbe

### Phyllanthaceae (2 plants)
Examples: Bignay, Katuk

### Lentibulariaceae (2 plants)
Examples: Bladderwort, Butterwort

### Papaveraceae (2 plants)
Examples: Bloodroot, California Poppy

### Linaceae (2 plants)
Examples: Blue Flax, Flax

### Menyanthaceae (2 plants)
Examples: Bog Bean, Floating Heart

### Menispermaceae (2 plants)
Examples: Carolina Snailseed, Moonseed Vine

### Blechnaceae (2 plants)
Examples: Chain Fern, Netted Chain Fern

### Osmundaceae (2 plants)
Examples: Cinnamon Fern, Royal Fern

### Montiaceae (2 plants)
Examples: Western miner's lettuce, Miner's Lettuce

### Sarraceniaceae (2 plants)
Examples: Cobra Lily, Pitcher Plant

### Chrysobalaceae (2 plants)
Examples: Coco Plum, Gopher Apple

### Onagraceae (2 plants)
Examples: Fireweed, Gaura

### Thelypteridaceae (2 plants)
Examples: Marsh Fern, Southern Shield Fern

### Pandanaceae (2 plants)
Examples: Pandanus, Screw Pine

### Portulacaceae (2 plants)
Examples: Piedmont Purslane, Purslane

### Droseraceae (2 plants)
Examples: Sundew, Venus Flytrap

### Myricaceae (2 plants)
Examples: Sweet Gale, Wax Myrtle

### Calophyllaceae (1 plants)
Examples: Bacuri

### Musaceae (1 plants)
Examples: Banana

### Strelitziaceae (1 plants)
Examples: Bird of Paradise

### Iridaceae (1 plants)
Examples: Blue Flag Iris

### Dennstaedtiaceae (1 plants)
Examples: Bracken Fern

### Lecythidaceae (1 plants)
Examples: Cannonball Tree

### Typhaceae (1 plants)
Examples: Cattail

### Hymenochaetaceae (1 plants)
Examples: Chaga Host

### Fomitopsidaceae (1 plants)
Examples: Chicken of the Woods Host

### Caryophyllaceae (1 plants)
Examples: Chickweed

### Cordycipitaceae (1 plants)
Examples: Cordyceps Host

### Zygophyllaceae (1 plants)
Examples: Desert Date

### Aspleniaceae (1 plants)
Examples: Ebony Spleenwort

### Dilleniaceae (1 plants)
Examples: Elephant Apple

### Saururaceae (1 plants)
Examples: Fish Mint

### Schisandraceae (1 plants)
Examples: Florida Anise

### Celastraceae (1 plants)
Examples: Florida Boxwood

### Gnetaceae (1 plants)
Examples: Gnetum

### Chrysobalanaceae (1 plants)
Examples: Gopher Tortoise Burrow Plants

### Podocarpaceae (1 plants)
Examples: Illawarra Plum

### Liliaceae (1 plants)
Examples: Indian Cucumber Root

### Simmondsiaceae (1 plants)
Examples: Jojoba

### Dryopteridaceae (1 plants)
Examples: Leatherleaf Fern

### Hericiaceae (1 plants)
Examples: Lion's Mane Host

### Orchidaceae (1 plants)
Examples: Madagascar Vanilla

### Pteridaceae (1 plants)
Examples: Maidenhair Fern

### Meripilaceae (1 plants)
Examples: Maitake Host

### Mazaceae (1 plants)
Examples: Mazus

### Araucariaceae (1 plants)
Examples: Monkey Puzzle Tree

### Moringaceae (1 plants)
Examples: Moringa

### Nepenthaceae (1 plants)
Examples: Nepenthes

### Onocleaceae (1 plants)
Examples: Ostrich Fern

### Pleurotaceae (1 plants)
Examples: Oyster Mushroom Host

### Caricaceae (1 plants)
Examples: Papaya

### Bromeliaceae (1 plants)
Examples: Pineapple

### Lythraceae (1 plants)
Examples: Pomegranate Tree

### Costaceae (1 plants)
Examples: Red Button Ginger

### Ganodermataceae (1 plants)
Examples: Reishi Host

### Polypodiaceae (1 plants)
Examples: Resurrection Fern

### Cycadaceae (1 plants)
Examples: Sago Palm

### Bataceae (1 plants)
Examples: Saltwort

### Plumbaginaceae (1 plants)
Examples: Sea Lavender

### Omphalotaceae (1 plants)
Examples: Shiitake Oak

### Proteaceae (1 plants)
Examples: Silk Oak

### Acoraceae (1 plants)
Examples: Sweet Flag

### Tamaricaceae (1 plants)
Examples: Tamarisk

### Polyporaceae (1 plants)
Examples: Turkey Tail Host

### Cabombaceae (1 plants)
Examples: Watershield

### Strophariaceae (1 plants)
Examples: Wine Cap Substrate

### Gelsemiaceae (1 plants)
Examples: Yellow Jessamine

## When Done

```bash
npm run build
```

Verify build succeeds, then:

```bash
git add -A
git commit -m "Add permaculture notes for all 137 plant families"
```
