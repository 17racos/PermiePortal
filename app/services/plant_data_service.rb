# frozen_string_literal: true
class PlantDataService
  def self.process_plant_submission(params, user)
    ActiveRecord::Base.transaction do
      plant = EnhancedPlant.new(params)
      plant.submitted_by = user if plant.respond_to?(:submitted_by)

      if plant.save
        # Trigger background job for image processing if image present
        ProcessPlantImageJob.perform_later(plant.id) if params[:image].present?

        return { success: true, plant: plant }
      else
        return { success: false, errors: plant.errors.full_messages }
      end
    end
  rescue => e
    Rails.logger.error("Error processing plant submission: #{e.message}")
    return { success: false, errors: ['Internal error occurred'] }
  end
end