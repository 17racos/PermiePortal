class CreateEnhancedSchemaEnums < ActiveRecord::Migration[7.1]
  def up
    create_enum_type('plant_type_enum', [
      'tree', 'shrub', 'herbaceous', 'vine', 'grass', 'fern', 'moss', 'aquatic'
    ])
    create_enum_type('life_cycle_enum', [
      'annual', 'biennial', 'perennial', 'short_lived_perennial'
    ])
    create_enum_type('name_type_enum', [
      'common', 'regional', 'traditional', 'trade', 'historical'
    ])
    create_enum_type('trait_data_type_enum', [
      'numeric', 'categorical', 'boolean', 'text'
    ])
    create_enum_type('soil_drainage_enum', [
      'poor', 'moderate', 'good', 'excellent'
    ])
    create_enum_type('soil_fertility_enum', [
      'poor', 'moderate', 'rich', 'very_rich'
    ])
    create_enum_type('light_requirement_enum', [
      'full_shade', 'partial_shade', 'partial_sun', 'full_sun'
    ])
    create_enum_type('evidence_type_enum', [
      'scientific', 'traditional', 'observational', 'theoretical'
    ])
    create_enum_type('invasiveness_risk_enum', [
      'none', 'low', 'moderate', 'high', 'severe'
    ])
    create_enum_type('legal_status_enum', [
      'unrestricted', 'restricted', 'prohibited', 'permit_required'
    ])
    create_enum_type('pest_type_enum', [
      'insect', 'disease', 'fungal', 'bacterial', 'viral', 'nematode', 'mammal', 'bird'
    ])
    create_enum_type('pest_relationship_type_enum', [
      'susceptible', 'resistant', 'immune', 'attracts', 'repels'
    ])
  end

  private

  def create_enum_type(name, values)
    execute <<-SQL
      DO $$
      BEGIN
        IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = '#{name}') THEN
          CREATE TYPE #{name} AS ENUM (#{values.map { |v| "'#{v}'" }.join(', ')});
        END IF;
      END;
      $$;
    SQL
  end
end
