# frozen_string_literal: true
# Helper method to create or update a record
def create_or_update_record(model, find_by_attr, attributes)
  record = model.find_or_initialize_by(find_by_attr => attributes[find_by_attr])
  if record.new_record?
    puts "Creating #{model} - #{attributes[find_by_attr]}"
  else
    puts "Updating #{model} - #{attributes[find_by_attr]}"
  end
  record.assign_attributes(attributes)
  record.save!
rescue ActiveRecord::RecordInvalid => e
  puts "Failed to seed #{model} - #{attributes[find_by_attr]}: #{e.message}"
end

# Load file data based on format
def load_file_data(file_path, format)
  case format
  when :yaml
    YAML.load_file(file_path)
  when :json
    JSON.parse(File.read(file_path))
  when :csv
    CSV.foreach(file_path, headers: true, header_converters: :symbol).map(&:to_h)
  else
    raise ArgumentError, "Unsupported file format: #{format}"
  end
end

# Attach the image file to a record if the image attribute is present
#def attach_image(record, image_filename)
#  return unless image_filename.present?
#
#  image_path = Rails.root.join('db', 'seeds', 'images', image_filename) # Adjust this path if necessary
#  if File.exist?(image_path)
#    record.picture.attach(io: File.open(image_path), filename: image_filename)
#  else
#    puts "Image #{image_filename} not found for #{record.class.name}."
#  end
#end

def map_plant_attributes(data)
  {
    common_name: data['common_name'],
    picture: data['picture'],
    scientific_name: data['scientific_name'],
    aka: data['aka'],
    family: data['family'],
    zone_range: data['zone'],
    perennial: data['perennial'],
    layers: data['layers'],
    plant_functions: data['plant_function'],
    description: data['description'],
    purpose: data['purpose'],
    companions: data['companions'],
    avoid: data['avoid'],
    pests: data['pests'],
    min_temp: data['min_temp'],
    max_temp: data['max_temp'],
    ideal_temp_min: data['ideal_temp_min'],
    ideal_temp_max: data['ideal_temp_max'],
  }
end

# Map attributes for pests
def map_pest_attributes(data)
  {
    name: data['name'],
    slug: data['slug'] || data['name'].parameterize,
    picture: data['picture'],
    scientific_name: data['scientific_name'],
    description: data['description'],
    characteristics: data['characteristics'],
    control_methods: if data['control_methods'].is_a?(Hash)
                       data['control_methods']
    elsif data['control_methods'].is_a?(String) && !data['control_methods'].empty?
      { 'default' => data['control_methods'] }
    else
      {}
    end,
    natural_enemies: if data['natural_enemies'].is_a?(Array)
                       data['natural_enemies']
    elsif data['natural_enemies'].is_a?(String)
      data['natural_enemies'].split(',').map(&:strip)
    else
      []
    end
  }
end

def create_or_update_record(model, identifier, attributes)
  record = model.find_by(identifier => attributes[identifier])
  if record.present?
    # Force update even if record exists
    record.update!(attributes)
    puts "Updated record for #{attributes[identifier]}"
  else
    model.create!(attributes)
    puts "Created record for #{attributes[identifier]}"
  end
end

# Seed pests from all YAML files in the pests subdirectory
def seed_pests
  pests_directory = Rails.root.join('db', 'seeds', 'pests')
  pest_files = Dir.glob("#{pests_directory}/*.yml")

  if pest_files.empty?
    puts "No YAML files found in #{pests_directory}. Skipping pest seeding."
    return
  end

  pest_files.each do |file|
    puts "Seeding pests from #{file}..."
    pests_data = load_file_data(file, :yaml)

    # Use compact to remove any nil entries
    pests_data.compact.each do |data|
      # Debug output to verify the data is as expected
      puts "Processing pest: #{data['name'] || 'Unknown'}"
      attributes = map_pest_attributes(data)
      create_or_update_record(Pest, :name, attributes)
    end
  end

  puts 'Pests seeded successfully!'
end


# Seed plants and establish relationships with pests
def seed_plants
  plant_files = Dir.glob(Rails.root.join('db', 'seeds', '*-data.yml')).reject { |f| f.include?('pests-data.yml') }

  plant_files.each do |file|
    puts "Processing file: #{file}"
    plant_data = load_file_data(file, :yaml)

    plant_data.each do |data|
      attributes = map_plant_attributes(data)
      pests = attributes.delete(:pests) || []

      # Use EnhancedPlant instead of Plant
      plant = EnhancedPlant.find_or_initialize_by(common_name: attributes[:common_name])
      if plant.new_record?
        puts "Creating enhanced plant: #{attributes[:common_name]}"
      else
        puts "Updating enhanced plant: #{attributes[:common_name]}"
      end

      # Map old attributes to new enhanced plant structure
      enhanced_attributes = {
        common_name: attributes[:common_name],
        scientific_name: attributes[:scientific_name],
        family: attributes[:family],
        description_detailed: attributes[:description],
        growing_notes: attributes[:characteristics],
        plant_type: map_plant_type(attributes[:layers]),
        life_cycle: attributes[:perennial] ? 'perennial' : 'annual'
      }

      plant.assign_attributes(enhanced_attributes)
      plant.save!

      # Create environmental requirements if zone data exists
      if attributes[:zone_range].present?
        env_req = plant.environmental_requirements || plant.build_environmental_requirements
        zone_min, zone_max = parse_zone_range(attributes[:zone_range])
        env_req.update!(
          hardiness_zone_min: zone_min,
          hardiness_zone_max: zone_max,
          temp_min_survival: attributes[:min_temp] ? fahrenheit_to_celsius(attributes[:min_temp]) : nil,
          temp_max_survival: attributes[:max_temp] ? fahrenheit_to_celsius(attributes[:max_temp]) : nil,
          temp_optimal_min: attributes[:ideal_temp_min] ? fahrenheit_to_celsius(attributes[:ideal_temp_min]) : nil,
          temp_optimal_max: attributes[:ideal_temp_max] ? fahrenheit_to_celsius(attributes[:ideal_temp_max]) : nil
        )
      end

      # Create plant uses from functions
      if attributes[:plant_functions].present?
        attributes[:plant_functions].each do |function|
          use_category = UseCategory.find_or_create_by(name: function)
          PlantUse.find_or_create_by(
            enhanced_plant: plant,
            use_category: use_category
          ) do |plant_use|
            plant_use.effectiveness_score = 0.8 # Default effectiveness (0.0-1.0 scale)
            plant_use.confidence_score = 0.7   # Default confidence (0.0-1.0 scale)
          end
        end
      end

      # Associate pests with the plant (if pest relationships are still needed)
      if pests.any?
        Pest.where(name: pests)
        # Note: You may need to create a new association table for enhanced plants and pests
        # For now, we'll skip this as the enhanced schema doesn't include pest relationships
      end
    end

    puts "Finished processing file: #{file}"
  end
rescue ActiveRecord::RecordInvalid => e
  puts "Error while seeding plants: #{e.message}"
end

private

def map_plant_type(layers)
  return 'tree' if layers&.include?('Canopy')
  return 'shrub' if layers&.include?('Shrub')
  return 'herbaceous' if layers&.include?('Herbaceous')
  return 'herbaceous' if layers&.include?('Ground') # Map ground cover to herbaceous
  return 'vine' if layers&.include?('Vine')
  'herbaceous' # default
end

def parse_zone_range(zone_range)
  return [nil, nil] if zone_range.blank?

  if zone_range.is_a?(String)
    # Remove parentheses and clean the string
    cleaned = zone_range.gsub(/[()]/, '').strip

    # Split on dash and extract numeric parts
    parts = cleaned.split('-')

    # Extract numeric part from each zone (e.g., "8b" -> 8, "11" -> 11)
    zone_min = parts[0]&.match(/\d+/)&.to_s&.to_i
    zone_max = parts[1]&.match(/\d+/)&.to_s&.to_i

    # Validate zones are in valid range (1-13)
    zone_min = nil if zone_min && (zone_min < 1 || zone_min > 13)
    zone_max = nil if zone_max && (zone_max < 1 || zone_max > 13)

    [zone_min, zone_max]
  elsif zone_range.is_a?(Range)
    [zone_range.begin, zone_range.end]
  else
    [nil, nil]
  end
end

def fahrenheit_to_celsius(fahrenheit)
  return nil if fahrenheit.nil?
  ((fahrenheit.to_f - 32) * 5.0 / 9.0).round(1)
end

# Main seed execution
def run_seeds
  seed_pests        # Step 1: Seed pests first
  seed_plants       # Step 2: Seed plants and establish relationships
  puts 'Seeding completed!'
rescue StandardError => e
  puts "An error occurred during seeding: #{e.message}"
end


# db/seeds.rb

guides = [
  {
    title: 'Vermicomposting',
    body: 'Discover the art of vermicomposting, a sustainable gardening technique that uses worms to turn organic waste into nutrient-rich compost. Vermicomposting helps reduce food waste, enriches your soil with essential nutrients, and supports eco-friendly gardening practices. This guide covers everything from choosing the right worms, like red wigglers, to setting up a worm bin and maintaining a thriving compost system. Perfect for beginners and seasoned gardeners, vermicomposting is an easy and effective way to create organic compost that boosts plant growth and improves soil health. Start your worm composting journey today and transform kitchen scraps into a valuable resource for your garden.',
    image: 'vermicompost.jpg'
  },
  {
    title: 'How to Make a Worm Bin',
    body: 'Creating a DIY worm bin is an easy and affordable way to start vermicomposting at home. A well-designed worm bin provides the perfect environment for red wigglers to thrive while efficiently breaking down food scraps into nutrient-rich compost. This guide walks you through selecting the right container, adding ventilation and drainage, and preparing bedding to keep your worms healthy and productive. Whether you are setting up a bin for an indoor or outdoor composting system, this step-by-step guide ensures success. Build your own worm bin today and take the first step toward sustainable waste reduction and organic soil enrichment!',
    image: 'how-to-make-a-worm-bin.jpg'
  },
  {
    title: 'Turmeric Informational',
    body: 'Turmeric (Curcuma longa), often called the "Golden Spice," is a powerful superfood known for its anti-inflammatory, antioxidant, and immune-boosting properties. This ancient root has been used for centuries in Ayurvedic and Traditional Chinese Medicine to promote health and well-being. The active compound, **curcumin**, is scientifically proven to support joint health, aid digestion, improve brain function, and help prevent chronic diseases such as heart disease, diabetes, and cancer. Turmeric is also a natural remedy for arthritis, skin conditions, and gut health. Learn how to maximize its benefits by combining it with black pepper for enhanced absorption and incorporating it into your diet through golden milk, turmeric tea, or curcumin supplements. Whether used as a culinary spice, herbal remedy, or skincare ingredient, turmeric remains a cornerstone of natural health and holistic wellness. Discover the science behind its healing potential, the best ways to consume it, and how to harness the power of this remarkable spice for optimal health and longevity.',
    image: 'turmeric-informational.jpg'
  },
  {
    title: 'Moringa Informational',
    body: 'Discover the incredible health benefits of Moringa oleifera, also known as the "Miracle Tree." This nutrient-dense superfood is packed with antioxidants, vitamins, and minerals that support immune function, heart health, brain function, and digestive well-being. Moringa is a powerful anti-inflammatory and detoxifying plant that aids in blood sugar regulation, skin rejuvenation, and energy boost. Learn how to incorporate moringa powder, leaves, seeds, and oil into your diet to maximize its medicinal and nutritional properties. Explore the sustainable benefits of moringa for soil restoration, carbon sequestration, and water purification. Whether you are looking for a natural supplement, a plant-based protein source, or a holistic approach to wellness, Moringa is the ultimate superfood for health and sustainability.',
    image: 'moringa-informational.jpg'
  },
  {
    title: 'Plant Families',
    body: 'Unlock the secrets of plant families and discover how understanding botanical relationships can transform your gardening and permaculture practices. This guide explores the major plant families, their unique characteristics, and how they influence companion planting and crop rotation. Learn how grouping plants by family can improve soil health, optimize nutrient cycling, and reduce pests naturally. Whether you are planning a vegetable garden or creating a diverse permaculture system, this guide will help you harness the power of plant families for sustainable and efficient garden design. Perfect for gardeners and permaculture enthusiasts alike, start exploring plant relationships today!',
    image: 'plant-families.jpg'
  },
  {
  title: 'Unlocking Natures Blueprint',
  body: 'Dive deep into the principles of permaculture with this comprehensive guide through the eyes of Bill Molison, one of the founders of Permaculture. Explore the design ethics and innovative techniques that create sustainable, regenerative ecosystems. Learn about closed-loop systems, companion planting, water harvesting, and the integration of plants, animals, and natural elements to build resilient landscapes. Whether you are an experienced practitioner or just beginning your journey, this guide offers valuable insights to transform your garden into a self-sustaining ecosystem.',
  image: 'unlocking-natures-blueprint.jpg'
},
{
  title: 'Importance of Soil Biodiversity',
  body: 'Discover the critical role of soil biodiversity in maintaining healthy, productive landscapes. This guide explains how a vibrant community of microorganisms, earthworms, fungi, and insects work together to enhance nutrient cycling, improve water retention, and suppress diseases. Learn practical strategies to nurture soil life through organic practices, cover cropping, and reduced chemical inputs, ensuring your soil remains a living, thriving foundation for sustainable agriculture.',
  image: 'soil-biodiversity.jpg'
},
]

guides.each do |guide|
  Guide.find_or_create_by(title: guide[:title]) do |g|
    g.body = guide[:body]
    g.image = guide[:image] # Store only the filename, not a full path
  end
end

puts "#{guides.size} guides have been added or updated."

# db/seeds.rb


rotten_article = [
  {
    title: 'We Saved the Lake by Killing It!',
    body: 'We saved the lake by killing it! And now it\'s so clear, you can see the full extent of our brilliance... right down to the dead zone.',
    slug: 'we-saved-the-lake-by-killing-it',
    is_published: true,
    image: 'lake-collapsing.jpg'
  },
  {
    title: 'Grass! Humanity\'s most expensive crop that feeds no one, shelters nothing, and demands everything.',
    body: 'Lawns! Because nothing screams "environmental stewardship" like weekly fossil-fueled grass mutilation. The crown jewel of the American Dream - where we spend thousands to fight nature, kill the soil, to please HOA overlords. What\'s not to love? Because going broke, polluting the air, and fighting nature every weekend is clearly the most logical way to show you\'re a responsible homeowner.',
    slug: 'great-american-lawn',
    is_published: false,
    image: 'green-buzzcut.jpg'
  },
  {
    title: 'Genghis Khan: History\'s Greatest Environmentalist',
    body: 'How one man lowered global carbon levels using nothing but carbon-neutral cavalry operations, low-tech ecological interventions, and the most efficient compost-to-carbon strategy in recorded history. Before Greta, there was Genghis-fighting the good fight for the environment one empire at a time...',
    slug: 'genghis-kahn-historys-greatest-environmentalist',
    is_published: true,
    image: 'genghis-khan-the-enviornmentalist.jpg'
  }
]


rotten_article.each do |article|
  # Make sure slug is properly assigned
  RottenArticle.find_or_initialize_by(slug: article[:slug]).tap do |a|
    a.title = article[:title]
    a.body = article[:body]
    a.is_published = article[:is_published]
    a.image = article[:image]
    a.save!  # Save the article
  end
end

puts "#{rotten_article.size} Rotten Articles have been added or updated."


# Run the seeds
run_seeds

