class AddPlantNameIndexesAndFunctions < ActiveRecord::Migration[7.0]
  def change
    enable_extension 'pg_trgm'
  end

  def up
    # Add indexes for faster name lookups
    add_index :enhanced_plants, "LOWER(common_name)", name: 'index_enhanced_plants_on_lower_common_name'
    add_index :enhanced_plants, "LOWER(scientific_name)", name: 'index_enhanced_plants_on_lower_scientific_name'
    
    # Add GIN index for faster text search
    execute <<-SQL
      CREATE INDEX index_enhanced_plants_on_name_trigram 
      ON enhanced_plants 
      USING gin (LOWER(common_name) gin_trgm_ops, LOWER(scientific_name) gin_trgm_ops);
    SQL

    # Create function for fuzzy name matching
    execute <<-SQL
      CREATE OR REPLACE FUNCTION fuzzy_plant_name_match(search_term text, similarity_threshold float DEFAULT 0.6)
      RETURNS TABLE (
        plant_name text,
        match_type text,
        similarity float
      ) AS $$
      BEGIN
        RETURN QUERY
        WITH matches AS (
          SELECT 
            common_name as name,
            'common' as type,
            similarity(LOWER(common_name), LOWER(search_term)) as sim
          FROM enhanced_plants
          WHERE LOWER(common_name) % LOWER(search_term)
          UNION ALL
          SELECT 
            scientific_name as name,
            'scientific' as type,
            similarity(LOWER(scientific_name), LOWER(search_term)) as sim
          FROM enhanced_plants
          WHERE LOWER(scientific_name) % LOWER(search_term)
        )
        SELECT 
          name,
          type,
          sim
        FROM matches
        WHERE sim >= similarity_threshold
        ORDER BY sim DESC;
      END;
      $$ LANGUAGE plpgsql;
    SQL

    # Create function for batch fuzzy matching
    execute <<-SQL
      CREATE OR REPLACE FUNCTION batch_fuzzy_plant_match(search_terms text[], similarity_threshold float DEFAULT 0.6)
      RETURNS TABLE (
        search_term text,
        plant_name text,
        match_type text,
        similarity float
      ) AS $$
      BEGIN
        RETURN QUERY
        SELECT 
          term,
          m.name,
          m.type,
          m.sim
        FROM unnest(search_terms) AS term
        CROSS JOIN LATERAL fuzzy_plant_name_match(term, similarity_threshold) m;
      END;
      $$ LANGUAGE plpgsql;
    SQL
  end

  def down
    # Remove indexes
    remove_index :enhanced_plants, name: 'index_enhanced_plants_on_lower_common_name'
    remove_index :enhanced_plants, name: 'index_enhanced_plants_on_lower_scientific_name'
    execute "DROP INDEX IF EXISTS index_enhanced_plants_on_name_trigram;"
    
    # Remove functions
    execute "DROP FUNCTION IF EXISTS fuzzy_plant_name_match(text, float);"
    execute "DROP FUNCTION IF EXISTS batch_fuzzy_plant_match(text[], float);"
  end
end 