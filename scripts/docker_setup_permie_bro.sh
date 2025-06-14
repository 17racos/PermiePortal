#!/bin/bash

# Docker setup script for PermieBro AI system
echo "🌱 Setting up PermieBro AI System in Docker..."

# Wait for all services to be healthy
echo "⏳ Waiting for services to be ready..."

# Wait for database
until pg_isready -h db -p 5432 -U postgres; do
  echo "Waiting for database..."
  sleep 2
done

# Wait for Ollama
until curl -f http://ollama:11434/api/tags > /dev/null 2>&1; do
  echo "Waiting for Ollama..."
  sleep 5
done

echo "✅ All services are ready!"

# Run database migrations
echo "🗄️  Running database migrations..."
bundle exec rails db:create db:migrate

# Setup PermieBro AI system
echo "🤖 Setting up PermieBro AI system..."
bundle exec rails permie_bro:setup

# Download Ollama models if not already present
echo "📥 Ensuring Ollama models are available..."
curl -X POST http://ollama:11434/api/pull \
  -H "Content-Type: application/json" \
  -d '{"name": "llama3.1:8b"}' &

# Test the system
echo "🧪 Testing PermieBro AI..."
bundle exec rails permie_bro:test_ai

echo "✅ PermieBro setup complete!"
echo "🌐 Access the application at http://localhost:3000"
echo "🦙 Ollama API available at http://localhost:11434" 