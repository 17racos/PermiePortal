# db/migrate/20250615_create_plant_uses.rb
class CreatePlantUses < ActiveRecord::Migration[7.0]
    def change
      create_table :plant_uses do |t|
        t.references :enhanced_plant, null: false, foreign_key: true
        t.references :use_category, null: false, foreign_key: true
        t.float :effectiveness_score, default: 0.0, null: false
        t.float :confidence_score, default: 0.0, null: false
  
        t.timestamps
      end
  
      add_index :plant_uses, [:enhanced_plant_id, :use_category_id], unique: true
    end
  end
  