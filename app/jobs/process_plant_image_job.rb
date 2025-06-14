# frozen_string_literal: true
class ProcessPlantImageJob < ApplicationJob
  queue_as :default

  def perform(plant_id)
    plant = EnhancedPlant.find_by(id: plant_id)
    return unless plant&.image&.attached?

    # Process image variants
    plant.image.variant(resize_to_limit: [800, 800]).processed
    plant.image.variant(resize_to_fill: [400, 400]).processed

    # Update plant status if the field exists
    plant.update(image_processed: true) if plant.respond_to?(:image_processed)
  rescue => e
    Rails.logger.error("Error processing plant image: #{e.message}")
    # Could add retry logic or notification system here
  end
end