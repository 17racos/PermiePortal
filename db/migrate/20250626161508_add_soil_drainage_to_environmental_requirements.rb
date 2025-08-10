class AddSoilDrainageToEnvironmentalRequirements < ActiveRecord::Migration[7.1]
  def change
    add_column :environmental_requirements, :soil_drainage, :string
  end
end
