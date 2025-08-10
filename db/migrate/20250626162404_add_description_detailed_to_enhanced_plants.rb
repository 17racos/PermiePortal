class AddDescriptionDetailedToEnhancedPlants < ActiveRecord::Migration[7.1]
  def change
    add_column :enhanced_plants, :description_detailed, :text
  end
end
