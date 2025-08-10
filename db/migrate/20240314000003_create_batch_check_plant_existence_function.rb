class CreateBatchCheckPlantExistenceFunction < ActiveRecord::Migration[7.0]
  def up
    execute <<-SQL
      CREATE OR REPLACE FUNCTION batch_check_plant_existence(plant_names text[])
      RETURNS TABLE (plant_name text, plant_exists boolean) AS $$
      BEGIN
        RETURN QUERY
        SELECT 
          name,
          CASE WHEN ep.id IS NOT NULL THEN true ELSE false END as plant_exists
        FROM unnest(plant_names) AS name
        LEFT JOIN enhanced_plants ep ON 
          LOWER(ep.common_name) = LOWER(name) OR 
          LOWER(ep.scientific_name) = LOWER(name);
      END;
      $$ LANGUAGE plpgsql;
    SQL
  end

  def down
    execute "DROP FUNCTION IF EXISTS batch_check_plant_existence(text[]);"
  end
end
