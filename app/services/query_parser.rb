class QueryParser
  INTENT_PATTERNS = {
    'find_by_name' => [
      /what is/i,
      /tell me about/i,
      /information about/i,
      /show me/i,
      /find.*plant.*called/i
    ],
    'find_by_conditions' => [
      /plants? (?:that|which) (?:grow|thrive) in/i,
      /good for/i,
      /suitable for/i,
      /tolerates?/i,
      /can handle/i,
      /grows? in/i
    ],
    'companion_planting' => [
      /companion/i,
      /plant with/i,
      /goes well with/i,
      /guild/i,
      /pair with/i,
      /grow.*together/i
    ],
    'problem_solving' => [
      /pest control/i,
      /nitrogen fix/i,
      /erosion control/i,
      /ground cover/i,
      /attract.*pollinators/i,
      /repel.*pests/i
    ]
  }.freeze

  CONDITION_PATTERNS = {
    'drought' => /drought|dry|arid|water[- ]wise|xerophytic/i,
    'shade' => /shade|shady|low light|dark/i,
    'poor_soil' => /poor soil|bad soil|clay|sandy|rocky/i,
    'cold' => /cold|frost|winter|hardy|freeze/i,
    'hot' => /hot|heat|summer|warm/i,
    'wet' => /wet|moist|boggy|swampy|flood/i,
    'windy' => /wind|windy|exposed/i,
    'acidic' => /acidic|acid|low ph/i,
    'alkaline' => /alkaline|basic|high ph/i,
    'salty' => /salt|saline|coastal/i
  }.freeze

  TRAIT_PATTERNS = {
    'fast_growing' => /fast[- ]growing|rapid growth|quick|vigorous/i,
    'slow_growing' => /slow[- ]growing|slow growth/i,
    'tall' => /tall|high|large/i,
    'short' => /short|small|compact|dwarf/i,
    'spreading' => /spreading|wide|broad/i,
    'climbing' => /climbing|vine|vining/i,
    'evergreen' => /evergreen|year[- ]round/i,
    'deciduous' => /deciduous|loses leaves/i,
    'fragrant' => /fragrant|scented|aromatic/i,
    'colorful' => /colorful|bright|showy/i,
    'edible' => /edible|food|eat|fruit|vegetable/i,
    'medicinal' => /medicinal|medicine|healing/i,
    'native' => /native|indigenous/i,
    'invasive' => /invasive|aggressive|spreads/i
  }.freeze

  USE_PATTERNS = {
    'food' => /food|edible|eat|fruit|vegetable|herb|spice/i,
    'medicine' => /medicinal|medicine|healing|therapeutic/i,
    'timber' => /timber|wood|lumber|construction/i,
    'ornamental' => /ornamental|decorative|beautiful|landscape/i,
    'wildlife' => /wildlife|birds|pollinators|bees|butterflies/i,
    'erosion_control' => /erosion|slope|bank|stabilize/i,
    'windbreak' => /windbreak|wind protection|shelter/i,
    'privacy' => /privacy|screen|hedge|barrier/i
  }.freeze

  def parse(query)
    {
      intent: extract_intent(query),
      keywords: extract_keywords(query),
      traits: extract_traits(query),
      conditions: extract_conditions(query),
      uses: extract_uses(query),
      plant_names: extract_plant_names(query),
      zones: extract_zones(query),
      measurements: extract_measurements(query)
    }
  end

  private

  def extract_intent(query)
    INTENT_PATTERNS.each do |intent, patterns|
      return intent if patterns.any? { |pattern| query.match?(pattern) }
    end
    'general_search'
  end

  def extract_keywords(query)
    # Remove common stop words and extract meaningful terms
    stop_words = %w[the a an and or but in on at to for of with by from up about into over after]
    
    words = query.downcase
                 .gsub(/[^\w\s]/, ' ')
                 .split(/\s+/)
                 .reject { |word| stop_words.include?(word) || word.length < 3 }
    
    # Remove duplicates and return
    words.uniq
  end

  def extract_traits(query)
    traits = []
    TRAIT_PATTERNS.each do |trait, pattern|
      traits << trait.to_s if query.match?(pattern)
    end
    traits
  end

  def extract_conditions(query)
    conditions = []
    CONDITION_PATTERNS.each do |condition, pattern|
      conditions << condition.to_s if query.match?(pattern)
    end
    conditions
  end

  def extract_uses(query)
    uses = []
    USE_PATTERNS.each do |use, pattern|
      uses << use.to_s if query.match?(pattern)
    end
    uses
  end

  def extract_plant_names(query)
    plant_names = []
    
    # Check against known plant names in database
    # This is a simplified approach - in production you'd want more sophisticated NER
    if defined?(EnhancedPlant)
      common_names = EnhancedPlant.pluck(:common_name).compact
      scientific_names = EnhancedPlant.pluck(:scientific_name).compact
      alias_names = PlantName.pluck(:name).compact if defined?(PlantName)
      
      all_names = (common_names + scientific_names + (alias_names || [])).uniq
      
      all_names.each do |name|
        if query.downcase.include?(name.downcase)
          plant_names << name
        end
      end
    end
    
    # Also look for capitalized words that might be plant names
    capitalized_words = query.scan(/\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\b/)
    plant_names += capitalized_words
    
    plant_names.uniq
  end

  def extract_zones(query)
    zones = []
    
    # Look for hardiness zone patterns
    zone_matches = query.scan(/zone\s*(\d+[ab]?)/i)
    zones += zone_matches.flatten.map(&:downcase)
    
    # Look for direct zone numbers
    zone_numbers = query.scan(/\b(\d+[ab]?)\s*zone/i)
    zones += zone_numbers.flatten.map(&:downcase)
    
    zones.uniq
  end

  def extract_measurements(query)
    measurements = {}
    
    # Height measurements
    height_matches = query.scan(/(\d+(?:\.\d+)?)\s*(?:feet|ft|meters?|m)\s*(?:tall|high)/i)
    if height_matches.any?
      value, unit = height_matches.first
      measurements[:max_height] = convert_to_cm(value.to_f, unit.downcase)
    end
    
    # Width measurements
    width_matches = query.scan(/(\d+(?:\.\d+)?)\s*(?:feet|ft|meters?|m)\s*(?:wide|across)/i)
    if width_matches.any?
      value, unit = width_matches.first
      measurements[:max_width] = convert_to_cm(value.to_f, unit.downcase)
    end
    
    # Size descriptors
    if query.match?(/small|compact|dwarf/i)
      measurements[:max_height] = 200 # 2 meters
    elsif query.match?(/large|big|tall/i)
      measurements[:min_height] = 300 # 3 meters
    end
    
    measurements
  end

  def convert_to_cm(value, unit)
    case unit
    when /feet?|ft/
      (value * 30.48).round
    when /meters?|m/
      (value * 100).round
    else
      value.round
    end
  end
end 