# app/services/ollama_model_manager.rb
class OllamaModelManager
    MODEL_CONFIG = {
      conversation: {
        primary: ENV['OLLAMA_CONVERSATION_MODEL'] || 'llama3.1:8b',
        fallback: 'llama3.1:8b',
        description: 'Natural conversations'
      },
      quick: {
        primary: ENV['OLLAMA_QUICK_MODEL'] || 'mistral:7b',
        fallback: 'llama3.1:8b',
        description: 'Quick queries'
      },
      analysis: {
        primary: ENV['OLLAMA_ANALYSIS_MODEL'] || 'llama3.1:13b',
        fallback: 'llama3.1:8b',
        description: 'In-depth analysis'
      },
      structured: {
        primary: ENV['OLLAMA_STRUCTURED_MODEL'] || 'codellama:7b',
        fallback: 'llama3.1:8b',
        description: 'Structured data'
      }
    }.freeze
  
    def self.available_models
      OllamaClient.models.map { |m| m['name'] }
    end
  
    def self.best_model(category)
      config = MODEL_CONFIG[category]
      models = available_models
  
      models.find { |m| m.include?(config[:primary].split(':').first) } ||
        models.find { |m| m.include?(config[:fallback].split(':').first) } ||
        models.first
    end
  end
  