# frozen_string_literal: true
class GptPlantQueryService
  def initialize(api_key = nil)
    @api_key = api_key || ENV['OPENAI_API_KEY'] || Rails.application.credentials.dig(:openai, :api_key)
    # Now that OpenAI gem is installed, we can use it if API key is available
    @client = @api_key ? OpenAI::Client.new(access_token: @api_key) : nil
  end

  def process_query(user_query, context: {})
    # Parse the query to extract structured data
    parsed_query = NaturalLanguageQueryParser.new(user_query).parse

    # Search for relevant plants
    search_results = search_plants(parsed_query, user_query)

    # Generate response (use GPT if available, otherwise fallback)
    gpt_response = if @client
                     generate_gpt_response(user_query, search_results, context)
                   else
                     generate_fallback_response(user_query, search_results, context)
                   end

    # Handle both Arrays and ActiveRecord relations
    plants_count = search_results.respond_to?(:count) ? search_results.count : search_results.size
    plants_limited = search_results.respond_to?(:limit) ? search_results.limit(10) : search_results.first(10)

    {
      query: user_query,
      parsed_query: parsed_query,
      plants_found: plants_count,
      plants: plants_limited,
      gpt_response: gpt_response,
      suggestions: generate_suggestions(parsed_query)
    }
  end

  def chat_with_context(messages, plant_context = [])
    return { error: 'OpenAI API key not configured' } unless @client

    system_prompt = build_system_prompt(plant_context)

    full_messages = [
      { role: 'system', content: system_prompt },
      *messages
    ]

    begin
      response = @client.chat(
        parameters: {
          model: 'gpt-4',
          messages: full_messages,
          max_tokens: 1000,
          temperature: 0.7
        }
      )

      {
        response: response.dig('choices', 0, 'message', 'content'),
        usage: response['usage']
      }
    rescue => e
      Rails.logger.error "GPT API Error: #{e.message}"
      { error: "Failed to get GPT response: #{e.message}" }
    end
  end

  def generate_plant_recommendations(criteria)
    # Parse criteria
    parsed_criteria = NaturalLanguageQueryParser.new(criteria).parse

    # Search for matching plants
    matching_plants = search_plants(parsed_criteria, criteria)

    if @client
      # Generate GPT recommendations
      plants_for_data = matching_plants.respond_to?(:limit) ? matching_plants.limit(20) : matching_plants.first(20)
      plant_data = plants_for_data.map do |plant|
        {
          name: plant.common_name,
          scientific_name: plant.scientific_name,
          description: plant.description_short,
          uses: plant.primary_uses,
          zones: plant.hardiness_zones,
          tags: plant.semantic_tags.pluck(:name)
        }
      end

      prompt = build_recommendation_prompt(criteria, plant_data)

      begin
        response = @client.chat(
          parameters: {
            model: 'gpt-4',
            messages: [{ role: 'user', content: prompt }],
            max_tokens: 1500,
            temperature: 0.8
          }
        )

        plants_limited = matching_plants.respond_to?(:limit) ? matching_plants.limit(10) : matching_plants.first(10)

        {
          criteria: criteria,
          recommendations: response.dig('choices', 0, 'message', 'content'),
          plants_considered: plant_data.count,
          matching_plants: plants_limited
        }
      rescue => e
        Rails.logger.error "GPT Recommendation Error: #{e.message}"
        fallback_recommendations(criteria, matching_plants)
      end
    else
      fallback_recommendations(criteria, matching_plants)
    end
  end

  def explain_plant_relationships(plant_name)
    plant = EnhancedPlant.find_by(common_name: plant_name)
    return { error: 'Plant not found' } unless plant

    companions = plant.beneficial_companions.limit(10)
    antagonists = plant.antagonistic_plants.limit(5)

    if @client
      prompt = build_relationship_prompt(plant, companions, antagonists)

      begin
        response = @client.chat(
          parameters: {
            model: 'gpt-4',
            messages: [{ role: 'user', content: prompt }],
            max_tokens: 1000,
            temperature: 0.7
          }
        )

        {
          plant: plant.common_name,
          explanation: response.dig('choices', 0, 'message', 'content'),
          companions: companions,
          antagonists: antagonists
        }
      rescue => e
        Rails.logger.error "GPT Relationship Error: #{e.message}"
        fallback_relationships(plant, companions, antagonists)
      end
    else
      fallback_relationships(plant, companions, antagonists)
    end
  end

  private

  def search_plants(parsed_query, original_query)
    search_service = EnhancedPlantSearchService.new

    if parsed_query.any?
      # Use the natural language search method which expects parsed data
      search_service.natural_language_search(original_query)
    else
      search_service.natural_language_search(original_query)
    end
  end

  def generate_gpt_response(user_query, plants, context)
    # Handle both Arrays and ActiveRecord relations
    plants_array = plants.respond_to?(:limit) ? plants.limit(10) : plants.first(10)
    plant_count = plants.respond_to?(:count) ? plants.count : plants.size

    plant_summaries = plants_array.map do |plant|
      "#{plant.common_name} (#{plant.scientific_name}): #{plant.description_short&.truncate(100)}"
    end.join("\n")

    prompt = <<~PROMPT
      You are PermieBro, an expert permaculture assistant. A user asked: "#{user_query}"

      I found #{plant_count} matching plants in our database:
      #{plant_summaries}

      Please provide a helpful, friendly response that:
      1. Directly answers their question
      2. Mentions specific plants from the results when relevant
      3. Gives practical permaculture advice
      4. Suggests companion planting or polyculture ideas if appropriate
      5. Keeps the tone conversational and encouraging

      Context: #{context}
    PROMPT

    begin
      response = @client.chat(
        parameters: {
          model: 'gpt-4',
          messages: [{ role: 'user', content: prompt }],
          max_tokens: 800,
          temperature: 0.8
        }
      )

      response.dig('choices', 0, 'message', 'content')
    rescue => e
      Rails.logger.error "GPT Response Error: #{e.message}"
      generate_fallback_response(user_query, plants, context)
    end
  end

  def build_system_prompt(plant_context)
    context_text = if plant_context.any?
                     plant_context.map { |p| "#{p.common_name}: #{p.description_short}" }.join("\n")
    else
      'No specific plant context provided.'
    end

    <<~PROMPT
      You are PermieBro, a knowledgeable and friendly permaculture assistant. You help people with:
      - Plant selection and companion planting
      - Permaculture design principles
      - Sustainable gardening practices
      - Plant care and growing tips
      - Ecosystem relationships and biodiversity

      Current plant context:
      #{context_text}

      Always be encouraging, practical, and focus on sustainable, regenerative practices.
      When discussing plants, mention their ecological benefits and relationships with other plants.
    PROMPT
  end

  def build_recommendation_prompt(criteria, plant_data)
    plants_text = plant_data.map do |plant|
      "#{plant[:name]} (#{plant[:scientific_name]}): #{plant[:description]} | Uses: #{plant[:uses].join(', ')} | Zones: #{plant[:zones]} | Tags: #{plant[:tags].join(', ')}"
    end.join("\n")

    <<~PROMPT
      As PermieBro, a permaculture expert, please recommend the best plants for this request: "#{criteria}"

      Here are the matching plants from our database:
      #{plants_text}

      Please provide:
      1. Top 3-5 plant recommendations with reasons why they're perfect
      2. How these plants work together in a polyculture system
      3. Practical growing tips for the user's situation
      4. Any companion planting suggestions
      5. Seasonal considerations

      Make it conversational and encouraging!
    PROMPT
  end

  def build_relationship_prompt(plant, companions, antagonists)
    companions_text = companions.map { |c| "#{c.common_name} (#{c.scientific_name})" }.join(', ')
    antagonists_text = antagonists.map { |a| "#{a.common_name} (#{a.scientific_name})" }.join(', ')

    <<~PROMPT
      As PermieBro, explain the plant relationships for #{plant.common_name} (#{plant.scientific_name}).

      Beneficial companions: #{companions_text}
      Plants to avoid: #{antagonists_text}

      Please explain:
      1. Why these companion relationships work (root systems, nutrients, pest control, etc.)
      2. How to arrange these plants in a garden design
      3. What benefits each companion provides
      4. Why certain plants should be avoided and what problems they might cause
      5. Practical tips for implementing these relationships

      Keep it educational but friendly and practical!
    PROMPT
  end

  def generate_fallback_response(user_query, plants, context)
    plant_count = plants.respond_to?(:count) ? plants.count : plants.size

    if plant_count == 0
      "I couldn't find any plants matching '#{user_query}'. Try searching with different terms like 'drought tolerant', 'shade plants', or specific plant names."
    elsif plant_count == 1
      plant = plants.first
      "I found 1 plant matching '#{user_query}': #{plant.common_name} (#{plant.scientific_name}). #{plant.description_short&.truncate(150) || 'Check the plant details for more information.'}"
    elsif plant_count <= 5
      plants_array = plants.respond_to?(:limit) ? plants.limit(5) : plants.first(5)
      plant_names = plants_array.map(&:common_name).join(', ')
      "I found #{plant_count} plants matching '#{user_query}': #{plant_names}. These plants should meet your criteria - check their individual pages for detailed growing information and companion planting suggestions."
    else
      plants_array = plants.respond_to?(:limit) ? plants.limit(3) : plants.first(3)
      top_plants = plants_array.map(&:common_name).join(', ')
      "Great! I found #{plant_count} plants matching '#{user_query}'. The top matches include: #{top_plants}, and #{plant_count - 3} more. Use the filters to narrow down your search, or explore the results to find the perfect plants for your garden."
    end
  end

  def fallback_recommendations(criteria, plants)
    plant_count = plants.respond_to?(:count) ? plants.count : plants.size
    plants_array = plants.respond_to?(:limit) ? plants.limit(10) : plants.first(10)

    {
      criteria: criteria,
      recommendations: generate_fallback_recommendations(criteria, plants),
      plants_considered: plant_count,
      matching_plants: plants_array
    }
  end

  def fallback_relationships(plant, companions, antagonists)
    {
      plant: plant.common_name,
      explanation: generate_fallback_relationships(plant, companions, antagonists),
      companions: companions,
      antagonists: antagonists
    }
  end

  def generate_fallback_recommendations(criteria, plants)
    plant_count = plants.respond_to?(:count) ? plants.count : plants.size

    if plant_count == 0
      "I couldn't find plants matching '#{criteria}'. Try adjusting your criteria or search terms."
    else
      top_plants = plants.respond_to?(:limit) ? plants.limit(5) : plants.first(5)
      recommendations = "Based on '#{criteria}', here are my top recommendations:\n\n"

      top_plants.each_with_index do |plant, index|
        uses = plant.primary_uses.any? ? plant.primary_uses.join(', ') : 'Multiple uses'
        zones = plant.hardiness_zones || 'Check individual requirements'

        recommendations += "#{index + 1}. **#{plant.common_name}** (#{plant.scientific_name})\n"
        recommendations += "   - Uses: #{uses}\n"
        recommendations += "   - Zones: #{zones}\n"
        recommendations += "   - #{plant.description_short&.truncate(100) || 'Great choice for your garden'}\n\n"
      end

      if plant_count > 5
        recommendations += "Plus #{plant_count - 5} more plants that match your criteria!"
      end

      recommendations
    end
  end

  def generate_fallback_relationships(plant, companions, antagonists)
    explanation = "#{plant.common_name} relationships:\n\n"

    if companions.any?
      explanation += "**Good Companions (#{companions.count}):**\n"
      companions.each do |companion|
        explanation += "• #{companion.common_name} - Works well together\n"
      end
      explanation += "\n"
    end

    if antagonists.any?
      explanation += "**Plants to Avoid (#{antagonists.count}):**\n"
      antagonists.each do |antagonist|
        explanation += "• #{antagonist.common_name} - May compete or conflict\n"
      end
      explanation += "\n"
    end

    if companions.empty? && antagonists.empty?
      explanation += "No specific companion or antagonistic relationships recorded for #{plant.common_name} yet. "
      explanation += 'Consider general permaculture principles like grouping plants with similar water and light needs.'
    else
      explanation += 'These relationships are based on traditional companion planting knowledge and permaculture principles. '
      explanation += 'Consider your specific growing conditions and local climate when planning your garden.'
    end

    explanation
  end

  def generate_suggestions(parsed_query)
    suggestions = []

    if parsed_query[:semantic_tags]
      suggestions << 'Try searching for plants with different characteristics'
      suggestions << 'Consider companion planting with these plants'
    end

    if parsed_query[:zone_range]
      suggestions << 'Look for plants in adjacent hardiness zones'
      suggestions << 'Consider microclimates in your garden'
    end

    suggestions << 'Ask about specific growing conditions'
    suggestions << 'Inquire about companion planting strategies'
    suggestions << 'Request seasonal planting advice'

    suggestions.sample(3)
  end
end