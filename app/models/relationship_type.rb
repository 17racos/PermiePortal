# frozen_string_literal: true
class RelationshipType < ApplicationRecord
  has_many :plant_relationships, dependent: :destroy

  validates :name, presence: true, uniqueness: true, length: { maximum: 100 }

  scope :beneficial, -> { where(is_beneficial: true) }
  scope :antagonistic, -> { where(is_beneficial: false) }
  scope :neutral, -> { where(is_beneficial: nil) }

  def beneficial?
    is_beneficial == true
  end

  def antagonistic?
    is_beneficial == false
  end

  def neutral?
    is_beneficial.nil?
  end

  def relationship_count
    plant_relationships.count
  end

  def display_name
    case is_beneficial
    when true
      "#{name} (beneficial)"
    when false
      "#{name} (antagonistic)"
    else
      "#{name} (neutral)"
    end
  end
end