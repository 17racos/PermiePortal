module LlmHelper
  def self.status
    {
      enabled: true, # or logic to check if LLM is available
      provider: "Ollama",
      url: ENV['OLLAMA_URL'] || "http://localhost:11434",
      model: ENV['OLLAMA_MODEL'] || "llama3.1:8b",
      available_models: ["llama3.1:8b", "mistral", "other-models"]
    }
  end
end