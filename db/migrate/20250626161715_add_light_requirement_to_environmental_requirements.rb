class AddLightRequirementToEnvironmentalRequirements < ActiveRecord::Migration[7.1]
  def change
    add_column :environmental_requirements, :light_requirement, :string
  end
end
