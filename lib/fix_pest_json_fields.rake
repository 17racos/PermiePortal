namespace :db do
    desc "Fix JSON fields for pests stored as strings (control_methods and natural_enemies)"
    task fix_pest_json_fields: :environment do
      puts "Starting fix of pest JSON fields..."
  
      Pest.find_each do |pest|
        if pest.control_methods.is_a?(String)
          begin
            parsed = JSON.parse(pest.control_methods)
          rescue JSON::ParserError
            parsed = {}
          end
          pest.update_columns(control_methods: parsed)
          puts "Fixed control_methods for Pest ##{pest.id}"
        end
  
        if pest.natural_enemies.is_a?(String)
          begin
            parsed = JSON.parse(pest.natural_enemies)
          rescue JSON::ParserError
            parsed = []
          end
          pest.update_columns(natural_enemies: parsed)
          puts "Fixed natural_enemies for Pest ##{pest.id}"
        end
      end
  
      puts "Pest JSON fields fix complete."
    end
  end
  