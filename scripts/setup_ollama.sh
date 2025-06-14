#!/bin/bash

# Setup script for Ollama in Docker container
echo "🦙 Setting up Ollama for PermieBro..."

# Wait for Ollama service to be ready
echo "Waiting for Ollama service to start..."
until curl -f http://ollama:11434/api/tags > /dev/null 2>&1; do
  echo "Waiting for Ollama..."
  sleep 5
done

echo "✅ Ollama service is ready!"

# Pull required models
echo "📥 Downloading Llama 3.1 8B model..."
curl -X POST http://ollama:11434/api/pull \
  -H "Content-Type: application/json" \
  -d '{"name": "llama3.1:8b"}'

echo "📥 Downloading Llama 3.1 latest model..."
curl -X POST http://ollama:11434/api/pull \
  -H "Content-Type: application/json" \
  -d '{"name": "llama3.1:latest"}'

# Test the model
echo "🧪 Testing Ollama with a plant query..."
curl -X POST http://ollama:11434/api/generate \
  -H "Content-Type: application/json" \
  -d '{
    "model": "llama3.1:8b",
    "prompt": "What are good companion plants for tomatoes? Give a brief answer.",
    "stream": false
  }'

echo "✅ Ollama setup complete!" 