# frozen_string_literal: true
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
      },
      {
        name: "create_planting_schedule",
        description: "Create a planting schedule based on location and plant selection",
        parameters: {
          type: "object",
          properties: {
            plants: {
              type: "array",
              items: { type: "string" },
              description: "List of plants to include in schedule"
            },
            location: {
              type: "string",
              description: "Geographic location or USDA zone"
            },
            garden_type: {
              type: "string",
              enum: ["vegetable", "herb", "flower", "mixed", "food_forest"],
              description: "Type of garden being planned"
            },
            start_date: {
              type: "string",
              description: "Preferred start date (YYYY-MM-DD format)"
            }
          },
          required: ["plants", "location"]
        }
      }
    ]
  end
  
  def self.permaculture_functions
    [
      {
        name: "design_plant_guild",
        description: "Design a permaculture plant guild around a central plant",
        parameters: {
          type: "object",
          properties: {
            central_plant: {
              type: "string",
              description: "The main plant around which to build the guild"
            },
            space_size: {
              type: "string",
              enum: ["small", "medium", "large"],
              description: "Available space for the guild"
            },
            primary_functions: {
              type: "array",
              items: { type: "string" },
              description: "Desired functions (e.g., 'nitrogen_fixing', 'pest_control', 'ground_cover', 'pollinator_support')"
            },
            climate_zone: {
              type: "string",
              description: "USDA hardiness zone"
            }
          },
          required: ["central_plant"]
        }
      },
      {
        name: "analyze_ecosystem_services",
        description: "Analyze the ecosystem services provided by a plant or plant combination",
        parameters: {
          type: "object",
          properties: {
            plants: {
              type: "array",
              items: { type: "string" },
              description: "List of plants to analyze"
            },
            service_types: {
              type: "array",
              items: { 
                type: "string",
                enum: ["carbon_sequestration", "soil_improvement", "water_management", "biodiversity_support", "pest_control"]
              },
              description: "Types of ecosystem services to focus on"
            }
          },
          required: ["plants"]
        }
      }
    ]
  end
  
  def self.all_functions
    plant_search_functions + plant_care_functions + permaculture_functions
  end
  
  # Function implementations for GPT to call
  def self.execute_function(function_name, arguments)
    case function_name
    when "search_plants_by_criteria"
      search_plants_by_criteria(arguments)
    when "get_plant_details"
      get_plant_details(arguments)
    when "find_companion_plants"
      find_companion_plants(arguments)
    when "recommend_plants_for_location"
      recommend_plants_for_location(arguments)
    when "get_seasonal_care_calendar"
      get_seasonal_care_calendar(arguments)
    when "diagnose_plant_problems"
      diagnose_plant_problems(arguments)
    when "create_planting_schedule"
      create_planting_schedule(arguments)
    when "design_plant_guild"
      design_plant_guild(arguments)
    when "analyze_ecosystem_services"
      analyze_ecosystem_services(arguments)
    else
      { error: "Unknown function: #{function_name}" }
    end
  end
  
  private
  
  def self.search_plants_by_criteria(args)
    search_service = EnhancedPlantSearchService.new
    
    # Build search criteria from arguments
    criteria = {}
    criteria[:zone_range] = args['zone_range'] if args['zone_range']
    criteria[:plant_type] = args['plant_type'] if args['plant_type']
    criteria[:sunlight] = args['sunlight'] if args['sunlight']
    criteria[:water_needs] = args['water_needs'] if args['water_needs']
    criteria[:uses] = args['uses'] if args['uses']
    criteria[:traits] = args['traits'] if args['traits']
    criteria[:soil_type] = args['soil_type'] if args['soil_type']
    criteria[:mature_size] = args['mature_size'] if args['mature_size']
    
    results = search_service.advanced_search(criteria)
    
    {
      plants_found: results.count,
      plants: results.limit(20).map do |plant|
        {
          common_name: plant.common_name,
          scientific_name: plant.scientific_name,
          description: plant.description_brief,
          zones: "#{plant.environmental_requirements&.zone_min}-#{plant.environmental_requirements&.zone_max}",
          uses: plant.plant_uses.joins(:use_category).pluck('use_categories.name').uniq
        }
      end
    }
  end
  
  def self.get_plant_details(args)
    plant = EnhancedPlant.find_by(common_name: args['plant_identifier']) ||
            EnhancedPlant.find_by(scientific_name: args['plant_identifier'])
    
    return { error: "Plant not found" } unless plant
    
    detail_type = args['detail_type'] || 'summary'
    
    if detail_type == 'all'
      contexts = PlantContext.generate_gpt_context(plant)
      { plant: plant.common_name, details: contexts }
    else
      context = PlantContext.send("generate_#{detail_type}_context", plant)
      { plant: plant.common_name, detail_type: detail_type, content: context }
    end
  end
  
  def self.find_companion_plants(args)
    plant = EnhancedPlant.find_by(common_name: args['primary_plant'])
    return { error: "Plant not found" } unless plant
    
    relationship_type = args['relationship_type'] || 'beneficial'
    
    companions = case relationship_type
                when 'beneficial'
                  plant.beneficial_companions
                when 'avoid'
                  plant.antagonistic_companions
                else
                  plant.beneficial_companions
                end
    
    {
      primary_plant: plant.common_name,
      relationship_type: relationship_type,
      companions: companions.limit(15).map do |companion|
        {
          name: companion.common_name,
          scientific_name: companion.scientific_name,
          description: companion.description_brief
        }
      end
    }
  end
  
  def self.recommend_plants_for_location(args)
    location = args['location'] || {}
    zone = location['zone']
    goals = args['garden_goals'] || []
    
    scope = EnhancedPlant.joins(:environmental_requirements)
    
    if zone
      zone_num = zone.to_i
      scope = scope.where(
        environmental_requirements: {
          zone_min: ..zone_num,
          zone_max: zone_num..
        }
      )
    end
    
    # Filter by goals/uses
    if goals.any?
      use_categories = UseCategory.where(name: goals)
      if use_categories.any?
        scope = scope.joins(:plant_uses).where(plant_uses: { use_category: use_categories })
      end
    end
    
    plants = scope.distinct.limit(20)
    
    {
      location: location,
      goals: goals,
      recommendations: plants.map do |plant|
        {
          name: plant.common_name,
          scientific_name: plant.scientific_name,
          description: plant.description_brief,
          why_recommended: "Suitable for zone #{zone}, meets goals: #{goals.join(', ')}"
        }
      end
    }
  end
  
  def self.get_seasonal_care_calendar(args)
    plants = args['plants'] || []
    location = args['location']
    season = args['season'] || 'all'
    
    plant_objects = EnhancedPlant.where(common_name: plants)
    
    calendar = {}
    
    plant_objects.each do |plant|
      calendar[plant.common_name] = {
        spring: "Plant preparation, soil amendment, early planting",
        summer: "Regular watering, pest monitoring, harvesting",
        fall: "Harvest completion, seed collection, winter prep",
        winter: "Dormancy period, planning for next year"
      }
    end
    
    if season != 'all'
      calendar = calendar.transform_values { |seasons| { season.to_sym => seasons[season.to_sym] } }
    end
    
    { plants: plants, location: location, season: season, calendar: calendar }
  end
  
  def self.diagnose_plant_problems(args)
    plant_name = args['plant_name']
    symptoms = args['symptoms'] || []
    
    # Simple diagnosis based on common symptoms
    diagnosis = {
      plant: plant_name,
      symptoms: symptoms,
      possible_causes: [],
      recommendations: []
    }
    
    symptoms.each do |symptom|
      case symptom.downcase
      when /yellow.*leaves/
        diagnosis[:possible_causes] << "Overwatering or nutrient deficiency"
        diagnosis[:recommendations] << "Check soil drainage and consider fertilizing"
      when /wilting/
        diagnosis[:possible_causes] << "Underwatering or root problems"
        diagnosis[:recommendations] << "Check soil moisture and root health"
      when /spots.*leaves/
        diagnosis[:possible_causes] << "Fungal or bacterial disease"
        diagnosis[:recommendations] << "Improve air circulation, consider fungicide"
      when /brown.*edges/
        diagnosis[:possible_causes] << "Fertilizer burn or low humidity"
        diagnosis[:recommendations] << "Reduce fertilizer, increase humidity"
      end
    end
    
    diagnosis
  end
  
  def self.create_planting_schedule(args)
    plants = args['plants'] || []
    location = args['location']
    start_date = args['start_date'] || Date.current.to_s
    
    # Simple scheduling based on plant types
    schedule = {}
    
    plants.each_with_index do |plant_name, index|
      plant = EnhancedPlant.find_by(common_name: plant_name)
      next unless plant
      
      # Stagger planting dates
      plant_date = Date.parse(start_date) + (index * 2).weeks
      
      schedule[plant_name] = {
        planting_date: plant_date.to_s,
        notes: "Plant in #{location}, ensure proper spacing and soil preparation"
      }
    end
    
    { location: location, start_date: start_date, schedule: schedule }
  end
  
  def self.design_plant_guild(args)
    central_plant_name = args['central_plant']
    central_plant = EnhancedPlant.find_by(common_name: central_plant_name)
    
    return { error: "Central plant not found" } unless central_plant
    
    # Find complementary plants
    companions = central_plant.beneficial_companions.limit(5)
    nitrogen_fixers = EnhancedPlant.joins(:semantic_tags)
                                  .where(semantic_tags: { name: 'nitrogen_fixing' })
                                  .limit(2)
    
    guild = {
      central_plant: central_plant_name,
      design: {
        canopy: central_plant.plant_type == 'tree' ? [central_plant_name] : [],
        understory: companions.where(plant_type: 'shrub').pluck(:common_name),
        ground_cover: companions.where(plant_type: 'ground_cover').pluck(:common_name),
        nitrogen_fixers: nitrogen_fixers.pluck(:common_name),
        support_plants: companions.where.not(plant_type: ['shrub', 'ground_cover']).pluck(:common_name)
      }
    }
    
    guild
  end
  
  def self.analyze_ecosystem_services(args)
    plants = args['plants'] || []
    service_types = args['service_types'] || []
    
    plant_objects = EnhancedPlant.where(common_name: plants)
    
    analysis = {
      plants_analyzed: plants,
      ecosystem_services: {}
    }
    
    service_types.each do |service|
      case service
      when 'carbon_sequestration'
        trees = plant_objects.where(plant_type: 'tree')
        analysis[:ecosystem_services][service] = {
          rating: trees.count > 0 ? 'High' : 'Low',
          plants_contributing: trees.pluck(:common_name)
        }
      when 'soil_improvement'
        nitrogen_fixers = plant_objects.joins(:semantic_tags)
                                     .where(semantic_tags: { name: 'nitrogen_fixing' })
        analysis[:ecosystem_services][service] = {
          rating: nitrogen_fixers.count > 0 ? 'High' : 'Medium',
          plants_contributing: nitrogen_fixers.pluck(:common_name)
        }
      when 'biodiversity_support'
        pollinator_plants = plant_objects.joins(:semantic_tags)
                                       .where(semantic_tags: { name: 'pollinator_friendly' })
        analysis[:ecosystem_services][service] = {
          rating: pollinator_plants.count > 0 ? 'High' : 'Medium',
          plants_contributing: pollinator_plants.pluck(:common_name)
        }
      end
    end
    
    analysis
  end
end 