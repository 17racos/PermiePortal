# frozen_string_literal: true
class PlantMigrationService
  attr_reader :migrated_count, :errors

  def initialize
    @migrated_count = 0
    @errors = []
  end

  def migrate_all_plants
    Plant.find_each do |old_plant|
      begin
        migrate_plant(old_plant)
        @migrated_count += 1
      rescue => e
        @errors << { plant: old_plant.common_name, error: e.message }
        Rails.logger.error "Failed to migrate plant #{old_plant.common_name}: #{e.message}"
      end
    end

    create_default_trait_categories
    create_default_use_categories
    create_default_relationship_types

    {
      migrated: @migrated_count,
      errors: @errors.count,
      error_details: @errors
    }
  end

  def migrate_plant(old_plant)
    ActiveRecord::Base.transaction do
      # Create enhanced plant
      enhanced_plant = create_enhanced_plant(old_plant)

      # Migrate environmental data
      create_environmental_requirements(enhanced_plant, old_plant)

      # Migrate uses
      migrate_uses(enhanced_plant, old_plant)

      # Migrate traits from existing data
      extract_and_create_traits(enhanced_plant, old_plant)

      # Migrate relationships
      migrate_relationships(enhanced_plant, old_plant)

      # Generate initial embedding text
      update_search_vector(enhanced_plant)

      enhanced_plant
    end
  end

  private

  def create_enhanced_plant(old_plant)
    EnhancedPlant.create!(
      common_name: old_plant.common_name,
      scientific_name: old_plant.scientific_name,
      family: old_plant.family,
      plant_type: infer_plant_type(old_plant),
      life_cycle: old_plant.perennial? ? 'perennial' : 'annual',
      description_short: extract_short_description(old_plant.description),
      description_detailed: old_plant.description,
      growing_notes: old_plant.purpose,
      data_quality_score: calculate_data_quality(old_plant)
    )
  end

  def create_environmental_requirements(enhanced_plant, old_plant)
    zone_min, zone_max = parse_zone_range(old_plant.zone_range)

    EnvironmentalRequirements.create!(
      enhanced_plant: enhanced_plant,
      hardiness_zone_min: zone_min,
      hardiness_zone_max: zone_max,
      temp_optimal_min: parse_temperature(old_plant.ideal_temp_min),
      temp_optimal_max: parse_temperature(old_plant.ideal_temp_max),
      temp_min_survival: parse_temperature(old_plant.min_temp),
      temp_max_survival: parse_temperature(old_plant.max_temp),
      light_requirement: infer_light_requirement(old_plant),
      climate_description: extract_climate_description(old_plant.description),
      soil_description: extract_soil_description(old_plant.description)
    )
  end

  def migrate_uses(enhanced_plant, old_plant)
    return unless old_plant.plant_functions.present?

    old_plant.plant_functions.each do |function|
      use_category = find_or_create_use_category(function)

      PlantUse.create!(
        enhanced_plant: enhanced_plant,
        use_category: use_category,
        effectiveness_score: 0.8, # Default confidence
        confidence_score: 0.7
      )
    end
  end

  def extract_and_create_traits(enhanced_plant, old_plant)
    # Extract traits from description and existing fields
    extract_growth_traits(enhanced_plant, old_plant)
    extract_size_traits(enhanced_plant, old_plant)
    extract_descriptive_traits(enhanced_plant, old_plant)
  end

  def extract_growth_traits(enhanced_plant, old_plant)
    description = old_plant.description.to_s.downcase

    # Growth rate
    if description.match?(/fast[- ]growing|rapid|vigorous/i)
      create_trait(enhanced_plant, 'growth_rate', 'fast')
    elsif description.match?(/slow[- ]growing|slow/i)
      create_trait(enhanced_plant, 'growth_rate', 'slow')
    end

    # Drought tolerance
    if description.match?(/drought[- ]tolerant|drought[- ]resistant|dry/i)
      create_trait(enhanced_plant, 'drought_tolerance', true)
    end

    # Shade tolerance
    if description.match?(/shade[- ]tolerant|partial shade|full shade/i)
      create_trait(enhanced_plant, 'shade_tolerance', true)
    end
  end

  def extract_size_traits(enhanced_plant, old_plant)
    # Use layers to infer size
    if old_plant.layers.present?
      layers = old_plant.layers.map(&:downcase)

      if layers.include?('canopy')
        enhanced_plant.update!(
          mature_height_min_cm: 800,
          mature_height_max_cm: 3000
        )
      elsif layers.include?('understory')
        enhanced_plant.update!(
          mature_height_min_cm: 200,
          mature_height_max_cm: 800
        )
      elsif layers.include?('shrub')
        enhanced_plant.update!(
          mature_height_min_cm: 50,
          mature_height_max_cm: 300
        )
      elsif layers.include?('ground cover')
        enhanced_plant.update!(
          mature_height_min_cm: 5,
          mature_height_max_cm: 50
        )
      end
    end
  end

  def extract_descriptive_traits(enhanced_plant, old_plant)
    description = old_plant.description.to_s

    # Extract color information
    colors = description.scan(/\b(red|blue|yellow|purple|pink|white|orange|green)\b/i).flatten
    if colors.any?
      create_trait(enhanced_plant, 'flower_color', colors.first.downcase)
    end

    # Extract fragrance
    if description.match?(/fragrant|scented|aromatic/i)
      create_trait(enhanced_plant, 'fragrant', true)
    end

    # Extract edibility
    if description.match?(/edible|food|fruit|vegetable/i)
      create_trait(enhanced_plant, 'edible', true)
    end
  end

  def migrate_relationships(enhanced_plant, old_plant)
    # Migrate companions
    if old_plant.companions.present?
      beneficial_type = find_or_create_relationship_type('beneficial_companion')

      old_plant.companions.each do |companion_name|
        companion = find_plant_by_name(companion_name)
        next unless companion

        PlantRelationship.create!(
          plant_a: enhanced_plant,
          plant_b: companion,
          relationship_type: beneficial_type,
          strength_score: 0.7,
          confidence_score: 0.6,
          evidence_type: 'traditional'
        )
      end
    end

    # Migrate avoid list
    if old_plant.avoid.present?
      antagonistic_type = find_or_create_relationship_type('antagonistic')

      old_plant.avoid.each do |avoid_name|
        avoided_plant = find_plant_by_name(avoid_name)
        next unless avoided_plant

        PlantRelationship.create!(
          plant_a: enhanced_plant,
          plant_b: avoided_plant,
          relationship_type: antagonistic_type,
          strength_score: 0.8,
          confidence_score: 0.6,
          evidence_type: 'traditional'
        )
      end
    end
  end

  def create_trait(enhanced_plant, category_name, value)
    category = find_or_create_trait_category(category_name)

    trait_attributes = {
      enhanced_plant: enhanced_plant,
      trait_category: category,
      confidence_score: 0.6,
      source: 'migration_extraction'
    }

    case category.data_type
    when 'boolean'
      trait_attributes[:boolean_value] = value
    when 'categorical'
      trait_attributes[:categorical_value] = value.to_s
    when 'numeric'
      trait_attributes[:numeric_value] = value.to_f
    when 'text'
      trait_attributes[:text_value] = value.to_s
    end

    PlantTrait.create!(trait_attributes)
  end

  def infer_plant_type(old_plant)
    return nil unless old_plant.layers.present?

    layers = old_plant.layers.map(&:downcase)

    if layers.include?('canopy')
      'tree'
    elsif layers.include?('understory')
      'shrub'
    elsif layers.include?('vine')
      'vine'
    elsif layers.include?('ground cover')
      'herbaceous'
    else
      'herbaceous'
    end
  end

  def infer_light_requirement(old_plant)
    return nil unless old_plant.layers.present?

    layers = old_plant.layers.map(&:downcase)

    if layers.include?('canopy')
      'full_sun'
    elsif layers.include?('understory')
      'partial_shade'
    elsif layers.include?('ground cover')
      'partial_shade'
    else
      'full_sun'
    end
  end

  def parse_zone_range(zone_range)
    return [nil, nil] unless zone_range.present?

    if zone_range.is_a?(Range)
      [zone_range.begin, zone_range.end]
    elsif zone_range.to_s.include?('-')
      min_zone, max_zone = zone_range.to_s.split('-').map(&:to_i)
      [min_zone, max_zone]
    else
      zone = zone_range.to_i
      [zone, zone]
    end
  end

  def parse_temperature(temp_string)
    return nil unless temp_string.present?

    # Extract numeric value from temperature string
    temp_string.to_s.scan(/[-]?\d+(?:\.\d+)?/).first&.to_f
  end

  def extract_short_description(description)
    return nil unless description.present?

    # Take first sentence or first 150 characters
    sentences = description.split(/[.!?]/)
    first_sentence = sentences.first&.strip

    if first_sentence && first_sentence.length <= 150
      first_sentence
    else
      description.truncate(150)
    end
  end

  def extract_climate_description(description)
    return nil unless description.present?

    # Extract climate-related sentences
    climate_keywords = %w[climate temperature heat cold drought wet dry sun shade wind]
    sentences = description.split(/[.!?]/)

    climate_sentences = sentences.select do |sentence|
      climate_keywords.any? { |keyword| sentence.downcase.include?(keyword) }
    end

    climate_sentences.first(2).join('. ').presence
  end

  def extract_soil_description(description)
    return nil unless description.present?

    # Extract soil-related sentences
    soil_keywords = %w[soil drainage ph acidic alkaline sandy clay loam rich poor]
    sentences = description.split(/[.!?]/)

    soil_sentences = sentences.select do |sentence|
      soil_keywords.any? { |keyword| sentence.downcase.include?(keyword) }
    end

    soil_sentences.first(2).join('. ').presence
  end

  def calculate_data_quality(old_plant)
    score = 0.0

    # Basic information
    score += 0.2 if old_plant.common_name.present?
    score += 0.2 if old_plant.scientific_name.present?
    score += 0.1 if old_plant.family.present?

    # Environmental data
    score += 0.1 if old_plant.zone_range.present?
    score += 0.1 if old_plant.ideal_temp_min.present?
    score += 0.1 if old_plant.ideal_temp_max.present?

    # Functional data
    score += 0.1 if old_plant.plant_functions.present?
    score += 0.05 if old_plant.companions.present?
    score += 0.05 if old_plant.description.present?

    [score, 1.0].min
  end

  def find_plant_by_name(name)
    # Try to find in enhanced plants first
    enhanced_plant = EnhancedPlant.find_by(common_name: name) ||
                    EnhancedPlant.find_by(scientific_name: name)

    return enhanced_plant if enhanced_plant

    # Try to find in old plants and migrate if found
    old_plant = Plant.find_by(common_name: name) ||
               Plant.find_by(scientific_name: name)

    return nil unless old_plant

    # Migrate the found plant
    migrate_plant(old_plant)
  end

  def find_or_create_trait_category(name)
    TraitCategory.find_or_create_by(name: name) do |category|
      category.data_type = infer_data_type(name)
      category.description = 'Auto-created during migration'
    end
  end

  def find_or_create_use_category(name)
    UseCategory.find_or_create_by(name: name) do |category|
      category.description = 'Auto-created during migration'
    end
  end

  def find_or_create_relationship_type(name)
    RelationshipType.find_or_create_by(name: name) do |type|
      type.description = 'Auto-created during migration'
      type.is_beneficial = name.include?('beneficial')
    end
  end

  def infer_data_type(trait_name)
    boolean_traits = %w[drought_tolerance shade_tolerance fragrant edible invasive native]
    categorical_traits = %w[growth_rate flower_color plant_type]

    if boolean_traits.include?(trait_name)
      'boolean'
    elsif categorical_traits.include?(trait_name)
      'categorical'
    else
      'text'
    end
  end

  def update_search_vector(enhanced_plant)
    # The search vector will be automatically updated by the database trigger
    enhanced_plant.touch
  end

  def create_default_trait_categories
    default_categories = [
      { name: 'growth_rate', data_type: 'categorical', description: 'How fast the plant grows' },
      { name: 'drought_tolerance', data_type: 'boolean', description: 'Can tolerate drought conditions' },
      { name: 'shade_tolerance', data_type: 'boolean', description: 'Can grow in shade' },
      { name: 'flower_color', data_type: 'categorical', description: 'Primary flower color' },
      { name: 'fragrant', data_type: 'boolean', description: 'Has fragrant flowers or foliage' },
      { name: 'edible', data_type: 'boolean', description: 'Has edible parts' },
      { name: 'invasive', data_type: 'boolean', description: 'Tends to spread aggressively' },
      { name: 'native', data_type: 'boolean', description: 'Native to the region' },
      { name: 'mature_height', data_type: 'numeric', unit: 'cm', description: 'Height at maturity' },
      { name: 'mature_width', data_type: 'numeric', unit: 'cm', description: 'Width at maturity' }
    ]

    default_categories.each do |attrs|
      TraitCategory.find_or_create_by(name: attrs[:name]) do |category|
        category.assign_attributes(attrs.except(:name))
      end
    end
  end

  def create_default_use_categories
    default_uses = [
      { name: 'food', description: 'Edible parts for human consumption' },
      { name: 'medicine', description: 'Medicinal properties' },
      { name: 'timber', description: 'Wood for construction or crafts' },
      { name: 'ornamental', description: 'Decorative landscaping' },
      { name: 'wildlife_habitat', description: 'Provides habitat for wildlife' },
      { name: 'erosion_control', description: 'Prevents soil erosion' },
      { name: 'windbreak', description: 'Protection from wind' },
      { name: 'nitrogen_fixation', description: 'Fixes nitrogen in soil' },
      { name: 'ground_cover', description: 'Covers and protects soil' },
      { name: 'pollinator_attractant', description: 'Attracts beneficial insects' }
    ]

    default_uses.each do |attrs|
      UseCategory.find_or_create_by(name: attrs[:name]) do |category|
        category.assign_attributes(attrs.except(:name))
      end
    end
  end

  def create_default_relationship_types
    default_relationships = [
      { name: 'beneficial_companion', description: 'Plants that benefit each other', is_beneficial: true },
      { name: 'antagonistic', description: 'Plants that inhibit each other', is_beneficial: false },
      { name: 'neutral', description: 'Plants with no significant interaction', is_beneficial: nil },
      { name: 'nurse_plant', description: 'Provides protection for other plants', is_beneficial: true },
      { name: 'guild_member', description: 'Part of a plant guild system', is_beneficial: true }
    ]

    default_relationships.each do |attrs|
      RelationshipType.find_or_create_by(name: attrs[:name]) do |type|
        type.assign_attributes(attrs.except(:name))
      end
    end
  end
end