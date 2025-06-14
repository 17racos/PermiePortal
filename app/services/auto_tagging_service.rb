# frozen_string_literal: true
class AutoTaggingService
  def self.tag_all_plants
    puts 'Starting auto-tagging for all plants...'
    tagged_count = 0

    EnhancedPlant.includes(:plant_uses, :environmental_requirements, use_categories: []).find_each do |plant|
      tags_added = new(plant).assign_tags
      if tags_added > 0
        tagged_count += 1
        puts "Tagged #{plant.common_name} with #{tags_added} tags"
      end
    end

    puts "Auto-tagged #{tagged_count} plants"
    tagged_count
  end

  def initialize(plant)
    @plant = plant
  end

  def assign_tags
    tags_added = 0

    tags_added += assign_use_tags
    tags_added += assign_environmental_tags
    tags_added += assign_growth_habit_tags
    tags_added += assign_trait_tags_from_description
    tags_added += assign_drought_tolerance_tags

    tags_added
  end

  private

  def assign_use_tags
    tags_added = 0

    @plant.plant_uses.includes(:use_category).each do |plant_use|
      use_name = plant_use.use_category.name.downcase
      confidence = calculate_confidence_from_effectiveness(plant_use.effectiveness_score)

      case use_name
      when /edible|food|fruit|vegetable|culinary/
        if assign_tag('edible', confidence: confidence, source: 'extracted')
          tags_added += 1

          # Add specific edible subcategories
          if use_name.include?('fruit') || use_name.include?('berry')
            assign_tag('edible_fruit', confidence: confidence, source: 'extracted')
            tags_added += 1
          elsif use_name.include?('leaf') || use_name.include?('herb') || use_name.include?('salad')
            assign_tag('edible_leaves', confidence: confidence, source: 'extracted')
            tags_added += 1
          elsif use_name.include?('root') || use_name.include?('tuber')
            assign_tag('edible_roots', confidence: confidence, source: 'extracted')
            tags_added += 1
          end
        end

      when /medicinal|medicine|healing|therapeutic/
        if assign_tag('medicinal', confidence: confidence, source: 'extracted')
          tags_added += 1
        end

      when /ornamental|decorative|landscape|beautiful/
        if assign_tag('ornamental', confidence: confidence, source: 'extracted')
          tags_added += 1
        end

      when /nitrogen|legume|soil improvement/
        if assign_tag('nitrogen_fixing', confidence: confidence, source: 'extracted')
          tags_added += 1
        end

      when /wildlife|bird|habitat|pollinator/
        if assign_tag('wildlife_habitat', confidence: confidence, source: 'extracted')
          tags_added += 1
        end

        if use_name.include?('pollinator') || use_name.include?('bee') || use_name.include?('butterfly')
          assign_tag('pollinator_friendly', confidence: confidence, source: 'extracted')
          tags_added += 1
        end
      end
    end

    tags_added
  end

  def assign_environmental_tags
    tags_added = 0
    return tags_added unless @plant.environmental_requirements

    env = @plant.environmental_requirements

    # Light requirements
    case env.light_requirement
    when 'full_sun'
      if assign_tag('full_sun', confidence: 1.0, source: 'extracted')
        tags_added += 1
      end
    when 'partial_shade', 'full_shade'
      if assign_tag('shade_tolerant', confidence: 0.9, source: 'extracted')
        tags_added += 1
      end
    end

    tags_added
  end

  def assign_growth_habit_tags
    tags_added = 0

    case @plant.plant_type
    when 'vine'
      if assign_tag('climbing', confidence: 1.0, source: 'inferred')
        tags_added += 1
      end
    when 'herbaceous'
      # Check if it's likely ground cover based on size
      if @plant.mature_height_max_cm && @plant.mature_height_max_cm < 30
        if assign_tag('ground_cover', confidence: 0.7, source: 'inferred')
          tags_added += 1
        end
      end
    end

    tags_added
  end

  def assign_trait_tags_from_description
    tags_added = 0
    return tags_added unless @plant.description_detailed

    description = @plant.description_detailed.downcase

    # Pattern matching for traits
    patterns = {
      'fast_growing' => /fast[_\s-]?growing|rapid[_\s-]?growth|vigorous|quick[_\s-]?establishment/,
      'low_maintenance' => /low[_\s-]?maintenance|easy[_\s-]?care|self[_\s-]?sufficient|minimal[_\s-]?care/,
      'pollinator_friendly' => /pollinator|bee[_\s-]?friendly|nectar|butterfly|attracts.*bees/,
      'pest_resistant' => /pest[_\s-]?resistant|repels.*pests|naturally.*resistant/,
      'disease_resistant' => /disease[_\s-]?resistant|disease[_\s-]?tolerant|hardy|robust/
    }

    patterns.each do |tag_name, pattern|
      if description.match?(pattern)
        if assign_tag(tag_name, confidence: 0.7, source: 'extracted')
          tags_added += 1
        end
      end
    end

    tags_added
  end

  def assign_drought_tolerance_tags
    tags_added = 0
    return tags_added unless @plant.environmental_requirements&.drought_tolerance_score

    drought_score = @plant.environmental_requirements.drought_tolerance_score

    if drought_score >= 0.7
      if assign_tag('drought_tolerant', confidence: drought_score, source: 'extracted')
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

  def calculate_confidence_from_effectiveness(effectiveness_score)
    return 0.8 unless effectiveness_score

    # Convert effectiveness score (0-1) to confidence (0.5-1.0)
    0.5 + (effectiveness_score * 0.5)
  end
end