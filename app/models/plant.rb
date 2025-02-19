class Plant < ApplicationRecord
  # === Associations ===
  has_many :plant_pests, dependent: :destroy
  has_many :pests, through: :plant_pests

  # === Validations ===
  validates :common_name, presence: true, uniqueness: { case_sensitive: false }
  validates :scientific_name, :zone, :layers, :plant_function, :purpose, presence: true
  validates :description, length: { maximum: 65_535 }, allow_blank: true
  validates :purpose, length: { maximum: 65_535 }
  validates :perennial, inclusion: { in: [true, false] }
  validates :zone, presence: true
  validates :layers, presence: true, allow_blank: true
  validates :plant_function, presence: true, allow_blank: true

  # === Scopes ===
  before_save :set_zone_range

  scope :filter_by_plant_function, ->(functions) { 
    where("plant_function @> ARRAY[?]::text[]", functions) 
  }

  scope :filter_by_layers, ->(layers) { 
    where("layers @> ARRAY[?]::text[]", layers) 
  }

  scope :filter_by_zones, ->(search_zones) {
    where(
      search_zones.map { |_| "(zone_min <= ? AND zone_max >= ?)" }
      .join(" OR "),
      *search_zones.flat_map { |z| [z, z] }
    )
  }

  # === Instance Methods ===

  # Generate a URL-friendly parameter using common_name
  def to_param
    common_name.parameterize
  end

  # Parse a given field into an array
  def parsed_array(field)
    Array.wrap(field).map(&:strip)
  end

  # Parsed layers array
  def layers_array
    parsed_array(layers)
  end

  # Parsed plant functions array
  def functions_array
    parsed_array(plant_function)
  end

  # Retrieve valid associated pests
  def valid_pests
    pests.distinct
  end

  # Convert Fahrenheit to Celsius
  def self.f_to_c(f)
    ((f - 32) * 5.0 / 9.0).round(1)
  end

  # Display Ideal Temp Range in Both Fahrenheit & Celsius
  def ideal_temp_range
    "#{ideal_temp_min}°F – #{ideal_temp_max}°F (#{self.class.f_to_c(ideal_temp_min)}°C – #{self.class.f_to_c(ideal_temp_max)}°C)"
  end

  # Display Min & Max Temperature Tolerance in Both Units
  def temperature_extremes
    "❄️ #{min_temp}°F (#{self.class.f_to_c(min_temp)}°C) – 🔥 #{max_temp}°F (#{self.class.f_to_c(max_temp)}°C)"
  end

  # === Class Methods ===

  # Find a plant by its parameterized common_name
  def self.find_by_common_name(parameterized_name)
    where("LOWER(common_name) = ?", parameterized_name.tr('-', ' ').downcase).first
  end

  private

  # Extracts min/max values from "x-y" string
  def set_zone_range
    if zone.present? && zone.match(/^(\d+)-(\d+)$/)
      self.zone_min = $1.to_i
      self.zone_max = $2.to_i
    end
  end
end
