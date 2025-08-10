# frozen_string_literal: true
class EnhancedPlant < ApplicationRecord
  extend FriendlyId
  friendly_id :common_name, use: :slugged

  # Associations
  has_many :plant_names, dependent: :destroy
  has_many :plant_traits, dependent: :destroy
  has_one :environmental_requirements, dependent: :destroy
  has_many :plant_uses, dependent: :destroy
  has_many :use_categories, through: :plant_uses

  # Semantic tagging associations
  has_many :plant_semantic_tags, dependent: :destroy
  has_many :semantic_tags, through: :plant_semantic_tags

  # Plant relationships
  has_many :plant_relationships_as_a, class_name: 'PlantRelationship', foreign_key: 'plant_a_id', dependent: :destroy
  has_many :plant_relationships_as_b, class_name: 'PlantRelationship', foreign_key: 'plant_b_id', dependent: :destroy
  has_many :related_plants_a, through: :plant_relationships_as_a, source: :plant_b
  has_many :related_plants_b, through: :plant_relationships_as_b, source: :plant_a

  # Guild memberships
  has_many :guild_members, dependent: :destroy
  has_many :plant_guilds, through: :guild_members

  # Regional data
  has_many :plant_regional_data, class_name: 'PlantRegionalData', dependent: :destroy
  has_many :regions, through: :plant_regional_data

  # Pest relationships (commented out until models are created)
  # has_many :enhanced_plant_pest_relationships, dependent: :destroy
  # has_many :enhanced_pests_diseases, through: :enhanced_plant_pest_relationships

  # Validations
  validates :common_name, presence: true, uniqueness: { case_sensitive: false }
  validates :scientific_name, presence: true, uniqueness: { case_sensitive: false }
  validates :family, presence: true
  validates :growth_habit, presence: true
  validates :life_cycle, presence: true
  validates :data_quality_score, numericality: { greater_than_or_equal_to: 0, less_than_or_equal_to: 1 }, allow_nil: true
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
  scope :by_zone, ->(zone) { joins(:environmental_requirements).where('environmental_requirements.hardiness_zone @> ARRAY[?]::varchar[]', zone) }
  scope :by_soil_type, ->(soil_type) { joins(:environmental_requirements).where('environmental_requirements.soil_types @> ARRAY[?]::varchar[]', soil_type) }
  scope :by_function, ->(function) { joins(:plant_uses).where('plant_uses.use_type = ?', function) }
  scope :by_trait, ->(trait) { joins(:plant_traits).where('plant_traits.trait_type = ?', trait) }

  # Add database-level caching
  after_commit :clear_cache
  after_touch :clear_cache

  # Optimize database queries with materialized view
  def self.refresh_materialized_view
    connection.execute(<<-SQL)
      REFRESH MATERIALIZED VIEW CONCURRENTLY enhanced_plants_search;
    SQL
  end

  def self.search_by_text(query)
    return none unless query.present?

    # Use materialized view for faster text search
    from('enhanced_plants_search')
      .where("search_vector @@ plainto_tsquery('english', ?)", query)
      .order("ts_rank(search_vector, plainto_tsquery('english', ?)) DESC", query)
  end

  # Optimize batch existence check with a single query
  def self.batch_check_existence(plant_names)
    return [] if plant_names.empty?

    # Get existing plants in a single query
    existing_plants = where(
      'LOWER(common_name) = ANY(ARRAY[?]) OR LOWER(scientific_name) = ANY(ARRAY[?])',
      plant_names,
      plant_names
    ).pluck(:common_name, :scientific_name).flatten.map(&:downcase)

    # Return missing plants
    plant_names - existing_plants
  end

  # Optimize advanced search with better query performance
  def self.advanced_search(params)
    plants = all

    # Text search with optimized query
    if params[:query].present?
      search_terms = params[:query].downcase.split(/\W+/).reject(&:empty?)
      if search_terms.any?
        plants = plants.where(
          search_terms.map { |term| 
            "(LOWER(common_name) LIKE :term OR LOWER(scientific_name) LIKE :term)"
          }.join(' OR '),
          term: "%#{search_terms.join('%')}%"
        )
      end
    end

    # Function filters with eager loading and caching
    if params[:functions].present?
      cache_key = "plant_functions/#{params[:functions].sort.join(':')}"
      plants = Rails.cache.fetch(cache_key, expires_in: 1.hour) do
        plants.joins(:plant_uses)
              .joins(:use_categories)
              .where(use_categories: { name: params[:functions] })
              .distinct
      end
    end

    # Layer filters with caching
    if params[:layers].present?
      cache_key = "plant_layers/#{params[:layers].sort.join(':')}"
      plants = Rails.cache.fetch(cache_key, expires_in: 1.hour) do
        plants.where(plant_type: params[:layers])
      end
    end

    # Zone range with optimized query and caching
    if params[:min_zone].present? || params[:max_zone].present?
      cache_key = "plant_zones/#{params[:min_zone]}-#{params[:max_zone]}"
      plants = Rails.cache.fetch(cache_key, expires_in: 1.hour) do
        plants.joins(:environmental_requirements)
        plants = plants.where('environmental_requirements.hardiness_zone_min >= ?', params[:min_zone]) if params[:min_zone].present?
        plants = plants.where('environmental_requirements.hardiness_zone_max <= ?', params[:max_zone]) if params[:max_zone].present?
        plants
      end
    end

    # Eager load associations to prevent N+1 queries
    plants.includes(
      :environmental_requirements,
      :plant_uses,
      :plant_traits,
      :semantic_tags
    ).order(data_quality_score: :desc)
  end

  # Class methods for plant name extraction and validation
  class << self
    # Extract plant names from text with improved accuracy
    def extract_plant_names(text)
      return [] unless text.present?

      # Common words to exclude
      excluded_words = %w[the and or but in on at to for with by from about like]
      
      # Split text into words and filter
      words = text.downcase.split(/\W+/)
      words = words.reject { |w| excluded_words.include?(w) || w.length < 3 }
      
      # Find potential plant names
      potential_names = find_potential_plant_names(words)
      
      # Batch check existence
      batch_check_existence(potential_names)
    end

    # Find potential plant names from words
    def find_potential_plant_names(words)
      return [] if words.empty?

      # Get all plant names from cache
      plant_names = Rails.cache.fetch('all_plant_names', expires_in: 1.hour) do
        pluck(:common_name, :scientific_name).flatten.map(&:downcase)
      end

      # Find matches using fuzzy matching
      words.select do |word|
        plant_names.any? do |plant_name|
          plant_name.include?(word) || 
          word.include?(plant_name) ||
          levenshtein_distance(word, plant_name) <= 2
        end
      end
    end

    # Levenshtein distance for fuzzy matching
    def levenshtein_distance(a, b)
      return b.length if a.empty?
      return a.length if b.empty?

      matrix = Array.new(a.length + 1) { Array.new(b.length + 1) }

      (0..a.length).each { |i| matrix[i][0] = i }
      (0..b.length).each { |j| matrix[0][j] = j }

      (1..a.length).each do |i|
        (1..b.length).each do |j|
          cost = a[i - 1] == b[j - 1] ? 0 : 1
          matrix[i][j] = [
            matrix[i - 1][j] + 1,     # deletion
            matrix[i][j - 1] + 1,     # insertion
            matrix[i - 1][j - 1] + cost # substitution
          ].min
        end
      end

      matrix[a.length][b.length]
    end
  end

  # Instance methods
  def to_param
    common_name
  end

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

  # Semantic tag methods
  def add_semantic_tag(tag_name, confidence: 1.0, source: 'manual')
    tag = SemanticTag.find_or_create_by(name: tag_name.downcase) do |t|
      t.category = 'trait' # default category
    end

    plant_semantic_tags.find_or_create_by(semantic_tag: tag) do |pst|
      pst.confidence_score = confidence
      pst.source = source
    end
  end

  def remove_semantic_tag(tag_name)
    tag = SemanticTag.find_by(name: tag_name.downcase)
    return false unless tag

    plant_semantic_tags.where(semantic_tag: tag).destroy_all
    true
  end

  def has_semantic_tag?(tag_name, min_confidence: 0.5)
    semantic_tags.joins(:plant_semantic_tags)
                 .where(name: tag_name.downcase)
                 .where('plant_semantic_tags.confidence_score >= ?', min_confidence)
                 .exists?
  end

  def tags_by_category
    semantic_tags.group_by(&:category)
  end

  def high_confidence_tags(min_confidence: 0.7)
    semantic_tags.joins(:plant_semantic_tags)
                 .where('plant_semantic_tags.confidence_score >= ?', min_confidence)
  end

  def similar_plants_by_tags(limit: 10)
    tag_ids = semantic_tags.pluck(:id)
    return EnhancedPlant.none if tag_ids.empty?

    EnhancedPlant
      .joins(:plant_semantic_tags)
      .where(plant_semantic_tags: { semantic_tag_id: tag_ids })
      .where.not(id: id)
      .group('enhanced_plants.id')
      .order('COUNT(plant_semantic_tags.id) DESC')
      .limit(limit)
  end

  # Image handling
  def display_image
    return 'default_plant.jpg' if common_name.nil? || common_name.strip.empty?

    # Try multiple naming conventions in order of preference

    # 1. Try underscore format (bok_choy.jpg, black_ginger.jpg)
    image_name_underscore = common_name
      .downcase
      .gsub("'", '')        # Remove apostrophes
      .gsub(/[^a-z0-9\s]/, '') # Remove other special characters
      .strip
      .gsub(/\s+/, '_')    # Replace spaces with underscores

    image_path_underscore = "#{image_name_underscore}.jpg"

    if Rails.application.assets&.find_asset(image_path_underscore) ||
       File.exist?(Rails.root.join('app', 'assets', 'images', image_path_underscore))
      return image_path_underscore
    end

    # 2. Try no spaces/underscores format (beebalm.jpg, holybasil.jpg)
    image_name_nospace = common_name
      .downcase
      .gsub("'", '')        # Remove apostrophes
      .gsub(/[^a-z0-9\s]/, '') # Remove other special characters
      .strip
      .gsub(/\s+/, '')     # Remove all spaces

    image_path_nospace = "#{image_name_nospace}.jpg"

    if Rails.application.assets&.find_asset(image_path_nospace) ||
       File.exist?(Rails.root.join('app', 'assets', 'images', image_path_nospace))
      return image_path_nospace
    end

    # 3. Try hyphen format (original logic)
    image_name_hyphen = common_name.downcase.gsub(/\s+/, '-').gsub(/[^a-z0-9\-]/, '')
    image_path_hyphen = "#{image_name_hyphen}.jpg"

    if Rails.application.assets&.find_asset(image_path_hyphen) ||
       File.exist?(Rails.root.join('app', 'assets', 'images', image_path_hyphen))
      return image_path_hyphen
    end

    # Final fallback to default image
    'default_plant.jpg'
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

  def self.auto_seed_from_stub(stub)
    return nil unless stub.is_a?(PlantStub)

    # Try to find existing plant first
    existing = find_by(common_name: stub.common_name) || 
               find_by(scientific_name: stub.scientific_name)
    return existing if existing

    # Create new plant with basic data
    plant = new(
      common_name: stub.common_name,
      scientific_name: stub.scientific_name,
      family: stub.family,
      habitat: stub.habitat,
      medicinal_uses: stub.medicinal_uses,
      propagation_methods: stub.propagation_methods,
      environmental_requirements: stub.environmental_requirements,
      status: 'auto_seeded',
      needs_verification: true
    )

    # Try to fetch additional data from external sources
    begin
      # Fetch from USDA Plants Database
      usda_data = fetch_usda_data(stub.scientific_name)
      if usda_data
        plant.update(
          family: usda_data[:family] || plant.family,
          habitat: usda_data[:habitat] || plant.habitat,
          environmental_requirements: plant.environmental_requirements.merge(usda_data[:requirements] || {})
        )
      end

      # Fetch from Permaculture Plants Database
      permaculture_data = fetch_permaculture_data(stub.common_name)
      if permaculture_data
        plant.update(
          medicinal_uses: (plant.medicinal_uses + permaculture_data[:medicinal_uses]).uniq,
          propagation_methods: (plant.propagation_methods + permaculture_data[:propagation_methods]).uniq,
          environmental_requirements: plant.environmental_requirements.merge(permaculture_data[:requirements] || {})
        )
      end

      # Fetch from Herbal Medicine Database
      herbal_data = fetch_herbal_data(stub.common_name)
      if herbal_data
        plant.update(
          medicinal_uses: (plant.medicinal_uses + herbal_data[:medicinal_uses]).uniq,
          environmental_requirements: plant.environmental_requirements.merge(herbal_data[:requirements] || {})
        )
      end
    rescue => e
      Rails.logger.error "Error fetching additional data for #{stub.common_name}: #{e.message}"
    end

    # Save the plant
    plant.save
    plant
  end

  private

  def self.fetch_usda_data(scientific_name)
    return nil unless scientific_name

    # TODO: Implement USDA Plants Database API call
    # This would fetch basic plant information, family, and environmental requirements
    nil
  end

  def self.fetch_permaculture_data(common_name)
    return nil unless common_name

    # TODO: Implement Permaculture Plants Database API call
    # This would fetch permaculture-specific information like companion planting and uses
    nil
  end

  def self.fetch_herbal_data(common_name)
    return nil unless common_name

    # TODO: Implement Herbal Medicine Database API call
    # This would fetch medicinal uses and growing requirements
    nil
  end

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

  def clear_cache
    Rails.cache.delete_matched("plant_existence/*")
    Rails.cache.delete_matched("plant_functions/*")
    Rails.cache.delete_matched("plant_layers/*")
    Rails.cache.delete_matched("plant_zones/*")
    Rails.cache.delete([self, 'full_description'])
    Rails.cache.delete('all_plant_names')
  end
end