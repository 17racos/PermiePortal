# frozen_string_literal: true
# PermieBro AI Assistant Examples and Test Cases
# Run these examples to test the AI-powered plant search system

class PermieBroExamples
  def self.run_all_examples
    puts '🌱 PermieBro AI Assistant Examples'
    puts '=' * 50

    # Initialize the service
    permie_bro = PermieBroService.new(
      llm_provider: :ollama, # Using Ollama for local AI processing
      use_vector_search: true
    )

    # Example queries
    examples = [
      {
        title: 'Drought-tolerant shade plants for zone 9',
        query: 'What native Florida plants are drought-tolerant and grow in shade for zone 9?',
        context: { location: 'Florida', zone: '9b' }
      },
      {
        title: 'Companion plants for tomatoes',
        query: 'What are good companion plants for tomatoes that help with pest control?',
        context: { zone: '7a' }
      },
      {
        title: 'Edible ground cover plants',
        query: 'I need edible ground cover plants that spread quickly and are deer resistant',
        context: { zone: '6b' }
      },
      {
        title: 'Medicinal herbs for beginners',
        query: 'What are easy-to-grow medicinal herbs for a beginner gardener?',
        context: {}
      },
      {
        title: 'Nitrogen-fixing trees',
        query: 'I want nitrogen-fixing trees for my food forest that also provide fruit or nuts',
        context: { zone: '8a' }
      }
    ]

    examples.each_with_index do |example, index|
      puts "\n#{index + 1}. #{example[:title]}"
      puts '-' * 40
      puts "Query: #{example[:query]}"

      begin
        result = permie_bro.ask(example[:query], example[:context])

        puts "\n🤖 PermieBro Response:"
        puts result[:answer]

        puts "\n📊 Search Results:"
        puts "Found #{result[:plants].count} relevant plants"
        puts "Confidence: #{(result[:confidence] * 100).round}%"

        if result[:plants].any?
          puts "\n🌿 Top Plants:"
          result[:plants].first(3).each_with_index do |plant, i|
            puts "  #{i + 1}. #{plant.common_name} (#{plant.scientific_name})"
          end
        end

        puts "\n🔍 Query Analysis:"
        analysis = result[:query_analysis]
        puts "  Concepts: #{analysis[:extracted_concepts].map { |c| c[:concept] }.join(', ')}"
        puts "  Environmental filters: #{analysis[:environmental_filters]}"
        puts "  Use cases: #{analysis[:use_cases].join(', ')}" if analysis[:use_cases].any?

      rescue => e
        puts "❌ Error: #{e.message}"
      end

      puts "\n" + '=' * 50
    end
  end

  def self.test_search_components
    puts '🧪 Testing Individual Search Components'
    puts '=' * 50

    # Test AI Search Service
    puts "\n1. Testing AI Plant Search Service"
    ai_search = AiPlantSearchService.new

    result = ai_search.search(
      query: 'drought tolerant edible plants zone 9',
      limit: 5
    )

    puts "Found #{result[:plants].count} plants"
    puts "Query analysis: #{result[:query_analysis][:extracted_concepts].map { |c| c[:concept] }}"

    # Test Vector Search Service
    puts "\n2. Testing Vector Search Service"
    begin
      vector_search = VectorSearchService.new(backend: :local_faiss)

      # Index a few plants for testing
      plants = EnhancedPlant.includes(:semantic_tags).limit(10)
      puts "Indexing #{plants.count} plants..."

      plants.each { |plant| vector_search.index_plant(plant) }

      # Search
      results = vector_search.search('edible drought tolerant', limit: 3)
      puts "Vector search found #{results.count} results"

    rescue => e
      puts "Vector search not available: #{e.message}"
    end

    # Test Semantic Ontology
    puts "\n3. Testing Semantic Ontology"
    begin
      concepts = EnhancedSemanticOntology.find_by_natural_language('drought tolerant edible')
      puts "Found #{concepts.count} semantic concepts"
      concepts.first(3).each { |c| puts "  - #{c.name} (#{c.category})" }
    rescue => e
      puts "Semantic ontology not set up: #{e.message}"
    end
  end

  def self.benchmark_search_performance
    puts '⚡ Benchmarking Search Performance'
    puts '=' * 50

    queries = [
      'drought tolerant plants',
      'companion plants for tomatoes',
      'medicinal herbs zone 7',
      'edible ground cover',
      'nitrogen fixing trees'
    ]

    ai_search = AiPlantSearchService.new

    queries.each do |query|
      puts "\nQuery: #{query}"

      # Benchmark traditional search
      start_time = Time.current
      result = ai_search.search(query: query, limit: 10)
      traditional_time = Time.current - start_time

      puts "  Traditional search: #{(traditional_time * 1000).round}ms (#{result[:plants].count} results)"

      # Benchmark with caching
      start_time = Time.current
      cached_result = ai_search.search(query: query, limit: 10, use_cache: true)
      cached_time = Time.current - start_time

      puts "  Cached search: #{(cached_time * 1000).round}ms (#{cached_result[:plants].count} results)"

      speedup = traditional_time / cached_time
      puts "  Cache speedup: #{speedup.round(1)}x"
    end
  end

  def self.test_bulk_tagging
    puts '🏷️  Testing Bulk Auto-Tagging'
    puts '=' * 50

    # Test the enhanced auto-tagging service
    plants = EnhancedPlant.limit(10)

    plants.each do |plant|
      puts "\nPlant: #{plant.common_name}"

      before_count = plant.semantic_tags.count

      # Run auto-tagging
      service = EnhancedAutoTaggingService.new(plant)
      tags_added = service.auto_tag_plant

      after_count = plant.reload.semantic_tags.count

      puts "  Tags before: #{before_count}"
      puts "  Tags after: #{after_count}"
      puts "  Tags added: #{tags_added}"

      if plant.semantic_tags.any?
        puts "  Current tags: #{plant.semantic_tags.pluck(:name).join(', ')}"
      end
    end
  end

  def self.generate_sample_ontology
    puts '🌳 Generating Sample Semantic Ontology'
    puts '=' * 50

    # Create hierarchical ontology structure
    ontology_data = {
      'Edibility' => {
        category: 'edibility',
        children: ['Edible Fruit', 'Edible Leaves', 'Edible Roots', 'Edible Seeds', 'Edible Flowers']
      },
      'Environmental Adaptation' => {
        category: 'environmental',
        children: ['Drought Tolerant', 'Shade Tolerant', 'Cold Hardy', 'Heat Tolerant', 'Salt Tolerant']
      },
      'Ecosystem Function' => {
        category: 'ecosystem_function',
        children: ['Nitrogen Fixing', 'Pollinator Friendly', 'Ground Cover', 'Erosion Control', 'Wildlife Food']
      },
      'Human Use' => {
        category: 'human_use',
        children: ['Medicinal', 'Ornamental', 'Timber', 'Fiber', 'Dye']
      },
      'Growth Habit' => {
        category: 'growth_habit',
        children: ['Tree', 'Shrub', 'Herbaceous', 'Vine', 'Annual', 'Perennial']
      }
    }

    ontology_data.each do |parent_name, data|
      begin
        parent = EnhancedSemanticOntology.find_or_create_by(name: parent_name) do |o|
          o.category = data[:category]
          o.ai_weight = 0.9
          o.include_in_nlp = true
          o.description = "Root concept for #{parent_name.downcase}"
        end

        puts "Created parent: #{parent_name}"

        data[:children].each do |child_name|
          EnhancedSemanticOntology.find_or_create_by(
            name: child_name,
            parent: parent
          ) do |o|
            o.category = data[:category]
            o.ai_weight = 0.8
            o.include_in_nlp = true
            o.description = "#{child_name} concept under #{parent_name}"
          end

          puts "  - Created child: #{child_name}"
        end

      rescue => e
        puts "Error creating ontology: #{e.message}"
      end
    end

    puts "\nSample ontology created successfully!"
  end
end

# Usage examples:
if __FILE__ == $0
  puts 'Choose an example to run:'
  puts '1. Run all PermieBro examples'
  puts '2. Test search components'
  puts '3. Benchmark performance'
  puts '4. Test bulk tagging'
  puts '5. Generate sample ontology'

  print 'Enter choice (1-5): '
  choice = gets.chomp.to_i

  case choice
  when 1
    PermieBroExamples.run_all_examples
  when 2
    PermieBroExamples.test_search_components
  when 3
    PermieBroExamples.benchmark_search_performance
  when 4
    PermieBroExamples.test_bulk_tagging
  when 5
    PermieBroExamples.generate_sample_ontology
  else
    puts 'Invalid choice. Running all examples...'
    PermieBroExamples.run_all_examples
  end
end