# frozen_string_literal: true
class ApplicationController < ActionController::Base
  def health
    health_status = {
      status: 'ok',
      timestamp: Time.current,
      services: {
        database: check_database,
        redis: check_redis,
        ollama: check_ollama
      }
    }

    render json: health_status
  end

  private

  def check_database
    ActiveRecord::Base.connection.execute('SELECT 1')
    { status: 'ok' }
  rescue => e
    { status: 'error', message: e.message }
  end

  def check_redis
    Redis.current.ping
    { status: 'ok' }
  rescue => e
    { status: 'error', message: e.message }
  end

  def check_ollama
    response = HTTP.timeout(5).get(ENV.fetch('OLLAMA_URL', 'http://localhost:11434') + '/api/health')
    { status: response.status.success? ? 'ok' : 'error' }
  rescue => e
    { status: 'error', message: e.message }
  end
end
