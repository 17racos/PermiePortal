# frozen_string_literal: true
class EnvironmentalRequirements < ApplicationRecord
  belongs_to :enhanced_plant

  validates :hardiness_zone_min, :hardiness_zone_max,
            numericality: { in: 1..13 }, allow_nil: true
  validates :heat_zone_min, :heat_zone_max,
            numericality: { in: 1..12 }, allow_nil: true
  validates :drought_tolerance_score, :flood_tolerance_score,
            inclusion: { in: 0.0..1.0 }, allow_nil: true
  validates :soil_ph_min, :soil_ph_max,
            numericality: { in: 0.0..14.0 }, allow_nil: true

  enum soil_drainage: {
    poor: 'poor',
    moderate: 'moderate',
    good: 'good',
    excellent: 'excellent'
  }, _prefix: :drainage

  enum soil_fertility: {
    poor: 'poor',
    moderate: 'moderate',
    rich: 'rich',
    very_rich: 'very_rich'
  }, _prefix: :fertility

  enum light_requirement: {
    full_shade: 'full_shade',
    partial_shade: 'partial_shade',
    partial_sun: 'partial_sun',
    full_sun: 'full_sun'
  }

  scope :for_zone, ->(zone) { where('hardiness_zone_min <= ? AND hardiness_zone_max >= ?', zone, zone) }
  scope :drought_tolerant, -> { where('drought_tolerance_score > ?', 0.6) }
  scope :shade_tolerant, -> { where(light_requirement: ['full_shade', 'partial_shade']) }
  scope :sun_loving, -> { where(light_requirement: ['full_sun', 'partial_sun']) }

  def zone_range
    return nil unless hardiness_zone_min && hardiness_zone_max

    if hardiness_zone_min == hardiness_zone_max
      hardiness_zone_min.to_s
    else
      "#{hardiness_zone_min}-#{hardiness_zone_max}"
    end
  end

  def heat_zone_range
    return nil unless heat_zone_min && heat_zone_max

    if heat_zone_min == heat_zone_max
      heat_zone_min.to_s
    else
      "#{heat_zone_min}-#{heat_zone_max}"
    end
  end

  def ph_range
    return nil unless soil_ph_min && soil_ph_max

    if soil_ph_min == soil_ph_max
      soil_ph_min.to_s
    else
      "#{soil_ph_min}-#{soil_ph_max}"
    end
  end

  def temperature_range_celsius
    return nil unless temp_optimal_min && temp_optimal_max

    "#{temp_optimal_min}°C - #{temp_optimal_max}°C"
  end

  def temperature_range_fahrenheit
    return nil unless temp_optimal_min && temp_optimal_max

    min_f = (temp_optimal_min * 9/5) + 32
    max_f = (temp_optimal_max * 9/5) + 32
    "#{min_f.round}°F - #{max_f.round}°F"
  end

  def rainfall_range_inches
    return nil unless annual_rainfall_min_mm && annual_rainfall_max_mm

    min_inches = (annual_rainfall_min_mm / 25.4).round(1)
    max_inches = (annual_rainfall_max_mm / 25.4).round(1)
    "#{min_inches}\" - #{max_inches}\""
  end

  def is_suitable_for_zone?(zone)
    return false unless hardiness_zone_min && hardiness_zone_max

    zone >= hardiness_zone_min && zone <= hardiness_zone_max
  end

  def drought_tolerance_level
    return 'Unknown' unless drought_tolerance_score

    case drought_tolerance_score
    when 0.0..0.3
      'Low'
    when 0.3..0.6
      'Moderate'
    when 0.6..0.8
      'High'
    when 0.8..1.0
      'Very High'
    end
  end

  def light_needs_description
    case light_requirement
    when 'full_shade'
      'Thrives in full shade (less than 3 hours direct sun)'
    when 'partial_shade'
      'Prefers partial shade (3-6 hours direct sun)'
    when 'partial_sun'
      'Needs partial sun (4-6 hours direct sun)'
    when 'full_sun'
      'Requires full sun (6+ hours direct sun)'
    end
  end

  def soil_preferences
    preferences = []
    preferences << "pH #{ph_range}" if ph_range
    preferences << "#{soil_drainage} drainage" if soil_drainage
    preferences << "#{soil_fertility} fertility" if soil_fertility
    preferences.join(', ')
  end

  def climate_summary
    summary = []
    summary << "Zones #{zone_range}" if zone_range
    summary << temperature_range_celsius if temperature_range_celsius
    summary << "#{drought_tolerance_level} drought tolerance" if drought_tolerance_score
    summary << light_needs_description if light_requirement
    summary.join(' • ')
  end
end