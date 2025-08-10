class CreateEnhancedPlantSchema < ActiveRecord::Migration[7.0]
  def change
    create_table :enhanced_plants do |t|
      t.string :common_name, null: false
      t.string :scientific_name
      t.string :family
      t.text :description
      t.string :growth_habit
      t.string :habitat
      t.string :edibility
      t.string :medicinal_uses
      t.string :toxicity
      t.string :plant_type  # For enum :plant_type
      t.string :life_cycle  # 🔥 You need this for enum :life_cycle
      t.timestamps
    end
  end
end
