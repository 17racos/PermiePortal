class CreateCommonPlantCombinationsView < ActiveRecord::Migration[7.0]
  def up
    if table_exists?(:plant_combinations)
      execute <<-SQL
        CREATE MATERIALIZED VIEW common_plant_combinations AS
        WITH plant_pairs AS (
          SELECT 
            p1.common_name as plant1,
            p2.common_name as plant2,
            COUNT(*) as co_occurrence_count
          FROM enhanced_plants p1
          JOIN enhanced_plants p2 ON p1.id < p2.id
          JOIN plant_combinations pc ON 
            (pc.plant1_id = p1.id AND pc.plant2_id = p2.id) OR
            (pc.plant1_id = p2.id AND pc.plant2_id = p1.id)
          GROUP BY p1.common_name, p2.common_name
          HAVING COUNT(*) >= 3
        )
        SELECT 
          plant1,
          plant2,
          co_occurrence_count,
          NOW() as last_updated
        FROM plant_pairs
        ORDER BY co_occurrence_count DESC;

        CREATE INDEX idx_common_plant_combinations_names 
          ON common_plant_combinations (plant1, plant2);

        CREATE INDEX idx_common_plant_combinations_count 
          ON common_plant_combinations (co_occurrence_count DESC);
      SQL

      execute <<-SQL
        CREATE OR REPLACE FUNCTION refresh_common_plant_combinations()
        RETURNS trigger AS $$
        BEGIN
          REFRESH MATERIALIZED VIEW CONCURRENTLY common_plant_combinations;
          RETURN NULL;
        END;
        $$ LANGUAGE plpgsql;
      SQL

      execute <<-SQL
        CREATE TRIGGER refresh_common_plant_combinations_trigger
        AFTER INSERT OR UPDATE OR DELETE ON plant_combinations
        FOR EACH STATEMENT
        EXECUTE FUNCTION refresh_common_plant_combinations();
      SQL
    else
      Rails.logger.warn "Skipping creation of common_plant_combinations view because plant_combinations table does not exist."
    end
  end

  def down
    if table_exists?(:plant_combinations)
      execute "DROP TRIGGER IF EXISTS refresh_common_plant_combinations_trigger ON plant_combinations;"
      execute "DROP FUNCTION IF EXISTS refresh_common_plant_combinations();"
    end
    execute "DROP MATERIALIZED VIEW IF EXISTS common_plant_combinations;"
  end
end
