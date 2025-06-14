# frozen_string_literal: true
class PlantContext < ApplicationRecord
  belongs_to :enhanced_plant
  
  validates :context_type, inclusion: { 
    in: %w[summary care_guide companion_planting climate_adaptation uses_detailed] 
  }
  validates :content, presence: true
  
  scope :by_type, ->(type) { where(context_type: type) }
  
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
  
  def self.create_contexts_for_plant(plant)
    contexts = generate_gpt_context(plant)
    
    contexts.each do |type, content|
      find_or_create_by(
        enhanced_plant: plant,
        context_type: type.to_s
      ) do |context|
        context.content = content
      end
    end
  end
  
  private
  
  def self.generate_summary_context(plant)
    env = plant.environmental_requirements
    tags = plant.semantic_tags.pluck(:name).join(', ')
    uses = plant.plant_uses.joins(:use_category).pluck('use_categories.name').uniq.join(', ')
    
    zone_range = env&.zone_range || 'Unknown'
    sunlight = env&.light_requirement&.humanize || 'Unknown'
    
    <<~CONTEXT
      #{plant.common_name} (#{plant.scientific_name}) is a #{plant.plant_type} #{plant.life_cycle} 
      plant from the #{plant.family} family. It grows in USDA zones #{zone_range} 
      and prefers #{sunlight} sunlight.
      
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
      - Hardiness zones: #{env.zone_range || 'Unknown'}
      - Soil pH: #{env.ph_range || 'Unknown'}
      - Soil drainage: #{env.soil_drainage&.humanize || 'Unknown'}
      
      GROWING CONDITIONS:
      - Sunlight: #{env.light_requirement&.humanize || 'Unknown'}
      - Temperature range: #{env.temperature_range_celsius || 'Unknown'}
      - Drought tolerance: #{env.drought_tolerance_level}
      
      MAINTENANCE:
      - Light needs: #{env.light_needs_description || 'Unknown'}
      - Soil preferences: #{env.soil_preferences}
      - Growth rate: #{plant.semantic_tags.where(category: 'growth_habit').pluck(:name).join(', ')}
      
      #{plant.growing_notes}
    CONTEXT
  end
  
  def self.generate_companion_context(plant)
    beneficial = plant.beneficial_companions.limit(10).pluck(:common_name)
    antagonistic = plant.antagonistic_plants.limit(5).pluck(:common_name)
    
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
      
      HARDINESS:
      - USDA Zones: #{env.zone_range || 'Unknown'}
      - Heat Zones: #{env.heat_zone_range || 'Unknown'}
      - Temperature range: #{env.temperature_range_celsius || 'Unknown'}
      
      ENVIRONMENTAL ADAPTATIONS:
      - Drought tolerance: #{env.drought_tolerance_level}
      - Light requirements: #{env.light_needs_description || 'Unknown'}
      - Soil preferences: #{env.soil_preferences}
      
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
      effectiveness_score = effectiveness ? (effectiveness * 10).round : 'Unknown'
      context += "#{use_name.upcase} (Effectiveness: #{effectiveness_score}/10):\n"
      
      # Get specific use details
      use_details = plant.plant_uses.joins(:use_category)
                        .where(use_categories: { name: use_name })
                        .pluck(:safety_notes, :preparation_method, :traditional_knowledge)
                        .compact
      
      use_details.each do |safety, method, traditional|
        context += "- #{safety}\n" if safety.present?
        context += "- Preparation: #{method}\n" if method.present?
        context += "- Traditional use: #{traditional}\n" if traditional.present?
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