# db/migrate/20250615123000_create_use_categories.rb
class CreateUseCategories < ActiveRecord::Migration[7.0]
    def change
      create_table :use_categories do |t|
        t.string :name, null: false
        t.timestamps
      end
  
      add_index :use_categories, :name, unique: true
    end
  end
  