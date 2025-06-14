# frozen_string_literal: true
class CreatePests < ActiveRecord::Migration[7.1]
  def change
    create_table :pests do |t|
      t.string :name, null: false
      t.string :slug, null: false
      t.string :picture
      t.string :scientific_name
      t.text :description
      t.text :characteristics
      t.jsonb :control_methods, default: {}  # Expecting a hash
      t.jsonb :natural_enemies, default: []    # Expecting an array

      t.timestamps
    end

    add_index :pests, :name, unique: true
    add_index :pests, :slug, unique: true
  end
end
