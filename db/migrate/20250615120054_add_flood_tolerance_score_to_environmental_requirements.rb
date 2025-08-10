class AddFloodToleranceScoreToEnvironmentalRequirements < ActiveRecord::Migration[7.1]
  def change
    add_column :environmental_requirements, :flood_tolerance_score, :float
  end
end
