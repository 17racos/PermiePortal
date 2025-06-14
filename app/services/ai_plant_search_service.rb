# frozen_string_literal: true
# AI-Powered Plant Search Service for PermieBro
class AiPlantSearchService
  include ActiveModel::Model

  attr_accessor :query, :location, :zone, :limit, :use_cache, :ai_provider

  def initialize(attributes = {})
    super
    @limit ||= 20
    @use_cache = false # Disable caching for now
    @ai_provider ||= :local # :openai, :anthropic, :local
  end

  def search(query:, location: nil, zone: nil, limit: 20)
    @query = query
    @location = location
    @zone = zone
    @limit = limit

    # Check cache first
    if use_cache
      cached_result = check_query_cache
      return cached_result if cached_result
    end

    # Parse natural language query
    parsed_query = parse_natural_language_query(@query)

    # Multi-stage search
    results = {
      semantic_matches: semantic_search(parsed_query),
      environmental_matches: environmental_search(parsed_query),
      companion_matches: companion_search(parsed_query),
      regional_matches: regional_search(parsed_query)
    }

    # Combine and rank results
    final_results = combine_and_rank_results(results, parsed_query)

    # Cache results
    cache_results(final_results) if use_cache

    {
      plants: final_results.is_a?(Array) ? final_results.first(@limit) : final_results.limit(@limit),
      query_analysis: parsed_query,
      search_metadata: generate_search_metadata(results)
    }
  end

  private

  def parse_natural_language_query(query_text)
    {
      original_query: query_text,
      extracted_concepts: extract_concepts(query_text),
      environmental_filters: extract_environmental_filters(query_text),
      use_cases: extract_use_cases(query_text),
      geographic_context: extract_geographic_context(query_text),
      companion_requests: extract_companion_requests(query_text),
      exclusions: extract_exclusions(query_text)
    }
  end

  def extract_concepts(text)
    # Find semantic concepts in the query
    concepts = []

    # Direct ontology matches
    ontology_matches = EnhancedSemanticOntology.find_by_natural_language(text)
    concepts.concat(ontology_matches.map { |o| { type: :ontology, concept: o, confidence: 0.9 } })

    # Pattern-based extraction
    patterns = {
      edible: /\b(edible|food|eat|fruit|vegetable|herb|spice|culinary)\b/i,
      medicinal: /\b(medicinal|medicine|healing|therapeutic|remedy)\b/i,
      drought_tolerant: /\b(drought[_\s-]?tolerant|dry[_\s-]?climate|water[_\s-]?wise|xerophytic)\b/i,
      shade_tolerant: /\b(shade[_\s-]?tolerant|partial[_\s-]?shade|full[_\s-]?shade|low[_\s-]?light)\b/i,
      deer_resistant: /\b(deer[_\s-]?resistant|deer[_\s-]?proof|deer.*don.*eat)\b/i,
      native: /\b(native|indigenous|local|wild)\b/i,
      pollinator: /\b(pollinator|bee|butterfly|hummingbird|beneficial.*insect)\b/i,
      ground_cover: /\b(ground[_\s-]?cover|erosion[_\s-]?control|carpet|mat)\b/i,
      nitrogen_fixing: /\b(nitrogen[_\s-]?fixing|legume|bean|pea)\b/i,
      evergreen: /\b(evergreen|year[_\s-]?round.*foliage)\b/i,
      deciduous: /\b(deciduous|fall.*color|autumn.*color)\b/i
    }

    patterns.each do |concept_name, pattern|
      if text.match?(pattern)
        concepts << { type: :pattern, concept: concept_name, confidence: 0.8 }
      end
    end

    concepts
  end

  def extract_environmental_filters(text)
    filters = {}

    # Hardiness zones
    zone_match = text.match(/zone\s*(\d+[ab]?)/i)
    filters[:hardiness_zone] = zone_match[1] if zone_match

    # Light requirements
    if text.match?(/\b(full[_\s-]?sun|sunny)\b/i)
      filters[:light_requirement] = 'full_sun'
    elsif text.match?(/\b(partial[_\s-]?shade|part[_\s-]?shade)\b/i)
      filters[:light_requirement] = 'partial_shade'
    elsif text.match?(/\b(full[_\s-]?shade|deep[_\s-]?shade)\b/i)
      filters[:light_requirement] = 'full_shade'
    end

    # Water requirements
    if text.match?(/\b(drought[_\s-]?tolerant|dry|low[_\s-]?water)\b/i)
      filters[:water_requirement] = 'low'
    elsif text.match?(/\b(moist|wet|high[_\s-]?water)\b/i)
      filters[:water_requirement] = 'high'
    end

    # Soil preferences
    if text.match?(/\b(acidic|acid[_\s-]?soil)\b/i)
      filters[:soil_ph] = 'acidic'
    elsif text.match?(/\b(alkaline|basic[_\s-]?soil)\b/i)
      filters[:soil_ph] = 'alkaline'
    end

    filters
  end

  def extract_use_cases(text)
    use_cases = []

    use_patterns = {
      'Food/Culinary' => /\b(food|culinary|cooking|kitchen|eat|edible)\b/i,
      'Medicine/Health' => /\b(medicinal|medicine|health|healing|therapeutic)\b/i,
      'Landscaping' => /\b(landscape|ornamental|decorative|garden|yard)\b/i,
      'Wildlife Support' => /\b(wildlife|pollinator|bird|bee|butterfly)\b/i,
      'Erosion Control' => /\b(erosion|slope|bank|stabilization)\b/i,
      'Privacy/Screening' => /\b(privacy|screen|hedge|barrier|fence)\b/i,
      'Companion Planting' => /\b(companion|guild|polyculture|permaculture)\b/i
    }

    use_patterns.each do |use_name, pattern|
      use_cases << use_name if text.match?(pattern)
    end

    use_cases
  end

  def extract_geographic_context(text)
    context = {}

    # States/regions
    state_match = text.match(/\b(florida|california|texas|new york|oregon|washington|arizona|nevada|utah|colorado|montana|maine|vermont|north carolina|south carolina|georgia|alabama|mississippi|louisiana|arkansas|tennessee|kentucky|virginia|west virginia|maryland|delaware|new jersey|pennsylvania|connecticut|rhode island|massachusetts|new hampshire|ohio|indiana|illinois|michigan|wisconsin|minnesota|iowa|missouri|north dakota|south dakota|nebraska|kansas|oklahoma|new mexico|wyoming|idaho|alaska|hawaii)\b/i)
    context[:state] = state_match[1].downcase if state_match

    # Climate descriptors
    if text.match?(/\b(tropical|humid|subtropical)\b/i)
      context[:climate] = 'tropical'
    elsif text.match?(/\b(desert|arid|dry)\b/i)
      context[:climate] = 'arid'
    elsif text.match?(/\b(temperate|moderate)\b/i)
      context[:climate] = 'temperate'
    elsif text.match?(/\b(cold|northern|boreal)\b/i)
      context[:climate] = 'cold'
    end

    context
  end

  def extract_companion_requests(text)
    companions = []

    # Look for "companion for X" or "goes with X"
    companion_match = text.match(/\b(?:companion|pair|plant.*with|goes.*with|guild.*with)\s+(?:for\s+)?([a-zA-Z\s]+?)(?:\s|$|,|\?|!)/i)
    if companion_match
      plant_name = companion_match[1].strip
      companions << plant_name
    end

    # Common companion plants mentioned
    common_companions = %w[tomato tomatoes corn beans squash cucumber pepper peppers basil marigold nasturtium]
    common_companions.each do |companion|
      companions << companion if text.match?(/\b#{companion}\b/i)
    end

    companions.uniq
  end

  def extract_exclusions(text)
    exclusions = []

    # Look for "not", "avoid", "except", "without"
    exclusion_patterns = [
      /\b(?:not|avoid|except|without|no)\s+([a-zA-Z\s]+?)(?:\s|$|,|\?|!)/i,
      /\b(?:don.*want|don.*like|dislike)\s+([a-zA-Z\s]+?)(?:\s|$|,|\?|!)/i
    ]

    exclusion_patterns.each do |pattern|
      matches = text.scan(pattern)
      exclusions.concat(matches.flatten.map(&:strip))
    end

    exclusions
  end

  def semantic_search(parsed_query)
    plant_ids = Set.new

    # Search by extracted concepts
    parsed_query[:extracted_concepts].each do |concept_data|
      case concept_data[:type]
      when :ontology
        # Use ontology relationships
        ontology = concept_data[:concept]
        related_plants = ontology.enhanced_plants
                                .joins(:plant_ontology_tags)
                                .where('plant_ontology_tags.confidence_score >= ?', 0.6)
        plant_ids.merge(related_plants.pluck(:id))

      when :pattern
        # Use existing semantic tags
        tag = SemanticTag.find_by(name: concept_data[:concept].to_s)
        if tag
          related_plants = tag.enhanced_plants
                             .joins(:plant_semantic_tags)
                             .where('plant_semantic_tags.confidence_score >= ?', 0.6)
          plant_ids.merge(related_plants.pluck(:id))
        end
      end
    end

    EnhancedPlant.where(id: plant_ids.to_a).limit(limit)
  end

  def environmental_search(parsed_query)
    scope = EnhancedPlant.joins(:environmental_requirements)

    parsed_query[:environmental_filters].each do |filter_type, value|
      case filter_type
      when :hardiness_zone
        zone_num = value.to_i
        scope = scope.where(
          'environmental_requirements.hardiness_zone_min <= ? AND environmental_requirements.hardiness_zone_max >= ?',
          zone_num, zone_num
        )
      when :light_requirement
        scope = scope.where(environmental_requirements: { light_requirement: value })
      when :water_requirement
        case value
        when 'low'
          scope = scope.where('environmental_requirements.drought_tolerance_score >= ?', 0.7)
        when 'high'
          scope = scope.where('environmental_requirements.water_requirement_score >= ?', 0.7)
        end
      end
    end

    scope.limit(limit)
  end

  def companion_search(parsed_query)
    return EnhancedPlant.none if parsed_query[:companion_requests].empty?

    companion_plants = []

    parsed_query[:companion_requests].each do |companion_name|
      # Find the companion plant
      base_plant = EnhancedPlant.where('common_name ILIKE ?', "%#{companion_name}%").first
      next unless base_plant

      # Find its companions
      companions = base_plant.plant_relationships
                            .where(relationship_type: ['companion', 'beneficial', 'guild_member'])
                            .includes(:related_plant)
                            .map(&:related_plant)

      companion_plants.concat(companions)
    end

    EnhancedPlant.where(id: companion_plants.map(&:id)).limit(limit)
  end

  def regional_search(parsed_query)
    return EnhancedPlant.none if parsed_query[:geographic_context].empty?

    scope = EnhancedPlant.all

    if state = parsed_query[:geographic_context][:state]
      # This would require regional data in your database
      # For now, we'll use a simple approach
      scope = scope.joins(:plant_regions)
                  .where('plant_regions.region_name ILIKE ?', "%#{state}%")
    end

    scope.limit(limit)
  end

  def combine_and_rank_results(results, parsed_query)
    # Weight different result types
    weights = {
      semantic_matches: 0.4,
      environmental_matches: 0.3,
      companion_matches: 0.2,
      regional_matches: 0.1
    }

    plant_scores = {}

    results.each do |result_type, plants|
      plants.each do |plant|
        plant_scores[plant.id] ||= { plant: plant, score: 0, sources: [] }
        plant_scores[plant.id][:score] += weights[result_type]
        plant_scores[plant.id][:sources] << result_type
      end
    end

    # Apply exclusions
    if parsed_query[:exclusions].any?
      exclusion_pattern = parsed_query[:exclusions].map { |ex| "%#{ex}%" }
      plant_scores.reject! do |plant_id, data|
        plant = data[:plant]
        exclusion_pattern.any? do |pattern|
          plant.common_name&.match?(/#{Regexp.escape(pattern.gsub('%', ''))}/i) ||
          plant.description_detailed&.match?(/#{Regexp.escape(pattern.gsub('%', ''))}/i)
        end
      end
    end

    # Sort by score and return plants
    plant_scores.values
                .sort_by { |data| -data[:score] }
                .first(limit)
                .map { |data| data[:plant] }
  end

  def generate_search_metadata(results)
    {
      total_semantic_matches: results[:semantic_matches].count,
      total_environmental_matches: results[:environmental_matches].count,
      total_companion_matches: results[:companion_matches].count,
      total_regional_matches: results[:regional_matches].count,
      search_timestamp: Time.current,
      ai_provider: ai_provider
    }
  end

  def check_query_cache
    query_hash = Digest::SHA256.hexdigest(@query.downcase.strip)

    cached = AiQueryCache.find_by(query_hash: query_hash)
    return nil unless cached

    # Update access time and hit count
    cached.update!(
      last_accessed_at: Time.current,
      hit_count: cached.hit_count + 1
    )

    # Return cached plants
    plant_ids = cached.plant_ids || []
    plants = EnhancedPlant.where(id: plant_ids)

    {
      plants: plants,
      query_analysis: { cached: true, original_query: @query },
      search_metadata: { source: :cache, hit_count: cached.hit_count }
    }
  end

  def cache_results(plants)
    query_hash = Digest::SHA256.hexdigest(@query.downcase.strip)
    plant_ids = plants.respond_to?(:pluck) ? plants.pluck(:id) : plants.map(&:id)

    AiQueryCache.create!(
      query_text: @query,
      query_hash: query_hash,
      plant_ids: plant_ids,
      response_data: {
        plant_count: plant_ids.length,
        generated_at: Time.current
      },
      last_accessed_at: Time.current
    )
  rescue ActiveRecord::RecordNotUnique
    # Query already cached, update it
    cached = AiQueryCache.find_by(query_hash: query_hash)
    cached&.update!(
      plant_ids: plant_ids,
      last_accessed_at: Time.current,
      hit_count: cached.hit_count + 1
    )
  end
end