# frozen_string_literal: true
class UpdatePlantFieldsForFiltering < ActiveRecord::Migration[7.1]
  def change
    # Rename plant_function to plant_functions (keeping the existing array type)
    rename_column :plants, :plant_function, :plant_functions

    # Update zone to be a range
    rename_column :plants, :zone, :zone_range

    # First ensure the zone data is in the correct format (assuming it's in the format "1-10")
    # This will handle any potential data inconsistencies
    execute <<-SQL
      UPDATE plants#{' '}
      SET zone_range = CASE
        WHEN zone_range ~ '^\\d+-\\d+$' THEN#{' '}
          int4range(
            CAST(split_part(zone_range, '-', 1) AS integer),
            CAST(split_part(zone_range, '-', 2) AS integer) + 1
          )::text
        ELSE#{' '}
          '[1,14)'::text  -- Default range if format is invalid
      END;
    SQL

    # Now change the column type to int4range with proper casting
    change_column :plants, :zone_range, :int4range,
      using: "case when zone_range ~ '^\\[\\d+,\\d+\\)$' then zone_range::int4range else '[1,14)'::int4range end"
  end
end