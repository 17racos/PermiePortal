# frozen_string_literal: true
class HealthController < ApplicationController
  def show
    render json: {
      status: 'ok',
      timestamp: Time.current,
      services: {
        database: database_healthy?,
        redis: redis_healthy?,
        ollama: ollama_healthy?
      }
    }
  end

  private

  def database_healthy?
    ActiveRecord::Base.connection.active?
  rescue StandardError
    false
  end

  def redis_healthy?
    Redis.new(url: ENV['REDIS_URL']).ping == 'PONG'
  rescue StandardError
    false
  end

  def ollama_healthy?
    return false unless ENV['OLLAMA_URL'].present?
    
    response = HTTP.get("#{ENV['OLLAMA_URL']}/api/health")
    response.status.success?
  rescue StandardError
    false
  end
end