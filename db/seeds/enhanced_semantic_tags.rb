# frozen_string_literal: true
# Enhanced Semantic Tags for Plant Database
# This file creates comprehensive semantic tags for better plant categorization and search

puts 'Creating enhanced semantic tags...'

# Define all enhanced semantic tags with categories and descriptions
enhanced_tags = [
  # Growth characteristics
  { name: 'fast_growing', category: 'growth', description: 'Plants that grow rapidly and establish quickly' },
  { name: 'slow_growing', category: 'growth', description: 'Plants that grow slowly and take time to establish' },
  { name: 'compact', category: 'size', description: 'Small, dwarf, or miniature plants suitable for small spaces' },
  { name: 'spreading', category: 'growth', description: 'Plants that spread via runners, rhizomes, or stolons' },
  { name: 'climbing', category: 'growth', description: 'Vines and climbing plants that need support' },
  { name: 'trailing', category: 'growth', description: 'Plants with trailing or cascading growth habit' },

  # Seasonal characteristics
  { name: 'spring_blooming', category: 'seasonal', description: 'Plants that bloom in spring (March-May)' },
  { name: 'summer_blooming', category: 'seasonal', description: 'Plants that bloom in summer (June-August)' },
  { name: 'fall_blooming', category: 'seasonal', description: 'Plants that bloom in fall (September-November)' },
  { name: 'winter_blooming', category: 'seasonal', description: 'Plants that bloom in winter (December-February)' },
  { name: 'long_blooming', category: 'seasonal', description: 'Plants with extended or continuous blooming period' },

  # Environmental adaptations
  { name: 'shade_tolerant', category: 'environmental', description: 'Plants that can grow in partial to full shade' },
  { name: 'sun_loving', category: 'environmental', description: 'Plants that prefer full sun conditions' },
  { name: 'wind_resistant', category: 'environmental', description: 'Plants that can withstand windy conditions' },
  { name: 'salt_tolerant', category: 'environmental', description: 'Plants that can tolerate salt spray or saline conditions' },
  { name: 'heat_tolerant', category: 'environmental', description: 'Plants that can withstand high temperatures' },
  { name: 'frost_tolerant', category: 'environmental', description: 'Plants that can survive frost and freezing temperatures' },
  { name: 'drought_tolerant', category: 'environmental', description: 'Plants that can survive with minimal water once established' },

  # Soil preferences
  { name: 'clay_tolerant', category: 'soil', description: 'Plants that can grow in heavy clay soils' },
  { name: 'sandy_soil', category: 'soil', description: 'Plants that prefer well-draining sandy soils' },
  { name: 'wet_soil', category: 'soil', description: 'Plants that prefer consistently moist or wet soils' },
  { name: 'alkaline_soil', category: 'soil', description: 'Plants that prefer alkaline (high pH) soils' },
  { name: 'acidic_soil', category: 'soil', description: 'Plants that prefer acidic (low pH) soils' },

  # Wildlife value
  { name: 'butterfly_attractor', category: 'wildlife', description: 'Plants that attract butterflies and moths' },
  { name: 'bee_friendly', category: 'wildlife', description: 'Plants that provide nectar and pollen for bees' },
  { name: 'bird_food', category: 'wildlife', description: 'Plants that provide seeds, berries, or fruits for birds' },
  { name: 'hummingbird', category: 'wildlife', description: 'Plants that attract hummingbirds with nectar-rich flowers' },

  # Maintenance
  { name: 'low_maintenance', category: 'care', description: 'Plants that require minimal care once established' },
  { name: 'high_maintenance', category: 'care', description: 'Plants that require regular attention and care' },

  # Special features
  { name: 'fragrant', category: 'features', description: 'Plants with fragrant flowers, foliage, or other parts' },
  { name: 'colorful_foliage', category: 'features', description: 'Plants with colorful or variegated foliage' },
  { name: 'interesting_bark', category: 'features', description: 'Plants with attractive or unusual bark texture' },
  { name: 'autumn_color', category: 'features', description: 'Plants that provide good fall color' },

  # Uses
  { name: 'cut_flower', category: 'use', description: 'Plants suitable for cut flower arrangements' },
  { name: 'dried_flower', category: 'use', description: 'Plants suitable for dried flower arrangements' },
  { name: 'hedge_plant', category: 'use', description: 'Plants suitable for hedges and screens' },
  { name: 'specimen_plant', category: 'use', description: 'Plants suitable as focal points or specimens' },
  { name: 'mass_planting', category: 'use', description: 'Plants suitable for mass plantings or drifts' },

  # Edible specifics
  { name: 'fruit_tree', category: 'edible', description: 'Trees that produce edible fruits' },
  { name: 'nut_tree', category: 'edible', description: 'Trees that produce edible nuts' },
  { name: 'herb', category: 'edible', description: 'Plants used for culinary seasoning and flavoring' },
  { name: 'vegetable', category: 'edible', description: 'Plants grown for edible leaves, stems, or roots' },
  { name: 'tea_plant', category: 'edible', description: 'Plants used to make herbal teas and tisanes' },

  # Medicinal specifics
  { name: 'anti_inflammatory', category: 'medicinal', description: 'Plants with anti-inflammatory properties' },
  { name: 'digestive', category: 'medicinal', description: 'Plants that aid digestion and stomach health' },
  { name: 'respiratory', category: 'medicinal', description: 'Plants that support respiratory health' },
  { name: 'skin_care', category: 'medicinal', description: 'Plants used for skin care and wound healing' },

  # Permaculture functions
  { name: 'windbreak', category: 'permaculture', description: 'Plants suitable for wind protection and shelter' },
  { name: 'erosion_control', category: 'permaculture', description: 'Plants that help prevent soil erosion' },
  { name: 'living_mulch', category: 'permaculture', description: 'Ground cover plants that suppress weeds' },
  { name: 'chop_and_drop', category: 'permaculture', description: 'Plants suitable for biomass and mulch production' },
  { name: 'pioneer_species', category: 'permaculture', description: 'Plants that improve disturbed or poor soils' },

  # Problem indicators
  { name: 'invasive_potential', category: 'caution', description: 'Plants that may become invasive in some regions' },
  { name: 'toxic', category: 'caution', description: 'Plants that are toxic or poisonous' },
  { name: 'thorny', category: 'caution', description: 'Plants with thorns, spines, or prickles' },

  # Special growing conditions
  { name: 'greenhouse', category: 'growing', description: 'Plants suitable for greenhouse or indoor growing' },
  { name: 'aquatic', category: 'growing', description: 'Plants that grow in water or very wet conditions' },
  { name: 'epiphytic', category: 'growing', description: 'Plants that grow on other plants (air plants)' },
  { name: 'succulent', category: 'growing', description: 'Plants with fleshy, water-storing tissues' },

  # Original high-value tags
  { name: 'aromatic', category: 'features', description: 'Plants with aromatic foliage or flowers' },
  { name: 'evergreen', category: 'seasonal', description: 'Plants that retain foliage year-round' },
  { name: 'deciduous', category: 'seasonal', description: 'Plants that lose leaves seasonally' },
  { name: 'container_suitable', category: 'growing', description: 'Plants suitable for container growing' },
  { name: 'deer_resistant', category: 'wildlife', description: 'Plants that deer typically avoid eating' },
  { name: 'cold_hardy', category: 'environmental', description: 'Plants that can survive cold winters' },
  { name: 'self_seeding', category: 'growth', description: 'Plants that readily self-seed and naturalize' },
  { name: 'invasive', category: 'caution', description: 'Plants that spread aggressively and may be problematic' },
  { name: 'native', category: 'origin', description: 'Plants native to the local region' },
  { name: 'tropical', category: 'origin', description: 'Plants from tropical regions requiring warm conditions' }
]

# Create or update each semantic tag
created_count = 0
updated_count = 0

enhanced_tags.each do |tag_data|
  tag = SemanticTag.find_or_initialize_by(name: tag_data[:name])

  if tag.new_record?
    tag.assign_attributes(tag_data)
    tag.save!
    created_count += 1
    puts "✓ Created: #{tag_data[:name]} (#{tag_data[:category]})"
  else
    # Update existing tag if needed
    if tag.category != tag_data[:category] || tag.description != tag_data[:description]
      tag.update!(
        category: tag_data[:category],
        description: tag_data[:description]
      )
      updated_count += 1
      puts "↻ Updated: #{tag_data[:name]} (#{tag_data[:category]})"
    end
  end
end

puts "\nEnhanced semantic tags setup completed!"
puts "Created: #{created_count} new tags"
puts "Updated: #{updated_count} existing tags"
puts "Total enhanced tags: #{enhanced_tags.count}"

# Show tag distribution by category
puts "\nTag distribution by category:"
SemanticTag.group(:category).count.sort.each do |category, count|
  puts "  #{category}: #{count} tags"
end

def create_plant_semantic_tag_associations
  puts 'Creating plant-semantic tag associations...'

  # Manual tagging for edible plants
  edible_plant_names = [
    'Tomato', 'Carrot', 'Broccoli', 'Asparagus', 'Avocado',
    'Blueberry', 'Coconut Tree', 'Banana', 'Almond Tree', 'Bok Choy'
  ]

  edible_plants = EnhancedPlant.where(common_name: edible_plant_names)
  edible_tag = SemanticTag.find_by(name: 'edible')

  if edible_tag
    edible_plants.each do |plant|
      PlantSemanticTag.find_or_create_by(
        enhanced_plant: plant,
        semantic_tag: edible_tag
      ) do |pst|
        pst.confidence_score = 0.9
        pst.source = 'manual'
      end
    end
    puts "Tagged #{edible_plants.count} plants as edible"
  end

  # Manual tagging for medicinal plants
  medicinal_plant_names = [
    'Aloe', 'Chamomile', 'Calendula', 'Ashwagandha', 'Comfrey', 'Echinacea'
  ]

  medicinal_plants = EnhancedPlant.where(common_name: medicinal_plant_names)
  medicinal_tag = SemanticTag.find_by(name: 'medicinal')

  if medicinal_tag
    medicinal_plants.each do |plant|
      PlantSemanticTag.find_or_create_by(
        enhanced_plant: plant,
        semantic_tag: medicinal_tag
      ) do |pst|
        pst.confidence_score = 0.9
        pst.source = 'manual'
      end
    end
    puts "Tagged #{medicinal_plants.count} plants as medicinal"
  end

  # Manual tagging for nitrogen fixing plants (legumes)
  legume_plants = EnhancedPlant.where(
    'family ILIKE ? OR family ILIKE ?',
    '%leguminosae%', '%fabaceae%'
  )
  nitrogen_fixing_tag = SemanticTag.find_by(name: 'nitrogen_fixing')

  if nitrogen_fixing_tag
    legume_plants.each do |plant|
      PlantSemanticTag.find_or_create_by(
        enhanced_plant: plant,
        semantic_tag: nitrogen_fixing_tag
      ) do |pst|
        pst.confidence_score = 0.9
        pst.source = 'manual'
      end
    end
    puts "Tagged #{legume_plants.count} legume plants as nitrogen_fixing"
  end

  # Manual tagging for ground cover plants
  groundcover_plant_names = ['Chickweed']
  groundcover_plants = EnhancedPlant.where(
    'common_name ILIKE ANY (ARRAY[?])',
    groundcover_plant_names.map { |name| "%#{name}%" }
  )
  groundcover_tag = SemanticTag.find_by(name: 'ground_cover')

  if groundcover_tag
    groundcover_plants.each do |plant|
      PlantSemanticTag.find_or_create_by(
        enhanced_plant: plant,
        semantic_tag: groundcover_tag
      ) do |pst|
        pst.confidence_score = 0.8
        pst.source = 'manual'
      end
    end
    puts "Tagged #{groundcover_plants.count} plants as ground_cover"
  end

  puts 'Plant-semantic tag associations created successfully!'
end

# Run the creation functions
create_plant_semantic_tag_associations