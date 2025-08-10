# frozen_string_literal: true

class PermieGptService
  include HTTParty
  include SemanticTagsHelper
  include Retryable

  # Configuration
  base_uri ENV.fetch('OLLAMA_BASE_URL', 'http://localhost:11434')
  default_timeout 30
  retry_on [Timeout::Error, Net::ReadTimeout, Net::OpenTimeout], attempts: 3, base_sleep_seconds: 1

  # Constants for configuration
  OLLAMA_MODEL = ENV.fetch('OLLAMA_MODEL', 'mistral')
  REQUEST_TIMEOUT = 30.seconds
  CACHE_EXPIRY = 1.hour
  MAX_RETRIES = 3
  RETRY_DELAY = 1.second
  MAX_TOKENS = 4096
  TEMPERATURE = 0.7
  TOP_P = 0.9
  BATCH_SIZE = 50
  MAX_PROMPT_LENGTH = 4000
  MIN_SIMILARITY = 0.6

  # Initialize with configuration
  def initialize
    @model = OLLAMA_MODEL
    @cache = ActiveSupport::Cache::RedisCacheStore.new(
      url: ENV.fetch('REDIS_URL', 'redis://localhost:6379/1'),
      expires_in: 1.hour
    )
    @semantic_tags = load_semantic_tags
    @plant_extractor = PlantNameExtractorService.new
    @ollama_client = OllamaClient.new
  end

  # Main query method with optimized error handling
  def query(params)
    cache_key = generate_cache_key(params)
    
    # Try to get from cache first
    cached_response = @cache.read(cache_key)
    return cached_response if cached_response.present?

    # Generate new response
    response = generate_response(params)
    
    # Cache successful response
    @cache.write(cache_key, response) if response[:success]
    
    response
  rescue StandardError => e
    Rails.logger.error("PermieGPT Error: #{e.message}")
    {
      success: false,
      error: "Failed to generate response",
      message: e.message
    }
  end

  # Stream response for long-running queries
  def stream_query(context, &block)
    return error_response("Invalid context") unless valid_context?(context)

    # Process query with retries
    with_retries(max_attempts: MAX_RETRIES, base_sleep_seconds: RETRY_DELAY) do
      process_stream(context, &block)
    end
  rescue StandardError => e
    Rails.logger.error("Stream Error: #{e.message}")
    error_response("An error occurred while processing your request")
  end

  # Health check with optimized database query
  def health_check
    # Check database connection
    db_healthy = ActiveRecord::Base.connection.execute("SELECT 1").first.present?
    
    # Check AI service
    ai_healthy = @ollama_client.health_check
    
    {
      success: true,
      data: {
        database: db_healthy,
        llm_available: ai_healthy,
        model: ENV.fetch('OLLAMA_MODEL', 'mistral'),
        timestamp: Time.current
      }
    }
  end

  private

  def generate_response(params)
    prompt = build_prompt(params)
    
    # Make Ollama request
    ollama_response = @ollama_client.generate_completion(prompt)
    
    if ollama_response[:success]
      {
        success: true,
        response: ollama_response[:text],
        usage: ollama_response[:usage]
      }
    else
      {
        success: false,
        error: "Ollama request failed",
        message: ollama_response[:error]
      }
    end
  end

  def build_prompt(params)
    <<~PROMPT
      You are a permaculture gardening expert. Please provide detailed advice for the following query:

      Query: #{params[:query]}
      Location: #{params[:location]}
      Growing Zone: #{params[:zone]}
      Soil Type: #{params[:soil]}
      Experience Level: #{params[:experience_level]}
      Goals: #{params[:goals].join(', ')}

      Please provide:
      1. Specific plant recommendations
      2. Growing tips
      3. Companion planting suggestions
      4. Maintenance advice
      5. Any relevant warnings or considerations

      Format the response in clear, easy-to-follow sections.
    PROMPT
  end

  def generate_cache_key(params)
    [
      'permie_gpt',
      params[:query],
      params[:location],
      params[:zone],
      params[:soil],
      params[:experience_level],
      params[:goals].sort.join(',')
    ].join(':')
  end

  # Process query with optimized context building
  def process_query(params)
    # Extract plant names
    plant_names = extract_plant_names(params[:query])
    
    # Build context with optimized data loading
    context = build_context(params, plant_names)
    
    # Generate prompt
    prompt = build_prompt(params)
    
    # Make API request
    response = make_api_request(prompt)
    
    # Process and cache response
    process_response(response, params)
  end

  # Process stream with optimized data handling
  def process_stream(context, &block)
    # Extract plant names
    plant_names = @plant_extractor.extract_plant_names(context[:query])
    
    # Build context with optimized data loading
    enhanced_context = build_context(context, plant_names)
    
    # Stream response
    stream_response(enhanced_context, &block)
  end

  # Build context with optimized data loading
  def build_context(params, plant_names)
    # Load plant data in a single query with eager loading
    plants = EnhancedPlant.includes(
      :environmental_requirements,
      :plant_uses,
      :plant_traits,
      :semantic_tags
    ).where(
      'LOWER(common_name) = ANY(ARRAY[?]) OR LOWER(scientific_name) = ANY(ARRAY[?])',
      plant_names,
      plant_names
    )

    # Get common plant combinations
    combinations = get_common_combinations(plants)

    {
      location: params[:location],
      zone: params[:zone],
      soil: params[:soil],
      experience_level: params[:experience_level],
      goals: params[:goals],
      plants: plants,
      combinations: combinations
    }
  end

  # Get common plant combinations from materialized view
  def get_common_combinations(plants)
    return [] if plants.empty?

    plant_names = plants.map(&:common_name)
    
    ActiveRecord::Base.connection.execute(
      "SELECT plant1, plant2, co_occurrence_count 
       FROM common_plant_combinations 
       WHERE plant1 = ANY(ARRAY[?]) OR plant2 = ANY(ARRAY[?])
       ORDER BY co_occurrence_count DESC
       LIMIT 5",
      plant_names,
      plant_names
    ).values
  end

  # Make API request with retries
  def make_api_request(prompt)
    response = self.class.post(
      '/api/generate',
      body: prompt.to_json,
      headers: { 'Content-Type' => 'application/json' }
    )

    raise "API request failed: #{response.code}" unless response.success?
    response
  end

  # Process API response
  def process_response(response, params)
    result = {
      success: true,
      data: {
        response: response.parsed_response['response'],
        knowledge_gaps: identify_knowledge_gaps(response.parsed_response['response'])
      }
    }

    # Cache successful response
    @cache.write(generate_cache_key(params), result)
    result
  end

  # Stream response with optimized data handling
  def stream_response(context, &block)
    prompt = build_prompt(context)
    
    # Check prompt length
    if prompt.length > MAX_PROMPT_LENGTH
      prompt = truncate_prompt(prompt)
    end

    # Stream completion
    @ollama_client.stream_completion(prompt, &block)
  end

  # Identify knowledge gaps in response
  def identify_knowledge_gaps(response)
    gaps = []
    
    # Check for missing information
    gaps << { gap: "Local climate specifics", recommendation: "Consider adding more local climate data" } if response.include?("climate")
    gaps << { gap: "Soil details", recommendation: "Add more soil-specific information" } if response.include?("soil")
    gaps << { gap: "Plant interactions", recommendation: "Include more plant interaction data" } if response.include?("interaction")
    
    gaps
  end

  # Error response helper
  def error_response(message)
    {
      success: false,
      error: message,
      fallback_response: generate_fallback_response
    }
  end

  # Generate fallback response
  def generate_fallback_response
    {
      response: "I apologize, but I'm having trouble accessing the AI model right now. Here's a basic response based on traditional permaculture principles:\n\n" +
                "1. Start with a site analysis\n" +
                "2. Consider local climate and soil conditions\n" +
                "3. Choose plants that are well-suited to your specific conditions\n" +
                "4. Implement appropriate growing techniques\n" +
                "5. Monitor and adjust as needed\n\n" +
                "Would you like me to try the search again, or would you prefer to use the traditional search filters?",
      knowledge_gaps: []
    }
  end

  # Extract plant names with improved accuracy
  def extract_plant_names(text)
    return [] unless text.present?

    # Use database function for fuzzy matching
    words = text.downcase.split(/\W+/)
    words = words.reject { |w| w.length < 3 }
    
    # Batch check existence using database function
    result = ActiveRecord::Base.connection.execute(
      "SELECT plant_name, exists FROM batch_check_plant_existence(ARRAY[?])",
      words
    )

    # Return only existing plants
    result.values.select { |_, exists| exists }.map(&:first)
  end

  # Constants for excluded words and patterns
  EXCLUDED_WORDS = %w[
    how what when where why which who
    and or but if then else
    the a an in on at to for
    with by from about like
    first second third
    one two three
    this that these those
    gardening magic sunshine soil savvy
    growing tips tricks stake pinch mulch retain
    want need help looking find
    best good great amazing
    please thank thanks
    would could should
    make grow plant
    garden yard space
    area spot place
    zone climate weather
    soil ground dirt
    water rain sun
    hot cold warm cool
    dry wet moist
    easy hard simple
    fast slow quick
    big small large tiny
    many few some
    all none any
    each every both
    either neither
    only just even
    still yet already
    again also too
    very really quite
    much many more
    less least most
    better best worse
    worst good great
    well fine nice
    bad poor wrong
    right correct true
    false wrong incorrect
    yes no maybe
    perhaps possibly
    probably definitely
    certainly surely
    actually basically
    generally normally
    usually typically
    commonly frequently
    rarely seldom
    never always
    often sometimes
    occasionally rarely
    hardly barely
    scarcely almost
    nearly about
    approximately roughly
    exactly precisely
    specifically particularly
    especially mainly
    mostly largely
    primarily chiefly
    principally essentially
    fundamentally basically
  ].freeze

  PLANT_PATTERNS = [
    /(?:grow|plant|cultivate|raise)\s+([a-z]+(?:\s+[a-z]+)*)/i,
    /(?:add|include|use|try)\s+([a-z]+(?:\s+[a-z]+)*)/i,
    /(?:looking for|searching for|want to grow)\s+([a-z]+(?:\s+[a-z]+)*)/i,
    /(?:best|good|great)\s+([a-z]+(?:\s+[a-z]+)*)\s+(?:for|in|at)/i,
    /(?:companion|partner|pair)\s+(?:with|for)\s+([a-z]+(?:\s+[a-z]+)*)/i,
    /(?:recommend|suggest)\s+([a-z]+(?:\s+[a-z]+)*)/i,
    /(?:thinking about|considering)\s+([a-z]+(?:\s+[a-z]+)*)/i,
    /(?:heard good things about|interested in)\s+([a-z]+(?:\s+[a-z]+)*)/i,
    /(?:need help with|struggling with)\s+([a-z]+(?:\s+[a-z]+)*)/i,
    /(?:tips for|advice on)\s+([a-z]+(?:\s+[a-z]+)*)/i
  ].freeze

  # Plant variations mapping
  def plant_variations
    {
      'passiflora' => ['passionflower', 'maypop', 'granadilla', 'blue passionflower', 'purple passionflower'],
      'ocimum' => ['basil', 'sweet basil', 'holy basil', 'thai basil', 'lemon basil', 'cinnamon basil', 'genovese basil', 'purple basil', 'ruffles basil'],
      'mentha' => ['mint', 'peppermint', 'spearmint', 'chocolate mint', 'apple mint', 'pineapple mint'],
      'rosmarinus' => ['rosemary', 'prostrate rosemary', 'upright rosemary', 'tuscan rosemary'],
      'thymus' => ['thyme', 'lemon thyme', 'creeping thyme', 'english thyme', 'french thyme'],
      'salvia' => ['sage', 'common sage', 'purple sage', 'golden sage', 'tricolor sage'],
      'lavandula' => ['lavender', 'english lavender', 'french lavender', 'spanish lavender'],
      'origanum' => ['oregano', 'greek oregano', 'italian oregano', 'golden oregano'],
      'petroselinum' => ['parsley', 'italian parsley', 'curly parsley', 'flat leaf parsley'],
      'allium' => ['chives', 'garlic chives', 'onion chives', 'siberian chives'],
      'melissa' => ['lemon balm', 'sweet melissa', 'common balm'],
      'calendula' => ['marigold', 'pot marigold', 'english marigold'],
      'echinacea' => ['coneflower', 'purple coneflower', 'pale purple coneflower'],
      'aloe' => ['aloe vera', 'medicinal aloe', 'barbados aloe'],
      'matricaria' => ['chamomile', 'german chamomile', 'roman chamomile'],
      'hypericum' => ['st johns wort', 'perforate st johns wort'],
      'valeriana' => ['valerian', 'garden valerian', 'common valerian'],
      'artemisia' => ['mugwort', 'common mugwort', 'sweet annie'],
      'tanacetum' => ['tansy', 'common tansy', 'golden buttons'],
      'achillea' => ['yarrow', 'common yarrow', 'milfoil']
    }
  end

  # Validate context
  def valid_context?(context)
    context.is_a?(Hash) && 
    context[:query].present? && 
    context[:query].is_a?(String)
  end

  # Truncate prompt while preserving important information
  def truncate_prompt(prompt)
    # Split into sections
    sections = prompt.split("\n\n")
    
    # Keep essential sections
    essential_sections = sections.select { |s| s.start_with?('Question:', 'Context:') }
    
    # Add truncated plant information
    plant_section = sections.find { |s| s.start_with?('Plants:') }
    if plant_section
      plants = plant_section.split("\n")[1..-1]
      truncated_plants = plants.first(3) + ["... (truncated)"] if plants.length > 3
      essential_sections << "Plants:\n#{truncated_plants.join("\n")}"
    end
    
    # Rebuild prompt
    essential_sections.join("\n\n")
  end
end 