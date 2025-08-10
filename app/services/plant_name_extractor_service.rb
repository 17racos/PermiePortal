class PlantNameExtractorService
  # Constants
  MIN_WORD_LENGTH = 3
  MAX_WORD_LENGTH = 50
  BATCH_SIZE = 50
  CACHE_EXPIRY = 1.hour
  SIMILARITY_THRESHOLD = 0.6

  # Initialize with configuration
  def initialize
    @cache = ActiveSupport::Cache::RedisCacheStore.new(
      url: ENV.fetch('REDIS_URL', 'redis://localhost:6379/1'),
      expires_in: 1.hour
    )
    @excluded_words = load_excluded_words
    @plant_patterns = load_plant_patterns
  end

  # Main extraction method with optimized processing
  def extract_plants(text)
    return [] if text.blank?

    # Try to get from cache first
    cache_key = "plant_extractor:#{Digest::MD5.hexdigest(text)}"
    cached_result = @cache.read(cache_key)
    return cached_result if cached_result.present?

    # Extract potential plant names
    potential_names = extract_potential_names(text)
    
    # Batch query for existing plants
    existing_plants = find_existing_plants(potential_names)
    
    # Cache and return results
    result = existing_plants.map { |plant| plant.common_name }
    @cache.write(cache_key, result)
    result
  end

  private

  def extract_potential_names(text)
    # Split text into words and create potential combinations
    words = text.downcase.split(/\W+/)
    potential_names = []

    # Add single words
    potential_names.concat(words)

    # Add two-word combinations
    words.each_cons(2) do |word1, word2|
      potential_names << "#{word1} #{word2}"
    end

    # Add three-word combinations
    words.each_cons(3) do |word1, word2, word3|
      potential_names << "#{word1} #{word2} #{word3}"
    end

    potential_names.uniq
  end

  def find_existing_plants(potential_names)
    # Batch query for all potential names
    EnhancedPlant.where(
      "LOWER(common_name) = ANY(ARRAY[?]) OR LOWER(scientific_name) = ANY(ARRAY[?])",
      potential_names,
      potential_names
    ).distinct
  end

  # Load excluded words from configuration
  def load_excluded_words
    Set.new([
      'the', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'with', 'by',
      'from', 'about', 'like', 'how', 'what', 'when', 'where', 'why', 'which',
      'who', 'whom', 'whose', 'this', 'that', 'these', 'those', 'there', 'here',
      'some', 'any', 'all', 'none', 'both', 'either', 'neither', 'each', 'every',
      'many', 'much', 'few', 'little', 'more', 'most', 'less', 'least', 'other',
      'another', 'such', 'same', 'different', 'various', 'several', 'few', 'many'
    ])
  end

  # Load plant name patterns
  def load_plant_patterns
    [
      /^[a-z]+(?:flower|leaf|root|berry|fruit|seed|herb|grass|tree|shrub|vine)$/i,
      /^[a-z]+(?:aceae|ales|opsida|phyta)$/i,
      /^[a-z]+(?:us|um|a|is|es)$/i
    ]
  end
end 