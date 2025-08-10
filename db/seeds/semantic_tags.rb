# frozen_string_literal: true
def create_semantic_tags
  puts 'Creating semantic tags...'

  # Trait categories
  SemanticTag.find_or_create_by!(name: 'drought_tolerant') do |tag|
    tag.category = 'trait'
    tag.synonyms = ['drought resistant', 'xerophytic', 'water wise', 'low water', 'dry conditions']
    tag.description = 'Plants that can survive with minimal water'
  end

  SemanticTag.find_or_create_by!(name: 'pollinator_friendly') do |tag|
    tag.category = 'trait'
    tag.synonyms = ['bee friendly', 'attracts pollinators', 'nectar rich', 'butterfly plant']
    tag.description = 'Plants that attract and support pollinators'
  end

  # Growth habit examples
  SemanticTag.find_or_create_by!(name: 'fast_growing') do |tag|
    tag.category = 'growth_habit'
    tag.synonyms = ['rapid growth', 'quick establishment', 'vigorous']
    tag.description = 'Plants that establish and grow quickly'
  end

  SemanticTag.find_or_create_by!(name: 'low_maintenance') do |tag|
    tag.category = 'trait'
    tag.synonyms = ['easy care', 'self sufficient', 'minimal care']
    tag.description = 'Plants that require minimal care once established'
  end

  # ... add the rest following the same pattern ...

  # Use categories with parent-child
  edible_tag = SemanticTag.find_or_create_by!(name: 'edible') do |tag|
    tag.category = 'use'
    tag.synonyms = ['food', 'culinary', 'edible parts']
    tag.description = 'Plants with edible parts'
  end

  SemanticTag.find_or_create_by!(name: 'edible_fruit') do |tag|
    tag.category = 'use'
    tag.parent_tag = edible_tag
    tag.synonyms = ['fruit', 'berry', 'fruiting']
    tag.description = 'Plants with edible fruits'
  end

  # Continue for all tags ...

  puts "Created or confirmed #{SemanticTag.count} semantic tags"
end

# Run the seed function only if no tags exist
create_semantic_tags if SemanticTag.count == 0
