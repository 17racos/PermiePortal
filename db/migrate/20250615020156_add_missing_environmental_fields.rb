class AddMissingEnvironmentalFields < ActiveRecord::Migration[6.1]
  def change
    add_column :environmental_requirements, :temp_min_survival, :integer
    add_column :environmental_requirements, :temp_max_survival, :integer
    add_column :environmental_requirements, :hardiness_zone_min, :integer
    add_column :environmental_requirements, :hardiness_zone_max, :integer
  end
end
