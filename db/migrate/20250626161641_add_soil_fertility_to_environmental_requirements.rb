class AddSoilFertilityToEnvironmentalRequirements < ActiveRecord::Migration[7.1]
  def change
    add_column :environmental_requirements, :soil_fertility, :string
  end
end
