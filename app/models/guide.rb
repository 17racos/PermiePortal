# frozen_string_literal: true
class Guide < ApplicationRecord
  extend FriendlyId
  friendly_id :title, use: :slugged

  validates :title, presence: true
  validates :body, presence: true
  validates :image, presence: true, allow_blank: true

  # ✅ Define the image URL method
  def image_url
    "/assets/guides/#{image}" if image.present?
  end
end
