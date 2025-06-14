# frozen_string_literal: true
# Enhanced Semantic Ontology for AI-Powered Plant Search
class EnhancedSemanticOntology < ApplicationRecord
  self.table_name = 'semantic_ontology'

  # Hierarchical structure
  belongs_to :parent, class_name: 'EnhancedSemanticOntology', optional: true
  has_many :children, class_name: 'EnhancedSemanticOntology', foreign_key: 'parent_id'

  # Plant associations
  has_many :plant_ontology_tags, dependent: :destroy
  has_many :enhanced_plants, through: :plant_ontology_tags

  # Validations
  validates :name, presence: true, uniqueness: { scope: :parent_id }
  validates :ontology_category, presence: true, inclusion: {
    in: %w[
      edibility medicinal environmental growth_habit ecosystem_function
      human_use companion_relationship size appearance lifecycle
      climate_adaptation geographic care_level propagation
    ]
  }
  validates :ai_weight, numericality: { in: 0.0..1.0 }

  # Category constants for reference
  CATEGORIES = %w[
    edibility medicinal environmental growth_habit ecosystem_function
    human_use companion_relationship size appearance lifecycle
    climate_adaptation geographic care_level propagation
  ].freeze

  # Scopes for AI queries
  scope :root_concepts, -> { where(parent_id: nil) }
  scope :high_ai_weight, -> { where('ai_weight >= ?', 0.7) }
  scope :for_natural_language, -> { where(include_in_nlp: true) }

  # AI-specific methods
  def self.find_by_natural_language(query_text)
    # Enhanced NLP matching with synonyms and embeddings
    query_terms = extract_query_terms(query_text)

    matches = where(
      query_terms.map { |term|
        '(name ILIKE ? OR ? = ANY(synonyms) OR ? = ANY(nlp_keywords))'
      }.join(' OR '),
      *query_terms.flat_map { |term| ["%#{term}%", term, term] }
    )

    # Weight by AI importance and query relevance
    matches.order(ai_weight: :desc, name: :asc)
  end

  def self.extract_query_terms(text)
    # Remove stop words and extract meaningful terms
    stop_words = %w[the a an and or but for in on at to from with by]

    text.downcase
        .gsub(/[^\w\s]/, ' ')
        .split(/\s+/)
        .reject { |word| stop_words.include?(word) || word.length < 3 }
        .uniq
  end

  def descendants_with_self
    [self] + children.flat_map(&:descendants_with_self)
  end

  def ai_search_vector
    # Generate search vector for embeddings
    [
      name,
      synonyms&.join(' '),
      nlp_keywords&.join(' '),
      description,
      children.pluck(:name).join(' ')
    ].compact.join(' ')
  end

  def related_concepts(limit: 10)
    # Find semantically related concepts
    same_category = self.class.where(ontology_category: ontology_category).where.not(id: id)
    same_parent = parent&.children&.where&.not(id: id) || self.class.none

    (same_category.to_a + same_parent.to_a)
      .uniq
      .sort_by(&:ai_weight)
      .reverse
      .first(limit)
  end

  # Generate embedding for vector search
  def generate_embedding
    return unless Rails.env.production? # Only in production with proper API

    # This would integrate with your chosen embedding service
    # embedding_text = ai_search_vector
    # self.embedding_vector = EmbeddingService.generate(embedding_text)
    # save!
  end
end