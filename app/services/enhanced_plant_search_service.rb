class EnhancedPlantSearchService
  attr_reader :query_parser

  def initialize
    @query_parser = QueryParser.new
  end

  def search(query, options = {})
    # Parse query for intent and entities
    parsed_query = @query_parser.parse(query)
    
    # Multiple search strategies
    results = {
      keyword: keyword_search(parsed_query[:keywords], options),
      trait: trait_search(parsed_query[:traits], options),
      environmental: environmental_search(parsed_query[:conditions], options),
      name: name_search(parsed_query[:plant_names], options)
    }
    
    # Combine and rank results
    combine_results(results, parsed_query[:intent], options)
  end

  def search_by_traits(trait_filters, options = {})
    find_plants_by_traits(trait_filters, options)
  end

  def search_by_environmental_conditions(conditions, options = {})
    find_suitable_plants(conditions, options)
  end

  def recommend_companions(plant_id, options = {})
    plant = EnhancedPlant.find(plant_id)
    
    # Get direct companions
    direct_companions = plant.beneficial_companions
    
    # Get plants with similar environmental needs
    similar_environment = []
    if plant.environmental_requirements
      similar_environment = EnhancedPlant.joins(:environmental_requirements)
        .where.not(id: plant_id)
        .where(environmental_requirements: {
          light_requirement: plant.environmental_requirements.light_requirement
        })
        .where(
          'ABS(environmental_requirements.hardiness_zone_min - ?) <= 2',
          plant.environmental_requirements.hardiness_zone_min || 5
        )
        .limit(options[:limit] || 10)
    end
    
    # Combine and deduplicate
    companions = (direct_companions + similar_environment).uniq
    companions.first(options[:limit] || 10)
  end

  private

  def keyword_search(keywords, options)
    return [] if keywords.empty?
    
    like_patterns = keywords.map { |k| "%#{k}%" }
    
    # Build ILIKE conditions for plant names and descriptions
    plant_conditions = keywords.map { 
      "(enhanced_plants.common_name ILIKE ? OR enhanced_plants.scientific_name ILIKE ? OR enhanced_plants.description_short ILIKE ?)" 
    }.join(' OR ')
    
    name_conditions = keywords.map { "plant_names.name ILIKE ?" }.join(' OR ')
    
    # Flatten the parameters for plant conditions (3 per keyword)
    plant_params = keywords.flat_map { |k| ["%#{k}%", "%#{k}%", "%#{k}%"] }
    
    EnhancedPlant.joins("LEFT JOIN plant_names ON plant_names.enhanced_plant_id = enhanced_plants.id")
                 .where(
                   "(#{plant_conditions}) OR (#{name_conditions})",
                   *plant_params,
                   *like_patterns
                 )
                 .distinct
                 .limit(options[:limit] || 20)
  end

  def trait_search(traits, options)
    return [] if traits.empty?
    
    find_plants_by_traits(traits, options)
  end

  def environmental_search(conditions, options)
    return [] if conditions.empty?
    
    find_suitable_plants(conditions, options)
  end

  def name_search(plant_names, options)
    return [] if plant_names.empty?
    
    # Build ILIKE conditions for each name
    name_conditions = plant_names.map { "name ILIKE ?" }.join(' OR ')
    like_patterns = plant_names.map { |name| "%#{name}%" }
    
    plant_ids = PlantName.where(name_conditions, *like_patterns).pluck(:enhanced_plant_id)
    
    EnhancedPlant.where(id: plant_ids).limit(options[:limit] || 20)
  end

  def combine_results(results, intent, options = {})
    # Weight different result types based on query intent
    weights = case intent
    when 'find_by_name'
      { name: 0.5, keyword: 0.3, trait: 0.0, environmental: 0.0 }
    when 'find_by_conditions'
      { environmental: 0.5, trait: 0.3, keyword: 0.0, name: 0.0 }
    when 'companion_planting'
      { trait: 0.4, environmental: 0.3, keyword: 0.1, name: 0.0 }
    when 'problem_solving'
      { trait: 0.4, environmental: 0.3, keyword: 0.1, name: 0.0 }
    when 'general_search'
      { keyword: 0.25, trait: 0.2, environmental: 0.15, name: 0.1 }
    else
      { keyword: 0.2, trait: 0.2, environmental: 0.2, name: 0.2 }
    end
    
    # Combine and score results
    combined_scores = {}
    
    results.each do |type, plants|
      next if plants.empty?
      
      plants.each do |plant|
        plant_id = plant.id
        score = extract_score(plant, type)
        
        combined_scores[plant_id] ||= { plant: plant, total_score: 0, sources: [] }
        combined_scores[plant_id][:total_score] += score * weights[type]
        combined_scores[plant_id][:sources] << type
      end
    end
    
    # Apply quality boost
    combined_scores.each do |plant_id, data|
      quality_boost = data[:plant].data_quality_score || 0.5
      data[:total_score] *= (0.8 + (quality_boost * 0.4)) # Boost by 0.8-1.2x based on quality
    end
    
    # Sort by combined score and return plants
    sorted_results = combined_scores.values
                                   .sort_by { |result| -result[:total_score] }
                                   .first(options[:limit] || 20)
    
    # Return enhanced results with metadata
    if options[:include_metadata]
      sorted_results.map do |result|
        {
          plant: result[:plant],
          score: result[:total_score],
          sources: result[:sources]
        }
      end
    else
      sorted_results.map { |result| result[:plant] }
    end
  end

  def extract_score(plant, search_type)
    case search_type
    when :keyword
      plant.try(:rank_score) || 0.5
    when :trait
      plant.try(:trait_match_score) || 0.6
    when :environmental
      plant.try(:environmental_match_score) || 0.6
    when :name
      0.8 # High score for name matches
    else
      0.5
    end
  end

  def find_plants_by_traits(trait_filters, options = {})
    return [] if trait_filters.empty?
    
    plants = EnhancedPlant.joins(plant_traits: :trait_category)
    
    trait_filters.each do |trait_name, criteria|
      plants = plants.where(trait_categories: { name: trait_name })
      
      case criteria
      when Hash
        if criteria[:min]
          plants = plants.where('plant_traits.numeric_value >= ?', criteria[:min])
        end
        if criteria[:max]
          plants = plants.where('plant_traits.numeric_value <= ?', criteria[:max])
        end
      when Array
        plants = plants.where(plant_traits: { categorical_value: criteria })
      when String
        plants = plants.where(plant_traits: { categorical_value: criteria })
      when TrueClass, FalseClass
        plants = plants.where(plant_traits: { boolean_value: criteria })
      end
    end
    
    plants.distinct.limit(options[:limit] || 20)
  end

  def find_suitable_plants(conditions, options = {})
    return [] if conditions.empty?
    
    plants = EnhancedPlant.joins(:environmental_requirements)
    
    conditions.each do |condition, value|
      case condition.to_s
      when 'drought_tolerant'
        plants = plants.where('environmental_requirements.drought_tolerance_score > ?', 0.6) if value
      when 'shade_tolerant'
        plants = plants.where(environmental_requirements: { light_requirement: ['full_shade', 'partial_shade'] }) if value
      when 'zone'
        plants = plants.where(
          'environmental_requirements.hardiness_zone_min <= ? AND environmental_requirements.hardiness_zone_max >= ?',
          value, value
        )
      when 'max_height'
        plants = plants.where('enhanced_plants.mature_height_max_cm <= ?', value)
      when 'light_requirement'
        plants = plants.where(environmental_requirements: { light_requirement: value })
      end
    end
    
    plants.limit(options[:limit] || 20)
  end
end 