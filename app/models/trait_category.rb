# frozen_string_literal: true
class TraitCategory < ApplicationRecord
  has_many :plant_traits, dependent: :destroy

  validates :name, presence: true, uniqueness: true, length: { maximum: 100 }
  validates :data_type, presence: true
  validates :unit, length: { maximum: 20 }, allow_blank: true

  enum data_type: {
    numeric: 'numeric',
    categorical: 'categorical',
    boolean: 'boolean',
    text: 'text'
  }

  scope :by_data_type, ->(type) { where(data_type: type) }
  scope :with_units, -> { where.not(unit: [nil, '']) }

  def self.search_by_keyword(keyword)
    where('search_keywords @> ?', [keyword].to_json)
      .or(where('synonyms @> ?', [keyword].to_json))
      .or(where('name ILIKE ?', "%#{keyword}%"))
  end

  def all_search_terms
    terms = [name]
    terms += synonyms if synonyms.present?
    terms += search_keywords if search_keywords.present?
    terms.flatten.uniq
  end

  def numeric_type?
    data_type == 'numeric'
  end

  def categorical_type?
    data_type == 'categorical'
  end

  def boolean_type?
    data_type == 'boolean'
  end

  def text_type?
    data_type == 'text'
  end
end