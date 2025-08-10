# AI Response System Guide

## Overview
The PermiePortal AI response system is designed to provide intelligent, context-aware responses to user queries about plants, gardening, and permaculture. This guide explains how the system works, how to configure it, and how to extend its capabilities.

## System Architecture

### Components
1. **PermieGPT Service**
   - Handles natural language processing
   - Manages context and user preferences
   - Integrates with Ollama for LLM capabilities
   - Formats responses with structured sections

2. **Response Formatter**
   - Structures responses into clear sections
   - Adds conversational elements
   - Includes knowledge gaps and recommendations
   - Provides resource links

3. **Context Manager**
   - Tracks user location and climate zone
   - Maintains soil type information
   - Stores user experience level
   - Records gardening goals

## Configuration

### Environment Variables
```bash
OLLAMA_URL=http://localhost:11434  # Ollama API endpoint
RAILS_ENV=development              # Application environment
DATABASE_URL=postgres://...        # Database connection
REDIS_URL=redis://localhost:6379/1 # Redis connection
```

### Response Sections
The system organizes responses into these key sections:
1. Site Analysis
2. Plant Profiles
3. Integration Strategy
4. Maintenance Plan
5. Knowledge Gaps
6. Seasonal Considerations
7. Pest & Disease Management
8. Harvest & Propagation

## Usage Examples

### Basic Query
```ruby
response = PermieGptService.new.query(
  query: "How do I grow tomatoes?",
  location: "California",
  zone: "9b",
  soil: "Sandy loam",
  experience_level: "Beginner",
  goals: ["Food production", "Easy maintenance"]
)
```

### Response Format
```json
{
  "success": true,
  "data": {
    "response": "Formatted response with sections...",
    "knowledge_gaps": [
      {
        "gap": "Specific soil pH requirements",
        "recommendation": "Conduct soil test"
      }
    ]
  }
}
```

## Customization

### Adding New Sections
1. Update the `sections` hash in `PermieGptService`
2. Add corresponding formatting in `format_response`
3. Update the response template

### Modifying Response Style
1. Adjust the conversational tone in `format_response`
2. Modify section prompts and descriptions
3. Update the closing message

## Troubleshooting

### Common Issues
1. **Slow Responses**
   - Check Ollama connection
   - Verify Redis caching
   - Monitor system resources

2. **Incomplete Responses**
   - Check section formatting
   - Verify context data
   - Review prompt templates

3. **Connection Errors**
   - Verify environment variables
   - Check service availability
   - Review network configuration

## Best Practices

### Response Quality
1. Keep responses concise but informative
2. Include practical, actionable advice
3. Highlight important considerations
4. Provide context-specific recommendations

### Performance
1. Use caching for common queries
2. Optimize prompt length
3. Batch similar requests
4. Monitor response times

### Maintenance
1. Regularly update plant data
2. Review and refine prompts
3. Monitor user feedback
4. Update knowledge base

## API Reference

### PermieGptService
```ruby
class PermieGptService
  def query(params)
    # Process query and return response
  end

  def format_response(response)
    # Format response with sections
  end
end
```

### Response Parameters
```ruby
{
  query: String,           # User's question
  location: String,        # Geographic location
  zone: String,           # USDA zone
  soil: String,           # Soil type
  experience_level: String,# User's experience
  goals: Array            # Gardening goals
}
```

## Contributing

### Adding Features
1. Fork the repository
2. Create a feature branch
3. Add tests
4. Submit pull request

### Code Style
1. Follow Ruby style guide
2. Add documentation
3. Include examples
4. Update tests

## Support

### Getting Help
1. Check troubleshooting guide
2. Review documentation
3. Submit issue on GitHub
4. Contact maintainers

### Resources
1. [Ollama Documentation](https://ollama.ai/docs)
2. [Ruby on Rails Guide](https://guides.rubyonrails.org)
3. [Permaculture Resources](https://permaculture.org)
4. [Plant Database](https://plants.usda.gov) 