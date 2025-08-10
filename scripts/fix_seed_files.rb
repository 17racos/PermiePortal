require 'yaml'

SEED_DIR = Rails.root.join('db', 'seeds')

Dir.glob(SEED_DIR.join('*-data.yml')).each do |file|
  plants = YAML.load_file(file)
  modified = false

  plants.each do |plant|
    unless plant.key?('growth_habit')
      plant['growth_habit'] = 'Tree'  # or "Herb", "Shrub", etc. — default safe guess
      modified = true
    end

    unless plant.key?('data_quality_score')
      plant['data_quality_score'] = 0.8
      modified = true
    end
  end

  if modified
    File.write(file, plants.to_yaml)
    puts "Updated: #{file}"
  end
end

puts "✅ All seed files patched."
