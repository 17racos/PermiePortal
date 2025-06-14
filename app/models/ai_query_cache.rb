# frozen_string_literal: true
# AI Query Cache Model
# Stores cached results from AI plant searches for performance
class AiQueryCache < ApplicationRecord
  # Validations
  validates :query_text, presence: true
  validates :query_hash, presence: true, uniqueness: true

  # Scopes
  scope :recent, -> { where('last_accessed_at > ?', 1.hour.ago) }
  scope :popular, -> { where('hit_count > ?', 5) }
  scope :old, -> { where('last_accessed_at < ?', 1.week.ago) }

  # Callbacks
  before_create :set_last_accessed_at

  # Class methods
  def self.cleanup_old_entries
    old.delete_all
  end

  def self.most_popular(limit = 10)
    order(hit_count: :desc).limit(limit)
  end

  # Instance methods
  def fresh?
    last_accessed_at && last_accessed_at > 1.hour.ago
  end

  def popular?
    hit_count > 5
  end

  private

  def set_last_accessed_at
    self.last_accessed_at ||= Time.current
  end
end