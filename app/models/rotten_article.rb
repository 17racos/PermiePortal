# frozen_string_literal: true
class RottenArticle < ApplicationRecord
  extend FriendlyId
  friendly_id :title, use: :slugged

  validates :title, presence: true
  validates :body, presence: true
  validates :image, presence: true, allow_blank: true

  # ✅ Define the image URL method
  def image_url
    "/rotten_articles/#{image}" if image.present?
  end
end
