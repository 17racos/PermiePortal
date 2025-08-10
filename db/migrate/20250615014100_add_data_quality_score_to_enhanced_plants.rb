class AddDataQualityScoreToEnhancedPlants < ActiveRecord::Migration[7.1]
  def change
    add_column :enhanced_plants, :data_quality_score, :float
  end
end
