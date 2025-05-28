namespace :enhanced_plants do
  desc "Migrate all existing plants to enhanced schema"
  task migrate: :environment do
    puts "Starting migration of existing plants to enhanced schema..."
    
    migration_service = PlantMigrationService.new
    result = migration_service.migrate_all_plants
    
    puts "\nMigration completed!"
    puts "Successfully migrated: #{result[:migrated]} plants"
    puts "Errors encountered: #{result[:errors]} plants"
    
    if result[:error_details].any?
      puts "\nError details:"
      result[:error_details].each do |error|
        puts "  - #{error[:plant]}: #{error[:error]}"
      end
    end
  end

  desc "Setup default data for enhanced schema"
  task setup_defaults: :environment do
    puts "Setting up default trait categories, use categories, and relationship types..."
    
    migration_service = PlantMigrationService.new
    migration_service.send(:create_default_trait_categories)
    migration_service.send(:create_default_use_categories)
    migration_service.send(:create_default_relationship_types)
    
    puts "Default data setup completed!"
    puts "Trait categories: #{TraitCategory.count}"
    puts "Use categories: #{UseCategory.count}"
    puts "Relationship types: #{RelationshipType.count}"
  end

  desc "Generate embeddings for all enhanced plants"
  task generate_embeddings: :environment do
    if !defined?(EmbeddingService)
      puts "EmbeddingService not available. Skipping embedding generation."
      next
    end

    puts "Generating embeddings for enhanced plants..."
    
    embedding_service = EmbeddingService.new
    count = 0
    errors = 0
    
    EnhancedPlant.where(embedding_vector: nil).find_each do |plant|
      begin
        text_for_embedding = [
          plant.common_name,
          plant.scientific_name,
          plant.description_short,
          plant.growing_notes
        ].compact.join('. ')
        
        embedding = embedding_service.generate_embedding(text_for_embedding)
        plant.update!(embedding_vector: embedding)
        
        count += 1
        print "." if count % 10 == 0
        
        # Rate limiting to avoid API limits
        sleep(0.1)
      rescue => e
        errors += 1
        puts "\nError generating embedding for #{plant.common_name}: #{e.message}"
      end
    end
    
    puts "\nEmbedding generation completed!"
    puts "Generated embeddings for #{count} plants"
    puts "Errors: #{errors}"
  end

  desc "Test search functionality"
  task test_search: :environment do
    puts "Testing enhanced plant search functionality..."
    
    search_service = EnhancedPlantSearchService.new
    
    test_queries = [
      "drought tolerant plants",
      "plants for shade",
      "edible ground cover",
      "nitrogen fixing trees",
      "companion plants for tomatoes"
    ]
    
    test_queries.each do |query|
      puts "\nTesting query: '#{query}'"
      results = search_service.search(query, limit: 5)
      
      if results.any?
        puts "Found #{results.count} results:"
        results.each do |plant|
          puts "  - #{plant.common_name} (#{plant.scientific_name})"
        end
      else
        puts "  No results found"
      end
    end
  end

  desc "Create sample enhanced plants"
  task create_samples: :environment do
    puts "Creating sample enhanced plants..."
    
    # Sample plant 1: Tomato
    tomato = EnhancedPlant.create!(
      common_name: "Tomato",
      scientific_name: "Solanum lycopersicum",
      family: "Solanaceae",
      plant_type: "herbaceous",
      life_cycle: "annual",
      description_short: "Popular warm-season fruit vegetable with red, juicy fruits",
      description_detailed: "Tomato is a tender, warm-season vegetable that produces edible fruits in various sizes, colors, and shapes. Plants can be determinate (bush) or indeterminate (vining) types.",
      growing_notes: "Requires warm soil, consistent moisture, and support for vining varieties. Benefits from mulching and regular feeding.",
      mature_height_min_cm: 30,
      mature_height_max_cm: 200,
      data_quality_score: 0.9
    )

    # Environmental requirements for tomato
    EnvironmentalRequirements.create!(
      enhanced_plant: tomato,
      hardiness_zone_min: 3,
      hardiness_zone_max: 11,
      temp_optimal_min: 18,
      temp_optimal_max: 29,
      light_requirement: "full_sun",
      soil_ph_min: 6.0,
      soil_ph_max: 6.8,
      drought_tolerance_score: 0.3,
      climate_description: "thrives in warm, sunny conditions with consistent moisture"
    )

    # Sample plant 2: Comfrey
    comfrey = EnhancedPlant.create!(
      common_name: "Comfrey",
      scientific_name: "Symphytum officinale",
      family: "Boraginaceae",
      plant_type: "herbaceous",
      life_cycle: "perennial",
      description_short: "Deep-rooted perennial herb excellent for soil improvement and medicinal use",
      description_detailed: "Comfrey is a robust perennial with large, hairy leaves and bell-shaped flowers. Its deep taproot mines nutrients from subsoil layers.",
      growing_notes: "Once established, very difficult to remove. Harvest leaves regularly for best growth. Avoid internal consumption.",
      mature_height_min_cm: 60,
      mature_height_max_cm: 120,
      data_quality_score: 0.85
    )

    # Environmental requirements for comfrey
    EnvironmentalRequirements.create!(
      enhanced_plant: comfrey,
      hardiness_zone_min: 3,
      hardiness_zone_max: 9,
      temp_optimal_min: 10,
      temp_optimal_max: 25,
      light_requirement: "partial_sun",
      soil_ph_min: 6.0,
      soil_ph_max: 7.5,
      drought_tolerance_score: 0.7,
      climate_description: "adaptable to various climates, prefers cool moist conditions"
    )

    puts "Sample plants created successfully!"
    puts "- #{tomato.common_name} (ID: #{tomato.id})"
    puts "- #{comfrey.common_name} (ID: #{comfrey.id})"
  end

  desc "Show enhanced schema statistics"
  task stats: :environment do
    puts "Enhanced Plant Schema Statistics"
    puts "=" * 40
    puts "Enhanced Plants: #{EnhancedPlant.count}"
    puts "Plant Names/Aliases: #{PlantName.count}"
    puts "Trait Categories: #{TraitCategory.count}"
    puts "Plant Traits: #{PlantTrait.count}"
    puts "Environmental Requirements: #{EnvironmentalRequirements.count}"
    puts "Use Categories: #{UseCategory.count}"
    puts "Plant Uses: #{PlantUse.count}"
    puts "Relationship Types: #{RelationshipType.count}"
    puts "Plant Relationships: #{PlantRelationship.count}"
    puts "Plant Guilds: #{PlantGuild.count}"
    puts "Guild Members: #{GuildMember.count}"
    
    if defined?(Region)
      puts "Regions: #{Region.count}"
      puts "Plant Regional Data: #{PlantRegionalData.count}"
    end
    
    puts "\nData Quality Distribution:"
    quality_ranges = [
      [0.0, 0.3, "Low"],
      [0.3, 0.6, "Medium"],
      [0.6, 0.8, "High"],
      [0.8, 1.0, "Very High"]
    ]
    
    quality_ranges.each do |min, max, label|
      count = EnhancedPlant.where(data_quality_score: min..max).count
      puts "  #{label} (#{min}-#{max}): #{count} plants"
    end
    
    # Check if embedding_vector column exists before querying
    if EnhancedPlant.column_names.include?('embedding_vector')
      puts "\nPlants with embeddings: #{EnhancedPlant.where.not(embedding_vector: nil).count}"
    else
      puts "\nEmbedding vectors: Not available (vector extension not installed)"
    end
  end

  desc "Validate enhanced schema data integrity"
  task validate: :environment do
    puts "Validating enhanced schema data integrity..."
    
    errors = []
    
    # Check for plants without environmental requirements
    plants_without_env = EnhancedPlant.left_joins(:environmental_requirements)
                                     .where(environmental_requirements: { id: nil })
    if plants_without_env.any?
      errors << "#{plants_without_env.count} plants missing environmental requirements"
    end
    
    # Check for invalid trait values
    invalid_traits = PlantTrait.joins(:trait_category)
                              .where(trait_categories: { data_type: 'numeric' })
                              .where(numeric_value: nil, numeric_min: nil, numeric_max: nil)
    if invalid_traits.any?
      errors << "#{invalid_traits.count} numeric traits with no values"
    end
    
    # Check for orphaned relationships
    orphaned_relationships = PlantRelationship.left_joins(:plant_a, :plant_b)
                                             .where(enhanced_plants: { id: nil })
    if orphaned_relationships.any?
      errors << "#{orphaned_relationships.count} orphaned plant relationships"
    end
    
    if errors.any?
      puts "Validation errors found:"
      errors.each { |error| puts "  - #{error}" }
    else
      puts "All validations passed!"
    end
  end

  desc "Run full setup (migrate, setup defaults, create samples)"
  task full_setup: :environment do
    puts "Running full enhanced plant schema setup..."
    
    Rake::Task['enhanced_plants:setup_defaults'].invoke
    Rake::Task['enhanced_plants:migrate'].invoke
    Rake::Task['enhanced_plants:create_samples'].invoke
    Rake::Task['enhanced_plants:stats'].invoke
    
    puts "\nFull setup completed!"
    puts "You can now test the search functionality with:"
    puts "  rake enhanced_plants:test_search"
    puts "\nTo generate embeddings for semantic search:"
    puts "  rake enhanced_plants:generate_embeddings"
  end
end 