# frozen_string_literal: true
class Region < ApplicationRecord
  has_many :plant_regional_data, dependent: :destroy
  has_many :enhanced_plants, through: :plant_regional_data

  validates :name, presence: true, length: { maximum: 255 }
  validates :country_code, length: { maximum: 3 }, allow_blank: true
  validates :climate_type, length: { maximum: 100 }, allow_blank: true
  validates :latitude_min, :latitude_max, numericality: { in: -90..90 }, allow_nil: true
  validates :longitude_min, :longitude_max, numericality: { in: -180..180 }, allow_nil: true

  scope :by_country, ->(country_code) { where(country_code: country_code) }
  scope :by_climate, ->(climate_type) { where(climate_type: climate_type) }
  scope :in_latitude_range, ->(lat_min, lat_max) { where(latitude_min: lat_min..lat_max) }

  def coordinate_bounds
    return nil unless latitude_min && latitude_max && longitude_min && longitude_max

    {
      north: latitude_max,
      south: latitude_min,
      east: longitude_max,
      west: longitude_min
    }
  end

  def temperature_range
    return nil unless avg_temp_min && avg_temp_max

    "#{avg_temp_min}°C to #{avg_temp_max}°C"
  end

  def growing_season_months
    return nil unless growing_season_days

    (growing_season_days / 30.0).round(1)
  end

  def climate_summary
    parts = []
    parts << climate_type if climate_type.present?
    parts << temperature_range if avg_temp_min && avg_temp_max
    parts << "#{avg_rainfall_mm}mm rainfall" if avg_rainfall_mm
    parts << "#{growing_season_months} month growing season" if growing_season_days

    parts.join(', ')
  end

  def suitable_plants(min_performance: 0.6)
    enhanced_plants.joins(:plant_regional_data)
                   .where(plant_regional_data: { performance_score: min_performance.. })
                   .where.not(plant_regional_data: { invasiveness_risk: ['high', 'severe'] })
  end
end