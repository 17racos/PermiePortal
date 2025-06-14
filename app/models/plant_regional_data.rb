# frozen_string_literal: true
class PlantRegionalData < ApplicationRecord
  belongs_to :enhanced_plant
  belongs_to :region

  validates :performance_score, inclusion: { in: 0.0..1.0 }, allow_nil: true
  validates :invasiveness_risk, inclusion: { in: %w[none low moderate high severe] }, allow_nil: true
  validates :legal_status, inclusion: { in: %w[unrestricted restricted prohibited permit_required] }, allow_nil: true

  enum invasiveness_risk: {
    none: 'none',
    low: 'low',
    moderate: 'moderate',
    high: 'high',
    severe: 'severe'
  }, _prefix: :invasiveness

  enum legal_status: {
    unrestricted: 'unrestricted',
    restricted: 'restricted',
    prohibited: 'prohibited',
    permit_required: 'permit_required'
  }, _prefix: :status

  scope :high_performance, -> { where('performance_score > ?', 0.7) }
  scope :low_invasiveness, -> { where(invasiveness_risk: ['none', 'low']) }
  scope :legal_to_plant, -> { where(legal_status: ['unrestricted', 'permit_required']) }

  def performance_level
    return 'Unknown' unless performance_score

    case performance_score
    when 0.0..0.3
      'Poor'
    when 0.3..0.6
      'Fair'
    when 0.6..0.8
      'Good'
    when 0.8..1.0
      'Excellent'
    end
  end

  def invasiveness_level
    case invasiveness_risk
    when 'none', 'low'
      'Safe'
    when 'moderate'
      'Caution'
    when 'high', 'severe'
      'Avoid'
    else
      'Unknown'
    end
  end

  def recommended_for_region?
    performance_score.to_f >= 0.6 &&
    (invasiveness_none? || invasiveness_low?) &&
    (status_unrestricted? || status_permit_required?)
  end
end