# frozen_string_literal: true
class ApplicationController < ActionController::Base
  def health
    render json: {
      status: 'ok',
      timestamp: Time.current,
      services: {
        database: database_healthy?,
        ollama: ollama_healthy?
      }
    }
  end

  private

  def database_healthy?
    ActiveRecord::Base.connection.execute('SELECT 1')
    true
  rescue
    false
  end

  def ollama_healthy?
    ollama_url = ENV['OLLAMA_URL'] || 'http://localhost:11434'
    response = HTTParty.get("#{ollama_url}/api/tags", timeout: 5)
    response.success?
  rescue
    false
  end
end
