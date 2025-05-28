# Implementation Examples for Enhanced PermieBro Schema

## Data Migration Scripts

### 1. Migrating Existing Plant Data

```ruby
# Migration script to convert existing plants to new schema
class MigrateToEnhancedSchema < ActiveRecord::Migration[7.1]
  def up
    # Create new tables (schema from previous document)
    create_enhanced_tables
    
    # Migrate existing plant data
    migrate_plant_data
    migrate_environmental_data
    migrate_uses_data
    migrate_relationships
  end
  
  private
  
  def migrate_plant_data
    Plant.find_each do |old_plant|
      new_plant = EnhancedPlant.create!(
        common_name: old_plant.common_name,
        scientific_name: old_plant.scientific_name,
        family: old_plant.family,
        plant_type: infer_plant_type(old_plant.layers),
        life_cycle: old_plant.perennial? ? 'perennial' : 'annual',
        description_short: extract_short_description(old_plant.description),
        description_detailed: old_plant.description,
        growing_notes: old_plant.purpose,
        data_quality_score: calculate_data_quality(old_plant)
      )
      
      # Migrate aliases
      migrate_aliases(old_plant, new_plant)
      
      # Generate initial embedding
      generate_embedding(new_plant)
    end
  end
  
  def migrate_environmental_data
    Plant.find_each do |old_plant|
      new_plant = EnhancedPlant.find_by(scientific_name: old_plant.scientific_name)
      
      # Parse zone range
      zone_min, zone_max = parse_zone_range(old_plant.zone_range)
      
      EnvironmentalRequirement.create!(
        plant_id: new_plant.id,
        hardiness_zone_min: zone_min,
        hardiness_zone_max: zone_max,
        temp_optimal_min: parse_temperature(old_plant.ideal_temp_min),
        temp_optimal_max: parse_temperature(old_plant.ideal_temp_max),
        temp_min_survival: parse_temperature(old_plant.min_temp),
        temp_max_survival: parse_temperature(old_plant.max_temp),
        light_requirement: infer_light_requirement(old_plant.layers),
        climate_description: extract_climate_description(old_plant.description)
      )
    end
  end
  
  def migrate_uses_data
    Plant.find_each do |old_plant|
      new_plant = EnhancedPlant.find_by(scientific_name: old_plant.scientific_name)
      
      # Convert plant_functions array to structured uses
      old_plant.plant_functions.each do |function|
        use_category = find_or_create_use_category(function)
        
        PlantUse.create!(
          plant_id: new_plant.id,
          use_category_id: use_category.id,
          effectiveness_score: 0.8, # Default confidence
          confidence_score: 0.7
        )
      end
    end
  end
  
  def migrate_relationships
    Plant.find_each do |old_plant|
      new_plant = EnhancedPlant.find_by(scientific_name: old_plant.scientific_name)
      
      # Migrate companions
      old_plant.companions.each do |companion_name|
        companion = find_plant_by_name(companion_name)
        next unless companion
        
        PlantRelationship.create!(
          plant_a_id: new_plant.id,
          plant_b_id: companion.id,
          relationship_type_id: beneficial_companion_type.id,
          strength_score: 0.7,
          confidence_score: 0.6,
          evidence_type: 'traditional'
        )
      end
      
      # Migrate avoid list
      old_plant.avoid.each do |avoid_name|
        avoided_plant = find_plant_by_name(avoid_name)
        next unless avoided_plant
        
        PlantRelationship.create!(
          plant_a_id: new_plant.id,
          plant_b_id: avoided_plant.id,
          relationship_type_id: antagonistic_type.id,
          strength_score: 0.8,
          confidence_score: 0.6,
          evidence_type: 'traditional'
        )
      end
    end
  end
end
```

### 2. Trait Extraction from Descriptions

```ruby
class TraitExtractor
  TRAIT_PATTERNS = {
    'drought_tolerance' => [
      /drought[- ]tolerant/i,
      /drought[- ]resistant/i,
      /dry conditions/i,
      /water[- ]wise/i
    ],
    'growth_rate' => [
      /fast[- ]growing/i,
      /rapid growth/i,
      /slow[- ]growing/i,
      /vigorous/i
    ],
    'soil_preference' => [
      /well[- ]drained/i,
      /sandy soil/i,
      /clay soil/i,
      /rich soil/i,
      /poor soil/i
    ]
  }.freeze
  
  def self.extract_traits_from_text(plant, text)
    TRAIT_PATTERNS.each do |trait_name, patterns|
      patterns.each do |pattern|
        if text.match?(pattern)
          create_trait(plant, trait_name, extract_value(text, pattern))
        end
      end
    end
  end
  
  private
  
  def self.create_trait(plant, trait_name, value)
    category = TraitCategory.find_or_create_by(name: trait_name)
    
    PlantTrait.create!(
      plant_id: plant.id,
      trait_category_id: category.id,
      text_value: value,
      confidence_score: 0.6, # Lower confidence for extracted traits
      source: 'text_extraction'
    )
  end
end
```

## Search API Implementation

### 1. Multi-Modal Search Service

```ruby
class PlantSearchService
  def initialize
    @embedding_service = EmbeddingService.new
    @trait_matcher = TraitMatcher.new
  end
  
  def search(query, options = {})
    # Parse query for intent and entities
    parsed_query = QueryParser.parse(query)
    
    # Multiple search strategies
    results = {
      semantic: semantic_search(query, options),
      keyword: keyword_search(parsed_query[:keywords], options),
      trait: trait_search(parsed_query[:traits], options),
      environmental: environmental_search(parsed_query[:conditions], options)
    }
    
    # Combine and rank results
    combine_results(results, parsed_query[:intent])
  end
  
  private
  
  def semantic_search(query, options)
    return [] unless options[:enable_semantic]
    
    embedding = @embedding_service.generate_embedding(query)
    
    Plant.joins(:environmental_requirements)
         .select("plants.*, 
                  1 - (plants.embedding_vector <=> '#{embedding}') as similarity_score")
         .where("1 - (plants.embedding_vector <=> ?) > ?", 
                embedding, options[:similarity_threshold] || 0.6)
         .order("plants.embedding_vector <=> '#{embedding}'")
         .limit(options[:limit] || 20)
  end
  
  def keyword_search(keywords, options)
    return [] if keywords.empty?
    
    query_string = keywords.join(' & ')
    
    Plant.joins(:plant_names)
         .where("plants.search_vector @@ plainto_tsquery('english', ?) 
                 OR plant_names.name ILIKE ANY(?)",
                query_string,
                keywords.map { |k| "%#{k}%" })
         .select("plants.*, 
                  ts_rank(plants.search_vector, plainto_tsquery('english', ?)) as rank_score",
                 query_string)
         .order('rank_score DESC')
         .distinct
         .limit(options[:limit] || 20)
  end
  
  def trait_search(traits, options)
    return [] if traits.empty?
    
    @trait_matcher.find_plants_by_traits(traits, options)
  end
  
  def environmental_search(conditions, options)
    return [] if conditions.empty?
    
    EnvironmentalMatcher.new.find_suitable_plants(conditions, options)
  end
  
  def combine_results(results, intent)
    # Weight different result types based on query intent
    weights = case intent
    when 'find_by_name'
      { keyword: 0.7, semantic: 0.2, trait: 0.1, environmental: 0.0 }
    when 'find_by_conditions'
      { environmental: 0.5, trait: 0.3, semantic: 0.2, keyword: 0.0 }
    when 'general_search'
      { semantic: 0.4, keyword: 0.3, trait: 0.2, environmental: 0.1 }
    else
      { semantic: 0.25, keyword: 0.25, trait: 0.25, environmental: 0.25 }
    end
    
    # Combine and score results
    combined_scores = {}
    
    results.each do |type, plants|
      plants.each do |plant|
        plant_id = plant.id
        score = (plant.try(:similarity_score) || 
                plant.try(:rank_score) || 
                plant.try(:suitability_score) || 0.5)
        
        combined_scores[plant_id] ||= { plant: plant, total_score: 0 }
        combined_scores[plant_id][:total_score] += score * weights[type]
      end
    end
    
    # Sort by combined score and return plants
    combined_scores.values
                   .sort_by { |result| -result[:total_score] }
                   .map { |result| result[:plant] }
                   .first(20)
  end
end
```

### 2. Fuzzy Trait Matching

```ruby
class TraitMatcher
  FUZZY_MAPPINGS = {
    'dry heat' => {
      drought_tolerance_score: { min: 0.7 },
      temp_optimal_max: { min: 30 }
    },
    'shade tolerant' => {
      light_requirement: ['full_shade', 'partial_shade']
    },
    'fast growing' => {
      growth_rate: ['fast', 'vigorous', 'rapid']
    },
    'attracts butterflies' => {
      pollinator_attractant: true,
      flower_color: ['purple', 'pink', 'red', 'orange']
    }
  }.freeze
  
  def find_plants_by_traits(trait_queries, options = {})
    plants = Plant.joins(:plant_traits, :environmental_requirements)
    
    trait_queries.each do |query|
      plants = apply_trait_filter(plants, query)
    end
    
    plants.select("plants.*, 
                   AVG(plant_traits.confidence_score) as avg_confidence")
          .group('plants.id')
          .having('AVG(plant_traits.confidence_score) > ?', 
                  options[:min_confidence] || 0.5)
          .order('avg_confidence DESC')
          .limit(options[:limit] || 20)
  end
  
  private
  
  def apply_trait_filter(plants, query)
    # Direct trait matching
    if mapping = FUZZY_MAPPINGS[query.downcase]
      apply_fuzzy_mapping(plants, mapping)
    else
      # Semantic trait matching using embeddings
      apply_semantic_trait_matching(plants, query)
    end
  end
  
  def apply_fuzzy_mapping(plants, mapping)
    conditions = []
    params = []
    
    mapping.each do |trait, criteria|
      case criteria
      when Hash
        if criteria[:min]
          conditions << "plant_traits.numeric_value >= ?"
          params << criteria[:min]
        end
        if criteria[:max]
          conditions << "plant_traits.numeric_value <= ?"
          params << criteria[:max]
        end
      when Array
        conditions << "plant_traits.categorical_value IN (?)"
        params << criteria
      when TrueClass, FalseClass
        conditions << "plant_traits.boolean_value = ?"
        params << criteria
      end
    end
    
    plants.where(conditions.join(' OR '), *params)
  end
end
```

### 3. Natural Language Query Processing

```ruby
class QueryParser
  INTENT_PATTERNS = {
    'find_by_name' => [
      /what is/i,
      /tell me about/i,
      /information about/i
    ],
    'find_by_conditions' => [
      /plants? (?:that|which) (?:grow|thrive) in/i,
      /good for/i,
      /suitable for/i,
      /tolerates?/i
    ],
    'companion_planting' => [
      /companion/i,
      /plant with/i,
      /goes well with/i,
      /guild/i
    ],
    'problem_solving' => [
      /pest control/i,
      /nitrogen fix/i,
      /erosion control/i,
      /ground cover/i
    ]
  }.freeze
  
  CONDITION_PATTERNS = {
    'drought' => /drought|dry|arid|water[- ]wise/i,
    'shade' => /shade|shady|low light/i,
    'poor_soil' => /poor soil|bad soil|clay|sandy/i,
    'cold' => /cold|frost|winter|hardy/i,
    'hot' => /hot|heat|summer|warm/i
  }.freeze
  
  def self.parse(query)
    {
      intent: extract_intent(query),
      keywords: extract_keywords(query),
      traits: extract_traits(query),
      conditions: extract_conditions(query),
      plant_names: extract_plant_names(query)
    }
  end
  
  private
  
  def self.extract_intent(query)
    INTENT_PATTERNS.each do |intent, patterns|
      return intent if patterns.any? { |pattern| query.match?(pattern) }
    end
    'general_search'
  end
  
  def self.extract_conditions(query)
    conditions = []
    CONDITION_PATTERNS.each do |condition, pattern|
      conditions << condition if query.match?(pattern)
    end
    conditions
  end
  
  def self.extract_plant_names(query)
    # Simple approach - look for capitalized words that might be plant names
    # In production, you'd want a more sophisticated NER system
    plant_names = []
    
    # Check against known plant names in database
    Plant.pluck(:common_name, :scientific_name).flatten.each do |name|
      if query.downcase.include?(name.downcase)
        plant_names << name
      end
    end
    
    plant_names
  end
end
```

## GPT Integration Layer

### 1. Context-Aware Plant Recommendations

```ruby
class GPTPlantAdvisor
  def initialize
    @client = OpenAI::Client.new(access_token: ENV['OPENAI_API_KEY'])
    @search_service = PlantSearchService.new
  end
  
  def get_recommendations(user_query, context = {})
    # First, get relevant plants from database
    candidate_plants = @search_service.search(user_query, enable_semantic: true)
    
    # Prepare context for GPT
    plant_context = prepare_plant_context(candidate_plants.first(10))
    user_context = prepare_user_context(context)
    
    # Generate GPT response with plant data
    response = @client.chat(
      parameters: {
        model: "gpt-4",
        messages: [
          {
            role: "system",
            content: build_system_prompt(plant_context, user_context)
          },
          {
            role: "user",
            content: user_query
          }
        ],
        temperature: 0.7,
        max_tokens: 1000
      }
    )
    
    {
      recommendation: response.dig("choices", 0, "message", "content"),
      source_plants: candidate_plants.first(5),
      confidence: calculate_confidence(candidate_plants, user_query)
    }
  end
  
  private
  
  def prepare_plant_context(plants)
    plants.map do |plant|
      {
        name: plant.common_name,
        scientific_name: plant.scientific_name,
        description: plant.description_short,
        growing_notes: plant.growing_notes,
        uses: plant.plant_uses.includes(:use_category)
                   .map { |use| use.use_category.name },
        environmental_needs: {
          zones: "#{plant.environmental_requirements&.hardiness_zone_min}-#{plant.environmental_requirements&.hardiness_zone_max}",
          light: plant.environmental_requirements&.light_requirement,
          water: plant.environmental_requirements&.drought_tolerance_score
        },
        companions: plant.beneficial_companions.pluck(:common_name),
        avoid: plant.antagonistic_plants.pluck(:common_name)
      }
    end
  end
  
  def build_system_prompt(plant_context, user_context)
    <<~PROMPT
      You are PermieBro, an expert permaculture advisor. You help people choose 
      appropriate plants for their specific conditions and goals.
      
      User Context:
      - Location: #{user_context[:location] || 'Not specified'}
      - Climate Zone: #{user_context[:zone] || 'Not specified'}
      - Garden Size: #{user_context[:size] || 'Not specified'}
      - Experience Level: #{user_context[:experience] || 'Not specified'}
      
      Available Plants Database:
      #{plant_context.to_json}
      
      Guidelines:
      1. Recommend plants from the provided database that best match the user's needs
      2. Consider climate compatibility, space requirements, and user experience level
      3. Suggest companion planting opportunities when relevant
      4. Mention any warnings or special considerations
      5. Provide practical growing tips
      6. Keep recommendations focused and actionable
      
      Always cite specific plants from the database and explain why they're suitable.
    PROMPT
  end
end
```

### 2. Embedding Generation Service

```ruby
class EmbeddingService
  def initialize
    @client = OpenAI::Client.new(access_token: ENV['OPENAI_API_KEY'])
  end
  
  def generate_plant_embeddings
    Plant.find_each do |plant|
      next if plant.embedding_vector.present?
      
      text_for_embedding = build_embedding_text(plant)
      embedding = generate_embedding(text_for_embedding)
      
      plant.update!(embedding_vector: embedding)
      
      # Rate limiting
      sleep(0.1)
    end
  end
  
  def generate_embedding(text)
    response = @client.embeddings(
      parameters: {
        model: "text-embedding-ada-002",
        input: text
      }
    )
    
    response.dig("data", 0, "embedding")
  end
  
  private
  
  def build_embedding_text(plant)
    parts = [
      plant.common_name,
      plant.scientific_name,
      plant.description_short,
      plant.growing_notes,
      plant.plant_uses.includes(:use_category).map(&:use_category).map(&:name).join(', '),
      plant.environmental_requirements&.climate_description,
      plant.environmental_requirements&.soil_description
    ].compact
    
    parts.join('. ')
  end
end
```

## Usage Examples

### 1. Natural Language Queries

```ruby
# Example queries that the enhanced system can handle:

# Basic plant lookup
search_service.search("What is comfrey good for?")

# Environmental conditions
search_service.search("Plants that grow well in dry heat")

# Companion planting
search_service.search("What can I plant with tomatoes?")

# Problem-solving
search_service.search("Ground cover for shady areas")

# Complex conditions
search_service.search("Edible plants for zone 7 that attract pollinators")

# Fuzzy matching
search_service.search("Something like mint but less invasive")
```

### 2. GPT-Enhanced Responses

```ruby
advisor = GPTPlantAdvisor.new

context = {
  location: "Pacific Northwest",
  zone: "8b",
  size: "small urban garden",
  experience: "beginner"
}

response = advisor.get_recommendations(
  "I want to start a food forest in my backyard", 
  context
)

puts response[:recommendation]
# => "For a small urban food forest in zone 8b Pacific Northwest, I recommend 
#     starting with these plants from our database:
#     
#     Canopy Layer: Consider dwarf fruit trees like...
#     Understory: Serviceberry (Amelanchier canadensis) provides...
#     Ground Cover: Wild ginger (Asarum canadense) thrives in..."
```

This implementation provides a robust foundation for the enhanced PermieBro database with sophisticated search capabilities and GPT integration while maintaining offline functionality. 