# frozen_string_literal: true
class EnhancedAutoTaggingService
  def self.tag_all_plants_enhanced
    puts 'Starting enhanced auto-tagging for all plants...'
    tagged_count = 0

    EnhancedPlant.includes(:plant_uses, :environmental_requirements, use_categories: []).find_each do |plant|
      tags_added = new(plant).assign_enhanced_tags
      if tags_added > 0
        tagged_count += 1
        puts "Enhanced tagged #{plant.common_name} with #{tags_added} new tags"
      end
    end

    puts "Enhanced auto-tagged #{tagged_count} plants"
    tagged_count
  end

  def initialize(plant)
    @plant = plant
  end

  def assign_enhanced_tags
    tags_added = 0

    # Run original tagging first
    original_service = AutoTaggingService.new(@plant)
    tags_added += original_service.assign_tags

    # Add new enhanced tags
    tags_added += assign_aromatic_tags
    tags_added += assign_seasonal_tags
    tags_added += assign_growth_habit_tags
    tags_added += assign_climate_tags
    tags_added += assign_maintenance_tags
    tags_added += assign_resistance_tags

    tags_added
  end

  private

  def assign_aromatic_tags
    tags_added = 0
    return tags_added unless @plant.description_detailed

    description = @plant.description_detailed.downcase

    # Aromatic patterns
    aromatic_patterns = [
      /fragrant|aromatic|scented|perfumed|sweet[_\s-]?smell/,
      /essential[_\s-]?oil|volatile[_\s-]?oil/,
      /mint|basil|rosemary|lavender|thyme|sage/ # Known aromatic plants
    ]

    if aromatic_patterns.any? { |pattern| description.match?(pattern) }
      if assign_tag('aromatic', confidence: 0.8, source: 'extracted')
        tags_added += 1
      end
    end

    tags_added
  end

  def assign_seasonal_tags
    tags_added = 0
    return tags_added unless @plant.description_detailed

    description = @plant.description_detailed.downcase

    # Spring blooming
    if description.match?(/spring[_\s-]?bloom|early[_\s-]?flower|march|april|may[_\s-]?flower/)
      if assign_tag('spring_blooming', confidence: 0.7, source: 'extracted')
        tags_added += 1
      end
    end

    # Summer blooming
    if description.match?(/summer[_\s-]?bloom|june|july|august[_\s-]?flower|mid[_\s-]?season/)
      if assign_tag('summer_blooming', confidence: 0.7, source: 'extracted')
        tags_added += 1
      end
    end

    # Fall blooming
    if description.match?(/fall[_\s-]?bloom|autumn[_\s-]?bloom|september|october|november[_\s-]?flower/)
      if assign_tag('fall_blooming', confidence: 0.7, source: 'extracted')
        tags_added += 1
      end
    end

    tags_added
  end

  def assign_growth_habit_tags
    tags_added = 0

    description = @plant.description_detailed&.downcase || ''

    # Container suitable
    container_patterns = [
      /container|pot[_\s-]?friendly|good[_\s-]?for[_\s-]?pots/,
      /small[_\s-]?space|compact[_\s-]?garden|patio[_\s-]?plant/
    ]

    if container_patterns.any? { |pattern| description.match?(pattern) } ||
       (@plant.mature_height_max_cm && @plant.mature_height_max_cm < 150) # Under 5 feet
      if assign_tag('container_suitable', confidence: 0.7, source: 'inferred')
        tags_added += 1
      end
    end

    # Self seeding
    if description.match?(/self[_\s-]?seed|reseed|naturaliz|volunteer|spread[_\s-]?by[_\s-]?seed/)
      if assign_tag('self_seeding', confidence: 0.8, source: 'extracted')
        tags_added += 1
      end
    end

    # Invasive
    if description.match?(/invasive|aggressive|hard[_\s-]?to[_\s-]?control|weedy|spreads[_\s-]?rapidly/)
      if assign_tag('invasive', confidence: 0.8, source: 'extracted')
        tags_added += 1
      end
    end

    # Compact
    if description.match?(/compact|dwarf|small[_\s-]?form|dense[_\s-]?growth/) ||
       (@plant.mature_height_max_cm && @plant.mature_height_max_cm < 60) # Under 2 feet
      if assign_tag('compact', confidence: 0.7, source: 'inferred')
        tags_added += 1
      end
    end

    # Spreading
    if description.match?(/spreading|mat[_\s-]?form|horizontal[_\s-]?growth|wide[_\s-]?spread/)
      if assign_tag('spreading', confidence: 0.8, source: 'extracted')
        tags_added += 1
      end
    end

    tags_added
  end

  def assign_climate_tags
    tags_added = 0

    description = @plant.description_detailed&.downcase || ''
    env = @plant.environmental_requirements

    # Cold hardy
    cold_patterns = [
      /cold[_\s-]?hardy|winter[_\s-]?hardy|frost[_\s-]?tolerant|freeze[_\s-]?resistant/,
      /cold[_\s-]?tolerant|hardy[_\s-]?to[_\s-]?zone/
    ]

    if cold_patterns.any? { |pattern| description.match?(pattern) } ||
       (env && env.hardiness_zone_min && env.hardiness_zone_min <= 5)
      if assign_tag('cold_hardy', confidence: 0.8, source: 'extracted')
        tags_added += 1
      end
    end

    # Tropical
    tropical_patterns = [
      /tropical|warm[_\s-]?climate|heat[_\s-]?loving|tropical[_\s-]?species/,
      /zone[_\s-]?10|zone[_\s-]?11|zone[_\s-]?12/
    ]

    if tropical_patterns.any? { |pattern| description.match?(pattern) } ||
       (env && env.hardiness_zone_min && env.hardiness_zone_min >= 9)
      if assign_tag('tropical', confidence: 0.8, source: 'extracted')
        tags_added += 1
      end
    end

    # Native (basic detection)
    if description.match?(/native|indigenous|naturally[_\s-]?occurring/)
      if assign_tag('native', confidence: 0.7, source: 'extracted')
        tags_added += 1
      end
    end

    tags_added
  end

  def assign_maintenance_tags
    tags_added = 0
    return tags_added unless @plant.description_detailed

    description = @plant.description_detailed.downcase

    # Enhanced low maintenance detection
    low_maintenance_patterns = [
      /low[_\s-]?maintenance|easy[_\s-]?care|minimal[_\s-]?care|self[_\s-]?sufficient/,
      /once[_\s-]?established|little[_\s-]?care|carefree|trouble[_\s-]?free/,
      /drought[_\s-]?tolerant.*established|established.*drought/
    ]

    if low_maintenance_patterns.any? { |pattern| description.match?(pattern) }
      if assign_tag('low_maintenance', confidence: 0.8, source: 'extracted')
        tags_added += 1
      end
    end

    tags_added
  end

  def assign_resistance_tags
    tags_added = 0
    return tags_added unless @plant.description_detailed

    description = @plant.description_detailed.downcase

    # Enhanced deer resistance detection
    deer_patterns = [
      /deer[_\s-]?resistant|deer[_\s-]?proof|deer[_\s-]?avoid|not[_\s-]?eaten[_\s-]?by[_\s-]?deer/,
      /aromatic.*deer|fragrant.*deer/ # Aromatic plants often deer resistant
    ]

    if deer_patterns.any? { |pattern| description.match?(pattern) }
      if assign_tag('deer_resistant', confidence: 0.8, source: 'extracted')
        tags_added += 1
      end
    end

    # Enhanced drought tolerance detection (improve underused tag)
    drought_patterns = [
      /drought[_\s-]?tolerant|drought[_\s-]?resistant|xerophytic|water[_\s-]?wise/,
      /dry[_\s-]?conditions|arid|desert[_\s-]?plant|low[_\s-]?water/,
      /once[_\s-]?established.*water|established.*drought/
    ]

    if drought_patterns.any? { |pattern| description.match?(pattern) } ||
       (@plant.environmental_requirements&.drought_tolerance_score &&
        @plant.environmental_requirements.drought_tolerance_score >= 0.6)
      if assign_tag('drought_tolerant', confidence: 0.8, source: 'extracted')
        tags_added += 1
      end
    end

    tags_added
  end

  def assign_tag(tag_name, confidence:, source:)
    tag = SemanticTag.find_by(name: tag_name)
    return false unless tag

    # Check if tag already exists
    existing_tag = @plant.plant_semantic_tags.find_by(semantic_tag: tag)
    if existing_tag
      # Update confidence if new score is higher
      if confidence > existing_tag.confidence_score
        existing_tag.update!(confidence_score: confidence, source: source)
      end
      return false # Don't count as newly added
    end

    # Create new tag assignment
    @plant.plant_semantic_tags.create!(
      semantic_tag: tag,
      confidence_score: confidence,
      source: source
    )

    true
  end
end