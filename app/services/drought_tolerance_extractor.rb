# frozen_string_literal: true
class DroughtToleranceExtractor
  # Drought tolerance keywords with confidence scores
  DROUGHT_KEYWORDS = {
    # High drought tolerance (0.8-1.0)
    'drought tolerant' => 0.9,
    'drought resistant' => 0.9,
    'xerophytic' => 1.0,
    'desert plant' => 1.0,
    'arid' => 0.8,
    'water-wise' => 0.8,
    'low water' => 0.7,
    'dry conditions' => 0.7,

    # Medium drought tolerance (0.5-0.7)
    'drought hardy' => 0.6,
    'once established' => 0.6,
    'minimal watering' => 0.6,
    'infrequent watering' => 0.6,
    'well-drained' => 0.5,

    # Low drought tolerance indicators (0.1-0.4)
    'moist soil' => 0.2,
    'regular watering' => 0.2,
    'high water' => 0.1,
    'wet conditions' => 0.1,
    'boggy' => 0.1,
    'marsh' => 0.1
  }.freeze

  def self.extract_and_populate_all
    updated_count = 0

    EnhancedPlant.includes(:environmental_requirements, plant_uses: :use_category).find_each do |plant|
      score = extract_drought_tolerance_score(plant)

      if score && plant.environmental_requirements
        plant.environmental_requirements.update!(drought_tolerance_score: score)
        updated_count += 1
        puts "Updated #{plant.common_name}: #{score}"
      end
    end

    puts "Updated drought tolerance for #{updated_count} plants"
    updated_count
  end

  def self.extract_drought_tolerance_score(plant)
    # Combine all text sources
    text_sources = [
      plant.description_detailed,
      plant.description_short,
      plant.growing_notes,
      plant.plant_uses.joins(:use_category).pluck('use_categories.name').join(' ')
    ].compact.join(' ').downcase

    return nil if text_sources.blank?

    # Find matching keywords and calculate weighted score
    matched_scores = []

    DROUGHT_KEYWORDS.each do |keyword, score|
      if text_sources.include?(keyword)
        matched_scores << score
        puts "  Found '#{keyword}' in #{plant.common_name} (score: #{score})"
      end
    end

    return nil if matched_scores.empty?

    # Calculate final score (average with slight bias toward higher scores)
    if matched_scores.length == 1
      matched_scores.first
    else
      # Weight higher scores slightly more
      weighted_average = matched_scores.sum / matched_scores.length
      max_score = matched_scores.max

      # Blend average with max (70% average, 30% max)
      final_score = (weighted_average * 0.7) + (max_score * 0.3)
      final_score.round(2)
    end
  end

  def self.analyze_drought_patterns
    puts '=== DROUGHT TOLERANCE ANALYSIS ==='

    # Check current state
    total_plants = EnhancedPlant.count
    plants_with_env = EnvironmentalRequirements.count
    plants_with_drought_scores = EnvironmentalRequirements.where('drought_tolerance_score IS NOT NULL').count

    puts "Total plants: #{total_plants}"
    puts "Plants with environmental requirements: #{plants_with_env}"
    puts "Plants with drought scores: #{plants_with_drought_scores}"

    if plants_with_drought_scores > 0
      scores = EnvironmentalRequirements.where('drought_tolerance_score IS NOT NULL').pluck(:drought_tolerance_score)
      puts 'Score distribution:'
      puts "  High (0.7-1.0): #{scores.count { |s| s >= 0.7 }}"
      puts "  Medium (0.4-0.7): #{scores.count { |s| s >= 0.4 && s < 0.7 }}"
      puts "  Low (0.0-0.4): #{scores.count { |s| s < 0.4 }}"
      puts "  Average score: #{(scores.sum / scores.length).round(2)}"
    end

    # Show examples by category
    puts "\nExamples by drought tolerance level:"

    high_drought = EnhancedPlant.joins(:environmental_requirements)
                               .where('environmental_requirements.drought_tolerance_score >= ?', 0.7)
                               .limit(5)
                               .pluck(:common_name, 'environmental_requirements.drought_tolerance_score')

    if high_drought.any?
      puts 'High drought tolerance:'
      high_drought.each { |name, score| puts "  #{name}: #{score}" }
    end

    low_drought = EnhancedPlant.joins(:environmental_requirements)
                              .where('environmental_requirements.drought_tolerance_score < ?', 0.4)
                              .limit(5)
                              .pluck(:common_name, 'environmental_requirements.drought_tolerance_score')

    if low_drought.any?
      puts 'Low drought tolerance:'
      low_drought.each { |name, score| puts "  #{name}: #{score}" }
    end
  end
end