# config/initializers/ollama.rb

require 'net/http'
require 'json'
require 'uri'

module OLLAMA
  ENDPOINT = ENV.fetch('OLLAMA_HOST', 'http://host.docker.internal:11434')
  HEADERS = { 'Content-Type' => 'application/json' }

  def self.generate_completion(prompt, model = 'llama3.1:8b')
    uri = URI.parse("#{ENDPOINT}/api/generate")
    body = { model: model, prompt: prompt }.to_json

    response = Net::HTTP.post(uri, body, HEADERS)
    json = JSON.parse(response.body)

    json['response']
  rescue => e
    Rails.logger.error("OLLAMA error: #{e.message}")
    "OLLAMA error: #{e.message}"
  end

  def self.available_models
    uri = URI.parse("#{ENDPOINT}/api/tags")
    response = Net::HTTP.get_response(uri)
    models = JSON.parse(response.body)['models']
    models.map { |m| m['name'] }
  rescue => e
    Rails.logger.error("OLLAMA list error: #{e.message}")
    []
  end
end
