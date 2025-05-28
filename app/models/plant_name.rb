class PlantName < ApplicationRecord
  belongs_to :enhanced_plant

  validates :name, presence: true, length: { maximum: 255 }
  validates :name_type, presence: true
  validates :confidence_score, inclusion: { in: 0.0..1.0 }
  validates :language_code, length: { maximum: 5 }, allow_blank: true
  validates :region, length: { maximum: 100 }, allow_blank: true

  enum name_type: {
    common: 'common',
    regional: 'regional',
    traditional: 'traditional',
    trade: 'trade',
    historical: 'historical'
  }

  scope :by_language, ->(lang) { where(language_code: lang) }
  scope :by_region, ->(region) { where(region: region) }
  scope :high_confidence, -> { where('confidence_score > ?', 0.7) }
  scope :primary_names, -> { where(name_type: ['common', 'regional']) }

  def self.search_by_name(query)
    where("name ILIKE ?", "%#{query}%")
  end
end 