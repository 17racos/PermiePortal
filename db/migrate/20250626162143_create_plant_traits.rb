class CreatePlantTraits < ActiveRecord::Migration[7.1]
  def change
    create_table :plant_traits do |t|
      t.string :name
      t.text :description

      t.timestamps
    end
  end
end
