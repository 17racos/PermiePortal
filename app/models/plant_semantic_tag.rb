# frozen_string_literal: true
class PlantSemanticTag < ApplicationRecord
  belongs_to :enhanced_plant
  belongs_to :semantic_tag

  validates :confidence_score, numericality: { in: 0.0..1.0 }
  validates :source, inclusion: { in: %w[manual extracted inferred user_generated bulk_assigned] }
  validates :enhanced_plant_id, uniqueness: { scope: :semantic_tag_id }

  scope :high_confidence, -> { where('confidence_score >= ?', 0.7) }
  scope :by_source, ->(source) { where(source: source) }
  scope :by_category, ->(category) { joins(:semantic_tag).where(semantic_tags: { category: category }) }

  # Bulk assign tags to plants
  def self.bulk_assign(plant_ids, tag_ids, options = {})
    confidence = options[:confidence] || 0.8
    source = options[:source] || 'bulk_assigned'

    records = plant_ids.product(tag_ids).map do |plant_id, tag_id|
      {
        enhanced_plant_id: plant_id,
        semantic_tag_id: tag_id,
        confidence_score: confidence,
        source: source,
        created_at: Time.current,
        updated_at: Time.current
      }
    end

    insert_all(records, unique_by: [:enhanced_plant_id, :semantic_tag_id])
  end

  # Update confidence score with validation
  def update_confidence(new_score, reason = nil)
    if new_score.between?(0.0, 1.0)
      update!(
        confidence_score: new_score,
        notes: [notes, "Confidence updated to #{new_score}: #{reason}"].compact.join('; ')
      )
    else
      errors.add(:confidence_score, 'must be between 0.0 and 1.0')
      false
    end
  end
end