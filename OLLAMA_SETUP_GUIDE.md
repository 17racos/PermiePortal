# Ollama LLM Integration Setup Guide for PermiePortal

## Overview

This guide will help you set up and configure the Ollama LLM integration for PermiePortal, enabling AI-powered plant recommendations, companion planting advice, and natural language queries using local language models.

## 🚀 Quick Start

### 1. Install Ollama

#### Linux/macOS:
```bash
curl -fsSL https://ollama.ai/install.sh | sh
```

#### Windows:
Download from [ollama.ai](https://ollama.ai/download)

### 2. Start Ollama Service
```bash
ollama serve
```

### 3. Pull a Language Model
```bash
# Recommended for good balance of speed and quality
ollama pull llama3.1:8b

# Or for better quality (larger model)
ollama pull llama3.1:13b

# Or for faster responses (smaller model)
ollama pull mistral:7b
```

### 4. Configure Environment Variables (Optional)
```bash
export OLLAMA_URL="http://localhost:11434"  # Default
export OLLAMA_MODEL="llama3.1:8b"           # Default
```

### 5. Run Database Migration
```bash
rails db:migrate
```

### 6. Generate Plant Contexts
```bash
rails ollama:generate_contexts
```

### 7. Test the Integration
```bash
rails ollama:test
```

## 📋 Features

### ✅ What's Included

1. **Natural Language Plant Queries**
   - Ask questions like "What are good companion plants for tomatoes?"
   - Get intelligent responses with plant recommendations

2. **Local LLM Processing**
   - No external API dependencies
   - Complete privacy - data never leaves your server
   - No usage costs or rate limits

3. **Chat Interface**
   - Interactive chat at `/plants/gpt_chat`
   - Context-aware conversations
   - Plant-specific advice

4. **API Endpoints**
   - RESTful API for all LLM features
   - Easy integration with frontend applications

5. **Plant Compatibility Analysis**
   - Analyze how well plants work together
   - Permaculture-focused recommendations

6. **AI-Enhanced Plant Search**
   - Intelligent plant search with natural language
   - Contextual recommendations

### 🔧 API Endpoints

#### POST `/api/v1/gpt/query`
Process natural language plant queries.

**Request:**
```json
{
  "query": "I need drought-tolerant plants for zone 8",
  "context": {
    "location": "Texas",
    "experience_level": "beginner"
  }
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "response": "For zone 8 in Texas, I recommend these drought-tolerant plants...",
    "type": "direct_response",
    "model": "llama3.1:8b",
    "usage": { "total_tokens": 150 }
  }
}
```

#### POST `/api/v1/gpt/chat`
Interactive chat with plant context.

**Request:**
```json
{
  "messages": [
    {"role": "user", "content": "How do I care for tomatoes?"}
  ],
  "plant_context": ["Tomato", "Basil"]
}
```

#### POST `/api/v1/gpt/search_plants`
AI-enhanced plant search.

**Request:**
```json
{
  "query": "plants that attract butterflies and are drought tolerant",
  "criteria": {
    "zone": "8"
  }
}
```

#### POST `/api/v1/gpt/analyze_compatibility`
Analyze plant compatibility for companion planting.

**Request:**
```json
{
  "plants": ["Tomato", "Basil", "Marigold"]
}
```

#### GET `/api/v1/gpt/status`
Check LLM integration status.

**Response:**
```json
{
  "success": true,
  "data": {
    "llm_available": true,
    "provider": "Ollama",
    "url": "http://localhost:11434",
    "model": "llama3.1:8b",
    "available_models": ["llama3.1:8b", "mistral:7b"],
    "features": {
      "query_processing": true,
      "chat": true,
      "plant_search": true,
      "recommendations": true,
      "compatibility_analysis": true
    }
  }
}
```

#### GET `/api/v1/gpt/models`
List available Ollama models.

**Response:**
```json
{
  "success": true,
  "data": {
    "available_models": ["llama3.1:8b", "mistral:7b"],
    "current_model": "llama3.1:8b",
    "provider": "Ollama"
  }
}
```

## 🛠 Configuration Options

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `OLLAMA_URL` | Ollama server URL | `http://localhost:11434` |
| `OLLAMA_MODEL` | Model to use for queries | `llama3.1:8b` |

### Model Recommendations

| Model | Size | Speed | Quality | Use Case |
|-------|------|-------|---------|----------|
| `mistral:7b` | ~4GB | Fast | Good | Quick queries, simple advice |
| `llama3.1:8b` | ~4.7GB | Medium | Very Good | **Recommended** - Best balance |
| `llama3.1:13b` | ~7.3GB | Slower | Excellent | Detailed analysis, complex queries |
| `codellama:7b` | ~3.8GB | Fast | Good | Structured responses |

## 📊 Monitoring and Maintenance

### Check Status
```bash
rails ollama:status
```

### Test Integration
```bash
rails ollama:test
```

### Benchmark Performance
```bash
rails ollama:benchmark
```

### Update Plant Contexts
```bash
rails ollama:update_contexts
```

### List Available Models
```bash
rails ollama:list_models
```

### Pull New Models
```bash
rails ollama:pull_model[llama3.1:13b]
```

### Clean Cache
```bash
rails ollama:cleanup_cache
```

## 🎯 Usage Examples

### Frontend Chat Interface

Visit `/plants/gpt_chat` for an interactive chat interface where you can:
- Ask about specific plants
- Get companion planting advice
- Request plant recommendations
- Diagnose plant problems

### API Integration

```javascript
// Query for drought-tolerant plants
const response = await fetch('/api/v1/gpt/query', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    query: "What are the best drought-tolerant vegetables for zone 9?",
    context: { location: "Arizona", experience_level: "intermediate" }
  })
});

const data = await response.json();
console.log(data.data.response);
```

### AI-Enhanced Plant Search

```javascript
// Search with natural language
const response = await fetch('/api/v1/gpt/search_plants', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    query: "plants that attract pollinators and grow in partial shade",
    criteria: { zone: "7" }
  })
});

const results = await response.json();
console.log(results.data.ai_response);
console.log(results.data.plants);
```

### Plant Compatibility Analysis

```javascript
// Analyze compatibility of multiple plants
const response = await fetch('/api/v1/gpt/analyze_compatibility', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    plants: ["Tomato", "Basil", "Marigold", "Nasturtium"]
  })
});

const analysis = await response.json();
console.log(analysis.data.analysis);
```

## 🚨 Troubleshooting

### Common Issues

1. **"Ollama not available"**
   - Ensure Ollama is installed: `ollama --version`
   - Start the service: `ollama serve`
   - Check if it's running: `curl http://localhost:11434/api/tags`

2. **"Model not found"**
   - List available models: `ollama list`
   - Pull the required model: `ollama pull llama3.1:8b`
   - Check model name matches exactly

3. **Slow responses**
   - Use a smaller model: `mistral:7b`
   - Ensure sufficient RAM (8GB+ recommended)
   - Check CPU usage during queries

4. **Connection refused**
   - Verify Ollama URL: `echo $OLLAMA_URL`
   - Check firewall settings
   - Ensure Ollama is bound to correct interface

### Debug Commands

```bash
# Check overall status
rails ollama:status

# Test the integration
rails ollama:test

# Benchmark performance
rails ollama:benchmark

# Check Ollama directly
curl http://localhost:11434/api/tags

# Check logs
tail -f log/development.log | grep -i ollama
```

## 💡 Best Practices

1. **Model Selection**
   - Start with `llama3.1:8b` for best balance
   - Use `mistral:7b` for faster responses
   - Upgrade to `llama3.1:13b` for better quality

2. **Performance Optimization**
   - Ensure adequate RAM (8GB+ recommended)
   - Use SSD storage for better model loading
   - Consider GPU acceleration for larger models

3. **Resource Management**
   - Monitor memory usage during queries
   - Set appropriate timeouts
   - Cache responses when possible

4. **Security**
   - Keep Ollama updated
   - Restrict network access if needed
   - Monitor resource usage

## 🔄 Fallback Mode

When Ollama is not available, the system runs in "fallback mode":
- Basic keyword-based responses
- Database search still works
- No AI-generated content
- All endpoints remain functional

This ensures your application continues to work even without LLM integration.

## 📈 Advanced Configuration

### Custom Model Parameters

You can customize model behavior by modifying the `OllamaGptService`:

```ruby
# In app/services/ollama_gpt_service.rb
options: {
  temperature: 0.7,    # Creativity (0.0-1.0)
  top_p: 0.9,         # Nucleus sampling
  top_k: 40,          # Top-k sampling
  num_predict: 1000   # Max tokens to generate
}
```

### Multiple Model Support

Set up different models for different use cases:

```bash
# Fast model for simple queries
export OLLAMA_MODEL_FAST="mistral:7b"

# Quality model for detailed analysis
export OLLAMA_MODEL_QUALITY="llama3.1:13b"
```

### Docker Integration

Add to your `docker-compose.yml`:

```yaml
services:
  ollama:
    image: ollama/ollama:latest
    ports:
      - "11434:11434"
    volumes:
      - ollama_data:/root/.ollama
    environment:
      - OLLAMA_HOST=0.0.0.0

volumes:
  ollama_data:
```

## 🆘 Support

If you encounter issues:
1. Check the troubleshooting section above
2. Run `rails ollama:test` for diagnostics
3. Check application logs for detailed error messages
4. Verify Ollama is running: `ollama list`
5. Test Ollama directly: `curl http://localhost:11434/api/tags`

## 📚 Model Information

### Recommended Models for Plant Advice

1. **llama3.1:8b** (Recommended)
   - Size: ~4.7GB
   - Good balance of speed and quality
   - Excellent for plant advice and recommendations

2. **mistral:7b** (Fast Option)
   - Size: ~4GB
   - Faster responses
   - Good for simple queries and quick advice

3. **llama3.1:13b** (Quality Option)
   - Size: ~7.3GB
   - Best quality responses
   - Ideal for detailed analysis and complex queries

### Installing Additional Models

```bash
# Pull specific models
ollama pull llama3.1:8b
ollama pull mistral:7b
ollama pull codellama:7b

# List all available models
ollama list

# Remove unused models
ollama rm model_name
```

---

**Happy Local AI Gardening! 🌱🤖** 