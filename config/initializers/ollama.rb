# frozen_string_literal: true

# Enhanced Ollama Configuration for ChatGPT-like Experience
Rails.application.configure do
  # Enhanced model configuration
  ollama_url = ENV['OLLAMA_URL'] || 'http://172.17.0.1:11434'
  
  # Intelligent model selection based on capabilities and performance
  OLLAMA_MODELS = {
    # Conversation-focused models (best for ChatGPT-like interactions)
    conversation: {
      primary: ENV['OLLAMA_CONVERSATION_MODEL'] || 'llama3.1:8b',
      fallback: 'llama3.1:8b',
      description: 'Optimized for natural conversations and complex dialogue'
    },
    
    # Quick response models (for simple queries)
    quick: {
      primary: ENV['OLLAMA_QUICK_MODEL'] || 'mistral:7b',
      fallback: 'llama3.1:8b',
      description: 'Fast responses for simple questions'
    },
    
    # Analysis models (for detailed plant analysis)
    analysis: {
      primary: ENV['OLLAMA_ANALYSIS_MODEL'] || 'llama3.1:13b',
      fallback: 'llama3.1:8b',
      description: 'Detailed analysis and comprehensive responses'
    },
    
    # Code/structured models (for plant data processing)
    structured: {
      primary: ENV['OLLAMA_STRUCTURED_MODEL'] || 'codellama:7b',
      fallback: 'llama3.1:8b',
      description: 'Structured responses and data processing'
    }
  }.freeze
  
  # Get the primary conversation model
  primary_model = OLLAMA_MODELS[:conversation][:primary]
  
  # Test Ollama connection with enhanced error handling
  begin
    response = HTTParty.get("#{ollama_url}/api/tags", timeout: 10)
    
    if response.success?
      Rails.logger.info "✅ Ollama connected at #{ollama_url} - Enhanced LLM features enabled"
      
      # Parse available models
      models_data = JSON.parse(response.body)['models'] rescue []
      available_models = models_data.map { |m| m['name'] }
      
      Rails.logger.info "   📋 Available models: #{available_models.join(', ')}" if available_models.any?
      
      # Check model availability and suggest optimizations
      OLLAMA_MODELS.each do |category, config|
        primary = config[:primary]
        fallback = config[:fallback]
        
        if available_models.any? { |name| name.include?(primary.split(':').first) }
          Rails.logger.info "   ✅ #{category.to_s.capitalize} model ready: #{primary}"
        elsif available_models.any? { |name| name.include?(fallback.split(':').first) }
          Rails.logger.warn "   ⚠️  Using fallback for #{category}: #{fallback} (#{primary} not found)"
        else
          Rails.logger.warn "   ❌ No suitable model for #{category} - install: ollama pull #{primary}"
        end
      end
      
      # Performance recommendations
      total_models = available_models.length
      if total_models == 0
        Rails.logger.warn "   💡 No models installed. Run: ollama pull #{primary_model}"
      elsif total_models == 1
        Rails.logger.info "   💡 For better performance, consider installing specialized models:"
        Rails.logger.info "      • Quick responses: ollama pull mistral:7b"
        Rails.logger.info "      • Better conversations: ollama pull llama3.1:13b"
      end
      
      # Memory usage estimation
      total_size_gb = models_data.sum { |m| (m['size'] || 0) / (1024.0 ** 3) }
      if total_size_gb > 0
        Rails.logger.info "   💾 Total model storage: #{total_size_gb.round(1)} GB"
        
        if total_size_gb > 20
          Rails.logger.warn "   ⚠️  High storage usage - consider removing unused models"
        end
      end
      
    else
      Rails.logger.warn "⚠️  Ollama API responded with error: #{response.code}"
      Rails.logger.warn "   Response: #{response.body}"
    end
    
  rescue Net::ReadTimeout, Net::TimeoutError
    Rails.logger.warn "⚠️  Ollama connection timeout - check if service is running"
    Rails.logger.warn "   Start Ollama: ollama serve"
    
  rescue Errno::ECONNREFUSED
    Rails.logger.warn "⚠️  Ollama connection refused at #{ollama_url}"
    Rails.logger.warn "   Ensure Ollama is running and accessible"
    
  rescue => e
    Rails.logger.warn "⚠️  Ollama not available: #{e.message}"
    Rails.logger.warn "   LLM features will run in fallback mode"
    Rails.logger.warn "   Install Ollama: curl -fsSL https://ollama.ai/install.sh | sh"
    Rails.logger.warn "   Start service: ollama serve"
    Rails.logger.warn "   Install model: ollama pull #{primary_model}"
  end
end

# Enhanced helper module with ChatGPT-like capabilities
module LlmHelper
  extend self
  
  def available?
    check_connection.fetch(:available, false)
  end
  
  def status
    connection_info = check_connection
    
    if connection_info[:available]
      models_info = get_models_info
      
      {
        enabled: true,
        provider: 'Ollama',
        url: ollama_url,
        models: {
          conversation: get_best_model(:conversation),
          quick: get_best_model(:quick),
          analysis: get_best_model(:analysis),
          structured: get_best_model(:structured)
        },
        capabilities: detect_capabilities(models_info),
        performance: assess_performance(models_info),
        recommendations: generate_recommendations(models_info)
      }
    else
      {
        enabled: false,
        fallback_mode: true,
        message: 'Ollama not available - ensure it is running and accessible',
        url: ollama_url,
        error: connection_info[:error]
      }
    end
  end
  
  def models
    return [] unless available?
    
    begin
      response = HTTParty.get("#{ollama_url}/api/tags", timeout: 5)
      models = JSON.parse(response.body)['models'] rescue []
      
      # Enhanced model information
      models.map do |model|
        {
          name: model['name'],
          size: model['size'],
          size_gb: (model['size'] || 0) / (1024.0 ** 3),
          modified: model['modified_at'],
          capabilities: detect_model_capabilities(model['name']),
          recommended_use: recommend_model_use(model['name'])
        }
      end
    rescue
      []
    end
  end
  
  def get_best_model(category = :conversation)
    return nil unless available?
    
    config = Rails.application.config_for(:ollama_models) rescue OLLAMA_MODELS
    model_config = config[category] || config[:conversation]
    
    available_models = models.map { |m| m[:name] }
    
    # Try primary model first
    primary = model_config[:primary]
    if available_models.any? { |name| name.include?(primary.split(':').first) }
      return primary
    end
    
    # Fall back to fallback model
    fallback = model_config[:fallback]
    if available_models.any? { |name| name.include?(fallback.split(':').first) }
      return fallback
    end
    
    # Use any available llama model as last resort
    available_models.find { |name| name.include?('llama') } || available_models.first
  end
  
  def conversation_ready?
    !get_best_model(:conversation).nil?
  end
  
  def supports_complex_conversations?
    best_model = get_best_model(:conversation)
    return false unless best_model
    
    # Check if model supports complex conversations
    complex_models = ['llama3.1:13b', 'llama3.1:70b', 'mixtral:8x7b', 'qwen2:7b']
    complex_models.any? { |model| best_model.include?(model.split(':').first) }
  end
  
  def recommended_settings_for_model(model_name)
    case model_name.downcase
    when /llama3\.1:8b/
      {
        temperature: 0.8,
        top_p: 0.95,
        top_k: 50,
        repeat_penalty: 1.1,
        num_predict: 2000,
        stop: ['Human:', 'User:', '\n\nUser:', '\n\nHuman:']
      }
    when /llama3\.1:13b/
      {
        temperature: 0.85,
        top_p: 0.95,
        top_k: 60,
        repeat_penalty: 1.05,
        num_predict: 3000,
        stop: ['Human:', 'User:', '\n\nUser:', '\n\nHuman:']
      }
    when /mistral/
      {
        temperature: 0.7,
        top_p: 0.9,
        top_k: 40,
        repeat_penalty: 1.1,
        num_predict: 1500,
        stop: ['Human:', 'User:', '\n\nUser:', '\n\nHuman:']
      }
    when /codellama/
      {
        temperature: 0.3,
        top_p: 0.8,
        top_k: 30,
        repeat_penalty: 1.2,
        num_predict: 2000,
        stop: ['```', 'Human:', 'User:']
      }
    else
      # Default settings for unknown models
      {
        temperature: 0.8,
        top_p: 0.9,
        top_k: 40,
        repeat_penalty: 1.1,
        num_predict: 1500,
        stop: ['Human:', 'User:', '\n\nUser:', '\n\nHuman:']
      }
    end
  end
  
  private
  
  def ollama_url
    ENV['OLLAMA_URL'] || 'http://172.17.0.1:11434'
  end
  
  def check_connection
    response = HTTParty.get("#{ollama_url}/api/tags", timeout: 5)
    
    if response.success?
      { available: true, response_time: response.response.time }
    else
      { available: false, error: "HTTP #{response.code}", response_body: response.body }
    end
  rescue Net::ReadTimeout, Net::TimeoutError
    { available: false, error: 'Connection timeout' }
  rescue Errno::ECONNREFUSED
    { available: false, error: 'Connection refused' }
  rescue => e
    { available: false, error: e.message }
  end
  
  def get_models_info
    return [] unless available?
    
    begin
      response = HTTParty.get("#{ollama_url}/api/tags", timeout: 5)
      JSON.parse(response.body)['models'] rescue []
    rescue
      []
    end
  end
  
  def detect_capabilities(models_info)
    capabilities = {
      basic_chat: false,
      complex_conversations: false,
      quick_responses: false,
      detailed_analysis: false,
      code_generation: false,
      multilingual: false
    }
    
    model_names = models_info.map { |m| m['name'].downcase }
    
    capabilities[:basic_chat] = model_names.any? { |name| name.include?('llama') || name.include?('mistral') }
    capabilities[:complex_conversations] = model_names.any? { |name| name.include?('13b') || name.include?('70b') || name.include?('mixtral') }
    capabilities[:quick_responses] = model_names.any? { |name| name.include?('mistral:7b') || name.include?('llama3:8b') }
    capabilities[:detailed_analysis] = model_names.any? { |name| name.include?('13b') || name.include?('70b') }
    capabilities[:code_generation] = model_names.any? { |name| name.include?('codellama') || name.include?('coder') }
    capabilities[:multilingual] = model_names.any? { |name| name.include?('qwen') || name.include?('yi') }
    
    capabilities
  end
  
  def assess_performance(models_info)
    total_size = models_info.sum { |m| m['size'] || 0 }
    model_count = models_info.length
    
    {
      model_count: model_count,
      total_size_gb: (total_size / (1024.0 ** 3)).round(1),
      memory_usage: estimate_memory_usage(models_info),
      response_speed: estimate_response_speed(models_info),
      quality_level: estimate_quality_level(models_info)
    }
  end
  
  def generate_recommendations(models_info)
    recommendations = []
    model_names = models_info.map { |m| m['name'].downcase }
    
    if models_info.empty?
      recommendations << {
        type: :critical,
        message: "Install a base model: ollama pull llama3.1:8b",
        action: "ollama pull llama3.1:8b"
      }
    elsif models_info.length == 1
      recommendations << {
        type: :improvement,
        message: "Consider adding a quick response model for faster interactions",
        action: "ollama pull mistral:7b"
      }
    end
    
    unless model_names.any? { |name| name.include?('13b') || name.include?('mixtral') }
      recommendations << {
        type: :enhancement,
        message: "For better conversation quality, consider a larger model",
        action: "ollama pull llama3.1:13b"
      }
    end
    
    if models_info.sum { |m| m['size'] || 0 } > 50 * (1024 ** 3)  # 50GB
      recommendations << {
        type: :optimization,
        message: "High storage usage - consider removing unused models",
        action: "ollama list && ollama rm <unused_model>"
      }
    end
    
    recommendations
  end
  
  def detect_model_capabilities(model_name)
    name_lower = model_name.downcase
    capabilities = []
    
    capabilities << 'conversation' if name_lower.include?('llama') || name_lower.include?('mistral')
    capabilities << 'quick_response' if name_lower.include?('mistral:7b') || name_lower.include?('7b')
    capabilities << 'detailed_analysis' if name_lower.include?('13b') || name_lower.include?('70b')
    capabilities << 'code_generation' if name_lower.include?('codellama') || name_lower.include?('coder')
    capabilities << 'high_quality' if name_lower.include?('13b') || name_lower.include?('70b') || name_lower.include?('mixtral')
    
    capabilities
  end
  
  def recommend_model_use(model_name)
    name_lower = model_name.downcase
    
    case name_lower
    when /mistral.*7b/
      'Quick responses and simple questions'
    when /llama3\.1.*8b/
      'General conversations and plant advice'
    when /llama3\.1.*13b/
      'Complex analysis and detailed explanations'
    when /llama3\.1.*70b/
      'Highest quality responses and complex reasoning'
    when /codellama/
      'Structured data processing and technical responses'
    when /mixtral/
      'High-quality conversations and complex tasks'
    else
      'General purpose AI assistant'
    end
  end
  
  def estimate_memory_usage(models_info)
    # Rough estimation: model size + 2GB overhead per model
    base_memory = models_info.sum { |m| (m['size'] || 0) / (1024.0 ** 3) }
    overhead = models_info.length * 2.0
    
    (base_memory + overhead).round(1)
  end
  
  def estimate_response_speed(models_info)
    # Based on typical model sizes and performance characteristics
    avg_size = models_info.empty? ? 0 : models_info.sum { |m| m['size'] || 0 } / models_info.length / (1024.0 ** 3)
    
    case avg_size
    when 0..3
      'Very Fast'
    when 3..6
      'Fast'
    when 6..10
      'Medium'
    when 10..20
      'Slow'
    else
      'Very Slow'
    end
  end
  
  def estimate_quality_level(models_info)
    model_names = models_info.map { |m| m['name'].downcase }
    
         if model_names.any? { |name| name.include?('70b') || name.include?('mixtral:8x7b') }
      'Excellent'
    elsif model_names.any? { |name| name.include?('13b') || name.include?('mixtral') }
      'Very Good'
    elsif model_names.any? { |name| name.include?('8b') }
      'Good'
    elsif model_names.any? { |name| name.include?('7b') }
      'Fair'
    else
      'Basic'
    end
  end
end 