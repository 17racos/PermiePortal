# frozen_string_literal: true
def create_semantic_tags
  puts 'Creating semantic tags...'

  # Trait categories
  SemanticTag.create!(
    name: 'drought_tolerant',
    category: 'trait',
    synonyms: ['drought resistant', 'xerophytic', 'water wise', 'low water', 'dry conditions'],
    description: 'Plants that can survive with minimal water'
  )

  SemanticTag.create!(
    name: 'pollinator_friendly',
    category: 'trait',
    synonyms: ['bee friendly', 'attracts pollinators', 'nectar rich', 'butterfly plant'],
    description: 'Plants that attract and support pollinators'
  )

  SemanticTag.create!(
    name: 'fast_growing',
    category: 'growth_habit',
    synonyms: ['rapid growth', 'quick establishment', 'vigorous'],
    description: 'Plants that establish and grow quickly'
  )

  SemanticTag.create!(
    name: 'low_maintenance',
    category: 'trait',
    synonyms: ['easy care', 'self sufficient', 'minimal care'],
    description: 'Plants that require minimal care once established'
  )

  SemanticTag.create!(
    name: 'shade_tolerant',
    category: 'environmental',
    synonyms: ['partial shade', 'tolerates shade', 'low light'],
    description: 'Plants that can grow in shaded conditions'
  )

  SemanticTag.create!(
    name: 'full_sun',
    category: 'environmental',
    synonyms: ['sunny', 'bright light', 'direct sun'],
    description: 'Plants that prefer full sunlight'
  )

  # Use categories
  edible_tag = SemanticTag.create!(
    name: 'edible',
    category: 'use',
    synonyms: ['food', 'culinary', 'edible parts'],
    description: 'Plants with edible parts'
  )

  SemanticTag.create!(
    name: 'medicinal',
    category: 'use',
    synonyms: ['medicine', 'healing', 'therapeutic'],
    description: 'Plants with medicinal properties'
  )

  SemanticTag.create!(
    name: 'ornamental',
    category: 'use',
    synonyms: ['decorative', 'beautiful', 'landscape'],
    description: 'Plants grown for aesthetic value'
  )

  SemanticTag.create!(
    name: 'nitrogen_fixing',
    category: 'trait',
    synonyms: ['fixes nitrogen', 'legume', 'soil improvement'],
    description: 'Plants that fix nitrogen from the atmosphere'
  )

  # Create subcategories for edible
  SemanticTag.create!(
    name: 'edible_fruit',
    category: 'use',
    parent_tag: edible_tag,
    synonyms: ['fruit', 'berry', 'fruiting'],
    description: 'Plants with edible fruits'
  )

  SemanticTag.create!(
    name: 'edible_leaves',
    category: 'use',
    parent_tag: edible_tag,
    synonyms: ['leafy greens', 'salad', 'herbs'],
    description: 'Plants with edible leaves'
  )

  SemanticTag.create!(
    name: 'edible_roots',
    category: 'use',
    parent_tag: edible_tag,
    synonyms: ['root vegetable', 'tuber', 'bulb'],
    description: 'Plants with edible roots or tubers'
  )

  # Resistance traits
  SemanticTag.create!(
    name: 'pest_resistant',
    category: 'resistance',
    synonyms: ['pest deterrent', 'naturally resistant', 'repels pests'],
    description: 'Plants that naturally resist common pests'
  )

  SemanticTag.create!(
    name: 'disease_resistant',
    category: 'resistance',
    synonyms: ['disease tolerant', 'hardy', 'robust'],
    description: 'Plants resistant to common diseases'
  )

  # Growth habits
  SemanticTag.create!(
    name: 'ground_cover',
    category: 'growth_habit',
    synonyms: ['spreading', 'low growing', 'carpet'],
    description: 'Plants that spread to cover ground'
  )

  SemanticTag.create!(
    name: 'climbing',
    category: 'growth_habit',
    synonyms: ['vine', 'climber', 'twining'],
    description: 'Plants that climb or vine'
  )

  # Seasonal tags
  SemanticTag.create!(
    name: 'spring_blooming',
    category: 'season',
    synonyms: ['early flowers', 'spring flowers'],
    description: 'Plants that bloom in spring'
  )

  SemanticTag.create!(
    name: 'fall_color',
    category: 'season',
    synonyms: ['autumn color', 'fall foliage'],
    description: 'Plants with attractive fall foliage'
  )

  # Wildlife support
  SemanticTag.create!(
    name: 'wildlife_habitat',
    category: 'use',
    synonyms: ['wildlife food', 'bird food', 'habitat'],
    description: 'Plants that provide habitat or food for wildlife'
  )

  puts "Created #{SemanticTag.count} semantic tags"
end

# Run the seed function
create_semantic_tags if SemanticTag.count == 0