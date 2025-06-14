# frozen_string_literal: true

namespace :ollama do
  desc "Generate plant contexts for all plants"
  task generate_contexts: :environment do
    puts "🌱 Generating plant contexts for all plants..."
    
    total_plants = EnhancedPlant.count
    processed = 0
    errors = 0
    
    EnhancedPlant.includes(:environmental_requirements, :semantic_tags, :plant_uses).find_each do |plant|
      begin
        PlantContext.create_contexts_for_plant(plant)
        processed += 1
        
        if processed % 50 == 0
          puts "   Processed #{processed}/#{total_plants} plants..."
        end
      rescue => e
        errors += 1
        puts "   ❌ Error processing #{plant.common_name}: #{e.message}"
      end
    end
    
    puts "✅ Completed! Processed #{processed} plants with #{errors} errors."
    puts "   Total contexts created: #{PlantContext.count}"
  end
  
  desc "Update existing plant contexts"
  task update_contexts: :environment do
    puts "🔄 Updating existing plant contexts..."
    
    PlantContext.includes(:enhanced_plant).find_each do |context|
      begin
        new_contexts = PlantContext.generate_gpt_context(context.enhanced_plant)
        new_content = new_contexts[context.context_type.to_sym]
        
        if new_content && new_content != context.content
          context.update!(content: new_content)
          puts "   Updated #{context.enhanced_plant.common_name} - #{context.context_type}"
        end
      rescue => e
        puts "   ❌ Error updating #{context.enhanced_plant.common_name}: #{e.message}"
      end
    end
    
    puts "✅ Context update completed!"
  end
  
  desc "Test Ollama integration"
  task test: :environment do
    puts "🧪 Testing Ollama integration..."
    
    # Test 1: Check if Ollama is available
    service = OllamaGptService.new
    if service.available?
      puts "✅ Ollama is available"
      puts "   URL: #{ENV['OLLAMA_URL'] || 'http://localhost:11434'}"
      puts "   Model: #{ENV['OLLAMA_MODEL'] || 'llama3.1:8b'}"
      
      # Get available models
      begin
        response = HTTParty.get("#{ENV['OLLAMA_URL'] || 'http://localhost:11434'}/api/tags", timeout: 5)
        if response.success?
          models = JSON.parse(response.body)['models']
          model_names = models.map { |m| m['name'] }
          puts "   Available models: #{model_names.join(', ')}"
        end
      rescue => e
        puts "   Could not fetch model list: #{e.message}"
      end
    else
      puts "❌ Ollama is not available"
      puts "   Make sure Ollama is running: ollama serve"
      puts "   And that you have a model installed: ollama pull llama3.1:8b"
      return
    end
    
    # Test 2: Initialize service
    begin
      service = OllamaGptService.new
      puts "✅ OllamaGptService initialized successfully"
    rescue => e
      puts "❌ Failed to initialize OllamaGptService: #{e.message}"
      return
    end
    
    # Test 3: Generate plant contexts
    begin
      plant = EnhancedPlant.first
      if plant
        contexts = PlantContext.generate_gpt_context(plant)
        puts "✅ Generated contexts for #{plant.common_name}: #{contexts.keys.join(', ')}"
      else
        puts "⚠️  No plants found in database"
      end
    rescue => e
      puts "❌ Failed to generate contexts: #{e.message}"
      return
    end
    
    # Test 4: Simple LLM query (with shorter timeout)
    begin
      puts "🤖 Testing simple LLM query..."
      
      # Use a very simple prompt to test basic functionality
      simple_query = "What is companion planting?"
      
      # Make a direct HTTP request with shorter timeout for testing
      response = HTTParty.post(
        "#{ENV['OLLAMA_URL'] || 'http://localhost:11434'}/api/generate",
        headers: { 'Content-Type' => 'application/json' },
        body: {
          model: ENV['OLLAMA_MODEL'] || 'llama3.1:8b',
          prompt: simple_query,
          stream: false,
          options: {
            temperature: 0.7,
            num_predict: 50  # Limit response length for testing
          }
        }.to_json,
        timeout: 30  # Shorter timeout for testing
      )
      
      if response.success?
        result = JSON.parse(response.body)
        if result['response'] && result['response'].length > 0
          puts "✅ LLM query successful"
          puts "   Response length: #{result['response'].length} characters"
          puts "   Sample: #{result['response'][0..100]}..."
        else
          puts "⚠️  LLM query returned empty response"
        end
      else
        puts "❌ LLM query failed with HTTP #{response.code}"
      end
    rescue Net::ReadTimeout => e
      puts "⚠️  LLM query timed out (this is normal for slower systems)"
      puts "   Consider using a smaller model or increasing timeout"
    rescue => e
      puts "❌ LLM query failed: #{e.message}"
    end
    
    puts "🎉 Ollama integration test completed!"
  end
  
  desc "Show Ollama integration status"
  task status: :environment do
    puts "📊 Ollama Integration Status"
    puts "=" * 50
    
    # LLM Status
    llm_status = LlmHelper.status
    puts "LLM Status: #{llm_status[:enabled] ? '✅ Enabled' : '❌ Disabled'}"
    puts "Provider: #{llm_status[:provider]}"
    puts "URL: #{llm_status[:url]}"
    puts "Model: #{llm_status[:model]}"
    puts "Available Models: #{llm_status[:available_models].join(', ')}" if llm_status[:available_models]
    puts
    
    # Database Status
    puts "Database Status:"
    puts "- Plants: #{EnhancedPlant.count}"
    puts "- Use Categories: #{UseCategory.count}"
    puts "- Semantic Tags: #{SemanticTag.count}"
    puts "- Plant Contexts: #{PlantContext.count}"
    puts "- Plant Relationships: #{PlantRelationship.count}"
    puts
    
    # Context Status
    context_stats = PlantContext.group(:context_type).count
    puts "Plant Contexts by Type:"
    context_stats.each do |type, count|
      puts "- #{type}: #{count}"
    end
    puts
    
    # Recent Activity
    recent_contexts = PlantContext.where('created_at > ?', 1.day.ago).count
    puts "Recent Activity:"
    puts "- Contexts created in last 24h: #{recent_contexts}"
    puts
    
    puts "🔗 API Endpoints Available:"
    puts "- POST /api/v1/gpt/query"
    puts "- POST /api/v1/gpt/chat"
    puts "- POST /api/v1/gpt/search_plants"
    puts "- POST /api/v1/gpt/recommendations"
    puts "- GET  /api/v1/gpt/relationships/:plant_name"
    puts "- POST /api/v1/gpt/analyze_compatibility"
    puts "- GET  /api/v1/gpt/status"
    puts "- GET  /api/v1/gpt/models"
  end
  
  desc "Pull a specific Ollama model"
  task :pull_model, [:model_name] => :environment do |t, args|
    model_name = args[:model_name] || 'llama3.1:8b'
    
    puts "📥 Pulling Ollama model: #{model_name}"
    puts "This may take a while depending on model size..."
    
    system("ollama pull #{model_name}")
    
    if $?.success?
      puts "✅ Successfully pulled #{model_name}"
      
      # Update environment variable suggestion
      puts "\n💡 To use this model, set:"
      puts "   export OLLAMA_MODEL=#{model_name}"
    else
      puts "❌ Failed to pull #{model_name}"
      puts "   Make sure Ollama is installed and running"
    end
  end
  
  desc "List available Ollama models"
  task list_models: :environment do
    puts "📋 Available Ollama Models"
    puts "=" * 30
    
    models = LlmHelper.models
    current_model = ENV['OLLAMA_MODEL'] || 'llama3.1:8b'
    
    if models.any?
      models.each do |model|
        current = model.include?(current_model.split(':').first) ? " ← current" : ""
        puts "  #{model}#{current}"
      end
    else
      puts "No models found. Pull a model first:"
      puts "  ollama pull llama3.1:8b"
    end
    
    puts "\nRecommended models for plant advice:"
    puts "  - llama3.1:8b (good balance of speed and quality)"
    puts "  - llama3.1:13b (better quality, slower)"
    puts "  - mistral:7b (fast, good for simple queries)"
    puts "  - codellama:7b (good for structured responses)"
  end
  
  desc "Clean up old cache entries"
  task cleanup_cache: :environment do
    puts "🧹 Cleaning up old cache entries..."
    
    # Clean Rails cache
    Rails.cache.clear
    puts "✅ Rails cache cleared"
    
    # Clean old plant contexts (optional - only if you want to regenerate them)
    # old_contexts = PlantContext.where('updated_at < ?', 1.month.ago)
    # puts "Found #{old_contexts.count} old contexts (older than 1 month)"
    # old_contexts.destroy_all
    # puts "✅ Old contexts cleaned up"
    
    puts "🎉 Cleanup completed!"
  end
  
  desc "Benchmark Ollama performance"
  task benchmark: :environment do
    puts "⚡ Benchmarking Ollama performance..."
    
    service = OllamaGptService.new
    
    unless service.available?
      puts "❌ Ollama not available"
      return
    end
    
    # Test different prompt lengths
    test_prompts = [
      "Hi",
      "What is permaculture?",
      "Explain companion planting in detail with examples.",
      "Write a comprehensive guide about sustainable gardening practices including soil health, water conservation, and biodiversity."
    ]
    
    test_prompts.each_with_index do |prompt, index|
      puts "\n📝 Test #{index + 1}: #{prompt.length} characters"
      
      start_time = Time.current
      
      begin
        response = HTTParty.post(
          "#{ENV['OLLAMA_URL'] || 'http://localhost:11434'}/api/generate",
          headers: { 'Content-Type' => 'application/json' },
          body: {
            model: ENV['OLLAMA_MODEL'] || 'llama3.1:8b',
            prompt: prompt,
            stream: false,
            options: {
              temperature: 0.7,
              num_predict: 100
            }
          }.to_json,
          timeout: 60
        )
        
        duration = Time.current - start_time
        
        if response.success?
          result = JSON.parse(response.body)
          puts "   ✅ Success in #{duration.round(2)}s"
          puts "   📊 Response: #{result['response']&.length || 0} chars"
          puts "   🔢 Tokens: #{result['eval_count'] || 0} generated, #{result['prompt_eval_count'] || 0} prompt"
        else
          puts "   ❌ Failed: HTTP #{response.code}"
        end
        
      rescue Net::ReadTimeout
        puts "   ⏰ Timeout after #{(Time.current - start_time).round(2)}s"
      rescue => e
        puts "   ❌ Error: #{e.message}"
      end
    end
    
    puts "\n🎉 Benchmark completed!"
  end
end

# Alias for backward compatibility
namespace :gpt do
  desc "Alias for ollama:status"
  task status: :environment do
    Rake::Task['ollama:status'].invoke
  end
  
  desc "Alias for ollama:test"
  task test: :environment do
    Rake::Task['ollama:test'].invoke
  end
  
  desc "Alias for ollama:generate_contexts"
  task generate_contexts: :environment do
    Rake::Task['ollama:generate_contexts'].invoke
  end
end 