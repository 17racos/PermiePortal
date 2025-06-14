# frozen_string_literal: true
namespace :permie_bro do
  desc 'Setup PermieBro AI system'
  task setup: :environment do
    puts '🌱 Setting up PermieBro AI System'
    puts '=' * 50

    # Run migrations
    puts 'Running migrations...'
    Rake::Task['db:migrate'].invoke

    # Generate semantic ontology
    puts 'Generating semantic ontology...'
    Rake::Task['permie_bro:generate_ontology'].invoke

    # Auto-tag existing plants
    puts 'Auto-tagging existing plants...'
    Rake::Task['permie_bro:auto_tag_plants'].invoke

    # Setup vector search
    puts 'Setting up vector search...'
    Rake::Task['permie_bro:setup_vector_search'].invoke

    puts '✅ PermieBro setup complete!'
  end

  desc 'Generate semantic ontology structure'
  task generate_ontology: :environment do
    puts '🌳 Generating Semantic Ontology'

    ontology_data = {
      # Core plant characteristics
      'Edibility' => {
        category: 'edibility',
        synonyms: ['food', 'culinary', 'edible'],
        children: [
          'Edible Fruit', 'Edible Leaves', 'Edible Roots', 'Edible Seeds',
          'Edible Flowers', 'Edible Bark', 'Edible Nuts'
        ]
      },
      'Medicinal Properties' => {
        category: 'medicinal',
        synonyms: ['medicine', 'therapeutic', 'healing'],
        children: [
          'Anti-inflammatory', 'Antimicrobial', 'Digestive Aid', 'Respiratory Support',
          'Immune Support', 'Pain Relief', 'Skin Care', 'Stress Relief'
        ]
      },
      'Environmental Adaptation' => {
        category: 'environmental',
        synonyms: ['climate', 'tolerance', 'adaptation'],
        children: [
          'Drought Tolerant', 'Shade Tolerant', 'Cold Hardy', 'Heat Tolerant',
          'Salt Tolerant', 'Wind Resistant', 'Flood Tolerant'
        ]
      },
      'Ecosystem Function' => {
        category: 'ecosystem_function',
        synonyms: ['ecological', 'function', 'role'],
        children: [
          'Nitrogen Fixing', 'Pollinator Friendly', 'Ground Cover', 'Erosion Control',
          'Wildlife Food', 'Windbreak', 'Living Mulch', 'Pest Deterrent'
        ]
      },
      'Growth Characteristics' => {
        category: 'growth_habit',
        synonyms: ['growth', 'habit', 'form'],
        children: [
          'Fast Growing', 'Slow Growing', 'Spreading', 'Clumping',
          'Self Seeding', 'Evergreen', 'Deciduous', 'Climbing'
        ]
      },
      'Maintenance Level' => {
        category: 'care_level',
        synonyms: ['care', 'maintenance', 'difficulty'],
        children: [
          'Low Maintenance', 'High Maintenance', 'Beginner Friendly',
          'Expert Level', 'Self Sufficient'
        ]
      },
      'Size Category' => {
        category: 'size',
        synonyms: ['size', 'height', 'scale'],
        children: [
          'Ground Cover', 'Small Shrub', 'Medium Shrub', 'Large Shrub',
          'Small Tree', 'Medium Tree', 'Large Tree', 'Vine'
        ]
      },
      'Companion Relationships' => {
        category: 'companion_relationship',
        synonyms: ['companion', 'guild', 'polyculture'],
        children: [
          'Three Sisters', 'Fruit Tree Guild', 'Herb Spiral', 'Forest Garden',
          'Beneficial Insects', 'Pest Control', 'Nutrient Cycling'
        ]
      }
    }

    total_created = 0

    ontology_data.each do |parent_name, data|
      begin
        # Create parent concept
        parent = EnhancedSemanticOntology.find_or_create_by(name: parent_name) do |o|
          o.ontology_category = data[:category]
          o.synonyms = data[:synonyms] || []
          o.nlp_keywords = data[:synonyms] || []
          o.ai_weight = 0.9
          o.include_in_nlp = true
          o.description = "Root concept for #{parent_name.downcase}"
        end

        puts "✓ Created parent: #{parent_name}"
        total_created += 1

        # Create child concepts
        data[:children].each do |child_name|
          EnhancedSemanticOntology.find_or_create_by(
            name: child_name,
            parent: parent
          ) do |o|
            o.ontology_category = data[:category]
            o.synonyms = generate_synonyms(child_name)
            o.nlp_keywords = generate_keywords(child_name)
            o.ai_weight = 0.8
            o.include_in_nlp = true
            o.description = "#{child_name} concept under #{parent_name}"
          end

          puts "  - Created child: #{child_name}"
          total_created += 1
        end

      rescue => e
        puts "❌ Error creating #{parent_name}: #{e.message}"
      end
    end

    puts "\n✅ Created #{total_created} ontology concepts"
  end

  desc 'Auto-tag all plants with semantic tags'
  task auto_tag_plants: :environment do
    puts '🏷️  Auto-tagging Plants'

    total_plants = EnhancedPlant.count
    tagged_count = 0
    total_tags_added = 0

    puts "Processing #{total_plants} plants..."

    EnhancedPlant.includes(:semantic_tags, :environmental_requirements, :plant_uses).find_each.with_index do |plant, index|
      begin
        service = EnhancedAutoTaggingService.new(plant)
        tags_added = service.auto_tag_plant

        if tags_added > 0
          tagged_count += 1
          total_tags_added += tags_added
        end

        print '.' if index % 50 == 0

      rescue => e
        puts "\n❌ Error tagging #{plant.common_name}: #{e.message}"
      end
    end

    puts "\n✅ Auto-tagging complete!"
    puts "Plants tagged: #{tagged_count}/#{total_plants}"
    puts "Total tags added: #{total_tags_added}"

    # Show tag distribution
    puts "\nTag distribution:"
    PlantSemanticTag.joins(:semantic_tag)
                    .group('semantic_tags.name')
                    .count
                    .sort_by { |k, v| -v }
                    .first(10)
                    .each { |tag, count| puts "  #{tag}: #{count} plants" }
  end

  desc 'Setup vector search index'
  task setup_vector_search: :environment do
    puts '🔍 Setting up Vector Search'

    begin
      vector_service = VectorSearchService.new(backend: :local_faiss)

      puts 'Indexing plants for vector search...'
      vector_service.bulk_index_plants

      puts '✅ Vector search setup complete!'

    rescue => e
      puts "❌ Vector search setup failed: #{e.message}"
      puts 'This is optional - the system will work without vector search'
    end
  end

  desc 'Test PermieBro AI responses'
  task test_ai: :environment do
    puts '🤖 Testing PermieBro AI'

    test_queries = [
      'What are good companion plants for tomatoes?',
      'I need drought-tolerant plants for zone 9',
      'What medicinal herbs are easy to grow?',
      'Show me edible ground cover plants',
      'What native Florida plants attract pollinators?'
    ]

    permie_bro = PermieBroService.new(llm_provider: :ollama)

    test_queries.each_with_index do |query, index|
      puts "\n#{index + 1}. Testing: #{query}"
      puts '-' * 40

      begin
        result = permie_bro.ask(query)

        puts "Response: #{result[:answer][0..200]}..."
        puts "Plants found: #{result[:plants].count}"
        puts "Confidence: #{(result[:confidence] * 100).round}%"

      rescue => e
        puts "❌ Error: #{e.message}"
      end
    end
  end

  desc 'Generate plant embeddings for vector search'
  task generate_embeddings: :environment do
    puts '🧠 Generating Plant Embeddings'

    vector_service = VectorSearchService.new

    EnhancedPlant.includes(:semantic_tags, :environmental_requirements).find_each.with_index do |plant, index|
      begin
        vector_service.index_plant(plant)
        print '.' if index % 10 == 0
      rescue => e
        puts "\n❌ Error generating embedding for #{plant.common_name}: #{e.message}"
      end
    end

    puts "\n✅ Embeddings generated!"
  end

  desc 'Clean up and optimize the AI system'
  task cleanup: :environment do
    puts '🧹 Cleaning up PermieBro AI System'

    # Remove old cached queries
    old_cache_count = AiQueryCache.where('last_accessed_at < ?', 1.week.ago).count
    AiQueryCache.where('last_accessed_at < ?', 1.week.ago).delete_all
    puts "Removed #{old_cache_count} old cached queries"

    # Remove low-confidence semantic tags
    low_confidence_count = PlantSemanticTag.where('confidence_score < ?', 0.3).count
    PlantSemanticTag.where('confidence_score < ?', 0.3).delete_all
    puts "Removed #{low_confidence_count} low-confidence semantic tags"

    # Update usage counts
    SemanticTag.joins(:plant_semantic_tags)
               .group('semantic_tags.id')
               .count
               .each do |tag_id, count|
      SemanticTag.find(tag_id).update!(usage_count: count)
    end
    puts 'Updated semantic tag usage counts'

    puts '✅ Cleanup complete!'
  end

  desc 'Show PermieBro system statistics'
  task stats: :environment do
    puts '📊 PermieBro AI System Statistics'
    puts '=' * 50

    puts "Plants: #{EnhancedPlant.count}"
    puts "Semantic Tags: #{SemanticTag.count}"
    puts "Plant-Tag Associations: #{PlantSemanticTag.count}"
    puts "Ontology Concepts: #{EnhancedSemanticOntology.count rescue 0}"
    puts "Cached Queries: #{AiQueryCache.count rescue 0}"

    puts "\nTop Semantic Tags:"
    PlantSemanticTag.joins(:semantic_tag)
                    .group('semantic_tags.name')
                    .count
                    .sort_by { |k, v| -v }
                    .first(10)
                    .each { |tag, count| puts "  #{tag}: #{count} plants" }

    puts "\nTag Sources:"
    PlantSemanticTag.group(:source).count.each { |source, count| puts "  #{source}: #{count}" }

    puts "\nAverage Confidence by Source:"
    PlantSemanticTag.group(:source)
                    .average(:confidence_score)
                    .each { |source, avg| puts "  #{source}: #{(avg * 100).round}%" }
  end

  private

  def generate_synonyms(term)
    # Generate common synonyms for ontology terms
    synonyms_map = {
      'Drought Tolerant' => ['xerophytic', 'water-wise', 'dry-climate'],
      'Shade Tolerant' => ['shade-loving', 'low-light', 'partial-shade'],
      'Pollinator Friendly' => ['bee-friendly', 'butterfly-attracting', 'nectar-rich'],
      'Ground Cover' => ['carpet', 'mat-forming', 'spreading'],
      'Nitrogen Fixing' => ['legume', 'soil-improving', 'nitrogen-enriching'],
      'Fast Growing' => ['quick-growing', 'rapid', 'vigorous'],
      'Low Maintenance' => ['easy-care', 'self-sufficient', 'hardy']
    }

    synonyms_map[term] || []
  end

  def generate_keywords(term)
    # Generate NLP keywords for better matching
    keywords = term.downcase.split(/\s+/)
    keywords += generate_synonyms(term)
    keywords.uniq
  end
end