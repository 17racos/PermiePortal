class AddHeatZonesToEnvironmentalRequirements < ActiveRecord::Migration[7.1]
  def change
    add_column :environmental_requirements, :heat_zone_min, :integer
    add_column :environmental_requirements, :heat_zone_max, :integer
  end
end
