# frozen_string_literal: true
# Vector Search Service for Plant Embeddings
# Supports FAISS, Qdrant, and pgvector backends
class VectorSearchService
  include ActiveModel::Model

  attr_accessor :backend, :embedding_model, :dimension

  SUPPORTED_BACKENDS = %i[faiss qdrant pgvector local_faiss].freeze
  EMBEDDING_MODELS = {
    'sentence-transformers/all-MiniLM-L6-v2' => 384,
    'sentence-transformers/all-mpnet-base-v2' => 768,
    'text-embedding-ada-002' => 1536,
    'local/all-MiniLM-L6-v2' => 384 # For offline usage
  }.freeze

  def initialize(attributes = {})
    super
    @backend ||= :local_faiss # Default to local FAISS for offline capability
    @embedding_model ||= 'local/all-MiniLM-L6-v2'
    @dimension = EMBEDDING_MODELS[@embedding_model] || 384

    setup_backend
  end

  def search(query_text, limit: 20, threshold: 0.7)
    # Generate query embedding
    query_embedding = generate_embedding(query_text)

    case backend
    when :faiss, :local_faiss
      search_faiss(query_embedding, limit, threshold)
    when :qdrant
      search_qdrant(query_embedding, limit, threshold)
    when :pgvector
      search_pgvector(query_embedding, limit, threshold)
    else
      raise "Unsupported backend: #{backend}"
    end
  end

  def index_plant(plant)
    # Generate comprehensive text for embedding
    plant_text = generate_plant_text(plant)
    embedding = generate_embedding(plant_text)

    case backend
    when :faiss, :local_faiss
      index_faiss(plant.id, embedding, plant_text)
    when :qdrant
      index_qdrant(plant.id, embedding, plant_text)
    when :pgvector
      index_pgvector(plant.id, embedding)
    end
  end

  def bulk_index_plants(plants = nil)
    plants ||= EnhancedPlant.includes(:semantic_tags, :environmental_requirements, :plant_uses)

    puts "Indexing #{plants.count} plants for vector search..."

    plants.find_each.with_index do |plant, index|
      begin
        index_plant(plant)
        print '.' if index % 10 == 0
      rescue => e
        puts "\nError indexing plant #{plant.id}: #{e.message}"
      end
    end

    puts "\nVector indexing completed!"
  end

  def similar_plants(plant, limit: 10)
    plant_text = generate_plant_text(plant)
    search(plant_text, limit: limit + 1, threshold: 0.5)
      .reject { |result| result[:plant_id] == plant.id }
      .first(limit)
  end

  private

  def setup_backend
    case backend
    when :local_faiss
      setup_local_faiss
    when :faiss
      setup_faiss
    when :qdrant
      setup_qdrant
    when :pgvector
      setup_pgvector
    end
  end

  def setup_local_faiss
    begin
      require 'faiss'
      @index_path = Rails.root.join('tmp', 'faiss_plant_index.bin')
      @metadata_path = Rails.root.join('tmp', 'faiss_metadata.json')

      if File.exist?(@index_path)
        load_faiss_index
      else
        create_faiss_index
      end
      @faiss_available = true
    rescue LoadError
      puts 'FAISS not available, falling back to simple text search'
      @faiss_available = false
      @simple_index = {}
    end
  end

  def setup_faiss
    # For cloud FAISS setup
    setup_local_faiss
  end

  def setup_qdrant
    # Qdrant client setup
    @qdrant_client = QdrantClient.new(
      url: ENV['QDRANT_URL'] || 'http://localhost:6333',
      api_key: ENV['QDRANT_API_KEY']
    )
    @collection_name = 'plants'

    ensure_qdrant_collection
  end

  def setup_pgvector
    # pgvector is handled through ActiveRecord
    # Ensure the extension is enabled in your migration
  end

  def generate_embedding(text)
    case embedding_model
    when /^local\//
      generate_local_embedding(text)
    when 'text-embedding-ada-002'
      generate_openai_embedding(text)
    else
      generate_sentence_transformer_embedding(text)
    end
  end

  def generate_local_embedding(text)
    # Use a local sentence transformer model
    # This would require python integration or a Ruby ML library
    # For now, we'll simulate with a simple hash-based approach

    # In production, you'd use something like:
    # python_script = Rails.root.join('lib', 'python', 'generate_embedding.py')
    # result = `python #{python_script} "#{text.gsub('"', '\"')}"`
    # JSON.parse(result)['embedding']

    # Simplified approach for demo
    generate_simple_embedding(text)
  end

  def generate_simple_embedding(text)
    # Simple TF-IDF-like embedding for demo purposes
    words = text.downcase.split(/\W+/).reject(&:empty?)
    vocab = load_vocabulary

    embedding = Array.new(dimension, 0.0)

    words.each do |word|
      if vocab[word]
        embedding[vocab[word] % dimension] += 1.0
      end
    end

    # Normalize
    magnitude = Math.sqrt(embedding.sum { |x| x * x })
    magnitude > 0 ? embedding.map { |x| x / magnitude } : embedding
  end

  def load_vocabulary
    # Load or create a vocabulary mapping
    vocab_path = Rails.root.join('tmp', 'vocabulary.json')

    if File.exist?(vocab_path)
      JSON.parse(File.read(vocab_path))
    else
      create_vocabulary
    end
  end

  def create_vocabulary
    # Create vocabulary from all plant text
    vocab = {}
    index = 0

    EnhancedPlant.find_each do |plant|
      text = generate_plant_text(plant)
      words = text.downcase.split(/\W+/).reject(&:empty?).uniq

      words.each do |word|
        unless vocab[word]
          vocab[word] = index
          index += 1
        end
      end
    end

    # Save vocabulary
    vocab_path = Rails.root.join('tmp', 'vocabulary.json')
    File.write(vocab_path, vocab.to_json)

    vocab
  end

  def generate_plant_text(plant)
    # Comprehensive text representation of the plant
    text_parts = [
      plant.common_name,
      plant.scientific_name,
      plant.family,
      plant.description_detailed,
      plant.description_short,
      plant.growing_notes,

      # Semantic tags
      plant.semantic_tags.pluck(:name).join(' '),

      # Environmental data
      plant.environmental_requirements&.light_requirement,
      plant.environmental_requirements&.soil_type,
      plant.environmental_requirements&.water_requirement,

      # Uses
      plant.plant_uses.joins(:use_category).pluck('use_categories.name').join(' '),

      # Plant type and characteristics
      plant.plant_type,
      plant.growth_habit,
      plant.lifecycle,

      # Size information
      (plant.mature_height_max_cm ? "height #{plant.mature_height_max_cm}cm" : nil),
      (plant.mature_spread_max_cm ? "spread #{plant.mature_spread_max_cm}cm" : nil),

      # Hardiness
      (plant.environmental_requirements ? "zone #{plant.environmental_requirements&.hardiness_zone_min}-#{plant.environmental_requirements&.hardiness_zone_max}" : nil)
    ].compact.join(' ')

    # Clean and normalize
    text_parts.gsub(/\s+/, ' ').strip
  end

  def search_faiss(query_embedding, limit, threshold)
    return simple_text_search(query_embedding, limit, threshold) unless @faiss_available
    return [] unless @faiss_index

    # Search FAISS index
    distances, indices = @faiss_index.search(query_embedding, limit)

    results = []
    distances.each_with_index do |distance, i|
      similarity = 1.0 - distance # Convert distance to similarity
      next if similarity < threshold

      plant_id = @metadata[indices[i]][:plant_id]
      results << {
        plant_id: plant_id,
        similarity: similarity,
        plant: EnhancedPlant.find_by(id: plant_id)
      }
    end

    results.compact
  end

  def simple_text_search(query_text, limit, threshold)
    # Simple text-based search fallback
    query_words = query_text.to_s.downcase.split(/\W+/).reject(&:empty?)
    return [] if query_words.empty?

    # Search through plants using basic text matching
    results = []
    Plant.includes(:plant_uses, :plant_pests).find_each do |plant|
      plant_text = [
        plant.common_name,
        plant.scientific_name,
        plant.family,
        plant.description_detailed,
        plant.description_short,
        plant.growing_notes
      ].compact.join(' ').downcase

      # Calculate simple similarity score
      matches = query_words.count { |word| plant_text.include?(word) }
      similarity = matches.to_f / query_words.length

      if similarity >= threshold
        results << {
          plant_id: plant.id,
          similarity: similarity,
          plant: plant
        }
      end
    end

    results.sort_by { |r| -r[:similarity] }.first(limit)
  end

  def search_qdrant(query_embedding, limit, threshold)
    response = @qdrant_client.search(
      collection_name: @collection_name,
      vector: query_embedding,
      limit: limit,
      score_threshold: threshold
    )

    response['result'].map do |result|
      {
        plant_id: result['payload']['plant_id'],
        similarity: result['score'],
        plant: EnhancedPlant.find_by(id: result['payload']['plant_id'])
      }
    end.compact
  end

  def search_pgvector(query_embedding, limit, threshold)
    # This would require the embedding_vector column in your plants table
    # EnhancedPlant.select("*, embedding_vector <=> '[#{query_embedding.join(',')}]' AS distance")
    #              .where("embedding_vector <=> '[#{query_embedding.join(',')}]' < ?", 1.0 - threshold)
    #              .order(:distance)
    #              .limit(limit)
    #              .map do |plant|
    #   {
    #     plant_id: plant.id,
    #     similarity: 1.0 - plant.distance,
    #     plant: plant
    #   }
    # end

    # Placeholder for pgvector implementation
    []
  end

  def index_faiss(plant_id, embedding, text)
    @faiss_index.add([embedding])
    @metadata << { plant_id: plant_id, text: text }

    # Periodically save index
    if @metadata.length % 100 == 0
      save_faiss_index
    end
  end

  def index_qdrant(plant_id, embedding, text)
    @qdrant_client.upsert(
      collection_name: @collection_name,
      points: [{
        id: plant_id,
        vector: embedding,
        payload: {
          plant_id: plant_id,
          text: text,
          indexed_at: Time.current.iso8601
        }
      }]
    )
  end

  def index_pgvector(plant_id, embedding)
    EnhancedPlant.find(plant_id)
    # plant.update!(embedding_vector: embedding)
  end

  def create_faiss_index
    return unless @faiss_available
    require 'faiss'
    @faiss_index = Faiss::IndexFlatIP.new(dimension)
    @metadata = []
  end

  def load_faiss_index
    require 'faiss'
    @faiss_index = Faiss.read_index(@index_path.to_s)
    @metadata = JSON.parse(File.read(@metadata_path), symbolize_names: true)
  end

  def save_faiss_index
    Faiss.write_index(@faiss_index, @index_path.to_s)
    File.write(@metadata_path, @metadata.to_json)
  end

  def ensure_qdrant_collection
    begin
      @qdrant_client.get_collection(@collection_name)
    rescue
      # Create collection if it doesn't exist
      @qdrant_client.create_collection(
        collection_name: @collection_name,
        vectors_config: {
          size: dimension,
          distance: 'Cosine'
        }
      )
    end
  end
end