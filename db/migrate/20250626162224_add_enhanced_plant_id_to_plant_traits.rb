class AddEnhancedPlantIdToPlantTraits < ActiveRecord::Migration[7.1]
  def change
    add_reference :plant_traits, :enhanced_plant, null: false, foreign_key: true
  end
end
