class AddMatureHeightToEnhancedPlants < ActiveRecord::Migration[7.1]
  def change
    add_column :enhanced_plants, :mature_height_min_cm, :integer
    add_column :enhanced_plants, :mature_height_max_cm, :integer
  end
end
