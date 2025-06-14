# frozen_string_literal: true
class SemanticTag < ApplicationRecord
  has_many :plant_semantic_tags, dependent: :destroy
  has_many :enhanced_plants, through: :plant_semantic_tags
  belongs_to :parent_tag, class_name: 'SemanticTag', optional: true
  has_many :child_tags, class_name: 'SemanticTag', foreign_key: 'parent_tag_id'

  validates :name, presence: true, uniqueness: true, length: { maximum: 100 }
  validates :category, presence: true, inclusion: {
    in: %w[trait use habitat season maintenance growth_habit resistance environmental]
  }
  validates :weight, numericality: { in: 0.0..1.0 }

  scope :by_category, ->(category) { where(category: category) }
  scope :root_tags, -> { where(parent_tag_id: nil) }
  scope :with_synonyms, ->(term) {
    where('name ILIKE ? OR ? = ANY(synonyms)', "%#{term}%", term.downcase)
  }

  # Find tags by natural language terms
  def self.find_by_natural_language(terms)
    terms = Array(terms).map(&:downcase)

    where(
      terms.map { |term|
        "(name ILIKE '%#{sanitize_sql_like(term)}%' OR '#{sanitize_sql_like(term)}' = ANY(synonyms))"
      }.join(' OR ')
    )
  end

  # Get all descendants including self
  def descendants
    return [self] if child_tags.empty?
    [self] + child_tags.flat_map(&:descendants)
  end

  # Get semantic similarity score with another tag
  def similarity_score(other_tag)
    return 1.0 if self == other_tag
    return 0.8 if parent_tag == other_tag.parent_tag && parent_tag.present?
    return 0.6 if category == other_tag.category
    0.0
  end

  # Get plants with this tag and high confidence
  def high_confidence_plants(min_confidence = 0.7)
    enhanced_plants.joins(:plant_semantic_tags)
                   .where(plant_semantic_tags: { confidence_score: min_confidence.. })
  end

  # Get usage statistics
  def usage_stats
    {
      plant_count: enhanced_plants.count,
      avg_confidence: plant_semantic_tags.average(:confidence_score)&.round(2),
      sources: plant_semantic_tags.group(:source).count
    }
  end
end