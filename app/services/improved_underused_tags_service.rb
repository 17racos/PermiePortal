# frozen_string_literal: true
class ImprovedUnderusedTagsService
  def self.improve_all_underused_tags
    puts 'Improving detection of underused semantic tags...'
    improved_count = 0

    EnhancedPlant.includes(:plant_uses, :environmental_requirements, :plant_traits, use_categories: []).find_each do |plant|
      tags_added = new(plant).improve_underused_tags
      if tags_added > 0
        improved_count += 1
        puts "Improved #{plant.common_name} with #{tags_added} better tags"
      end
    end

    puts "Improved #{improved_count} plants with better tag detection"
    improved_count
  end

  def initialize(plant)
    @plant = plant
  end

  def improve_underused_tags
    tags_added = 0

    tags_added += improve_pest_resistant_detection
    tags_added += improve_climbing_detection
    tags_added += improve_shade_tolerant_detection
    tags_added += improve_ornamental_detection
    tags_added += improve_disease_resistant_detection
    tags_added += improve_seasonal_blooming_detection
    tags_added += improve_evergreen_deciduous_detection

    tags_added
  end

  private

  def improve_pest_resistant_detection
    tags_added = 0
    description = @plant.description_detailed&.downcase || ''

    # Enhanced pest resistance patterns
    pest_patterns = [
      /pest[_\s-]?resistant|repels?[_\s-]?pests|naturally[_\s-]?resistant/,
      /companion[_\s-]?plant.*pest|pest[_\s-]?control|insect[_\s-]?repellent/,
      /aromatic.*pest|strong[_\s-]?scent.*pest|fragrant.*repel/,
      /marigold|nasturtium|catnip|mint|basil|rosemary|lavender/ # Known pest-resistant plants
    ]

    # Check plant uses for pest control
    pest_control_uses = @plant.plant_uses.joins(:use_category)
                              .where('use_categories.name ILIKE ?', '%pest%')

    if pest_patterns.any? { |pattern| description.match?(pattern) } || pest_control_uses.any?
      if assign_tag('pest_resistant', confidence: 0.8, source: 'extracted')
        tags_added += 1
      end
    end

    tags_added
  end

  def improve_climbing_detection
    tags_added = 0
    description = @plant.description_detailed&.downcase || ''

    # Enhanced climbing patterns
    climbing_patterns = [
      /climbing|climber|vine|vining|twining|scrambling/,
      /trellis|support|vertical[_\s-]?growth|grows[_\s-]?up/,
      /passion[_\s-]?flower|grape|ivy|bean.*pole|pea.*climbing/
    ]

    # Check plant type
    is_vine = @plant.plant_type == 'vine'

    # Check height vs spread ratio (climbers often tall but narrow)
    height_spread_ratio = if @plant.mature_height_max_cm && @plant.mature_width_max_cm && @plant.mature_width_max_cm > 0
                            @plant.mature_height_max_cm.to_f / @plant.mature_width_max_cm
                         else
                           0
                         end

    if climbing_patterns.any? { |pattern| description.match?(pattern) } ||
       is_vine ||
       height_spread_ratio > 2.0 # Much taller than wide
      if assign_tag('climbing', confidence: 0.8, source: 'extracted')
        tags_added += 1
      end
    end

    tags_added
  end

  def improve_shade_tolerant_detection
    tags_added = 0
    description = @plant.description_detailed&.downcase || ''
    env = @plant.environmental_requirements

    # Enhanced shade tolerance patterns
    shade_patterns = [
      /shade[_\s-]?tolerant|partial[_\s-]?shade|low[_\s-]?light|filtered[_\s-]?light/,
      /woodland|forest[_\s-]?plant|understory|dappled[_\s-]?shade/,
      /hosta|fern|moss|begonia|impatiens|caladium/ # Known shade plants
    ]

    # Check environmental requirements
    shade_from_env = env && (
      env.light_requirement == 'partial_shade' ||
      env.light_requirement == 'full_shade'
    )

    if shade_patterns.any? { |pattern| description.match?(pattern) } || shade_from_env
      if assign_tag('shade_tolerant', confidence: 0.8, source: 'extracted')
        tags_added += 1
      end
    end

    tags_added
  end

  def improve_ornamental_detection
    tags_added = 0
    description = @plant.description_detailed&.downcase || ''

    # Enhanced ornamental patterns
    ornamental_patterns = [
      /ornamental|decorative|beautiful|attractive|showy|colorful/,
      /landscape|garden[_\s-]?design|aesthetic|pretty|gorgeous/,
      /flower.*display|blooms?.*spectacular|striking.*appearance/,
      /foliage.*attractive|leaves.*colorful|variegated/
    ]

    # Check for ornamental uses
    ornamental_uses = @plant.plant_uses.joins(:use_category)
                            .where('use_categories.name ILIKE ?', '%ornamental%')

    # Check if it has attractive traits
    has_flowers = description.match?(/flower|bloom|blossom/)
    has_attractive_foliage = description.match?(/foliage|leaves.*color|variegated/)

    if ornamental_patterns.any? { |pattern| description.match?(pattern) } ||
       ornamental_uses.any? ||
       (has_flowers && has_attractive_foliage)
      if assign_tag('ornamental', confidence: 0.7, source: 'extracted')
        tags_added += 1
      end
    end

    tags_added
  end

  def improve_disease_resistant_detection
    tags_added = 0
    description = @plant.description_detailed&.downcase || ''

    # Enhanced disease resistance patterns
    disease_patterns = [
      /disease[_\s-]?resistant|disease[_\s-]?tolerant|hardy|robust/,
      /resistant[_\s-]?to.*disease|naturally[_\s-]?healthy|trouble[_\s-]?free/,
      /strong[_\s-]?constitution|vigorous.*healthy|rarely[_\s-]?sick/
    ]

    # Plants with good environmental tolerance often disease resistant
    env = @plant.environmental_requirements
    environmentally_hardy = env && (
      (env.drought_tolerance_score && env.drought_tolerance_score > 0.7) ||
      (env.hardiness_zone_min && env.hardiness_zone_min <= 4) # Very cold hardy
    )

    if disease_patterns.any? { |pattern| description.match?(pattern) } || environmentally_hardy
      if assign_tag('disease_resistant', confidence: 0.7, source: 'extracted')
        tags_added += 1
      end
    end

    tags_added
  end

  def improve_seasonal_blooming_detection
    tags_added = 0
    description = @plant.description_detailed&.downcase || ''

    # More comprehensive seasonal patterns
    spring_patterns = [
      /spring[_\s-]?bloom|early[_\s-]?bloom|march|april|may.*flower/,
      /first[_\s-]?to[_\s-]?bloom|early[_\s-]?season.*flower/
    ]

    summer_patterns = [
      /summer[_\s-]?bloom|june|july|august.*flower|mid[_\s-]?season/,
      /peak[_\s-]?bloom.*summer|continuous[_\s-]?bloom/
    ]

    fall_patterns = [
      /fall[_\s-]?bloom|autumn[_\s-]?bloom|september|october|november.*flower/,
      /late[_\s-]?season.*bloom|end[_\s-]?of[_\s-]?season/
    ]

    if spring_patterns.any? { |pattern| description.match?(pattern) }
      if assign_tag('spring_blooming', confidence: 0.8, source: 'extracted')
        tags_added += 1
      end
    end

    if summer_patterns.any? { |pattern| description.match?(pattern) }
      if assign_tag('summer_blooming', confidence: 0.8, source: 'extracted')
        tags_added += 1
      end
    end

    if fall_patterns.any? { |pattern| description.match?(pattern) }
      if assign_tag('fall_blooming', confidence: 0.8, source: 'extracted')
        tags_added += 1
      end
    end

    tags_added
  end

  def improve_evergreen_deciduous_detection
    tags_added = 0
    description = @plant.description_detailed&.downcase || ''

    # Evergreen patterns
    evergreen_patterns = [
      /evergreen|year[_\s-]?round[_\s-]?foliage|persistent[_\s-]?leaves/,
      /retains[_\s-]?leaves|keeps[_\s-]?foliage|non[_\s-]?deciduous/,
      /pine|fir|spruce|cedar|juniper|holly|rhododendron/ # Known evergreens
    ]

    # Deciduous patterns
    deciduous_patterns = [
      /deciduous|loses[_\s-]?leaves|drops[_\s-]?leaves|seasonal[_\s-]?foliage/,
      /fall[_\s-]?color|autumn[_\s-]?color|leaf[_\s-]?drop/,
      /maple|oak|birch|elm|ash.*tree/ # Known deciduous trees
    ]

    # Trees and shrubs are more likely to be evergreen/deciduous
    is_woody = @plant.plant_type.in?(['tree', 'shrub'])

    if evergreen_patterns.any? { |pattern| description.match?(pattern) } && is_woody
      if assign_tag('evergreen', confidence: 0.8, source: 'extracted')
        tags_added += 1
      end
    end

    if deciduous_patterns.any? { |pattern| description.match?(pattern) } && is_woody
      if assign_tag('deciduous', confidence: 0.8, source: 'extracted')
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