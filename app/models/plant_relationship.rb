# frozen_string_literal: true
class PlantRelationship < ApplicationRecord
  belongs_to :plant_a, class_name: 'EnhancedPlant'
  belongs_to :plant_b, class_name: 'EnhancedPlant'
  belongs_to :relationship_type

  validates :strength_score, inclusion: { in: 0.0..1.0 }, allow_nil: true
  validates :confidence_score, inclusion: { in: 0.0..1.0 }
  validates :plant_a_id, uniqueness: { scope: [:plant_b_id, :relationship_type_id] }
  validate :plants_must_be_different

  scope :beneficial, -> { joins(:relationship_type).where(relationship_types: { is_beneficial: true }) }
  scope :antagonistic, -> { joins(:relationship_type).where(relationship_types: { is_beneficial: false }) }
  scope :high_confidence, -> { where('confidence_score > ?', 0.7) }
  scope :strong, -> { where('strength_score > ?', 0.7) }

  def beneficial?
    relationship_type.beneficial?
  end

  def antagonistic?
    relationship_type.antagonistic?
  end

  def neutral?
    relationship_type.neutral?
  end

  def strength_level
    return 'Unknown' unless strength_score

    case strength_score
    when 0.0..0.3
      'Weak'
    when 0.3..0.6
      'Moderate'
    when 0.6..0.8
      'Strong'
    when 0.8..1.0
      'Very Strong'
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
    parts << relationship_type.name
    parts << "(#{strength_level} strength)" if strength_score
    parts << "(#{confidence_level} confidence)"
    parts << "- #{notes}" if notes.present?
    parts.join(' ')
  end

  def reliable?
    confidence_score >= 0.6
  end

  def reciprocal_relationship
    PlantRelationship.find_by(
      plant_a: plant_b,
      plant_b: plant_a,
      relationship_type: relationship_type
    )
  end

  def create_reciprocal!
    return if reciprocal_relationship.present?

    PlantRelationship.create!(
      plant_a: plant_b,
      plant_b: plant_a,
      relationship_type: relationship_type,
      strength_score: strength_score,
      confidence_score: confidence_score,
      evidence_type: evidence_type,
      notes: "Reciprocal of relationship between #{plant_a.common_name} and #{plant_b.common_name}"
    )
  end

  private

  def plants_must_be_different
    if plant_a_id == plant_b_id
      errors.add(:plant_b, 'cannot be the same as plant A')
    end
  end
end