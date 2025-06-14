# GPT Integration Setup Guide for PermiePortal

## Overview

This guide will help you set up and configure the GPT integration for PermiePortal, enabling AI-powered plant recommendations, companion planting advice, and natural language queries.

## 🚀 Quick Start

### 1. Configure OpenAI API Key

You have two options for setting up your OpenAI API key:

#### Option A: Environment Variable (Recommended)
```bash
export OPENAI_API_KEY="your_openai_api_key_here"
```

#### Option B: Rails Credentials
```bash
rails credentials:edit
```

Add to the credentials file:
```yaml
openai:
  api_key: your_openai_api_key_here
```

### 2. Run Database Migration
```bash
rails db:migrate
```

### 3. Generate Plant Contexts
```bash
rails gpt:generate_contexts
```

### 4. Test the Integration
```bash
rails gpt:test
```

## 📋 Features

### ✅ What's Included

1. **Natural Language Plant Queries**
   - Ask questions like "What are good companion plants for tomatoes?"
   - Get intelligent responses with plant recommendations

2. **Function Calling Integration**
   - GPT can search your plant database
   - Retrieve detailed plant information
   - Find companion plants
   - Generate location-based recommendations

3. **Chat Interface**
   - Interactive chat at `/plants/gpt_chat`
   - Context-aware conversations
   - Plant-specific advice

4. **API Endpoints**
   - RESTful API for all GPT features
   - Easy integration with frontend applications

5. **Plant Compatibility Analysis**
   - Analyze how well plants work together
   - Permaculture-focused recommendations

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
    "type": "function_call",
    "function_used": "search_plants_by_criteria",
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

#### POST `/api/v1/gpt/analyze_compatibility`
Analyze plant compatibility for companion planting.

**Request:**
```json
{
  "plants": ["Tomato", "Basil", "Marigold"]
}
```

#### GET `/api/v1/gpt/status`
Check GPT integration status.

**Response:**
```json
{
  "success": true,
  "data": {
    "gpt_available": true,
    "features": {
      "query_processing": true,
      "chat": true,
      "function_calling": true,
      "plant_analysis": true
    },
    "provider": "OpenAI",
    "model": "gpt-4-turbo-preview"
  }
}
```

## 🛠 Configuration Options

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `OPENAI_API_KEY` | Your OpenAI API key | None (required) |
| `OPENAI_ORGANIZATION_ID` | OpenAI organization ID | None (optional) |

### Model Configuration

The integration uses `gpt-4-turbo-preview` by default. You can modify this in:
- `app/services/enhanced_gpt_service.rb`
- `config/initializers/openai.rb`

## 📊 Monitoring and Maintenance

### Check Status
```bash
rails gpt:status
```

### Update Plant Contexts
```bash
rails gpt:update_contexts
```

### Clean Cache
```bash
rails gpt:cleanup_cache
```

## 🔍 Available GPT Functions

The system includes these function definitions for GPT to use:

### Plant Search Functions
- `search_plants_by_criteria` - Search by zone, type, uses, traits
- `get_plant_details` - Get comprehensive plant information
- `find_companion_plants` - Find beneficial/antagonistic companions
- `recommend_plants_for_location` - Location-based recommendations

### Plant Care Functions
- `get_seasonal_care_calendar` - Seasonal care instructions
- `diagnose_plant_problems` - Help diagnose plant issues
- `create_planting_schedule` - Generate planting schedules

### Permaculture Functions
- `design_plant_guild` - Design permaculture plant guilds
- `analyze_ecosystem_services` - Analyze ecosystem benefits

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

1. **"OpenAI API key not found"**
   - Ensure your API key is set correctly
   - Check environment variables or Rails credentials
   - Run `rails gpt:test` to verify configuration

2. **"GPT features will run in fallback mode"**
   - This means the API key isn't configured
   - The system will still work but without AI features
   - Set up your OpenAI API key to enable full functionality

3. **Function calling not working**
   - Ensure you're using a compatible OpenAI model
   - Check that function definitions are loaded correctly
   - Verify your API key has access to function calling

### Debug Commands

```bash
# Check overall status
rails gpt:status

# Test the integration
rails gpt:test

# Check logs
tail -f log/development.log | grep -i gpt
```

## 💡 Best Practices

1. **API Key Security**
   - Never commit API keys to version control
   - Use environment variables or Rails credentials
   - Rotate keys regularly

2. **Rate Limiting**
   - Be mindful of OpenAI API rate limits
   - Implement caching for repeated queries
   - Use fallback responses when appropriate

3. **Error Handling**
   - Always handle API failures gracefully
   - Provide meaningful fallback responses
   - Log errors for debugging

4. **Performance**
   - Generate plant contexts in advance
   - Use appropriate model parameters
   - Cache responses when possible

## 🔄 Fallback Mode

When the OpenAI API key is not configured, the system runs in "fallback mode":
- Basic keyword-based responses
- Database search still works
- No AI-generated content
- All endpoints remain functional

This ensures your application continues to work even without GPT integration.

## 📈 Future Enhancements

Planned improvements include:
- Vector embeddings for semantic search
- Integration with local LLM models (Ollama)
- Advanced plant recommendation algorithms
- Seasonal care reminders
- Integration with weather APIs

## 🆘 Support

If you encounter issues:
1. Check the troubleshooting section above
2. Run `rails gpt:test` for diagnostics
3. Check application logs for detailed error messages
4. Ensure your OpenAI API key is valid and has sufficient credits

---

**Happy Gardening with AI! 🌱🤖** 