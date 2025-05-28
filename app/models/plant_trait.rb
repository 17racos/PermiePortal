class PlantTrait < ApplicationRecord
  belongs_to :enhanced_plant
  belongs_to :trait_category

  validates :confidence_score, inclusion: { in: 0.0..1.0 }
  validate :value_presence
  validate :value_type_consistency

  scope :high_confidence, -> { where('confidence_score > ?', 0.7) }
  scope :by_category, ->(category_name) { joins(:trait_category).where(trait_categories: { name: category_name }) }
  scope :numeric_traits, -> { joins(:trait_category).where(trait_categories: { data_type: 'numeric' }) }
  scope :categorical_traits, -> { joins(:trait_category).where(trait_categories: { data_type: 'categorical' }) }

  def value
    case trait_category.data_type
    when 'numeric'
      if numeric_value.present?
        numeric_value
      elsif numeric_min.present? && numeric_max.present?
        { min: numeric_min, max: numeric_max }
      elsif numeric_min.present?
        { min: numeric_min }
      elsif numeric_max.present?
        { max: numeric_max }
      end
    when 'categorical'
      categorical_value
    when 'boolean'
      boolean_value
    when 'text'
      text_value
    end
  end

  def value=(val)
    case trait_category.data_type
    when 'numeric'
      if val.is_a?(Hash)
        self.numeric_min = val[:min] || val['min']
        self.numeric_max = val[:max] || val['max']
      else
        self.numeric_value = val
      end
    when 'categorical'
      self.categorical_value = val
    when 'boolean'
      self.boolean_value = val
    when 'text'
      self.text_value = val
    end
  end

  def display_value
    case trait_category.data_type
    when 'numeric'
      if numeric_value.present?
        unit = trait_category.unit.present? ? " #{trait_category.unit}" : ""
        "#{numeric_value}#{unit}"
      elsif numeric_min.present? && numeric_max.present?
        unit = trait_category.unit.present? ? " #{trait_category.unit}" : ""
        "#{numeric_min}-#{numeric_max}#{unit}"
      elsif numeric_min.present?
        unit = trait_category.unit.present? ? " #{trait_category.unit}" : ""
        "#{numeric_min}+#{unit}"
      elsif numeric_max.present?
        unit = trait_category.unit.present? ? " #{trait_category.unit}" : ""
        "up to #{numeric_max}#{unit}"
      end
    when 'categorical'
      categorical_value&.humanize
    when 'boolean'
      boolean_value ? 'Yes' : 'No'
    when 'text'
      text_value
    end
  end

  def matches_criteria?(criteria)
    case trait_category.data_type
    when 'numeric'
      return false unless numeric_value.present?
      
      if criteria.is_a?(Hash)
        result = true
        result &&= numeric_value >= criteria[:min] if criteria[:min]
        result &&= numeric_value <= criteria[:max] if criteria[:max]
        result
      else
        numeric_value == criteria
      end
    when 'categorical'
      if criteria.is_a?(Array)
        criteria.include?(categorical_value)
      else
        categorical_value == criteria
      end
    when 'boolean'
      boolean_value == criteria
    when 'text'
      text_value&.downcase&.include?(criteria.to_s.downcase)
    end
  end

  private

  def value_presence
    case trait_category&.data_type
    when 'numeric'
      if numeric_value.blank? && numeric_min.blank? && numeric_max.blank?
        errors.add(:base, 'At least one numeric value must be present')
      end
    when 'categorical'
      errors.add(:categorical_value, 'cannot be blank') if categorical_value.blank?
    when 'boolean'
      errors.add(:boolean_value, 'cannot be blank') if boolean_value.nil?
    when 'text'
      errors.add(:text_value, 'cannot be blank') if text_value.blank?
    end
  end

  def value_type_consistency
    return unless trait_category

    case trait_category.data_type
    when 'numeric'
      if categorical_value.present? || boolean_value.present? || text_value.present?
        errors.add(:base, 'Only numeric values should be set for numeric traits')
      end
    when 'categorical'
      if numeric_value.present? || numeric_min.present? || numeric_max.present? || boolean_value.present? || text_value.present?
        errors.add(:base, 'Only categorical value should be set for categorical traits')
      end
    when 'boolean'
      if numeric_value.present? || numeric_min.present? || numeric_max.present? || categorical_value.present? || text_value.present?
        errors.add(:base, 'Only boolean value should be set for boolean traits')
      end
    when 'text'
      if numeric_value.present? || numeric_min.present? || numeric_max.present? || categorical_value.present? || boolean_value.present?
        errors.add(:base, 'Only text value should be set for text traits')
      end
    end
  end
end 