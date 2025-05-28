class Plant < ApplicationRecord
  # === Active Storage ===
  has_one_attached :image

  # === Associations ===
  has_many :plant_pests, dependent: :destroy
  has_many :pests, through: :plant_pests

  # === Validations ===
  validates :common_name, presence: true, uniqueness: { case_sensitive: false }
  validates :scientific_name, :zone_range, :layers, :plant_functions, :purpose, presence: true
  validates :description, length: { maximum: 65_535 }, allow_blank: true
  validates :purpose, length: { maximum: 65_535 }
  validates :perennial, inclusion: { in: [true, false] }
  validates :layers, presence: true, allow_blank: true
  validates :plant_functions, presence: true, allow_blank: true

  # === Scopes ===
  scope :filter_by_plant_function, ->(functions) { 
    where("plant_functions @> ARRAY[?]::text[]", functions) 
  }

  scope :filter_by_layers, ->(layers) { 
    where("layers @> ARRAY[?]::text[]", layers) 
  }

  scope :filter_by_zones, ->(search_zones) {
    where(
      search_zones.map { |_| "(CAST(substring(zone FROM '^(\\d+)') AS INT) <= ? AND CAST(substring(zone FROM '-(\\d+)$') AS INT) >= ?)" }
      .join(" OR "),
      *search_zones.flat_map { |z| [z.to_i, z.to_i] }
    )
  }

  scope :search_by_name, ->(query) {
    sanitized = sanitize_sql_like(query.downcase)
    where("LOWER(common_name) LIKE ? OR LOWER(scientific_name) LIKE ?", 
          "%#{sanitized}%", "%#{sanitized}%")
  }

  # === Instance Methods ===
  def to_param
    common_name.parameterize
  end

  def parsed_array(field)
    Array.wrap(field).map(&:strip)
  end

  def layers_array
    parsed_array(layers)
  end

  def functions_array
    parsed_array(plant_functions)
  end

  def valid_pests
    pests.distinct
  end

  def self.f_to_c(f)
    return nil if f.nil?
    f = f.to_f
    ((f - 32) * 5.0 / 9.0).round(1)
  end

  def ideal_temp_range
    return "Temperature range not specified" if ideal_temp_min.nil? || ideal_temp_max.nil?
    "#{ideal_temp_min}°F – #{ideal_temp_max}°F (#{self.class.f_to_c(ideal_temp_min)}°C – #{self.class.f_to_c(ideal_temp_max)}°C)"
  end

  def temperature_extremes
    return "Temperature extremes not specified" if min_temp.nil? || max_temp.nil?
    "❄️ #{min_temp}°F (#{self.class.f_to_c(min_temp)}°C) – 🔥 #{max_temp}°F (#{self.class.f_to_c(max_temp)}°C)"
  end

  # === Image Methods ===
  def image_filename
    return "default_plant.jpg" if common_name.blank?
    
    filename = common_name
      .downcase
      .gsub("'", "")        # Remove apostrophes
      .gsub(/[^a-z0-9\s]/, "") # Remove other special characters
      .strip
      .gsub(/\s+/, '_')    # Replace spaces with underscores

    return "default_plant.jpg" if filename.blank?
    "#{filename}.jpg"
  end

  def image_exists?
    Rails.application.assets&.find_asset(image_filename).present?
  end

  def display_image
    image_exists? ? image_filename : "default_plant.jpg"
  end

  def image_path
    image_name = common_name.downcase.gsub(/[^a-z0-9]+/, '_')
    if File.exist?(Rails.root.join('app', 'assets', 'images', "#{image_name}.jpg"))
      "#{image_name}.jpg"
    else
      "default_plant.jpg"
    end
  end

  # === Class Methods ===
  def self.find_by_common_name(parameterized_name)
    where("LOWER(common_name) = ?", parameterized_name.tr('-', ' ').downcase).first
  end

  def self.advanced_search(params)
    results = all
    
    results = results.search_by_name(params[:query]) if params[:query].present?
    results = results.filter_by_plant_function(params[:functions]) if params[:functions].present?
    results = results.filter_by_layers(params[:layers]) if params[:layers].present?
    results = results.filter_by_zones(params[:zones]) if params[:zones].present?
    
    results
  end
  
  # Handle zone range
  def zone_range=(value)
    if value.is_a?(String)
      start_zone, end_zone = value.split('-').map(&:to_i)
      super(start_zone..end_zone)
    else
      super
    end
  end

  # Scopes for quick filters
  scope :edible, -> { where("plant_functions @> ARRAY[?]::varchar[]", "Edible") }
  scope :medicinal, -> { where("plant_functions @> ARRAY[?]::varchar[]", "Medicinal") }
  scope :nitrogen_fixers, -> { where("plant_functions @> ARRAY[?]::varchar[]", "Nitrogen Fixer") }
  scope :groundcover, -> { where("plant_functions @> ARRAY[?]::varchar[]", "Ground Cover") }
end
