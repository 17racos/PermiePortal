class AddMatureWidthToEnhancedPlants < ActiveRecord::Migration[7.1]
  def change
    add_column :enhanced_plants, :mature_width_min_cm, :integer
    add_column :enhanced_plants, :mature_width_max_cm, :integer
  end
end
