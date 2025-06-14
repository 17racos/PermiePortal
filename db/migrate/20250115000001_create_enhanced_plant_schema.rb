# frozen_string_literal: true
class CreateEnhancedPlantSchema < ActiveRecord::Migration[7.1]
  def up
    # Enable required extensions
    enable_extension 'uuid-ossp' unless extension_enabled?('uuid-ossp')
    # enable_extension 'vector' unless extension_enabled?('vector') # Commented out for now

    # Create enhanced plants table
    create_table :enhanced_plants do |t|
      t.uuid :uuid, default: -> { 'gen_random_uuid()' }, null: false

      # Basic Identification
      t.string :common_name, null: false
      t.string :scientific_name, null: false
      t.string :family, limit: 100
      t.string :genus, limit: 100
      t.string :species, limit: 100

      # Taxonomic and Classification
      t.enum :plant_type, enum_type: 'plant_type_enum', null: true
      t.enum :life_cycle, enum_type: 'life_cycle_enum', null: true

      # Physical Characteristics
      t.integer :mature_height_min_cm
      t.integer :mature_height_max_cm
      t.integer :mature_width_min_cm
      t.integer :mature_width_max_cm

      # Semantic Description Fields
      t.text :description_short
      t.text :description_detailed
      t.text :growing_notes
      t.text :cultural_significance

      # Metadata
      t.float :data_quality_score, default: 0.0

      # Search Optimization
      t.tsvector :search_vector
      # t.vector :embedding_vector, limit: 1536 # Commented out for now

      t.timestamps

      t.index :uuid, unique: true
      t.index :common_name
      t.index :scientific_name, unique: true
      t.index :family
      t.index :plant_type
      t.index :life_cycle
      t.index :data_quality_score
      t.index :search_vector, using: :gin
      # t.index :embedding_vector, using: :ivfflat, opclass: :vector_cosine_ops # Commented out for now
    end

    # Create plant names table for aliases and regional names
    create_table :plant_names do |t|
      t.references :enhanced_plant, null: false, foreign_key: { on_delete: :cascade }
      t.string :name, null: false
      t.enum :name_type, enum_type: 'name_type_enum', null: false
      t.string :language_code, limit: 5
      t.string :region, limit: 100
      t.float :confidence_score, default: 1.0
      t.string :source

      t.timestamps

      t.index :name
      t.index [:language_code, :region]
    end

    # Create trait categories
    create_table :trait_categories do |t|
      t.string :name, limit: 100, null: false
      t.text :description
      t.enum :data_type, enum_type: 'trait_data_type_enum', null: false
      t.string :unit, limit: 20
      t.json :synonyms
      t.json :search_keywords

      t.timestamps

      t.index :name, unique: true
      t.index :data_type
    end

    # Create plant traits
    create_table :plant_traits do |t|
      t.references :enhanced_plant, null: false, foreign_key: { on_delete: :cascade }
      t.references :trait_category, null: false, foreign_key: true

      # Flexible value storage
      t.float :numeric_value
      t.float :numeric_min
      t.float :numeric_max
      t.string :categorical_value, limit: 100
      t.boolean :boolean_value
      t.text :text_value

      # Confidence and context
      t.float :confidence_score, default: 1.0
      t.string :context
      t.string :source
      t.text :notes

      t.timestamps

      t.index :categorical_value
      t.index :numeric_value
      t.index :confidence_score
    end

    # Create environmental requirements
    create_table :environmental_requirements do |t|
      t.references :enhanced_plant, null: false, foreign_key: { on_delete: :cascade }

      # Climate Zones
      t.integer :hardiness_zone_min
      t.integer :hardiness_zone_max
      t.integer :heat_zone_min
      t.integer :heat_zone_max

      # Temperature (in Celsius)
      t.float :temp_min_survival
      t.float :temp_max_survival
      t.float :temp_optimal_min
      t.float :temp_optimal_max

      # Precipitation and Water
      t.integer :annual_rainfall_min_mm
      t.integer :annual_rainfall_max_mm
      t.float :drought_tolerance_score
      t.float :flood_tolerance_score

      # Soil Requirements
      t.float :soil_ph_min
      t.float :soil_ph_max
      t.enum :soil_drainage, enum_type: 'soil_drainage_enum'
      t.enum :soil_fertility, enum_type: 'soil_fertility_enum'

      # Light Requirements
      t.enum :light_requirement, enum_type: 'light_requirement_enum'
      t.json :light_tolerance

      # Semantic descriptions
      t.text :climate_description
      t.text :soil_description

      t.timestamps

      t.index [:hardiness_zone_min, :hardiness_zone_max]
      t.index :drought_tolerance_score
      t.index :light_requirement
    end

    # Create use categories
    create_table :use_categories do |t|
      t.string :name, limit: 100, null: false
      t.references :parent_category, null: true, foreign_key: { to_table: :use_categories }
      t.text :description
      t.json :search_terms

      t.timestamps

      t.index :name, unique: true
    end

    # Create plant uses
    create_table :plant_uses do |t|
      t.references :enhanced_plant, null: false, foreign_key: { on_delete: :cascade }
      t.references :use_category, null: false, foreign_key: true

      # Detailed information
      t.string :plant_part, limit: 100
      t.text :preparation_method
      t.float :effectiveness_score
      t.text :safety_notes
      t.text :traditional_knowledge

      # Seasonal information
      t.json :harvest_season
      t.string :processing_time, limit: 100

      # Source and confidence
      t.float :confidence_score, default: 1.0
      t.string :source

      t.timestamps

      t.index :plant_part
      t.index :effectiveness_score
    end

    # Create relationship types
    create_table :relationship_types do |t|
      t.string :name, limit: 100, null: false
      t.text :description
      t.boolean :is_beneficial
      t.string :strength_scale, limit: 50

      t.timestamps

      t.index :name, unique: true
      t.index :is_beneficial
    end

    # Create plant relationships
    create_table :plant_relationships do |t|
      t.references :plant_a, null: false, foreign_key: { to_table: :enhanced_plants, on_delete: :cascade }
      t.references :plant_b, null: false, foreign_key: { to_table: :enhanced_plants, on_delete: :cascade }
      t.references :relationship_type, null: false, foreign_key: true

      # Relationship details
      t.float :strength_score
      t.text :mechanism
      t.integer :distance_optimal_cm
      t.integer :distance_max_cm

      # Conditions
      t.json :climate_conditions
      t.json :soil_conditions

      # Evidence and confidence
      t.float :confidence_score, default: 1.0
      t.enum :evidence_type, enum_type: 'evidence_type_enum'
      t.string :source
      t.text :notes

      t.timestamps

      t.index :strength_score
      t.index [:plant_a_id, :plant_b_id, :relationship_type_id], unique: true, name: 'unique_plant_relationship'
    end

    # Create plant guilds
    create_table :plant_guilds do |t|
      t.string :name, null: false
      t.text :description
      t.json :climate_suitability
      t.float :space_requirement_sqm
      t.text :guild_purpose
      t.text :management_notes

      t.timestamps

      t.index :name
    end

    # Create guild members
    create_table :guild_members do |t|
      t.references :plant_guild, null: false, foreign_key: { on_delete: :cascade }
      t.references :enhanced_plant, null: false, foreign_key: { on_delete: :cascade }
      t.string :role, limit: 100
      t.float :importance_score
      t.integer :planting_order

      t.timestamps

      t.index [:plant_guild_id, :enhanced_plant_id], unique: true
    end

    # Create regions
    create_table :regions do |t|
      t.string :name, null: false
      t.string :country_code, limit: 3
      t.string :climate_type, limit: 100
      t.float :latitude_min
      t.float :latitude_max
      t.float :longitude_min
      t.float :longitude_max

      # Climate characteristics
      t.float :avg_temp_min
      t.float :avg_temp_max
      t.integer :avg_rainfall_mm
      t.integer :growing_season_days

      t.timestamps

      t.index :country_code
      t.index :climate_type
      t.index :name
    end

    # Create plant regional data
    create_table :plant_regional_data do |t|
      t.references :enhanced_plant, null: false, foreign_key: { on_delete: :cascade }
      t.references :region, null: false, foreign_key: { on_delete: :cascade }

      # Regional performance
      t.float :performance_score
      t.enum :invasiveness_risk, enum_type: 'invasiveness_risk_enum'
      t.enum :legal_status, enum_type: 'legal_status_enum'

      # Regional growing notes
      t.json :planting_season
      t.json :harvest_season
      t.text :special_considerations
      t.text :local_varieties

      # Local names and cultural info
      t.json :regional_names
      t.text :cultural_uses
      t.text :traditional_knowledge

      t.timestamps

      t.index :invasiveness_risk
      t.index :performance_score
    end

    # Enhanced pests and diseases
    create_table :enhanced_pests_diseases do |t|
      t.string :name, null: false
      t.string :scientific_name
      t.enum :pest_type, enum_type: 'pest_type_enum'
      t.text :description
      t.text :symptoms
      t.text :identification_notes

      t.timestamps

      t.index :pest_type
      t.index :name
    end

    # Enhanced plant pest relationships
    create_table :enhanced_plant_pest_relationships do |t|
      t.references :enhanced_plant, null: false, foreign_key: { on_delete: :cascade }
      t.references :enhanced_pests_disease, null: false, foreign_key: { on_delete: :cascade }

      t.enum :relationship_type, enum_type: 'pest_relationship_type_enum'
      t.float :severity_score

      # Management information
      t.json :prevention_methods
      t.json :treatment_methods
      t.json :biological_controls

      # Conditions
      t.json :climate_factors
      t.json :seasonal_timing

      t.float :confidence_score, default: 1.0
      t.string :source

      t.timestamps

      t.index :relationship_type
      t.index [:enhanced_plant_id, :enhanced_pests_disease_id], unique: true, name: 'unique_plant_pest_relationship'
    end

    # Create search vector update function
    execute <<-SQL
      CREATE OR REPLACE FUNCTION update_enhanced_plant_search_vector()
      RETURNS TRIGGER AS $$
      BEGIN
        NEW.search_vector :=#{' '}
          setweight(to_tsvector('english', COALESCE(NEW.common_name, '')), 'A') ||
          setweight(to_tsvector('english', COALESCE(NEW.scientific_name, '')), 'A') ||
          setweight(to_tsvector('english', COALESCE(NEW.description_short, '')), 'B') ||
          setweight(to_tsvector('english', COALESCE(NEW.description_detailed, '')), 'C') ||
          setweight(to_tsvector('english', COALESCE(NEW.growing_notes, '')), 'D');
        RETURN NEW;
      END;
      $$ LANGUAGE plpgsql;
    SQL

    # Create trigger for search vector updates
    execute <<-SQL
      CREATE TRIGGER enhanced_plants_search_vector_update
        BEFORE INSERT OR UPDATE ON enhanced_plants
        FOR EACH ROW EXECUTE FUNCTION update_enhanced_plant_search_vector();
    SQL

    # Create similarity search function (commented out for now)
    # execute <<-SQL
    #   CREATE OR REPLACE FUNCTION find_similar_enhanced_plants(
    #     query_embedding VECTOR(1536),
    #     similarity_threshold FLOAT DEFAULT 0.7,
    #     max_results INTEGER DEFAULT 10
    #   )
    #   RETURNS TABLE(
    #     plant_id INTEGER,
    #     common_name VARCHAR(255),
    #     similarity_score FLOAT
    #   ) AS $$
    #   BEGIN
    #     RETURN QUERY
    #     SELECT
    #       p.id,
    #       p.common_name,
    #       1 - (p.embedding_vector <=> query_embedding) AS similarity
    #     FROM enhanced_plants p
    #     WHERE p.embedding_vector IS NOT NULL
    #       AND 1 - (p.embedding_vector <=> query_embedding) > similarity_threshold
    #     ORDER BY p.embedding_vector <=> query_embedding
    #     LIMIT max_results;
    #   END;
    #   $$ LANGUAGE plpgsql;
    # SQL
  end

  def down
    # Drop functions and triggers
    # execute 'DROP FUNCTION IF EXISTS find_similar_enhanced_plants(VECTOR, FLOAT, INTEGER);' # Commented out for now
    execute 'DROP TRIGGER IF EXISTS enhanced_plants_search_vector_update ON enhanced_plants;'
    execute 'DROP FUNCTION IF EXISTS update_enhanced_plant_search_vector();'

    # Drop tables in reverse dependency order
    drop_table :enhanced_plant_pest_relationships
    drop_table :enhanced_pests_diseases
    drop_table :plant_regional_data
    drop_table :regions
    drop_table :guild_members
    drop_table :plant_guilds
    drop_table :plant_relationships
    drop_table :relationship_types
    drop_table :plant_uses
    drop_table :use_categories
    drop_table :environmental_requirements
    drop_table :plant_traits
    drop_table :trait_categories
    drop_table :plant_names
    drop_table :enhanced_plants

    # Drop enums
    execute 'DROP TYPE IF EXISTS pest_relationship_type_enum;'
    execute 'DROP TYPE IF EXISTS pest_type_enum;'
    execute 'DROP TYPE IF EXISTS legal_status_enum;'
    execute 'DROP TYPE IF EXISTS invasiveness_risk_enum;'
    execute 'DROP TYPE IF EXISTS evidence_type_enum;'
    execute 'DROP TYPE IF EXISTS light_requirement_enum;'
    execute 'DROP TYPE IF EXISTS soil_fertility_enum;'
    execute 'DROP TYPE IF EXISTS soil_drainage_enum;'
    execute 'DROP TYPE IF EXISTS trait_data_type_enum;'
    execute 'DROP TYPE IF EXISTS name_type_enum;'
    execute 'DROP TYPE IF EXISTS life_cycle_enum;'
    execute 'DROP TYPE IF EXISTS plant_type_enum;'
  end

  private

  def create_enums
    # This will be called by a separate migration to create enums first
  end
end