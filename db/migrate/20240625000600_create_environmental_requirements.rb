class CreateEnvironmentalRequirements < ActiveRecord::Migration[7.0]
  def change
    create_table :environmental_requirements do |t|
      t.references :enhanced_plant, null: false, foreign_key: true
      t.integer :temp_optimal_min
      t.integer :temp_optimal_max
      t.float :ph_min
      t.float :ph_max
      # Add any other fields you need here
      t.timestamps
    end
  end
end
