# frozen_string_literal: true
class DropOldPlantsTable < ActiveRecord::Migration[7.1]
  def up
    # Drop tables with foreign key dependencies first
    drop_table :plant_ontology_tags if table_exists?(:plant_ontology_tags)
    drop_table :plant_pests if table_exists?(:plant_pests)

    # Drop the old plants table
    drop_table :plants if table_exists?(:plants)

    puts '✅ Dropped old plants table and related dependency tables'
  end

  def down
    # Recreate plants table (basic structure for rollback)
    create_table :plants do |t|
      t.string :picture
      t.string :common_name, null: false
      t.string :scientific_name
      t.text :aka, default: [], array: true
      t.string :family
      t.int4range :zone_range
      t.string :ideal_temp_min
      t.string :ideal_temp_max
      t.string :min_temp
      t.string :max_temp
      t.boolean :perennial
      t.text :layers, default: [], array: true
      t.text :plant_functions, default: [], array: true
      t.text :description
      t.text :purpose
      t.text :avoid, default: [], array: true
      t.text :companions, default: [], array: true
      t.timestamps null: false
    end

    add_index :plants, :common_name, unique: true

    # Recreate plant_pests table
    create_table :plant_pests do |t|
      t.bigint :plant_id, null: false
      t.bigint :pest_id, null: false
      t.timestamps null: false
    end

    add_index :plant_pests, :plant_id
    add_index :plant_pests, :pest_id
    add_index :plant_pests, [:plant_id, :pest_id], unique: true
    add_foreign_key :plant_pests, :plants
    add_foreign_key :plant_pests, :pests

    puts '⚠️  Recreated old plants table structure (data will be empty)'
  end
end
