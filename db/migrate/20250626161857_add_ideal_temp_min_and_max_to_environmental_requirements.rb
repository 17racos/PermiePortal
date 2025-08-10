class AddIdealTempMinAndMaxToEnvironmentalRequirements < ActiveRecord::Migration[7.1]
  def change
    add_column :environmental_requirements, :ideal_temp_min, :float
    add_column :environmental_requirements, :ideal_temp_max, :float
  end
end
