class AddDroughtToleranceScoreToEnvironmentalRequirements < ActiveRecord::Migration[7.1]
  def change
    add_column :environmental_requirements, :drought_tolerance_score, :float
  end
end
