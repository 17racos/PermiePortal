class AddSoilPhMinAndMaxToEnvironmentalRequirements < ActiveRecord::Migration[7.1]
  def change
    add_column :environmental_requirements, :soil_ph_min, :float
    add_column :environmental_requirements, :soil_ph_max, :float
  end
end
