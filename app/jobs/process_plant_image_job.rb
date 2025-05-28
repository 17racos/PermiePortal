class ProcessPlantImageJob < ApplicationJob
  queue_as :default

  def perform(plant_id)
    plant = Plant.find_by(id: plant_id)
    return unless plant&.image&.attached?

    # Process image variants
    plant.image.variant(resize_to_limit: [800, 800]).processed
    plant.image.variant(resize_to_fill: [400, 400]).processed

    # Update plant status
    plant.update(image_processed: true)
  rescue => e
    Rails.logger.error("Error processing plant image: #{e.message}")
    # Could add retry logic or notification system here
  end
end 