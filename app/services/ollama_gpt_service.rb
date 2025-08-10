# frozen_string_literal: true
class OllamaGptService
  include HTTParty
  
  def initialize(base_url = nil, model = nil)
    @base_url = base_url || ENV['OLLAMA_URL'] || 'http://host.docker.internal:11434'
    @model = model || ENV['OLLAMA_MODEL'] || 'llama3.1:8b'
    @timeout = 180  # Increased timeout for complex conversations
    @max_retries = 3
    @conversation_memory = {}  # Store conversation context
  end

  def available?
    check_ollama_health
  end

  def generate_completion(prompt)
    return nil unless available?

    begin
      response = make_ollama_request(prompt, enhanced_options: true)
      response&.dig('response')
    rescue => e
      Rails.logger.error "Ollama Completion Error: #{e.message}"
      nil
    end
  end

  def process_plant_query(user_query, context: {})
    return fallback_response(user_query) unless available?

    begin
      # Build comprehensive system prompt with enhanced context
      system_prompt = build_enhanced_system_prompt(context)
      
      # Create a conversational prompt that feels more natural
      full_prompt = build_conversational_prompt(system_prompt, user_query, context)
      
      response = make_ollama_request(full_prompt, enhanced_options: true)
      
      if response && response['response']
        # Post-process response for better formatting
        formatted_response = format_response(response['response'])
        
        {
          success: true,
          response: formatted_response,
          type: 'conversational_response',
          model: @model,
          usage: {
            prompt_tokens: response.dig('prompt_eval_count') || 0,
            completion_tokens: response.dig('eval_count') || 0,
            total_tokens: (response.dig('prompt_eval_count') || 0) + (response.dig('eval_count') || 0)
          }
        }
      else
        {
          success: false,
          error: 'No response from Ollama',
          fallback_response: fallback_response(user_query)
        }
      end

    rescue => e
      Rails.logger.error "Ollama GPT Service Error: #{e.message}"
      Rails.logger.error e.backtrace.join("\n")
      
      {
        success: false,
        error: e.message,
        fallback_response: fallback_response(user_query)
      }
    end
  end

  def chat_with_context(messages, plant_context = [], session_id: nil)
    return { error: 'Ollama not available' } unless available?

    begin
      # Store conversation context for continuity
      @conversation_memory[session_id] = messages if session_id
      
      # Build enhanced conversational system prompt
      system_prompt = build_conversational_system_prompt(plant_context, messages)
      
      # Create natural conversation flow
      conversation = build_natural_conversation(system_prompt, messages, plant_context)
      
      response = make_ollama_request(conversation, enhanced_options: true)

      if response && response['response']
        formatted_response = format_conversational_response(response['response'], messages.last)
        
        {
          success: true,
          response: formatted_response,
          model: @model,
          usage: {
            prompt_tokens: response.dig('prompt_eval_count') || 0,
            completion_tokens: response.dig('eval_count') || 0,
            total_tokens: (response.dig('prompt_eval_count') || 0) + (response.dig('eval_count') || 0)
          }
        }
      else
        {
          success: false,
          error: 'No response from Ollama'
        }
      end

    rescue => e
      Rails.logger.error "Ollama Chat Error: #{e.message}"
      {
        success: false,
        error: e.message
      }
    end
  end

  def generate_plant_summary(plant)
    return nil unless available?

    begin
      # Get plant context
      context = PlantContext.generate_gpt_context(plant)
      
      prompt = build_summary_prompt(plant, context)

      response = make_ollama_request(prompt)
      
      response&.dig('response')

    rescue => e
      Rails.logger.error "Ollama Summary Generation Error: #{e.message}"
      nil
    end
  end

  def analyze_plant_compatibility(plants)
    return nil unless available?

    begin
      plant_data = plants.map do |plant|
        env = plant.environmental_requirements
        {
          name: plant.common_name,
          scientific_name: plant.scientific_name,
          requirements: {
            zone: env&.zone_range || 'Unknown',
            sunlight: env&.light_requirement&.humanize || 'Unknown',
            soil_ph: env&.ph_range || 'Unknown',
            drought_tolerance: env&.drought_tolerance_level || 'Unknown'
          },
          traits: plant.semantic_tags.pluck(:name)
        }
      end

      prompt = build_compatibility_prompt(plant_data)

      response = make_ollama_request(prompt)
      
      response&.dig('response')

    rescue => e
      Rails.logger.error "Ollama Compatibility Analysis Error: #{e.message}"
      nil
    end
  end

  def search_plants_with_ai(query, criteria = {})
    return nil unless available?

    begin
      # Get relevant plants from database first
      search_service = EnhancedPlantSearchService.new
      plants = search_service.natural_language_search(query)
      
      # Convert to array if it's an ActiveRecord relation
      plants_array = plants.respond_to?(:to_a) ? plants.to_a : plants
      
      # If no plants found, try a broader search
      if plants_array.empty?
        # Try keyword search as fallback
        plants = search_service.keyword_search_simple(query, { limit: 20 })
        plants_array = plants.respond_to?(:to_a) ? plants.to_a : plants
      end
      
      # If still no plants, return a helpful response
      if plants_array.empty?
        return {
          ai_response: "I couldn't find any plants matching '#{query}' in our database. You might try searching for more general terms like 'drought tolerant', 'shade plants', or specific plant types like 'herbs' or 'trees'. Our database contains #{EnhancedPlant.count} plants that you can explore.",
          plants_found: 0,
          plants_data: []
        }
      end
      
      # Limit to reasonable number for AI processing
      plants_data = plants_array.first(20).map do |plant|
        env = plant.environmental_requirements
        {
          name: plant.common_name,
          scientific_name: plant.scientific_name,
          description: plant.description_brief || plant.description_detailed&.truncate(100) || 'No description available',
          zones: env&.zone_range || 'Unknown',
          uses: plant.plant_uses.joins(:use_category).pluck('use_categories.name').uniq.first(3)
        }
      end

      prompt = build_plant_search_prompt(query, plants_data, criteria)
      
      response = make_ollama_request(prompt)
      
      {
        ai_response: response&.dig('response'),
        plants_found: plants_array.count,
        plants_data: plants_data
      }

    rescue => e
      Rails.logger.error "Ollama Plant Search Error: #{e.message}"
      # Return a fallback response instead of nil
      {
        ai_response: "I encountered an error while searching for plants. Please try a simpler search term or check back later.",
        plants_found: 0,
        plants_data: [],
        error: e.message
      }
    end
  end

  private

  def check_ollama_health
    begin
      response = HTTParty.get("#{@base_url}/api/tags", timeout: 5)
      response.success?
    rescue
      false
    end
  end

  def make_ollama_request(prompt, stream: false, enhanced_options: false)
    begin
      Rails.logger.info "Making Ollama request with prompt length: #{prompt.length}"
      
      options = if enhanced_options
        {
          temperature: 0.8,      # Higher creativity for conversations
          top_p: 0.95,          # More diverse vocabulary
          top_k: 50,            # Better word selection
          repeat_penalty: 1.1,   # Reduce repetition
          num_predict: 2000,     # Longer responses
          stop: ['Human:', 'User:', '\n\nUser:', '\n\nHuman:']  # Conversation boundaries
        }
      else
        {
          temperature: 0.7,
          top_p: 0.9,
          top_k: 40,
          num_predict: 1000
        }
      end

      response = HTTParty.post(
        "#{@base_url}/api/generate",
        headers: { 'Content-Type' => 'application/json' },
        body: {
          model: @model,
          prompt: prompt,
          stream: stream,
          options: options
        }.to_json,
        timeout: @timeout
      )

      Rails.logger.info "Ollama response status: #{response.code}"

      if response.success?
        parsed_response = JSON.parse(response.body)
        Rails.logger.info "Ollama response length: #{parsed_response['response']&.length || 0}"
        parsed_response
      else
        Rails.logger.error "Ollama API Error: #{response.code} - #{response.body}"
        nil
      end
    rescue Net::ReadTimeout => e
      Rails.logger.error "Ollama Request Timeout: #{e.message}"
      nil
    rescue => e
      Rails.logger.error "Ollama Request Error: #{e.message}"
      nil
    end
  end

  def build_enhanced_system_prompt(context = {})
    base_prompt = <<~PROMPT
      You are PermieBro, an enthusiastic and knowledgeable permaculture expert and plant consultant. You have extensive experience in:
      
      🌱 EXPERTISE AREAS:
      - Plant biology, ecology, and cultivation
      - Permaculture design principles and implementation  
      - Companion planting and polyculture systems
      - Sustainable gardening and regenerative agriculture
      - Regional climate adaptation and microclimates
      - Organic pest management and biological controls
      - Soil health, composting, and nutrient cycling
      - Water-wise gardening and natural irrigation
      - Native plant ecosystems and biodiversity
      - Food forests and edible landscaping

      🎯 COMMUNICATION STYLE:
      - Warm, encouraging, and genuinely excited about plants
      - Use vivid descriptions and relatable analogies
      - Share practical tips with enthusiasm
      - Ask thoughtful follow-up questions to better help
      - Acknowledge different experience levels compassionately
      - Use emojis naturally to add personality (but not excessively)
      - Tell brief, relevant stories from "experience" when helpful
      - Always provide actionable, practical advice

      🧠 CONVERSATION APPROACH:
      - Remember context from earlier in our conversation
      - Build upon previous topics naturally
      - Offer multiple solutions when appropriate
      - Explain the "why" behind recommendations
      - Suggest complementary ideas and connections
      - Be curious about the human's specific situation
      - Celebrate successes and encourage through challenges

      🌍 REGIONAL AWARENESS:
      #{context[:location] ? "- User is located in: #{context[:location]}" : "- Ask about location when relevant for specific advice"}
      #{context[:experience_level] ? "- User's experience level: #{context[:experience_level]}" : "- Gauge experience level through conversation"}
      #{context[:garden_type] ? "- Garden type: #{context[:garden_type]}" : ""}
      #{context[:climate_zone] ? "- Climate zone: #{context[:climate_zone]}" : ""}

      Remember: You're not just providing information—you're having a genuine conversation with someone who shares your passion for plants and sustainable living. Be helpful, encouraging, and authentically enthusiastic!
    PROMPT

    base_prompt
  end

  def build_conversational_prompt(system_prompt, user_query, context)
    # Detect question type to tailor response
    query_context = analyze_query_intent(user_query)
    
    conversational_setup = case query_context[:intent]
    when :greeting
      "The user is greeting you or starting a conversation. Respond warmly and invite them to ask about plants."
    when :identification
      "The user wants to identify a plant or learn about a specific plant. Be thorough but engaging."
    when :problem_solving
      "The user has a gardening problem. Be empathetic and provide multiple solution options."
    when :planning
      "The user is planning their garden. Ask clarifying questions and offer creative ideas."
    when :general_knowledge
      "The user wants to learn about gardening concepts. Teach enthusiastically with examples."
    else
      "The user has a plant or gardening question. Provide helpful, engaging advice."
    end

    <<~PROMPT
      #{system_prompt}

      CURRENT CONVERSATION CONTEXT:
      #{conversational_setup}

      USER'S MESSAGE: "#{user_query}"

      Please respond as PermieBro with enthusiasm and expertise. Make your response conversational, helpful, and engaging. If you need more information to give the best advice, ask thoughtful follow-up questions.

      RESPONSE:
    PROMPT
  end

  def build_natural_conversation(system_prompt, messages, plant_context)
    conversation_context = ""
    
    if plant_context.any?
      plant_names = plant_context.map(&:common_name).join(", ")
      conversation_context += "\nRELEVANT PLANTS IN CONTEXT: #{plant_names}"
    end

    # Build conversation history with natural flow
    conversation = system_prompt + conversation_context + "\n\n"
    conversation += "Here's our conversation so far:\n\n"
    
    messages.each_with_index do |message, index|
      role_name = message['role'] == 'user' ? 'Gardener' : 'PermieBro'
      
      # Add context cues for natural conversation flow
      if index == 0
        conversation += "#{role_name}: #{message['content']}\n\n"
      else
        previous_role = messages[index - 1]['role']
        if previous_role != message['role']
          conversation += "#{role_name}: #{message['content']}\n\n"
        else
          conversation += "#{message['content']}\n\n"
        end
      end
    end
    
    conversation += "PermieBro (responding naturally and helpfully):"
    conversation
  end

  def build_conversational_system_prompt(plant_context, messages)
    base_prompt = build_enhanced_system_prompt
    
    # Add conversation-specific context
    if messages.length > 1
      base_prompt += <<~CONTEXT

        CONVERSATION NOTES:
        - This is an ongoing conversation - reference earlier topics naturally
        - The gardener has asked #{messages.length} questions so far
        - Build rapport and maintain continuity with previous responses
        - Look for opportunities to connect new questions to earlier topics
      CONTEXT
    end

    if plant_context.any?
      plant_summaries = plant_context.map do |plant|
        "• #{plant.common_name} (#{plant.scientific_name}): #{plant.description_brief&.truncate(80) || 'No description available'}"
      end.join("\n")

      base_prompt += <<~CONTEXT

        CURRENT PLANT FOCUS:
        #{plant_summaries}
        
        Use this information to provide specific, relevant advice about these plants.
      CONTEXT
    end

    base_prompt
  end

  def format_response(response)
    # Clean up response formatting for better readability
    formatted = response.strip
    
    # Fix common formatting issues
    formatted = formatted.gsub(/\n{3,}/, "\n\n")  # Reduce excessive line breaks
    formatted = formatted.gsub(/(\w)\n(\w)/, '\1 \2')  # Join broken sentences
    formatted = formatted.gsub(/([.!?])\s*\n\s*([A-Z])/, '\1 \2')  # Fix sentence breaks
    
    # Ensure proper paragraph breaks
    formatted = formatted.gsub(/([.!?])\s*([A-Z])/, '\1\n\n\2')
    
    formatted
  end

  def format_conversational_response(response, last_user_message)
    formatted = format_response(response)
    
    # Remove any accidental role prefixes
    formatted = formatted.gsub(/^(PermieBro|Assistant|AI):\s*/i, '')
    
    # Ensure response doesn't repeat the user's question
    user_content = last_user_message['content'].strip
    if formatted.downcase.include?(user_content.downcase) && user_content.length > 20
      # Remove obvious repetitions
      formatted = formatted.gsub(/#{Regexp.escape(user_content)}/i, '').strip
    end
    
    formatted
  end

  def analyze_query_intent(query)
    query_lower = query.downcase
    
    intent = case query_lower
    when /^(hi|hello|hey|good (morning|afternoon|evening))/
      :greeting
    when /(what is|tell me about|identify|id this)/
      :identification  
    when /(problem|trouble|help|wrong|dying|disease|pest)/
      :problem_solving
    when /(plan|design|layout|where to plant|how to arrange)/
      :planning
    when /(companion|polyculture|guild|together)/
      :companion_planning
    when /(why|how|what|explain|difference|benefit)/
      :general_knowledge
    else
      :general_question
    end

    {
      intent: intent,
      complexity: query.split.length > 10 ? :complex : :simple,
      emotional_tone: detect_emotional_tone(query)
    }
  end

  def detect_emotional_tone(query)
    query_lower = query.downcase
    
    case query_lower
    when /frustrated|annoyed|angry|hate/
      :frustrated
    when /excited|love|amazing|wonderful/
      :excited
    when /worried|concerned|afraid|nervous/
      :concerned
    when /confused|don't understand|lost/
      :confused
    else
      :neutral
    end
  end

  def build_plant_expert_prompt(context = {})
    base_prompt = <<~PROMPT
      You are PermieBro, an expert permaculture and plant consultant with deep knowledge of:
      - Plant biology, ecology, and growing requirements
      - Companion planting and polyculture design
      - Permaculture principles and sustainable gardening
      - Regional climate adaptation and plant selection
      - Organic pest management and soil health

      Your personality is friendly, encouraging, and practical. You provide actionable advice
      while educating users about sustainable gardening practices.

      When answering questions:
      1. Provide practical, actionable advice
      2. Consider the user's location and climate when relevant
      3. Suggest companion plants and polyculture approaches
      4. Emphasize sustainable and organic methods
      5. Be encouraging and supportive of all gardening skill levels
      6. Keep responses concise but informative
    PROMPT

    if context[:location]
      base_prompt += "\n\nUser Location Context: #{context[:location]}"
    end

    if context[:experience_level]
      base_prompt += "\n\nUser Experience Level: #{context[:experience_level]}"
    end

    base_prompt
  end

  def build_query_prompt(system_prompt, user_query)
    <<~PROMPT
      #{system_prompt}

      User Question: #{user_query}

      Please provide a helpful, practical response that addresses the user's question about plants and gardening. Focus on actionable advice and permaculture principles.

      Response:
    PROMPT
  end

  def build_conversation_prompt(system_prompt, messages)
    conversation = system_prompt + "\n\nConversation:\n"
    
    messages.each do |message|
      role = message['role'] == 'user' ? 'Human' : 'PermieBro'
      conversation += "#{role}: #{message['content']}\n"
    end
    
    conversation += "PermieBro:"
    conversation
  end

  def build_chat_system_prompt(plant_context)
    prompt = build_plant_expert_prompt

    if plant_context.any?
      plant_info = plant_context.map do |plant|
        "#{plant.common_name} (#{plant.scientific_name}): #{plant.description_brief&.truncate(100)}"
      end.join("\n")

      prompt += <<~CONTEXT

        Current Plant Context:
        #{plant_info}

        Use this context to provide more specific and relevant advice.
      CONTEXT
    end

    prompt
  end

  def build_summary_prompt(plant, context)
    <<~PROMPT
      Create an engaging, informative summary for #{plant.common_name} (#{plant.scientific_name}) 
      that would be helpful for gardeners and permaculture enthusiasts.

      Plant Information:
      #{context[:summary]}

      Care Information:
      #{context[:care_guide]}

      Uses:
      #{context[:uses_detailed]}

      Please create a comprehensive but readable summary (300-500 words) that includes:
      1. A brief introduction to the plant
      2. Key growing requirements and care tips
      3. Primary uses and benefits
      4. Any special considerations or interesting facts

      Write in a friendly, encouraging tone that makes gardening accessible.

      Summary:
    PROMPT
  end

  def build_compatibility_prompt(plant_data)
    plants_info = plant_data.map do |plant|
      <<~PLANT
        #{plant[:name]} (#{plant[:scientific_name]}):
        - Zones: #{plant[:requirements][:zone]}
        - Sunlight: #{plant[:requirements][:sunlight]}
        - Soil pH: #{plant[:requirements][:soil_ph]}
        - Drought tolerance: #{plant[:requirements][:drought_tolerance]}
        - Traits: #{plant[:traits].join(', ')}
      PLANT
    end.join("\n\n")

    <<~PROMPT
      Analyze the compatibility of these plants for companion planting or polyculture design:

      #{plants_info}

      Please provide a detailed analysis including:
      1. Overall compatibility assessment
      2. Shared growing requirements
      3. Potential benefits of growing them together
      4. Any potential conflicts or considerations
      5. Suggestions for optimal arrangement or spacing

      Focus on practical permaculture principles and sustainable gardening practices.

      Analysis:
    PROMPT
  end

  def build_plant_search_prompt(query, plants_data, criteria)
    if plants_data.empty?
      return "I couldn't find any plants matching '#{query}' in our database. Please try a different search term."
    end

    plants_list = plants_data.map do |plant|
      "- #{plant[:name]} (#{plant[:scientific_name]}): #{plant[:description]&.truncate(80)} | Zones: #{plant[:zones]} | Uses: #{plant[:uses].join(', ')}"
    end.join("\n")

    <<~PROMPT
      A user is searching for plants with this query: "#{query}"

      Here are the relevant plants found in our database:
      #{plants_list}

      Please provide a helpful response that:
      1. Addresses the user's specific query
      2. Recommends the most suitable plants from the list
      3. Explains why these plants are good choices
      4. Provides practical growing tips
      5. Suggests companion planting ideas if relevant

      Keep the response informative but concise (200-400 words).

      Response:
    PROMPT
  end

  def fallback_response(query)
    # Simple keyword-based fallback
    if query.downcase.include?('companion')
      "I'd love to help with companion planting! Try searching for specific plants in our database, or ask about plants that grow well together in your climate zone."
    elsif query.downcase.include?('drought')
      "For drought-tolerant plants, consider looking at plants tagged as 'drought_tolerant' in our database. Native plants are often your best bet for water-wise gardening."
    elsif query.downcase.include?('zone')
      "Climate zones are important for plant selection! If you tell me your USDA hardiness zone, I can help recommend suitable plants."
    else
      "I'm here to help with plant questions! You can ask about specific plants, companion planting, care instructions, or plant recommendations for your area."
    end
  end
end 