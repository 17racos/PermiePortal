class CreatePlantContexts < ActiveRecord::Migration[7.1]
  def change
    create_table :plant_contexts do |t|
      t.references :enhanced_plant, null: false, foreign_key: true
      t.string :context_type, null: false
      t.text :content, null: false

      t.timestamps
    end
    
    add_index :plant_contexts, [:enhanced_plant_id, :context_type], unique: true
    add_index :plant_contexts, :context_type
  end
end
