class AddSearchOptimizationsToEnhancedPlants < ActiveRecord::Migration[7.0]
  def up
    execute <<~SQL
      CREATE INDEX enhanced_plants_search_idx
      ON enhanced_plants
      USING GIN (
        to_tsvector(
          'english',
          coalesce(common_name, '') || ' ' ||
          coalesce(scientific_name, '') || ' ' ||
          coalesce(family, '')
        )
      );
    SQL
  end

  def down
    execute "DROP INDEX IF EXISTS enhanced_plants_search_idx;"
  end
end

