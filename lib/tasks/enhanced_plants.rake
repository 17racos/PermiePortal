# frozen_string_literal: true
namespace :enhanced_plants do
  desc 'Migrate all existing plants to enhanced schema'
  task migrate: :environment do
    puts 'Starting migration of existing plants to enhanced schema...'

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

  desc 'Setup default data (trait categories, use categories, relationship types, semantic tags)'
  task setup_defaults: :environment do
    puts 'Setting up default enhanced plant data...'

    # Load enhanced semantic tags
    puts "\n=== Loading Enhanced Semantic Tags ==="
    load Rails.root.join('db', 'seeds', 'enhanced_semantic_tags.rb')

    # Create default trait categories
    puts "\n=== Creating Trait Categories ==="
    trait_categories = [
      { name: 'Physical Characteristics', data_type: 'categorical', description: 'Physical traits like size, color, texture' },
      { name: 'Growth Habits', data_type: 'categorical', description: 'How the plant grows and spreads' },
      { name: 'Flowering', data_type: 'categorical', description: 'Flowering characteristics and timing' },
      { name: 'Hardiness', data_type: 'numeric', description: 'Cold hardiness and temperature tolerance' },
      { name: 'Water Requirements', data_type: 'categorical', description: 'Water needs and drought tolerance' },
      { name: 'Light Requirements', data_type: 'categorical', description: 'Sunlight preferences' },
      { name: 'Soil Preferences', data_type: 'categorical', description: 'Soil type and pH preferences' },
      { name: 'Maintenance', data_type: 'categorical', description: 'Care requirements and maintenance level' },
      { name: 'Wildlife Value', data_type: 'categorical', description: 'Value to wildlife and pollinators' },
      { name: 'Special Features', data_type: 'categorical', description: 'Unique or notable characteristics' }
    ]

    trait_categories.each do |category_data|
      category = TraitCategory.find_or_create_by(name: category_data[:name]) do |cat|
        cat.data_type = category_data[:data_type]
        cat.description = category_data[:description]
      end
      puts "✓ #{category.name}"
    end

    # Create default use categories
    puts "\n=== Creating Use Categories ==="
    use_categories = [
      { name: 'Edible', parent: nil, description: 'Plants with edible parts' },
      { name: 'Fruits', parent: 'Edible', description: 'Edible fruits and berries' },
      { name: 'Vegetables', parent: 'Edible', description: 'Edible vegetables and greens' },
      { name: 'Herbs', parent: 'Edible', description: 'Culinary and medicinal herbs' },
      { name: 'Nuts', parent: 'Edible', description: 'Edible nuts and seeds' },
      { name: 'Medicinal', parent: nil, description: 'Plants with medicinal properties' },
      { name: 'Ornamental', parent: nil, description: 'Plants grown for beauty' },
      { name: 'Flowers', parent: 'Ornamental', description: 'Flowering ornamental plants' },
      { name: 'Foliage', parent: 'Ornamental', description: 'Plants grown for attractive foliage' },
      { name: 'Functional', parent: nil, description: 'Plants with practical functions' },
      { name: 'Nitrogen Fixation', parent: 'Functional', description: 'Plants that fix nitrogen' },
      { name: 'Erosion Control', parent: 'Functional', description: 'Plants that prevent erosion' },
      { name: 'Windbreak', parent: 'Functional', description: 'Plants that provide wind protection' },
      { name: 'Wildlife', parent: nil, description: 'Plants that support wildlife' },
      { name: 'Pollinator Support', parent: 'Wildlife', description: 'Plants that support pollinators' },
      { name: 'Bird Food', parent: 'Wildlife', description: 'Plants that provide food for birds' }
    ]

    # Create parent categories first, then children
    use_categories.select { |cat| cat[:parent].nil? }.each do |category_data|
      category = UseCategory.find_or_create_by(name: category_data[:name]) do |cat|
        cat.description = category_data[:description]
      end
      puts "✓ #{category.name}"
    end

    use_categories.select { |cat| cat[:parent].present? }.each do |category_data|
      parent = UseCategory.find_by(name: category_data[:parent])
      category = UseCategory.find_or_create_by(name: category_data[:name]) do |cat|
        cat.parent = parent
        cat.description = category_data[:description]
      end
      puts "✓ #{category.name} (parent: #{parent&.name})"
    end

    # Create default relationship types
    puts "\n=== Creating Relationship Types ==="
    relationship_types = [
      { name: 'beneficial', description: 'Plants that help each other grow' },
      { name: 'antagonistic', description: 'Plants that inhibit each other' },
      { name: 'neutral', description: 'Plants with no significant interaction' },
      { name: 'companion', description: 'Traditional companion planting pairs' },
      { name: 'guild_member', description: 'Plants that work well in guilds together' }
    ]

    relationship_types.each do |type_data|
      rel_type = RelationshipType.find_or_create_by(name: type_data[:name]) do |rt|
        rt.description = type_data[:description]
      end
      puts "✓ #{rel_type.name}"
    end

    puts "\nDefault data setup completed!"
    puts "Semantic tags: #{SemanticTag.count}"
    puts "Trait categories: #{TraitCategory.count}"
    puts "Use categories: #{UseCategory.count}"
    puts "Relationship types: #{RelationshipType.count}"
  end

  desc 'Generate embeddings for all enhanced plants'
  task generate_embeddings: :environment do
    if !defined?(EmbeddingService)
      puts 'EmbeddingService not available. Skipping embedding generation.'
      next
    end

    puts 'Generating embeddings for enhanced plants...'

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
        print '.' if count % 10 == 0

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

  desc 'Test search functionality'
  task test_search: :environment do
    puts 'Testing enhanced plant search functionality...'

    search_service = EnhancedPlantSearchService.new

    test_queries = [
      'drought tolerant plants',
      'plants for shade',
      'edible ground cover',
      'nitrogen fixing trees',
      'companion plants for tomatoes'
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
        puts '  No results found'
      end
    end
  end

  desc 'Create sample enhanced plants'
  task create_samples: :environment do
    puts 'Creating sample enhanced plants...'

    # Sample plant 1: Tomato
    tomato = EnhancedPlant.create!(
      common_name: 'Tomato',
      scientific_name: 'Solanum lycopersicum',
      family: 'Solanaceae',
      plant_type: 'herbaceous',
      life_cycle: 'annual',
      description_short: 'Popular warm-season fruit vegetable with red, juicy fruits',
      description_detailed: 'Tomato is a tender, warm-season vegetable that produces edible fruits in various sizes, colors, and shapes. Plants can be determinate (bush) or indeterminate (vining) types.',
      growing_notes: 'Requires warm soil, consistent moisture, and support for vining varieties. Benefits from mulching and regular feeding.',
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
      light_requirement: 'full_sun',
      soil_ph_min: 6.0,
      soil_ph_max: 6.8,
      drought_tolerance_score: 0.3,
      climate_description: 'thrives in warm, sunny conditions with consistent moisture'
    )

    # Sample plant 2: Comfrey
    comfrey = EnhancedPlant.create!(
      common_name: 'Comfrey',
      scientific_name: 'Symphytum officinale',
      family: 'Boraginaceae',
      plant_type: 'herbaceous',
      life_cycle: 'perennial',
      description_short: 'Deep-rooted perennial herb excellent for soil improvement and medicinal use',
      description_detailed: 'Comfrey is a robust perennial with large, hairy leaves and bell-shaped flowers. Its deep taproot mines nutrients from subsoil layers.',
      growing_notes: 'Once established, very difficult to remove. Harvest leaves regularly for best growth. Avoid internal consumption.',
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
      light_requirement: 'partial_sun',
      soil_ph_min: 6.0,
      soil_ph_max: 7.5,
      drought_tolerance_score: 0.7,
      climate_description: 'adaptable to various climates, prefers cool moist conditions'
    )

    puts 'Sample plants created successfully!'
    puts "- #{tomato.common_name} (ID: #{tomato.id})"
    puts "- #{comfrey.common_name} (ID: #{comfrey.id})"
  end

  desc 'Show enhanced schema statistics'
  task stats: :environment do
    puts 'Enhanced Plant Schema Statistics'
    puts '=' * 40
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
      [0.0, 0.3, 'Low'],
      [0.3, 0.6, 'Medium'],
      [0.6, 0.8, 'High'],
      [0.8, 1.0, 'Very High']
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

  desc 'Validate enhanced schema data integrity'
  task validate: :environment do
    puts 'Validating enhanced schema data integrity...'

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
      puts 'Validation errors found:'
      errors.each { |error| puts "  - #{error}" }
    else
      puts 'All validations passed!'
    end
  end

  desc 'Full setup: migrate, setup defaults, and tag plants'
  task full_setup: :environment do
    puts 'Starting full enhanced plants setup...'

    # Step 1: Migrate existing plants
    puts "\n=== Step 1: Migrating existing plants ==="
    Rake::Task['enhanced_plants:migrate'].invoke

    # Step 2: Setup default data
    puts "\n=== Step 2: Setting up default data ==="
    Rake::Task['enhanced_plants:setup_defaults'].invoke

    # Step 3: Enhanced comprehensive tagging
    puts "\n=== Step 3: Enhanced comprehensive tagging ==="
    Rake::Task['enhanced_plants:enhanced_comprehensive_tag'].invoke

    # Step 4: Show final statistics
    puts "\n=== Step 4: Final statistics ==="
    Rake::Task['enhanced_plants:stats'].invoke

    puts "\n✅ Full enhanced plants setup completed!"
    puts 'Your enhanced plant database is ready to use.'
  end

  desc 'Auto-tag all plants with semantic tags'
  task auto_tag: :environment do
    puts 'Running enhanced auto-tagging for all plants...'

    # First ensure semantic tags exist
    if SemanticTag.count == 0
      puts 'Setting up semantic tags...'
      load Rails.root.join('db', 'seeds', 'enhanced_semantic_tags.rb')
    else
      puts "Semantic tags already exist (#{SemanticTag.count} tags)"
    end

    # Run comprehensive auto-tagging
    puts 'Auto-tagging plants with semantic tags...'
    tagged_count = 0
    total_tags_added = 0

    # Manual tagging for specific plants that we know should have certain tags
    puts 'Applying manual semantic tag associations...'

    # Edible plants
    edible_plant_names = [
      'Tomato', 'Carrot', 'Broccoli', 'Asparagus', 'Avocado',
      'Blueberry', 'Coconut Tree', 'Banana', 'Almond Tree', 'Bok Choy',
      'Apple', 'Orange', 'Lemon', 'Strawberry', 'Grape', 'Peach',
      'Lettuce', 'Spinach', 'Kale', 'Cabbage', 'Onion', 'Garlic'
    ]

    edible_plants = EnhancedPlant.where(common_name: edible_plant_names)
    edible_tag = SemanticTag.find_by(name: 'edible')

    if edible_tag
      edible_plants.each do |plant|
        unless plant.plant_semantic_tags.where(semantic_tag: edible_tag).exists?
          plant.plant_semantic_tags.create!(
            semantic_tag: edible_tag,
            confidence_score: 0.9,
            source: 'manual'
          )
          total_tags_added += 1
        end
      end
      puts "Tagged #{edible_plants.count} plants as edible"
    end

    # Medicinal plants
    medicinal_plant_names = [
      'Aloe', 'Chamomile', 'Calendula', 'Ashwagandha', 'Comfrey', 'Echinacea',
      'Ginseng', 'Turmeric', 'Ginger', 'Lavender', 'Peppermint', 'Sage'
    ]

    medicinal_plants = EnhancedPlant.where(common_name: medicinal_plant_names)
    medicinal_tag = SemanticTag.find_by(name: 'medicinal')

    if medicinal_tag
      medicinal_plants.each do |plant|
        unless plant.plant_semantic_tags.where(semantic_tag: medicinal_tag).exists?
          plant.plant_semantic_tags.create!(
            semantic_tag: medicinal_tag,
            confidence_score: 0.9,
            source: 'manual'
          )
          total_tags_added += 1
        end
      end
      puts "Tagged #{medicinal_plants.count} plants as medicinal"
    end

    # Nitrogen fixing plants (legumes)
    legume_plants = EnhancedPlant.where(
      'family ILIKE ? OR family ILIKE ?',
      '%leguminosae%', '%fabaceae%'
    )
    nitrogen_fixing_tag = SemanticTag.find_by(name: 'nitrogen_fixing')

    if nitrogen_fixing_tag
      legume_plants.each do |plant|
        unless plant.plant_semantic_tags.where(semantic_tag: nitrogen_fixing_tag).exists?
          plant.plant_semantic_tags.create!(
            semantic_tag: nitrogen_fixing_tag,
            confidence_score: 0.9,
            source: 'extracted'
          )
          total_tags_added += 1
        end
      end
      puts "Tagged #{legume_plants.count} legume plants as nitrogen_fixing"
    end

    # Ground cover plants
    groundcover_patterns = [
      'Chickweed', 'Creeping', 'Moss', 'Ivy', 'Vinca', 'Ajuga'
    ]

    groundcover_plants = EnhancedPlant.where(
      groundcover_patterns.map { |pattern| 'common_name ILIKE ?' }.join(' OR '),
      *groundcover_patterns.map { |pattern| "%#{pattern}%" }
    )
    groundcover_tag = SemanticTag.find_by(name: 'ground_cover')

    if groundcover_tag
      groundcover_plants.each do |plant|
        unless plant.plant_semantic_tags.where(semantic_tag: groundcover_tag).exists?
          plant.plant_semantic_tags.create!(
            semantic_tag: groundcover_tag,
            confidence_score: 0.8,
            source: 'extracted'
          )
          total_tags_added += 1
        end
      end
      puts "Tagged #{groundcover_plants.count} plants as ground_cover"
    end

    # Aromatic plants
    aromatic_patterns = [
      'mint', 'basil', 'rosemary', 'thyme', 'lavender', 'sage',
      'oregano', 'cilantro', 'parsley', 'dill', 'fennel'
    ]

    aromatic_plants = EnhancedPlant.where(
      aromatic_patterns.map { |pattern| 'common_name ILIKE ?' }.join(' OR '),
      *aromatic_patterns.map { |pattern| "%#{pattern}%" }
    )
    aromatic_tag = SemanticTag.find_by(name: 'aromatic')

    if aromatic_tag
      aromatic_plants.each do |plant|
        unless plant.plant_semantic_tags.where(semantic_tag: aromatic_tag).exists?
          plant.plant_semantic_tags.create!(
            semantic_tag: aromatic_tag,
            confidence_score: 0.8,
            source: 'extracted'
          )
          total_tags_added += 1
        end
      end
      puts "Tagged #{aromatic_plants.count} plants as aromatic"
    end

    # Now run algorithmic auto-tagging for remaining plants
    puts 'Running algorithmic auto-tagging...'

    EnhancedPlant.find_each do |plant|
      begin
        tags_added_for_plant = 0

        # Check for drought tolerance based on environmental requirements
        if plant.environmental_requirements&.drought_tolerance_score &&
           plant.environmental_requirements.drought_tolerance_score > 0.6
          drought_tag = SemanticTag.find_by(name: 'drought_tolerant')
          if drought_tag && !plant.plant_semantic_tags.where(semantic_tag: drought_tag).exists?
            plant.plant_semantic_tags.create!(
              semantic_tag: drought_tag,
              confidence_score: 0.8,
              source: 'extracted'
            )
            tags_added_for_plant += 1
          end
        end

        # Check for pollinator friendly based on descriptions
        if plant.description_detailed&.match?(/pollinator|bee|butterfly|flower/i) ||
           plant.growing_notes&.match?(/pollinator|bee|butterfly|flower/i)
          pollinator_tag = SemanticTag.find_by(name: 'pollinator_friendly')
          if pollinator_tag && !plant.plant_semantic_tags.where(semantic_tag: pollinator_tag).exists?
            plant.plant_semantic_tags.create!(
              semantic_tag: pollinator_tag,
              confidence_score: 0.7,
              source: 'extracted'
            )
            tags_added_for_plant += 1
          end
        end

        # Check for cold hardy based on zone ranges
        if plant.environmental_requirements&.hardiness_zone_min &&
           plant.environmental_requirements.hardiness_zone_min <= 5
          cold_hardy_tag = SemanticTag.find_by(name: 'cold_hardy')
          if cold_hardy_tag && !plant.plant_semantic_tags.where(semantic_tag: cold_hardy_tag).exists?
            plant.plant_semantic_tags.create!(
              semantic_tag: cold_hardy_tag,
              confidence_score: 0.8,
              source: 'extracted'
            )
            tags_added_for_plant += 1
          end
        end

        # Check for tropical based on zone ranges
        if plant.environmental_requirements&.hardiness_zone_min &&
           plant.environmental_requirements.hardiness_zone_min >= 9
          tropical_tag = SemanticTag.find_by(name: 'tropical')
          if tropical_tag && !plant.plant_semantic_tags.where(semantic_tag: tropical_tag).exists?
            plant.plant_semantic_tags.create!(
              semantic_tag: tropical_tag,
              confidence_score: 0.8,
              source: 'extracted'
            )
            tags_added_for_plant += 1
          end
        end

        # Check for container suitable based on size
        if plant.mature_height_max_cm && plant.mature_height_max_cm <= 200
          container_tag = SemanticTag.find_by(name: 'container_suitable')
          if container_tag && !plant.plant_semantic_tags.where(semantic_tag: container_tag).exists?
            plant.plant_semantic_tags.create!(
              semantic_tag: container_tag,
              confidence_score: 0.7,
              source: 'extracted'
            )
            tags_added_for_plant += 1
          end
        end

        if tags_added_for_plant > 0
          tagged_count += 1
          total_tags_added += tags_added_for_plant
        end

        print '.' if tagged_count % 10 == 0

      rescue => e
        puts "\nError tagging #{plant.common_name}: #{e.message}"
      end
    end

    puts "\nAuto-tagging completed!"
    puts "Plants tagged: #{tagged_count}"
    puts "Total tags added: #{total_tags_added}"
    puts "Semantic tags in database: #{SemanticTag.count}"
    puts "Plant-tag associations: #{PlantSemanticTag.count}"

    # Show summary of tags
    puts "\nSemantic tag summary:"
    PlantSemanticTag.joins(:semantic_tag)
                    .group('semantic_tags.name')
                    .count
                    .sort_by { |k, v| -v }
                    .each { |tag, count| puts "  #{tag}: #{count} plants" }
  end

  desc 'Reset and rebuild all semantic tag associations'
  task reset_semantic_tags: :environment do
    puts 'Resetting and rebuilding all semantic tag associations...'

    # Clear existing associations
    puts 'Clearing existing plant-semantic tag associations...'
    PlantSemanticTag.delete_all

    # Run auto-tagging from scratch
    Rake::Task['enhanced_plants:auto_tag'].invoke

    puts "\nSemantic tag reset and rebuild completed!"
  end

  desc 'Verify quick filter semantic tags are working'
  task verify_quick_filters: :environment do
    puts 'Verifying quick filter semantic tags...'

    search_service = EnhancedPlantSearchService.new

    quick_filter_tags = [
      'edible', 'medicinal', 'pollinator_friendly', 'drought_tolerant',
      'nitrogen_fixing', 'ground_cover', 'aromatic', 'container_suitable', 'cold_hardy'
    ]

    all_working = true

    quick_filter_tags.each do |tag|
      begin
        result = search_service.search(semantic_tags: [tag])
        count = result.count

        if count > 0
          puts "✓ #{tag}: #{count} plants"
        else
          puts "✗ #{tag}: 0 plants (NO RESULTS)"
          all_working = false
        end
      rescue => e
        puts "✗ #{tag}: ERROR - #{e.message}"
        all_working = false
      end
    end

    puts "\n" + '='*50
    if all_working
      puts '✓ All quick filters are working correctly!'
    else
      puts "✗ Some quick filters have issues. Run 'rake enhanced_plants:auto_tag' to fix."
    end
    puts '='*50
  end

  desc 'Comprehensive semantic tagging for all plants'
  task comprehensive_tag: :environment do
    puts 'Running comprehensive semantic tagging for all plants...'

    total_tags_added = 0
    plants_updated = 0

    EnhancedPlant.find_each do |plant|
      tags_added_for_plant = 0

      # Get plant data for analysis
      description = [plant.description_detailed, plant.description_short, plant.growing_notes].compact.join(' ').downcase
      common_name = plant.common_name.downcase
      plant.scientific_name.downcase
      plant.family&.downcase || ''

      # Get plant uses for analysis
      use_names = plant.plant_uses.joins(:use_category).pluck('use_categories.name').map(&:downcase)

      # EDIBLE TAGGING - Enhanced detection
      edible_patterns = [
        /\b(edible|food|eat|culinary|cuisine|cooking|fruit|berry|nut|seed|leaf|root|tuber|vegetable)\b/,
        /\b(harvest|crop|produce|yield|nutrition|vitamin|protein|carbohydrate)\b/,
        /\b(salad|soup|tea|juice|oil|spice|herb|seasoning|flavor)\b/
      ]

      if edible_patterns.any? { |pattern| description.match?(pattern) } ||
         use_names.any? { |use| use.match?(/food|edible|culinary|fruit|vegetable|herb|spice/) } ||
         common_name.match?(/\b(apple|orange|lemon|tomato|carrot|lettuce|spinach|basil|mint|oregano|thyme|rosemary|sage|parsley|cilantro|dill|fennel|chive|onion|garlic|potato|bean|pea|corn|squash|cucumber|pepper|berry|grape|peach|plum|cherry|strawberry|blueberry|raspberry|blackberry)\b/)

        edible_tag = SemanticTag.find_by(name: 'edible')
        if edible_tag && !plant.plant_semantic_tags.where(semantic_tag: edible_tag).exists?
          plant.plant_semantic_tags.create!(
            semantic_tag: edible_tag,
            confidence_score: 0.8,
            source: 'extracted'
          )
          tags_added_for_plant += 1
        end
      end

      # MEDICINAL TAGGING - Enhanced detection
      medicinal_patterns = [
        /\b(medicinal|medicine|healing|therapeutic|remedy|treatment|cure|health)\b/,
        /\b(antiseptic|antibacterial|anti-inflammatory|antioxidant|analgesic|sedative)\b/,
        /\b(traditional.*medicine|folk.*medicine|herbal.*medicine|natural.*remedy)\b/,
        /\b(tea|tincture|extract|essential.*oil|poultice|salve|ointment)\b/
      ]

      if medicinal_patterns.any? { |pattern| description.match?(pattern) } ||
         use_names.any? { |use| use.match?(/medicinal|medicine|healing|therapeutic|remedy/) } ||
         common_name.match?(/\b(aloe|chamomile|calendula|echinacea|ginseng|turmeric|ginger|lavender|peppermint|sage|willow|elderberry|ginkgo|valerian|st.*john|milk.*thistle)\b/)

        medicinal_tag = SemanticTag.find_by(name: 'medicinal')
        if medicinal_tag && !plant.plant_semantic_tags.where(semantic_tag: medicinal_tag).exists?
          plant.plant_semantic_tags.create!(
            semantic_tag: medicinal_tag,
            confidence_score: 0.8,
            source: 'extracted'
          )
          tags_added_for_plant += 1
        end
      end

      # AROMATIC TAGGING - Enhanced detection
      aromatic_patterns = [
        /\b(aromatic|fragrant|scented|perfume|essential.*oil|volatile.*oil)\b/,
        /\b(smell|aroma|fragrance|scent|odor|perfumed)\b/,
        /\b(mint|basil|rosemary|thyme|lavender|sage|oregano|cilantro|parsley|dill|fennel)\b/
      ]

      if aromatic_patterns.any? { |pattern| description.match?(pattern) } ||
         common_name.match?(/\b(mint|basil|rosemary|thyme|lavender|sage|oregano|cilantro|parsley|dill|fennel|jasmine|rose|gardenia|honeysuckle|lilac|pine|cedar|eucalyptus)\b/)

        aromatic_tag = SemanticTag.find_by(name: 'aromatic')
        if aromatic_tag && !plant.plant_semantic_tags.where(semantic_tag: aromatic_tag).exists?
          plant.plant_semantic_tags.create!(
            semantic_tag: aromatic_tag,
            confidence_score: 0.8,
            source: 'extracted'
          )
          tags_added_for_plant += 1
        end
      end

      # POLLINATOR FRIENDLY - Enhanced detection
      pollinator_patterns = [
        /\b(pollinator|bee|butterfly|hummingbird|nectar|pollen|attract.*bee|attract.*butterfly)\b/,
        /\b(flower|bloom|blossom|flowering|blooming|colorful.*flower|showy.*flower)\b/,
        /\b(native.*bee|honey.*bee|bumble.*bee|beneficial.*insect)\b/
      ]

      if pollinator_patterns.any? { |pattern| description.match?(pattern) } ||
         use_names.any? { |use| use.match?(/pollinator|wildlife|bee|butterfly/) } ||
         description.match?(/flower/) && plant.plant_type.in?(['herbaceous', 'shrub', 'tree'])

        pollinator_tag = SemanticTag.find_by(name: 'pollinator_friendly')
        if pollinator_tag && !plant.plant_semantic_tags.where(semantic_tag: pollinator_tag).exists?
          plant.plant_semantic_tags.create!(
            semantic_tag: pollinator_tag,
            confidence_score: 0.7,
            source: 'extracted'
          )
          tags_added_for_plant += 1
        end
      end

      # GROUND COVER - Enhanced detection
      groundcover_patterns = [
        /\b(ground.*cover|groundcover|carpet|mat|spreading|creeping|trailing)\b/,
        /\b(low.*growing|prostrate|horizontal|runner|stolon)\b/,
        /\b(erosion.*control|slope.*stabilization|bank.*cover)\b/
      ]

      if groundcover_patterns.any? { |pattern| description.match?(pattern) } ||
         use_names.any? { |use| use.match?(/ground.*cover|erosion.*control/) } ||
         common_name.match?(/\b(creeping|trailing|carpet|moss|ivy|vinca|ajuga|sedum|thyme|clover)\b/) ||
         (plant.mature_height_max_cm && plant.mature_height_max_cm <= 50)

        groundcover_tag = SemanticTag.find_by(name: 'ground_cover')
        if groundcover_tag && !plant.plant_semantic_tags.where(semantic_tag: groundcover_tag).exists?
          plant.plant_semantic_tags.create!(
            semantic_tag: groundcover_tag,
            confidence_score: 0.8,
            source: 'extracted'
          )
          tags_added_for_plant += 1
        end
      end

      # DEER RESISTANT - Enhanced detection
      deer_resistant_patterns = [
        /\b(deer.*resistant|deer.*proof|deer.*repellent|deer.*deterrent)\b/,
        /\b(thorny|spiny|prickly|toxic|poisonous|bitter|strong.*scent)\b/,
        /\b(avoid.*deer|deer.*don.*eat|deer.*dislike)\b/
      ]

      if deer_resistant_patterns.any? { |pattern| description.match?(pattern) } ||
         common_name.match?(/\b(lavender|rosemary|sage|marigold|nasturtium|foxglove|oleander|barberry|holly|juniper)\b/)

        deer_resistant_tag = SemanticTag.find_by(name: 'deer_resistant')
        if deer_resistant_tag && !plant.plant_semantic_tags.where(semantic_tag: deer_resistant_tag).exists?
          plant.plant_semantic_tags.create!(
            semantic_tag: deer_resistant_tag,
            confidence_score: 0.7,
            source: 'extracted'
          )
          tags_added_for_plant += 1
        end
      end

      # EVERGREEN/DECIDUOUS - Enhanced detection
      if plant.plant_type.in?(['tree', 'shrub'])
        evergreen_patterns = [
          /\b(evergreen|year.*round.*foliage|persistent.*leaves|retains.*leaves)\b/,
          /\b(pine|fir|spruce|cedar|juniper|holly|rhododendron|boxwood|yew)\b/
        ]

        deciduous_patterns = [
          /\b(deciduous|loses.*leaves|drops.*leaves|seasonal.*foliage|fall.*color|autumn.*color)\b/,
          /\b(maple|oak|birch|elm|ash|cherry|apple|pear|willow|poplar)\b/
        ]

        if evergreen_patterns.any? { |pattern| description.match?(pattern) } ||
           common_name.match?(/\b(pine|fir|spruce|cedar|juniper|holly|rhododendron|boxwood|yew|arborvitae)\b/)

          evergreen_tag = SemanticTag.find_by(name: 'evergreen')
          if evergreen_tag && !plant.plant_semantic_tags.where(semantic_tag: evergreen_tag).exists?
            plant.plant_semantic_tags.create!(
              semantic_tag: evergreen_tag,
              confidence_score: 0.8,
              source: 'extracted'
            )
            tags_added_for_plant += 1
          end
        end

        if deciduous_patterns.any? { |pattern| description.match?(pattern) } ||
           common_name.match?(/\b(maple|oak|birch|elm|ash|cherry|apple|pear|willow|poplar|dogwood|redbud)\b/)

          deciduous_tag = SemanticTag.find_by(name: 'deciduous')
          if deciduous_tag && !plant.plant_semantic_tags.where(semantic_tag: deciduous_tag).exists?
            plant.plant_semantic_tags.create!(
              semantic_tag: deciduous_tag,
              confidence_score: 0.8,
              source: 'extracted'
            )
            tags_added_for_plant += 1
          end
        end
      end

      # NATIVE - Enhanced detection
      native_patterns = [
        /\b(native|indigenous|local|regional|wild|naturalized)\b/,
        /\b(native.*to|indigenous.*to|endemic.*to|naturally.*occurring)\b/
      ]

      if native_patterns.any? { |pattern| description.match?(pattern) }
        native_tag = SemanticTag.find_by(name: 'native')
        if native_tag && !plant.plant_semantic_tags.where(semantic_tag: native_tag).exists?
          plant.plant_semantic_tags.create!(
            semantic_tag: native_tag,
            confidence_score: 0.7,
            source: 'extracted'
          )
          tags_added_for_plant += 1
        end
      end

      # INVASIVE - Enhanced detection
      invasive_patterns = [
        /\b(invasive|aggressive|spreading|weedy|naturalized|escaped)\b/,
        /\b(control.*spread|contain|aggressive.*grower|takes.*over)\b/
      ]

      if invasive_patterns.any? { |pattern| description.match?(pattern) }
        invasive_tag = SemanticTag.find_by(name: 'invasive')
        if invasive_tag && !plant.plant_semantic_tags.where(semantic_tag: invasive_tag).exists?
          plant.plant_semantic_tags.create!(
            semantic_tag: invasive_tag,
            confidence_score: 0.7,
            source: 'extracted'
          )
          tags_added_for_plant += 1
        end
      end

      # SELF SEEDING - Enhanced detection
      self_seeding_patterns = [
        /\b(self.*seed|self.*sow|volunteer|reseed|naturalize|spread.*by.*seed)\b/,
        /\b(prolific.*seeder|abundant.*seed|easy.*from.*seed)\b/
      ]

      if self_seeding_patterns.any? { |pattern| description.match?(pattern) }
        self_seeding_tag = SemanticTag.find_by(name: 'self_seeding')
        if self_seeding_tag && !plant.plant_semantic_tags.where(semantic_tag: self_seeding_tag).exists?
          plant.plant_semantic_tags.create!(
            semantic_tag: self_seeding_tag,
            confidence_score: 0.7,
            source: 'extracted'
          )
          tags_added_for_plant += 1
        end
      end

      if tags_added_for_plant > 0
        plants_updated += 1
        total_tags_added += tags_added_for_plant
        print '.' if plants_updated % 10 == 0
      end
    end

    puts "\nComprehensive tagging completed!"
    puts "Plants updated: #{plants_updated}"
    puts "Total tags added: #{total_tags_added}"
    puts "Total plant-tag associations: #{PlantSemanticTag.count}"

    # Show updated summary
    puts "\nUpdated semantic tag summary:"
    PlantSemanticTag.joins(:semantic_tag)
                    .group('semantic_tags.name')
                    .count
                    .sort_by { |k, v| -v }
                    .each { |tag, count| puts "  #{tag}: #{count} plants" }
  end

  desc 'Enhanced comprehensive semantic tagging with advanced patterns'
  task enhanced_comprehensive_tag: :environment do
    puts 'Running enhanced comprehensive semantic tagging for all plants...'

    # Define comprehensive tag patterns with confidence scores
    tag_patterns = {
      # Growth characteristics
      'fast_growing' => { patterns: ['fast grow', 'rapid grow', 'quick grow', 'vigorous grow'], confidence: 0.8 },
      'slow_growing' => { patterns: ['slow grow', 'slow-growing', 'takes time'], confidence: 0.8 },
      'compact' => { patterns: ['compact', 'dwarf', 'small', 'miniature'], confidence: 0.9 },
      'spreading' => { patterns: ['spread', 'runner', 'rhizome', 'stolons'], confidence: 0.9 },
      'climbing' => { patterns: ['climb', 'vine', 'twining'], confidence: 0.9 },
      'trailing' => { patterns: ['trail', 'cascade', 'hanging'], confidence: 0.8 },

      # Seasonal characteristics
      'spring_blooming' => { patterns: ['spring bloom', 'early bloom', 'march bloom', 'april bloom', 'may bloom'], confidence: 0.8 },
      'summer_blooming' => { patterns: ['summer bloom', 'june bloom', 'july bloom', 'august bloom'], confidence: 0.8 },
      'fall_blooming' => { patterns: ['fall bloom', 'autumn bloom', 'september bloom', 'october bloom'], confidence: 0.8 },
      'winter_blooming' => { patterns: ['winter bloom', 'november bloom', 'december bloom', 'january bloom'], confidence: 0.8 },
      'long_blooming' => { patterns: ['long bloom', 'extended bloom', 'continuous bloom', 'repeat bloom'], confidence: 0.8 },

      # Environmental adaptations
      'shade_tolerant' => { patterns: ['shade', 'partial shade', 'low light', 'understory'], confidence: 0.9 },
      'sun_loving' => { patterns: ['full sun', 'bright sun', 'sunny'], confidence: 0.9 },
      'wind_resistant' => { patterns: ['wind', 'windbreak', 'shelter'], confidence: 0.8 },
      'salt_tolerant' => { patterns: ['salt', 'coastal', 'saline', 'seaside'], confidence: 0.9 },
      'heat_tolerant' => { patterns: ['heat', 'hot climate', 'desert'], confidence: 0.8 },
      'frost_tolerant' => { patterns: ['frost', 'freeze', 'hardy'], confidence: 0.8 },
      'drought_tolerant' => { patterns: ['drought', 'dry', 'arid', 'xerophytic', 'water-wise', 'low water', 'drought resistant', 'drought hardy'], confidence: 0.9 },

      # Soil preferences
      'clay_tolerant' => { patterns: ['clay soil', 'heavy soil'], confidence: 0.8 },
      'sandy_soil' => { patterns: ['sandy', 'well-drain', 'drainage'], confidence: 0.7 },
      'wet_soil' => { patterns: ['wet', 'moist', 'bog', 'marsh'], confidence: 0.8 },
      'alkaline_soil' => { patterns: ['alkaline', 'lime', 'chalk'], confidence: 0.9 },
      'acidic_soil' => { patterns: ['acid', 'acidic', 'ericaceous'], confidence: 0.9 },

      # Wildlife value
      'butterfly_attractor' => { patterns: ['butterfly', 'lepidoptera'], confidence: 0.9 },
      'bee_friendly' => { patterns: ['bee', 'honey', 'nectar'], confidence: 0.9 },
      'bird_food' => { patterns: ['bird', 'seed', 'berry', 'fruit'], confidence: 0.7 },
      'hummingbird' => { patterns: ['hummingbird', 'nectar'], confidence: 0.9 },

      # Maintenance
      'low_maintenance' => { patterns: ['low maintenance', 'easy', 'carefree', 'trouble-free'], confidence: 0.8 },
      'high_maintenance' => { patterns: ['high maintenance', 'demanding', 'fussy'], confidence: 0.8 },

      # Special features
      'fragrant' => { patterns: ['fragrant', 'scented', 'perfume', 'sweet smell'], confidence: 0.9 },
      'colorful_foliage' => { patterns: ['colorful', 'variegated', 'purple leaves', 'red leaves'], confidence: 0.9 },
      'interesting_bark' => { patterns: ['bark', 'trunk', 'stem'], confidence: 0.6 },
      'autumn_color' => { patterns: ['autumn color', 'fall color', 'yellow leaves', 'red fall'], confidence: 0.9 },

      # Uses
      'cut_flower' => { patterns: ['cut flower', 'bouquet', 'arrangement'], confidence: 0.9 },
      'dried_flower' => { patterns: ['dried', 'everlasting'], confidence: 0.8 },
      'hedge_plant' => { patterns: ['hedge', 'screen', 'border'], confidence: 0.9 },
      'specimen_plant' => { patterns: ['specimen', 'focal point', 'feature'], confidence: 0.8 },
      'mass_planting' => { patterns: ['mass', 'group', 'drift'], confidence: 0.8 },

      # Edible specifics
      'fruit_tree' => { patterns: ['fruit', 'apple', 'pear', 'cherry', 'plum'], confidence: 0.9 },
      'nut_tree' => { patterns: ['nut', 'walnut', 'pecan', 'almond'], confidence: 0.9 },
      'herb' => { patterns: ['herb', 'culinary', 'seasoning', 'cooking'], confidence: 0.9 },
      'vegetable' => { patterns: ['vegetable', 'salad', 'greens'], confidence: 0.9 },
      'tea_plant' => { patterns: ['tea', 'tisane', 'infusion'], confidence: 0.9 },

      # Medicinal specifics
      'anti_inflammatory' => { patterns: ['anti-inflammatory', 'inflammation', 'swelling'], confidence: 0.8 },
      'digestive' => { patterns: ['digestive', 'stomach', 'digestion'], confidence: 0.8 },
      'respiratory' => { patterns: ['respiratory', 'cough', 'lung', 'breathing'], confidence: 0.8 },
      'skin_care' => { patterns: ['skin', 'wound', 'healing', 'topical'], confidence: 0.8 },

      # Permaculture functions
      'windbreak' => { patterns: ['windbreak', 'wind protection', 'shelter'], confidence: 0.9 },
      'erosion_control' => { patterns: ['erosion', 'slope', 'bank', 'stabilize'], confidence: 0.9 },
      'living_mulch' => { patterns: ['living mulch', 'ground cover', 'suppress weed'], confidence: 0.8 },
      'chop_and_drop' => { patterns: ['chop and drop', 'biomass', 'mulch'], confidence: 0.8 },
      'pioneer_species' => { patterns: ['pioneer', 'disturbed soil', 'succession'], confidence: 0.8 },

      # Problem indicators
      'invasive_potential' => { patterns: ['invasive', 'aggressive', 'spreads rapidly', 'escape cultivation'], confidence: 0.9 },
      'toxic' => { patterns: ['toxic', 'poison', 'dangerous', 'harmful'], confidence: 0.9 },
      'thorny' => { patterns: ['thorn', 'spike', 'prickle'], confidence: 0.9 },

      # Special growing conditions
      'greenhouse' => { patterns: ['greenhouse', 'indoor', 'houseplant'], confidence: 0.8 },
      'aquatic' => { patterns: ['aquatic', 'water', 'pond', 'bog'], confidence: 0.6 },
      'epiphytic' => { patterns: ['epiphyte', 'air plant', 'tree-dwelling'], confidence: 0.9 },
      'succulent' => { patterns: ['succulent', 'fleshy', 'water-storing'], confidence: 0.9 }
    }

    total_tags_added = 0
    plants_updated = 0

    # First, clean up duplicate drought_tolerant tags
    puts 'Cleaning up duplicate drought_tolerant tags...'

    # Find plants with multiple drought_tolerant tags
    plants_with_duplicates = PlantSemanticTag.joins(:semantic_tag)
                                            .where(semantic_tags: { name: 'drought_tolerant' })
                                            .group(:enhanced_plant_id)
                                            .having('COUNT(*) > 1')
                                            .pluck(:enhanced_plant_id)

    plants_with_duplicates.each do |plant_id|
      # Keep only the first drought_tolerant tag for each plant
      duplicate_tags = PlantSemanticTag.joins(:semantic_tag)
                                      .where(semantic_tags: { name: 'drought_tolerant' })
                                      .where(enhanced_plant_id: plant_id)
                                      .order(:id)

      # Remove all but the first one
      duplicate_tags.offset(1).destroy_all
      puts "  Cleaned duplicates for plant ID #{plant_id}"
    end

    plants = EnhancedPlant.includes(:plant_uses, :use_categories, :semantic_tags, :environmental_requirements)

    plants.find_each.with_index do |plant, index|
      tags_added_for_plant = 0

      # Get all text to analyze
      text_to_analyze = [
        plant.common_name,
        plant.scientific_name,
        plant.family,
        plant.description_detailed,
        plant.description_short,
        plant.growing_notes,
        plant.plant_uses.joins(:use_category).pluck('use_categories.name').join(' ')
      ].compact.join(' ').downcase

      # Process each tag pattern
      tag_patterns.each do |tag_name, config|
        next if plant.semantic_tags.exists?(name: tag_name) # Skip if already has tag

        patterns = config[:patterns]
        confidence = config[:confidence]

        if patterns.any? { |pattern| text_to_analyze.include?(pattern) }
          begin
            # Create or find the semantic tag
            semantic_tag = SemanticTag.find_or_create_by(name: tag_name) do |tag|
              tag.category = 'trait'
              tag.description = "Auto-generated tag for #{tag_name.humanize}"
            end

            # Create the plant-semantic tag association
            plant.plant_semantic_tags.create!(
              semantic_tag: semantic_tag,
              confidence_score: confidence,
              source: 'extracted'
            )

            tags_added_for_plant += 1
            total_tags_added += 1

          rescue ActiveRecord::RecordInvalid
            # Skip if validation fails (likely duplicate)
            next
          end
        end
      end

      # Special logic for environmental requirements
      if plant.environmental_requirements
        env = plant.environmental_requirements

        # Drought tolerance
        if env.drought_tolerance_score && env.drought_tolerance_score > 0.7
          unless plant.semantic_tags.exists?(name: 'drought_tolerant')
            drought_tag = SemanticTag.find_or_create_by(name: 'drought_tolerant')
            plant.plant_semantic_tags.create!(
              semantic_tag: drought_tag,
              confidence_score: 0.9,
              source: 'extracted'
            )
            tags_added_for_plant += 1
            total_tags_added += 1
          end
        end

        # Light requirements
        if env.light_requirement == 'full_shade' || env.light_requirement == 'partial_shade'
          unless plant.semantic_tags.exists?(name: 'shade_tolerant')
            shade_tag = SemanticTag.find_or_create_by(name: 'shade_tolerant')
            plant.plant_semantic_tags.create!(
              semantic_tag: shade_tag,
              confidence_score: 0.9,
              source: 'extracted'
            )
            tags_added_for_plant += 1
            total_tags_added += 1
          end
        end

        if env.light_requirement == 'full_sun'
          unless plant.semantic_tags.exists?(name: 'sun_loving')
            sun_tag = SemanticTag.find_or_create_by(name: 'sun_loving')
            plant.plant_semantic_tags.create!(
              semantic_tag: sun_tag,
              confidence_score: 0.9,
              source: 'extracted'
            )
            tags_added_for_plant += 1
            total_tags_added += 1
          end
        end
      end

      # Plant type specific tagging
      case plant.plant_type
      when 'tree'
        if text_to_analyze.match?(/\b(fruit|apple|pear|cherry|plum|citrus)\b/)
          unless plant.semantic_tags.exists?(name: 'fruit_tree')
            fruit_tag = SemanticTag.find_or_create_by(name: 'fruit_tree')
            plant.plant_semantic_tags.create!(
              semantic_tag: fruit_tag,
              confidence_score: 0.9,
              source: 'extracted'
            )
            tags_added_for_plant += 1
            total_tags_added += 1
          end
        end

        if text_to_analyze.match?(/\b(nut|walnut|pecan|almond|hazelnut)\b/)
          unless plant.semantic_tags.exists?(name: 'nut_tree')
            nut_tag = SemanticTag.find_or_create_by(name: 'nut_tree')
            plant.plant_semantic_tags.create!(
              semantic_tag: nut_tag,
              confidence_score: 0.9,
              source: 'extracted'
            )
            tags_added_for_plant += 1
            total_tags_added += 1
          end
        end
      when 'herbaceous'
        if plant.plant_uses.joins(:use_category).exists?(use_categories: { name: ['Edible', 'Culinary'] })
          if text_to_analyze.match?(/\b(herb|seasoning|cooking|culinary)\b/)
            unless plant.semantic_tags.exists?(name: 'herb')
              herb_tag = SemanticTag.find_or_create_by(name: 'herb')
              plant.plant_semantic_tags.create!(
                semantic_tag: herb_tag,
                confidence_score: 0.9,
                source: 'extracted'
              )
              tags_added_for_plant += 1
              total_tags_added += 1
            end
          elsif text_to_analyze.match?(/\b(vegetable|salad|greens|leafy)\b/)
            unless plant.semantic_tags.exists?(name: 'vegetable')
              veg_tag = SemanticTag.find_or_create_by(name: 'vegetable')
              plant.plant_semantic_tags.create!(
                semantic_tag: veg_tag,
                confidence_score: 0.9,
                source: 'extracted'
              )
              tags_added_for_plant += 1
              total_tags_added += 1
            end
          end
        end
      end

      if tags_added_for_plant > 0
        plants_updated += 1
      end

      # Progress indicator
      if (index + 1) % 20 == 0
        puts "Processed #{index + 1}/#{plants.count} plants... (#{total_tags_added} tags added so far)"
      end
    end

    puts "\nEnhanced comprehensive tagging completed!"
    puts "Plants processed: #{plants.count}"
    puts "Plants updated: #{plants_updated}"
    puts "Total tags added: #{total_tags_added}"
    puts "Average tags per updated plant: #{(total_tags_added.to_f / plants_updated).round(1)}" if plants_updated > 0
  end
end