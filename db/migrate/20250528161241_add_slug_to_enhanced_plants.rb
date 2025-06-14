# frozen_string_literal: true
class AddSlugToEnhancedPlants < ActiveRecord::Migration[7.1]
  def change
    add_column :enhanced_plants, :slug, :string
    add_index :enhanced_plants, :slug
  end
end
