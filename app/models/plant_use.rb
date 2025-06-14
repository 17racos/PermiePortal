# frozen_string_literal: true
class PlantUse < ApplicationRecord
  belongs_to :enhanced_plant
  belongs_to :use_category

  validates :effectiveness_score, inclusion: { in: 0.0..1.0 }
  validates :confidence_score, inclusion: { in: 0.0..1.0 }
  validates :enhanced_plant_id, uniqueness: { scope: :use_category_id }

  scope :high_effectiveness, -> { where('effectiveness_score > ?', 0.7) }
  scope :high_confidence, -> { where('confidence_score > ?', 0.7) }
  scope :reliable, -> { high_effectiveness.high_confidence }

  def effectiveness_level
    case effectiveness_score
    when 0.0..0.3
      'Low'
    when 0.3..0.6
      'Moderate'
    when 0.6..0.8
      'High'
    when 0.8..1.0
      'Very High'
    else
      'Unknown'
    end
  end

  def confidence_level
    case confidence_score
    when 0.0..0.3
      'Low'
    when 0.3..0.6
      'Moderate'
    when 0.6..0.8
      'High'
    when 0.8..1.0
      'Very High'
    else
      'Unknown'
    end
  end

  def display_description
    parts = []
    parts << use_category.name
    parts << "(#{effectiveness_level} effectiveness" if effectiveness_score
    parts << "#{confidence_level} confidence)" if confidence_score
    parts << "- #{notes}" if notes.present?
    parts.join(' ')
  end

  def reliable?
    effectiveness_score >= 0.6 && confidence_score >= 0.6
  end
end