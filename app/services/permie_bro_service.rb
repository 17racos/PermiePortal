# frozen_string_literal: true
# PermieBro AI Assistant Service
# Integrates semantic search, vector search, and LLM responses
class PermieBroService
  include ActiveModel::Model

  attr_accessor :llm_provider, :temperature, :max_tokens, :use_vector_search

  SUPPORTED_PROVIDERS = %i[claude anthropic openai ollama local_llama mixtral].freeze

  def initialize(attributes = {})
    super
    @llm_provider ||= :ollama # Default to Ollama for local capability
    @temperature ||= 0.7
    @max_tokens ||= 1000
    @use_vector_search = true if @use_vector_search.nil?

    @ai_search_service = AiPlantSearchService.new
    @vector_search_service = VectorSearchService.new if use_vector_search
  end

  def ask(question, context = {})
    # Parse and search for relevant plants
    search_results = search_plants(question, context)

    # Generate AI response
    response = generate_response(question, search_results, context)

    {
      answer: response[:answer],
      plants: search_results[:plants],
      confidence: response[:confidence],
      sources: search_results[:search_metadata],
      query_analysis: search_results[:query_analysis],
      response_metadata: response[:metadata]
    }
  end

  def search_plants(question, context = {})
    # Combine traditional and vector search
    traditional_results = @ai_search_service.search(
      query: question,
      location: context[:location],
      zone: context[:zone],
      limit: 15
    )

    if use_vector_search && @vector_search_service
      vector_results = @vector_search_service.search(question, limit: 10)
      combined_plants = combine_search_results(traditional_results[:plants], vector_results)
    else
      combined_plants = traditional_results[:plants]
    end

    {
      plants: combined_plants.first(20),
      query_analysis: traditional_results[:query_analysis],
      search_metadata: traditional_results[:search_metadata]
    }
  end

  def generate_response(question, search_results, context = {})
    # Prepare context for LLM
    plant_context = prepare_plant_context(search_results[:plants])
    system_prompt = build_system_prompt
    user_prompt = build_user_prompt(question, plant_context, context)

    case llm_provider
    when :claude, :anthropic
      generate_claude_response(system_prompt, user_prompt)
    when :openai
      generate_openai_response(system_prompt, user_prompt)
    when :ollama
      generate_ollama_response(system_prompt, user_prompt)
    when :local_llama, :mixtral
      generate_local_response(system_prompt, user_prompt)
    else
      generate_fallback_response(question, search_results)
    end
  end

  private

  def combine_search_results(traditional_plants, vector_results)
    # Merge and deduplicate results from both search methods
    plant_scores = {}

    # Score traditional results
    traditional_plants.each_with_index do |plant, index|
      score = 1.0 - (index.to_f / traditional_plants.length) # Higher score for earlier results
      plant_scores[plant.id] = { plant: plant, score: score * 0.6, sources: [:traditional] }
    end

    # Add vector results
    vector_results.each do |result|
      plant_id = result[:plant_id]
      if plant_scores[plant_id]
        plant_scores[plant_id][:score] += result[:similarity] * 0.4
        plant_scores[plant_id][:sources] << :vector
      else
        plant_scores[plant_id] = {
          plant: result[:plant],
          score: result[:similarity] * 0.4,
          sources: [:vector]
        }
      end
    end

    # Sort by combined score
    plant_scores.values
                .sort_by { |data| -data[:score] }
                .map { |data| data[:plant] }
                .compact
  end

  def prepare_plant_context(plants)
    plants.first(10).map do |plant|
      {
        name: plant.common_name,
        scientific_name: plant.scientific_name,
        description: truncate_text(plant.description_detailed || plant.description_short, 200),
        tags: plant.semantic_tags.pluck(:name).join(', '),
        uses: plant.plant_uses.joins(:use_category).pluck('use_categories.name').join(', '),
        environmental: {
          zones: "#{plant.environmental_requirements&.hardiness_zone_min}-#{plant.environmental_requirements&.hardiness_zone_max}",
          light: plant.environmental_requirements&.light_requirement,
          water: plant.environmental_requirements&.water_requirement
        },
        companions: plant.plant_relationships
                        .where(relationship_type: ['companion', 'beneficial'])
                        .joins(:related_plant)
                        .pluck('enhanced_plants.common_name')
                        .first(3)
                        .join(', ')
      }
    end
  end

  def build_system_prompt
    <<~PROMPT
      You are PermieBro, an expert permaculture and plant consultant. You help people find the right plants for their specific needs, location, and growing conditions.

      Your expertise includes:
      - Plant identification and characteristics
      - Companion planting and polyculture design
      - Regional growing conditions and climate adaptation
      - Edible landscaping and food forests
      - Medicinal plants and their uses
      - Sustainable gardening practices
      - Pest management and plant health

      Guidelines for responses:
      1. Be helpful, friendly, and encouraging
      2. Provide specific, actionable advice
      3. Consider the user's location and growing conditions
      4. Suggest companion plants when relevant
      5. Mention any important warnings or considerations
      6. Keep responses concise but informative
      7. Always base recommendations on the plant data provided
      8. If you don't have enough information, say so and suggest what additional info would help

      When discussing plants, include:
      - Common and scientific names
      - Key growing requirements (zones, light, water)
      - Primary uses (food, medicine, landscaping, etc.)
      - Companion planting suggestions
      - Any special care considerations
    PROMPT
  end

  def build_user_prompt(question, plant_context, context)
    location_info = context[:location] ? "User location: #{context[:location]}" : ''
    zone_info = context[:zone] ? "Hardiness zone: #{context[:zone]}" : ''

    <<~PROMPT
      User Question: #{question}

      #{location_info}
      #{zone_info}

      Relevant Plants Found:
      #{format_plant_context(plant_context)}

      Please provide a helpful response based on the plant information above. Focus on the most relevant plants for the user's question.
    PROMPT
  end

  def format_plant_context(plant_context)
    plant_context.map.with_index do |plant, index|
      <<~PLANT
        #{index + 1}. #{plant[:name]} (#{plant[:scientific_name]})
           Description: #{plant[:description]}
           Tags: #{plant[:tags]}
           Uses: #{plant[:uses]}
           Growing: Zones #{plant[:environmental][:zones]}, #{plant[:environmental][:light]} light, #{plant[:environmental][:water]} water
           Companions: #{plant[:companions]}
      PLANT
    end.join("\n")
  end

  def generate_claude_response(system_prompt, user_prompt)
    # Claude/Anthropic API integration
    begin
      client = Anthropic::Client.new(access_token: ENV['ANTHROPIC_API_KEY'])

      response = client.messages(
        model: 'claude-3-sonnet-20240229',
        max_tokens: max_tokens,
        temperature: temperature,
        system: system_prompt,
        messages: [
          { role: 'user', content: user_prompt }
        ]
      )

      {
        answer: response.dig('content', 0, 'text'),
        confidence: 0.9,
        metadata: { provider: 'claude', model: 'claude-3-sonnet' }
      }
    rescue => e
      Rails.logger.error "Claude API error: #{e.message}"
      generate_fallback_response(user_prompt, {})
    end
  end

  def generate_openai_response(system_prompt, user_prompt)
    # OpenAI API integration
    begin
      client = OpenAI::Client.new(access_token: ENV['OPENAI_API_KEY'])

      response = client.chat(
        model: 'gpt-4',
        messages: [
          { role: 'system', content: system_prompt },
          { role: 'user', content: user_prompt }
        ],
        temperature: temperature,
        max_tokens: max_tokens
      )

      {
        answer: response.dig('choices', 0, 'message', 'content'),
        confidence: 0.9,
        metadata: { provider: 'openai', model: 'gpt-4' }
      }
    rescue => e
      Rails.logger.error "OpenAI API error: #{e.message}"
      generate_fallback_response(user_prompt, {})
    end
  end

  def generate_ollama_response(system_prompt, user_prompt)
    # Ollama integration
    begin
      ollama_url = ENV['OLLAMA_URL'] || 'http://localhost:11434'

      response = HTTParty.post("#{ollama_url}/api/generate", {
        body: {
          model: 'llama3.1:8b',
          prompt: "#{system_prompt}\n\nUser: #{user_prompt}\n\nAssistant:",
          stream: false,
          options: {
            temperature: temperature,
            num_predict: max_tokens
          }
        }.to_json,
        headers: { 'Content-Type' => 'application/json' }
      })

      if response.success?
        {
          answer: JSON.parse(response.body)['response'],
          confidence: 0.9,
          metadata: { provider: 'ollama', model: 'llama3.1:8b' }
        }
      else
        generate_fallback_response(user_prompt, {})
      end
    rescue => e
      Rails.logger.error "Ollama error: #{e.message}"
      generate_fallback_response(user_prompt, {})
    end
  end

  def generate_local_response(system_prompt, user_prompt)
    # Local LLM integration (Ollama, LlamaCpp, etc.)
    begin
      # This would integrate with your local LLM setup
      # Example using Ollama API:

      ollama_url = ENV['OLLAMA_URL'] || 'http://localhost:11434'
      model = llm_provider == :mixtral ? 'mixtral:8x7b' : 'llama3:8b'

      response = HTTParty.post("#{ollama_url}/api/generate", {
        body: {
          model: model,
          prompt: "#{system_prompt}\n\nUser: #{user_prompt}\n\nAssistant:",
          stream: false,
          options: {
            temperature: temperature,
            num_predict: max_tokens
          }
        }.to_json,
        headers: { 'Content-Type' => 'application/json' }
      })

      if response.success?
        {
          answer: JSON.parse(response.body)['response'],
          confidence: 0.8,
          metadata: { provider: 'local', model: model }
        }
      else
        generate_fallback_response(user_prompt, {})
      end
    rescue => e
      Rails.logger.error "Local LLM error: #{e.message}"
      generate_fallback_response(user_prompt, {})
    end
  end

  def generate_fallback_response(question, search_results)
    # Rule-based fallback when LLM is unavailable
    plants = search_results[:plants] || []

    if plants.any?
      answer = "Based on your question about '#{question}', here are some relevant plants:\n\n"

      plants.first(5).each_with_index do |plant, index|
        answer += "#{index + 1}. **#{plant.common_name}** (#{plant.scientific_name})\n"
        answer += "   #{truncate_text(plant.description_short || plant.description_detailed, 100)}\n"

        if plant.semantic_tags.any?
          tags = plant.semantic_tags.pluck(:name).first(3).join(', ')
          answer += "   Key characteristics: #{tags}\n"
        end

        if plant.environmental_requirements
          env = plant.environmental_requirements
          answer += "   Growing: Zones #{env.hardiness_zone_min}-#{env.hardiness_zone_max}, #{env.light_requirement} light\n"
        end

        answer += "\n"
      end

      answer += 'For more detailed information about any of these plants, please ask specific questions!'
    else
      answer = "I couldn't find specific plants matching your question about '#{question}'. Could you provide more details about what you're looking for? For example:\n\n"
      answer += "- Your location or hardiness zone\n"
      answer += "- Specific growing conditions (sun/shade, wet/dry)\n"
      answer += "- Intended use (food, medicine, landscaping)\n"
      answer += '- Any size or maintenance preferences'
    end

    {
      answer: answer,
      confidence: 0.6,
      metadata: { provider: 'fallback', method: 'rule_based' }
    }
  end

  def truncate_text(text, length)
    return '' unless text
    text.length > length ? "#{text[0...length]}..." : text
  end
end