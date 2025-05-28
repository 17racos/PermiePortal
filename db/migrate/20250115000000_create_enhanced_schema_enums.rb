class CreateEnhancedSchemaEnums < ActiveRecord::Migration[7.1]
  def up
    # Plant type enum
    execute <<-SQL
      CREATE TYPE plant_type_enum AS ENUM (
        'tree', 'shrub', 'herbaceous', 'vine', 'grass', 'fern', 'moss', 'aquatic'
      );
    SQL

    # Life cycle enum
    execute <<-SQL
      CREATE TYPE life_cycle_enum AS ENUM (
        'annual', 'biennial', 'perennial', 'short_lived_perennial'
      );
    SQL

    # Name type enum
    execute <<-SQL
      CREATE TYPE name_type_enum AS ENUM (
        'common', 'regional', 'traditional', 'trade', 'historical'
      );
    SQL

    # Trait data type enum
    execute <<-SQL
      CREATE TYPE trait_data_type_enum AS ENUM (
        'numeric', 'categorical', 'boolean', 'text'
      );
    SQL

    # Soil drainage enum
    execute <<-SQL
      CREATE TYPE soil_drainage_enum AS ENUM (
        'poor', 'moderate', 'good', 'excellent'
      );
    SQL

    # Soil fertility enum
    execute <<-SQL
      CREATE TYPE soil_fertility_enum AS ENUM (
        'poor', 'moderate', 'rich', 'very_rich'
      );
    SQL

    # Light requirement enum
    execute <<-SQL
      CREATE TYPE light_requirement_enum AS ENUM (
        'full_shade', 'partial_shade', 'partial_sun', 'full_sun'
      );
    SQL

    # Evidence type enum
    execute <<-SQL
      CREATE TYPE evidence_type_enum AS ENUM (
        'scientific', 'traditional', 'observational', 'theoretical'
      );
    SQL

    # Invasiveness risk enum
    execute <<-SQL
      CREATE TYPE invasiveness_risk_enum AS ENUM (
        'none', 'low', 'moderate', 'high', 'severe'
      );
    SQL

    # Legal status enum
    execute <<-SQL
      CREATE TYPE legal_status_enum AS ENUM (
        'unrestricted', 'restricted', 'prohibited', 'permit_required'
      );
    SQL

    # Pest type enum
    execute <<-SQL
      CREATE TYPE pest_type_enum AS ENUM (
        'insect', 'disease', 'fungal', 'bacterial', 'viral', 'nematode', 'mammal', 'bird'
      );
    SQL

    # Pest relationship type enum
    execute <<-SQL
      CREATE TYPE pest_relationship_type_enum AS ENUM (
        'susceptible', 'resistant', 'immune', 'attracts', 'repels'
      );
    SQL
  end

  def down
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
end 