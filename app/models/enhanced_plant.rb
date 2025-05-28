class EnhancedPlant < ApplicationRecord
  extend FriendlyId
  friendly_id :common_name, use: :slugged

  # Associations
  has_many :plant_names, dependent: :destroy
  has_many :plant_traits, dependent: :destroy
  has_one :environmental_requirements, dependent: :destroy
  has_many :plant_uses, dependent: :destroy
  has_many :use_categories, through: :plant_uses
  
  # Plant relationships
  has_many :plant_relationships_as_a, class_name: 'PlantRelationship', foreign_key: 'plant_a_id', dependent: :destroy
  has_many :plant_relationships_as_b, class_name: 'PlantRelationship', foreign_key: 'plant_b_id', dependent: :destroy
  has_many :related_plants_a, through: :plant_relationships_as_a, source: :plant_b
  has_many :related_plants_b, through: :plant_relationships_as_b, source: :plant_a
  
  # Guild memberships
  has_many :guild_members, dependent: :destroy
  has_many :plant_guilds, through: :guild_members
  
  # Regional data
  has_many :plant_regional_data, dependent: :destroy
  has_many :regions, through: :plant_regional_data
  
  # Pest relationships
  has_many :enhanced_plant_pest_relationships, dependent: :destroy
  has_many :enhanced_pests_diseases, through: :enhanced_plant_pest_relationships
  
  # Validations
  validates :common_name, presence: true, length: { maximum: 255 }
  validates :scientific_name, presence: true, uniqueness: true, length: { maximum: 255 }
  validates :family, length: { maximum: 100 }
  validates :genus, length: { maximum: 100 }
  validates :species, length: { maximum: 100 }
  validates :data_quality_score, inclusion: { in: 0.0..1.0 }
  validates :mature_height_min_cm, :mature_height_max_cm, 
            :mature_width_min_cm, :mature_width_max_cm, 
            numericality: { greater_than: 0 }, allow_nil: true

  # Enums
  enum plant_type: {
    tree: 'tree',
    shrub: 'shrub', 
    herbaceous: 'herbaceous',
    vine: 'vine',
    grass: 'grass',
    fern: 'fern',
    moss: 'moss',
    aquatic: 'aquatic'
  }

  enum life_cycle: {
    annual: 'annual',
    biennial: 'biennial',
    perennial: 'perennial',
    short_lived_perennial: 'short_lived_perennial'
  }

  # Scopes
  scope :by_family, ->(family) { where(family: family) }
  scope :by_plant_type, ->(type) { where(plant_type: type) }
  scope :by_life_cycle, ->(cycle) { where(life_cycle: cycle) }
  scope :with_high_quality, -> { where('data_quality_score > ?', 0.7) }
  scope :search_by_text, ->(query) { where("search_vector @@ plainto_tsquery('english', ?)", query) }

  # Instance methods
  def all_names
    ([common_name] + plant_names.pluck(:name)).uniq
  end

  def beneficial_companions
    related_plants_with_relationship_type('beneficial_companion')
  end

  def antagonistic_plants
    related_plants_with_relationship_type('antagonistic')
  end

  def all_relationships
    PlantRelationship.where('plant_a_id = ? OR plant_b_id = ?', id, id)
  end

  def traits_by_category(category_name)
    plant_traits.joins(:trait_category)
                .where(trait_categories: { name: category_name })
  end

  def get_trait_value(category_name)
    trait = traits_by_category(category_name).first
    return nil unless trait

    case trait.trait_category.data_type
    when 'numeric'
      trait.numeric_value || [trait.numeric_min, trait.numeric_max].compact
    when 'categorical'
      trait.categorical_value
    when 'boolean'
      trait.boolean_value
    when 'text'
      trait.text_value
    end
  end

  def hardiness_zones
    return nil unless environmental_requirements
    
    min_zone = environmental_requirements.hardiness_zone_min
    max_zone = environmental_requirements.hardiness_zone_max
    
    return nil unless min_zone && max_zone
    
    min_zone == max_zone ? min_zone.to_s : "#{min_zone}-#{max_zone}"
  end

  def drought_tolerance
    environmental_requirements&.drought_tolerance_score
  end

  def light_needs
    environmental_requirements&.light_requirement
  end

  def primary_uses
    plant_uses.joins(:use_category)
              .where('plant_uses.effectiveness_score > ?', 0.7)
              .pluck('use_categories.name')
  end

  def regional_performance(region_name)
    plant_regional_data.joins(:region)
                      .find_by(regions: { name: region_name })
                      &.performance_score
  end

  def is_invasive_in?(region_name)
    regional_data = plant_regional_data.joins(:region)
                                      .find_by(regions: { name: region_name })
    return false unless regional_data
    
    %w[moderate high severe].include?(regional_data.invasiveness_risk)
  end

  def companion_suggestions(limit: 5)
    beneficial_companions.joins(:environmental_requirements)
                        .where(environmental_requirements: {
                          hardiness_zone_min: environmental_requirements&.hardiness_zone_min&.-(2)..environmental_requirements&.hardiness_zone_max&.+(2),
                          light_requirement: environmental_requirements&.light_requirement
                        })
                        .limit(limit)
  end

  # Image handling
  def display_image
    # Try to find an image based on common name (lowercase, with hyphens)
    image_name = common_name.downcase.gsub(/\s+/, '-').gsub(/[^a-z0-9\-]/, '')
    image_path = "#{image_name}.jpg"
    
    # Check if the image exists in assets
    if Rails.application.assets&.find_asset(image_path) || 
       File.exist?(Rails.root.join('app', 'assets', 'images', image_path))
      image_path
    else
      # Fallback to a default plant image or nil
      'default-plant.jpg' if Rails.application.assets&.find_asset('default-plant.jpg')
    end
  end

  def has_image?
    display_image.present?
  end

  # Class methods
  def self.search_similar_by_embedding(embedding_vector, threshold: 0.7, limit: 10)
    # Commented out until vector extension is available
    # return none unless embedding_vector

    # connection.execute(
    #   "SELECT * FROM find_similar_enhanced_plants('#{embedding_vector}', #{threshold}, #{limit})"
    # ).map { |row| find(row['plant_id']) }
    
    # For now, return empty result
    none
  end

  def self.search_by_traits(trait_filters)
    plants = includes(:plant_traits, :trait_categories)
    
    trait_filters.each do |category_name, criteria|
      plants = plants.where(
        plant_traits: { trait_categories: { name: category_name } }
      )
      
      case criteria
      when Hash
        if criteria[:min]
          plants = plants.where('plant_traits.numeric_value >= ?', criteria[:min])
        end
        if criteria[:max]
          plants = plants.where('plant_traits.numeric_value <= ?', criteria[:max])
        end
      when Array
        plants = plants.where(plant_traits: { categorical_value: criteria })
      when String
        plants = plants.where(plant_traits: { categorical_value: criteria })
      end
    end
    
    plants.distinct
  end

  def self.search_by_environmental_conditions(conditions)
    plants = joins(:environmental_requirements)
    
    conditions.each do |condition, value|
      case condition.to_s
      when 'drought_tolerant'
        plants = plants.where('environmental_requirements.drought_tolerance_score > ?', 0.6) if value
      when 'shade_tolerant'
        plants = plants.where(environmental_requirements: { light_requirement: ['full_shade', 'partial_shade'] }) if value
      when 'zone'
        plants = plants.where(
          'environmental_requirements.hardiness_zone_min <= ? AND environmental_requirements.hardiness_zone_max >= ?',
          value, value
        )
      when 'max_height'
        plants = plants.where('enhanced_plants.mature_height_max_cm <= ?', value)
      end
    end
    
    plants
  end

  def self.for_region(region_name)
    joins(plant_regional_data: :region)
      .where(regions: { name: region_name })
      .where('plant_regional_data.performance_score > ?', 0.6)
      .where.not(plant_regional_data: { invasiveness_risk: ['high', 'severe'] })
  end

  def self.with_use(use_category_name)
    joins(plant_uses: :use_category)
      .where(use_categories: { name: use_category_name })
      .where('plant_uses.effectiveness_score > ?', 0.5)
  end

  private

  def related_plants_with_relationship_type(type_name)
    relationship_type = RelationshipType.find_by(name: type_name)
    return EnhancedPlant.none unless relationship_type

    related_a = EnhancedPlant.joins(:plant_relationships_as_b)
                            .where(plant_relationships: { 
                              plant_a_id: id, 
                              relationship_type: relationship_type 
                            })
    
    related_b = EnhancedPlant.joins(:plant_relationships_as_a)
                            .where(plant_relationships: { 
                              plant_b_id: id, 
                              relationship_type: relationship_type 
                            })
    
    EnhancedPlant.where(id: (related_a.pluck(:id) + related_b.pluck(:id)).uniq)
  end
end 