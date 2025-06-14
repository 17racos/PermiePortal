# frozen_string_literal: true
class PlantGuild < ApplicationRecord
  has_many :guild_members, dependent: :destroy
  has_many :enhanced_plants, through: :guild_members

  validates :name, presence: true, length: { maximum: 255 }
  validates :guild_purpose, presence: true

  scope :for_climate, ->(climate) { where('climate_suitability @> ?', [climate].to_json) }
  scope :by_purpose, ->(purpose) { where('guild_purpose ILIKE ?', "%#{purpose}%") }

  def member_count
    guild_members.count
  end

  def primary_plants
    guild_members.where(role: 'primary').includes(:enhanced_plant).map(&:enhanced_plant)
  end

  def support_plants
    guild_members.where(role: 'support').includes(:enhanced_plant).map(&:enhanced_plant)
  end

  def ground_cover_plants
    guild_members.where(role: 'ground_cover').includes(:enhanced_plant).map(&:enhanced_plant)
  end

  def nitrogen_fixers
    guild_members.joins(:enhanced_plant)
                 .joins('JOIN plant_uses ON plant_uses.enhanced_plant_id = enhanced_plants.id')
                 .joins('JOIN use_categories ON use_categories.id = plant_uses.use_category_id')
                 .where(use_categories: { name: 'nitrogen_fixation' })
                 .includes(:enhanced_plant)
                 .map(&:enhanced_plant)
                 .uniq
  end

  def suitable_for_climate?(climate_zone)
    return true if climate_suitability.blank?

    climate_suitability.include?(climate_zone.to_s)
  end

  def estimated_space_requirement
    # Calculate based on mature sizes of member plants
    total_area = 0

    enhanced_plants.each do |plant|
      width = plant.mature_width_max_cm || 100 # Default 1m if unknown
      area = (width / 100.0) ** 2 # Convert to square meters
      total_area += area
    end

    # Add 20% buffer for spacing
    (total_area * 1.2).round(1)
  end

  def compatibility_score
    # Calculate average compatibility between all plant pairs
    relationships = []

    enhanced_plants.each do |plant_a|
      enhanced_plants.each do |plant_b|
        next if plant_a == plant_b

        relationship = PlantRelationship.find_by(plant_a: plant_a, plant_b: plant_b)
        if relationship
          score = relationship.beneficial? ? relationship.strength_score : -relationship.strength_score
          relationships << score
        end
      end
    end

    return 0.5 if relationships.empty? # Neutral if no data

    relationships.sum / relationships.count
  end

  def layer_distribution
    layers = {}

    guild_members.includes(:enhanced_plant).each do |member|
      plant = member.enhanced_plant
      height = plant.mature_height_max_cm || 0

      layer = case height
              when 0..50
                'ground_cover'
              when 51..200
                'herbaceous'
              when 201..800
                'shrub'
              when 801..3000
                'understory'
              else
                'canopy'
              end

      layers[layer] ||= 0
      layers[layer] += 1
    end

    layers
  end

  def planting_sequence
    # Return plants in order they should be planted
    sequence = []

    # 1. Trees and large shrubs first
    sequence += guild_members.joins(:enhanced_plant)
                            .where('enhanced_plants.mature_height_max_cm > ?', 200)
                            .order('enhanced_plants.mature_height_max_cm DESC')

    # 2. Nitrogen fixers
    sequence += guild_members.joins(:enhanced_plant)
                            .joins('JOIN plant_uses ON plant_uses.enhanced_plant_id = enhanced_plants.id')
                            .joins('JOIN use_categories ON use_categories.id = plant_uses.use_category_id')
                            .where(use_categories: { name: 'nitrogen_fixation' })
                            .where.not(id: sequence.map(&:id))

    # 3. Other support plants
    sequence += guild_members.where(role: 'support')
                            .where.not(id: sequence.map(&:id))

    # 4. Ground cover last
    sequence += guild_members.where(role: 'ground_cover')
                            .where.not(id: sequence.map(&:id))

    # 5. Any remaining plants
    sequence += guild_members.where.not(id: sequence.map(&:id))

    sequence.map(&:enhanced_plant)
  end

  def maintenance_requirements
    requirements = {
      watering: 'moderate',
      pruning: 'seasonal',
      fertilizing: 'minimal',
      pest_management: 'integrated'
    }

    # Adjust based on plant needs
    if enhanced_plants.joins(:environmental_requirements)
                     .where('environmental_requirements.drought_tolerance_score < ?', 0.4)
                     .any?
      requirements[:watering] = 'regular'
    end

    if enhanced_plants.where(plant_type: ['tree', 'shrub']).count > member_count / 2
      requirements[:pruning] = 'regular'
    end

    requirements
  end
end