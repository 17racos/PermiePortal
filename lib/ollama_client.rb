# lib/ollama_client.rb
class OllamaClient
    include HTTParty
    base_uri ENV.fetch('OLLAMA_URL', 'http://localhost:11434')
  
    def self.models
      get('/api/tags', timeout: 5).parsed_response["models"]
    rescue => e
      Rails.logger.warn("❌ OllamaClient error: #{e.message}")
      []
    end
  
    def self.health_check
      get('/api/tags', timeout: 5)
    rescue => e
      OpenStruct.new(success?: false, error: e.message)
    end
  end
  