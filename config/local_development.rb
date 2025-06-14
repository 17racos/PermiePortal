# Local Development Configuration
# This file sets environment variables for local development
# Load this by running: source config/local_development.rb (if it were a shell script)
# Or better yet, we'll create a Rails initializer

# Set environment variables for local development
ENV['DATABASE_HOST'] = 'localhost'
ENV['DATABASE_USERNAME'] = 'postgres'
ENV['DATABASE_PASSWORD'] = 'postgres'
ENV['DATABASE_NAME'] = 'permieportal_development'

# Ollama Configuration
ENV['OLLAMA_URL'] = 'http://localhost:11434'
ENV['OLLAMA_MODEL'] = 'llama3.1:8b'

# Rails Configuration
ENV['RAILS_MAX_THREADS'] = '5'

Rails.logger.info "🔧 Local development configuration loaded"
Rails.logger.info "   Database Host: #{ENV['DATABASE_HOST']}"
Rails.logger.info "   Ollama URL: #{ENV['OLLAMA_URL']}"
Rails.logger.info "   Ollama Model: #{ENV['OLLAMA_MODEL']}" 