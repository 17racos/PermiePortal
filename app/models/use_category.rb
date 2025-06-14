# frozen_string_literal: true
class UseCategory < ApplicationRecord
  has_many :plant_uses, dependent: :destroy
  has_many :enhanced_plants, through: :plant_uses
  belongs_to :parent_category, class_name: 'UseCategory', optional: true
  has_many :subcategories, class_name: 'UseCategory', foreign_key: 'parent_category_id'

  validates :name, presence: true, uniqueness: true, length: { maximum: 100 }

  scope :top_level, -> { where(parent_category_id: nil) }
  scope :with_plants, -> { joins(:plant_uses).distinct }

  def self.search_by_term(term)
    where('search_terms @> ?', [term].to_json)
      .or(where('name ILIKE ?', "%#{term}%"))
      .or(where('description ILIKE ?', "%#{term}%"))
  end

  def all_search_terms
    terms = [name]
    terms += search_terms if search_terms.present?
    terms.flatten.uniq
  end

  def hierarchy_name
    if parent_category
      "#{parent_category.hierarchy_name} > #{name}"
    else
      name
    end
  end

  def plant_count
    plant_uses.count
  end

  def effective_plants(min_effectiveness: 0.5)
    enhanced_plants.joins(:plant_uses)
                  .where(plant_uses: { use_category: self })
                  .where('plant_uses.effectiveness_score >= ?', min_effectiveness)
  end
end