# GPT Integration Guide for PermiePortal

## Overview
This guide outlines how to structure your plant database for optimal GPT integration, enabling natural language queries and intelligent plant recommendations.

## 1. Data Structure for GPT Context

### Plant Context Embeddings
```ruby
# app/models/plant_context.rb
class PlantContext < ApplicationRecord
  belongs_to :enhanced_plant
  
  validates :context_type, inclusion: { 
    in: %w[summary care_guide companion_planting climate_adaptation uses_detailed] 
  }
  
  # Generate GPT-optimized plant descriptions
  def self.generate_gpt_context(plant)
    contexts = {}
    
    # Summary context for quick reference
    contexts[:summary] = generate_summary_context(plant)
    
    # Detailed care guide
    contexts[:care_guide] = generate_care_context(plant)
    
    # Companion planting context
    contexts[:companion_planting] = generate_companion_context(plant)
    
    # Climate adaptation context
    contexts[:climate_adaptation] = generate_climate_context(plant)
    
    # Uses and benefits context
    contexts[:uses_detailed] = generate_uses_context(plant)
    
    contexts
  end
  
  private
  
  def self.generate_summary_context(plant)
    env = plant.environmental_requirements
    tags = plant.semantic_tags.pluck(:name).join(', ')
    uses = plant.plant_uses.joins(:use_category).pluck('use_categories.name').join(', ')
    
    <<~CONTEXT
      #{plant.common_name} (#{plant.scientific_name}) is a #{plant.plant_type} #{plant.life_cycle} 
      plant from the #{plant.family} family. It grows in USDA zones #{env&.zone_min}-#{env&.zone_max} 
      and prefers #{env&.sunlight_requirements} sunlight with #{env&.water_requirements} water needs.
      
      Key characteristics: #{tags}
      Primary uses: #{uses}
      
      #{plant.description_detailed&.truncate(200)}
    CONTEXT
  end
  
  def self.generate_care_context(plant)
    env = plant.environmental_requirements
    return "Care information not available." unless env
    
    <<~CONTEXT
      CARE GUIDE for #{plant.common_name}:
      
      PLANTING:
      - Hardiness zones: #{env.zone_min}-#{env.zone_max}
      - Soil pH: #{env.soil_ph_min}-#{env.soil_ph_max}
      - Soil type: #{env.soil_type}
      - Drainage: #{env.soil_drainage}
      
      GROWING CONDITIONS:
      - Sunlight: #{env.sunlight_requirements}
      - Water needs: #{env.water_requirements}
      - Temperature range: #{env.temperature_min_c}°C to #{env.temperature_max_c}°C
      - Humidity: #{env.humidity_requirements}
      
      MAINTENANCE:
      - Drought tolerance: #{env.drought_tolerance}
      - Frost tolerance: #{env.frost_tolerance}
      - Growth rate: #{plant.semantic_tags.where(category: 'growth_habit').pluck(:name).join(', ')}
      
      #{plant.growing_notes}
    CONTEXT
  end
  
  def self.generate_companion_context(plant)
    beneficial = plant.beneficial_companions.limit(10).pluck(:common_name)
    antagonistic = plant.antagonistic_companions.limit(5).pluck(:common_name)
    
    context = "COMPANION PLANTING for #{plant.common_name}:\n\n"
    
    if beneficial.any?
      context += "BENEFICIAL COMPANIONS:\n"
      context += beneficial.map { |name| "- #{name}" }.join("\n")
      context += "\n\n"
    end
    
    if antagonistic.any?
      context += "AVOID PLANTING WITH:\n"
      context += antagonistic.map { |name| "- #{name}" }.join("\n")
      context += "\n\n"
    end
    
    # Add guild information if available
    if plant.guild_members.any?
      guilds = plant.guild_members.joins(:plant_guild).pluck('plant_guilds.name')
      context += "PLANT GUILDS: #{guilds.join(', ')}\n"
    end
    
    context
  end
  
  def self.generate_climate_context(plant)
    env = plant.environmental_requirements
    return "Climate information not available." unless env
    
    <<~CONTEXT
      CLIMATE ADAPTATION for #{plant.common_name}:
      
      TEMPERATURE TOLERANCE:
      - Minimum: #{env.temperature_min_c}°C (#{celsius_to_fahrenheit(env.temperature_min_c)}°F)
      - Maximum: #{env.temperature_max_c}°C (#{celsius_to_fahrenheit(env.temperature_max_c)}°F)
      - Ideal range: #{env.temperature_ideal_min_c}°C to #{env.temperature_ideal_max_c}°C
      
      ENVIRONMENTAL ADAPTATIONS:
      - Drought tolerance: #{env.drought_tolerance}
      - Frost tolerance: #{env.frost_tolerance}
      - Wind tolerance: #{env.wind_tolerance}
      - Salt tolerance: #{env.salt_tolerance}
      
      SEASONAL CONSIDERATIONS:
      #{plant.semantic_tags.where(category: 'season').pluck(:name, :description).map { |name, desc| "- #{name}: #{desc}" }.join("\n")}
    CONTEXT
  end
  
  def self.generate_uses_context(plant)
    uses_by_category = plant.plant_uses.joins(:use_category)
                           .group('use_categories.name')
                           .average(:effectiveness_score)
    
    context = "USES AND BENEFITS of #{plant.common_name}:\n\n"
    
    uses_by_category.each do |use_name, effectiveness|
      context += "#{use_name.upcase} (Effectiveness: #{(effectiveness * 10).round}/10):\n"
      
      # Get specific use details
      use_details = plant.plant_uses.joins(:use_category)
                        .where(use_categories: { name: use_name })
                        .pluck(:notes, :preparation_method)
                        .compact
      
      use_details.each do |notes, method|
        context += "- #{notes}\n" if notes.present?
        context += "- Preparation: #{method}\n" if method.present?
      end
      
      context += "\n"
    end
    
    # Add trait-based benefits
    beneficial_traits = plant.semantic_tags.where(category: 'trait').pluck(:name, :description)
    if beneficial_traits.any?
      context += "BENEFICIAL TRAITS:\n"
      beneficial_traits.each do |name, description|
        context += "- #{name.humanize}: #{description}\n"
      end
    end
    
    context
  end
  
  def self.celsius_to_fahrenheit(celsius)
    return nil unless celsius
    (celsius * 9.0 / 5.0 + 32).round(1)
  end
end
```

## 2. GPT Function Definitions

### Plant Search Functions
```ruby
# app/services/gpt_function_definitions.rb
class GptFunctionDefinitions
  def self.plant_search_functions
    [
      {
        name: "search_plants_by_criteria",
        description: "Search for plants based on multiple criteria like climate zone, plant type, uses, and traits",
        parameters: {
          type: "object",
          properties: {
            zone_range: {
              type: "string",
              description: "USDA hardiness zone range (e.g., '5-8', '9', '3-7')"
            },
            plant_type: {
              type: "string",
              enum: ["tree", "shrub", "herbaceous", "vine", "ground_cover", "grass"],
              description: "Type of plant growth habit"
            },
            sunlight: {
              type: "string",
              enum: ["full_sun", "partial_sun", "partial_shade", "full_shade"],
              description: "Sunlight requirements"
            },
            water_needs: {
              type: "string",
              enum: ["low", "moderate", "high"],
              description: "Water requirements"
            },
            uses: {
              type: "array",
              items: { type: "string" },
              description: "Intended uses (e.g., 'edible', 'medicinal', 'ornamental', 'wildlife_habitat')"
            },
            traits: {
              type: "array",
              items: { type: "string" },
              description: "Desired traits (e.g., 'drought_tolerant', 'fast_growing', 'pollinator_friendly')"
            },
            soil_type: {
              type: "string",
              enum: ["clay", "loam", "sand", "rocky", "any"],
              description: "Soil type preference"
            },
            mature_size: {
              type: "string",
              enum: ["small", "medium", "large"],
              description: "Mature plant size category"
            }
          }
        }
      },
      {
        name: "get_plant_details",
        description: "Get comprehensive details about a specific plant",
        parameters: {
          type: "object",
          properties: {
            plant_identifier: {
              type: "string",
              description: "Plant common name, scientific name, or ID"
            },
            detail_type: {
              type: "string",
              enum: ["summary", "care_guide", "companion_planting", "uses", "all"],
              description: "Type of details to retrieve"
            }
          },
          required: ["plant_identifier"]
        }
      },
      {
        name: "find_companion_plants",
        description: "Find plants that grow well together with a specified plant",
        parameters: {
          type: "object",
          properties: {
            primary_plant: {
              type: "string",
              description: "Name of the primary plant to find companions for"
            },
            relationship_type: {
              type: "string",
              enum: ["beneficial", "neutral", "avoid"],
              description: "Type of companion relationship"
            },
            shared_requirements: {
              type: "boolean",
              description: "Whether companions should have similar growing requirements"
            }
          },
          required: ["primary_plant"]
        }
      },
      {
        name: "recommend_plants_for_location",
        description: "Recommend plants suitable for a specific location and conditions",
        parameters: {
          type: "object",
          properties: {
            location: {
              type: "object",
              properties: {
                zone: { type: "string", description: "USDA hardiness zone" },
                climate: { type: "string", description: "Climate description (e.g., 'hot and dry', 'humid subtropical')" },
                soil_conditions: { type: "string", description: "Soil description" }
              }
            },
            garden_goals: {
              type: "array",
              items: { type: "string" },
              description: "Gardening goals (e.g., 'food production', 'wildlife habitat', 'low maintenance')"
            },
            experience_level: {
              type: "string",
              enum: ["beginner", "intermediate", "advanced"],
              description: "Gardener's experience level"
            },
            space_constraints: {
              type: "object",
              properties: {
                size: { type: "string", enum: ["small", "medium", "large"] },
                type: { type: "string", enum: ["container", "raised_bed", "ground", "greenhouse"] }
              }
            }
          }
        }
      }
    ]
  end
  
  def self.plant_care_functions
    [
      {
        name: "get_seasonal_care_calendar",
        description: "Get seasonal care instructions for specific plants",
        parameters: {
          type: "object",
          properties: {
            plants: {
              type: "array",
              items: { type: "string" },
              description: "List of plant names"
            },
            location: {
              type: "string",
              description: "Geographic location or USDA zone"
            },
            season: {
              type: "string",
              enum: ["spring", "summer", "fall", "winter", "all"],
              description: "Season for care instructions"
            }
          },
          required: ["plants"]
        }
      },
      {
        name: "diagnose_plant_problems",
        description: "Help diagnose plant problems based on symptoms",
        parameters: {
          type: "object",
          properties: {
            plant_name: {
              type: "string",
              description: "Name of the affected plant"
            },
            symptoms: {
              type: "array",
              items: { type: "string" },
              description: "Observed symptoms (e.g., 'yellowing leaves', 'wilting', 'spots on leaves')"
            },
            environmental_factors: {
              type: "object",
              properties: {
                recent_weather: { type: "string" },
                watering_frequency: { type: "string" },
                fertilizer_use: { type: "string" },
                location: { type: "string" }
              }
            }
          },
          required: ["plant_name", "symptoms"]
        }
      }
    ]
  end
end
```

## 3. GPT Service Implementation

### Main GPT Integration Service
```ruby
# app/services/gpt_plant_assistant.rb
class GptPlantAssistant
  include HTTParty
  base_uri 'https://api.openai.com/v1'
  
  def initialize(api_key = nil)
    @api_key = api_key || Rails.application.credentials.openai_api_key
    @headers = {
      'Authorization' => "Bearer #{@api_key}",
      'Content-Type' => 'application/json'
    }
  end
  
  def process_query(user_query, context = {})
    messages = build_messages(user_query, context)
    functions = GptFunctionDefinitions.plant_search_functions + 
                GptFunctionDefinitions.plant_care_functions
    
    response = self.class.post('/chat/completions',
      headers: @headers,
      body: {
        model: 'gpt-4-turbo-preview',
        messages: messages,
        functions: functions,
        function_call: 'auto',
        temperature: 0.7,
        max_tokens: 1500
      }.to_json
    )
    
    handle_response(response)
  end
  
  private
  
  def build_messages(user_query, context)
    system_message = build_system_message(context)
    
    [
      {
        role: 'system',
        content: system_message
      },
      {
        role: 'user',
        content: user_query
      }
    ]
  end
  
  def build_system_message(context)
    base_context = <<~CONTEXT
      You are PermieBot, an expert permaculture and plant specialist assistant. You help users find the right plants for their specific needs, provide growing advice, and suggest companion planting strategies.

      Your knowledge base includes:
      - #{EnhancedPlant.count} plants with detailed growing requirements
      - #{SemanticTag.count} semantic tags for plant characteristics
      - #{PlantRelationship.count} documented plant relationships
      - Comprehensive environmental and care data

      When helping users:
      1. Ask clarifying questions if the request is vague
      2. Consider climate zones, soil conditions, and space constraints
      3. Suggest companion plants and beneficial relationships
      4. Provide practical, actionable advice
      5. Consider the user's experience level
      6. Emphasize sustainable and permaculture principles

      Use the available functions to search for plants and retrieve detailed information.
    CONTEXT
    
    if context[:user_location]
      base_context += "\nUser location context: #{context[:user_location]}"
    end
    
    if context[:garden_type]
      base_context += "\nGarden type: #{context[:garden_type]}"
    end
    
    if context[:experience_level]
      base_context += "\nUser experience level: #{context[:experience_level]}"
    end
    
    base_context
  end
  
  def handle_response(response)
    return { error: 'API request failed', details: response.body } unless response.success?
    
    data = response.parsed_response
    message = data.dig('choices', 0, 'message')
    
    if message['function_call']
      # Execute the function call
      function_result = execute_function(message['function_call'])
      
      # Send function result back to GPT for final response
      follow_up_response = get_follow_up_response(message, function_result)
      
      {
        success: true,
        response: follow_up_response,
        function_used: message['function_call']['name'],
        raw_data: function_result
      }
    else
      {
        success: true,
        response: message['content'],
        function_used: nil
      }
    end
  end
  
  def execute_function(function_call)
    function_name = function_call['name']
    arguments = JSON.parse(function_call['arguments'])
    
    case function_name
    when 'search_plants_by_criteria'
      search_plants_by_criteria(arguments)
    when 'get_plant_details'
      get_plant_details(arguments)
    when 'find_companion_plants'
      find_companion_plants(arguments)
    when 'recommend_plants_for_location'
      recommend_plants_for_location(arguments)
    when 'get_seasonal_care_calendar'
      get_seasonal_care_calendar(arguments)
    when 'diagnose_plant_problems'
      diagnose_plant_problems(arguments)
    else
      { error: "Unknown function: #{function_name}" }
    end
  end
  
  def search_plants_by_criteria(args)
    service = EnhancedPlantSearchService.new
    
    # Convert arguments to search parameters
    search_options = {
      zone_range: parse_zone_range(args['zone_range']),
      plant_type: args['plant_type'],
      sunlight: args['sunlight'],
      water_needs: args['water_needs'],
      traits: args['traits'],
      uses: args['uses'],
      soil_type: args['soil_type'],
      mature_size: args['mature_size'],
      limit: 20
    }
    
    plants = service.search('', search_options.compact)
    
    {
      count: plants.count,
      plants: plants.map { |plant| plant_summary_for_gpt(plant) }
    }
  end
  
  def get_plant_details(args)
    plant = find_plant_by_identifier(args['plant_identifier'])
    return { error: 'Plant not found' } unless plant
    
    detail_type = args['detail_type'] || 'summary'
    
    case detail_type
    when 'summary'
      PlantContext.generate_summary_context(plant)
    when 'care_guide'
      PlantContext.generate_care_context(plant)
    when 'companion_planting'
      PlantContext.generate_companion_context(plant)
    when 'uses'
      PlantContext.generate_uses_context(plant)
    when 'all'
      PlantContext.generate_gpt_context(plant)
    end
  end
  
  def find_companion_plants(args)
    plant = find_plant_by_identifier(args['primary_plant'])
    return { error: 'Plant not found' } unless plant
    
    relationship_type = args['relationship_type'] || 'beneficial'
    
    companions = case relationship_type
                when 'beneficial'
                  plant.beneficial_companions.limit(10)
                when 'avoid'
                  plant.antagonistic_companions.limit(10)
                else
                  plant.neutral_companions.limit(10)
                end
    
    {
      primary_plant: plant.common_name,
      relationship_type: relationship_type,
      companions: companions.map { |c| plant_summary_for_gpt(c) }
    }
  end
  
  def recommend_plants_for_location(args)
    location = args['location'] || {}
    goals = args['garden_goals'] || []
    experience = args['experience_level'] || 'intermediate'
    
    # Build search criteria based on location and goals
    search_options = {
      zone_range: parse_zone_range(location['zone']),
      experience_level: experience,
      limit: 15
    }
    
    # Add goal-based filtering
    if goals.include?('food production')
      search_options[:uses] = ['edible']
    end
    
    if goals.include?('low maintenance')
      search_options[:traits] = ['low_maintenance', 'drought_tolerant']
    end
    
    if goals.include?('wildlife habitat')
      search_options[:traits] = ['pollinator_friendly', 'wildlife_habitat']
    end
    
    service = EnhancedPlantSearchService.new
    plants = service.search('', search_options.compact)
    
    {
      location: location,
      goals: goals,
      experience_level: experience,
      recommended_plants: plants.map { |plant| plant_summary_for_gpt(plant) }
    }
  end
  
  def plant_summary_for_gpt(plant)
    env = plant.environmental_requirements
    
    {
      common_name: plant.common_name,
      scientific_name: plant.scientific_name,
      plant_type: plant.plant_type,
      life_cycle: plant.life_cycle,
      family: plant.family,
      zones: env ? "#{env.zone_min}-#{env.zone_max}" : 'Unknown',
      sunlight: env&.sunlight_requirements,
      water_needs: env&.water_requirements,
      mature_size: "#{plant.mature_height_min_cm}-#{plant.mature_height_max_cm}cm",
      uses: plant.plant_uses.joins(:use_category).pluck('use_categories.name'),
      traits: plant.semantic_tags.pluck(:name),
      description: plant.description_detailed&.truncate(150)
    }
  end
  
  def find_plant_by_identifier(identifier)
    EnhancedPlant.where(
      "common_name ILIKE ? OR scientific_name ILIKE ? OR id::text = ?",
      "%#{identifier}%", "%#{identifier}%", identifier
    ).first
  end
  
  def parse_zone_range(zone_string)
    return nil unless zone_string
    
    if zone_string.include?('-')
      min_zone, max_zone = zone_string.split('-').map(&:to_i)
      (min_zone..max_zone)
    else
      zone = zone_string.to_i
      (zone..zone)
    end
  end
  
  def get_follow_up_response(original_message, function_result)
    follow_up_messages = [
      {
        role: 'assistant',
        content: original_message['content'],
        function_call: original_message['function_call']
      },
      {
        role: 'function',
        name: original_message['function_call']['name'],
        content: function_result.to_json
      }
    ]
    
    response = self.class.post('/chat/completions',
      headers: @headers,
      body: {
        model: 'gpt-4-turbo-preview',
        messages: follow_up_messages,
        temperature: 0.7,
        max_tokens: 1000
      }.to_json
    )
    
    if response.success?
      response.parsed_response.dig('choices', 0, 'message', 'content')
    else
      "I found the information but had trouble formatting the response. Here's the raw data: #{function_result}"
    end
  end
end
```

## 4. Controller Integration

### GPT Chat Controller
```ruby
# app/controllers/api/v1/gpt_chat_controller.rb
class Api::V1::GptChatController < ApplicationController
  before_action :authenticate_user! # Add authentication as needed
  
  def chat
    query = params[:message]
    context = build_user_context
    
    if query.blank?
      render json: { error: 'Message is required' }, status: 400
      return
    end
    
    gpt_service = GptPlantAssistant.new
    result = gpt_service.process_query(query, context)
    
    if result[:success]
      # Log the interaction
      log_chat_interaction(query, result)
      
      render json: {
        response: result[:response],
        function_used: result[:function_used],
        timestamp: Time.current
      }
    else
      render json: { 
        error: 'Failed to process query', 
        details: result[:error] 
      }, status: 500
    end
  end
  
  private
  
  def build_user_context
    context = {}
    
    # Add user location if available
    if current_user&.location
      context[:user_location] = current_user.location
    end
    
    # Add user preferences
    if current_user&.garden_preferences
      context[:garden_type] = current_user.garden_preferences['type']
      context[:experience_level] = current_user.garden_preferences['experience_level']
    end
    
    # Add session context
    context[:session_id] = session.id
    
    context
  end
  
  def log_chat_interaction(query, result)
    ChatLog.create!(
      user: current_user,
      query: query,
      response: result[:response],
      function_used: result[:function_used],
      session_id: session.id,
      response_time: Time.current
    )
  end
end
```

## 5. Frontend Integration

### JavaScript GPT Chat Interface
```javascript
// app/javascript/gpt_chat.js
class GptChatInterface {
  constructor(containerId) {
    this.container = document.getElementById(containerId);
    this.setupInterface();
    this.bindEvents();
  }
  
  setupInterface() {
    this.container.innerHTML = `
      <div class="gpt-chat-container">
        <div class="chat-messages" id="chatMessages"></div>
        <div class="chat-input-container">
          <input type="text" id="chatInput" placeholder="Ask me about plants..." />
          <button id="sendButton">Send</button>
        </div>
        <div class="suggested-queries">
          <h4>Try asking:</h4>
          <button class="suggestion" data-query="What drought tolerant plants work in zone 8?">
            Drought tolerant plants for zone 8
          </button>
          <button class="suggestion" data-query="Find companion plants for tomatoes">
            Companion plants for tomatoes
          </button>
          <button class="suggestion" data-query="Recommend low maintenance plants for beginners">
            Low maintenance plants for beginners
          </button>
        </div>
      </div>
    `;
  }
  
  bindEvents() {
    const input = document.getElementById('chatInput');
    const sendButton = document.getElementById('sendButton');
    const suggestions = document.querySelectorAll('.suggestion');
    
    sendButton.addEventListener('click', () => this.sendMessage());
    input.addEventListener('keypress', (e) => {
      if (e.key === 'Enter') this.sendMessage();
    });
    
    suggestions.forEach(button => {
      button.addEventListener('click', (e) => {
        const query = e.target.dataset.query;
        input.value = query;
        this.sendMessage();
      });
    });
  }
  
  async sendMessage() {
    const input = document.getElementById('chatInput');
    const message = input.value.trim();
    
    if (!message) return;
    
    this.addMessage('user', message);
    input.value = '';
    
    this.showTypingIndicator();
    
    try {
      const response = await fetch('/api/v1/gpt_chat/chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRF-Token': document.querySelector('[name="csrf-token"]').content
        },
        body: JSON.stringify({ message })
      });
      
      const data = await response.json();
      
      this.hideTypingIndicator();
      
      if (response.ok) {
        this.addMessage('assistant', data.response, data.function_used);
      } else {
        this.addMessage('error', data.error || 'Sorry, I encountered an error.');
      }
    } catch (error) {
      this.hideTypingIndicator();
      this.addMessage('error', 'Network error. Please try again.');
    }
  }
  
  addMessage(type, content, functionUsed = null) {
    const messagesContainer = document.getElementById('chatMessages');
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${type}`;
    
    let messageContent = `<div class="message-content">${content}</div>`;
    
    if (functionUsed) {
      messageContent += `<div class="function-indicator">Used: ${functionUsed}</div>`;
    }
    
    messageDiv.innerHTML = messageContent;
    messagesContainer.appendChild(messageDiv);
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
  }
  
  showTypingIndicator() {
    this.addMessage('assistant', '<div class="typing-indicator">PermieBot is thinking...</div>');
  }
  
  hideTypingIndicator() {
    const messages = document.querySelectorAll('.message.assistant');
    const lastMessage = messages[messages.length - 1];
    if (lastMessage && lastMessage.querySelector('.typing-indicator')) {
      lastMessage.remove();
    }
  }
}

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
  if (document.getElementById('gptChatContainer')) {
    new GptChatInterface('gptChatContainer');
  }
});
```

## 6. Performance Optimization

### Caching Strategy
```ruby
# app/services/gpt_cache_service.rb
class GptCacheService
  CACHE_EXPIRY = 1.hour
  
  def self.cached_query(query_hash, &block)
    Rails.cache.fetch("gpt_query:#{query_hash}", expires_in: CACHE_EXPIRY) do
      yield
    end
  end
  
  def self.generate_query_hash(query, context)
    Digest::SHA256.hexdigest("#{query}:#{context.to_json}")
  end
  
  def self.warm_cache_for_common_queries
    common_queries = [
      "drought tolerant plants for zone 8",
      "companion plants for tomatoes",
      "low maintenance plants for beginners",
      "edible plants for shade",
      "fast growing trees"
    ]
    
    gpt_service = GptPlantAssistant.new
    
    common_queries.each do |query|
      query_hash = generate_query_hash(query, {})
      cached_query(query_hash) do
        gpt_service.process_query(query)
      end
    end
  end
end
```

This GPT integration provides:
- **Natural language processing** for complex plant queries
- **Function calling** for structured data retrieval
- **Context-aware responses** based on user location and preferences
- **Caching** for improved performance
- **Interactive chat interface** for user engagement
- **Comprehensive plant knowledge** integration

The system can handle queries like:
- "I live in zone 7 and want drought-tolerant shrubs that attract butterflies"
- "What should I plant with my tomatoes in a small raised bed?"
- "I'm a beginner gardener in Florida - what are some easy plants to start with?" 