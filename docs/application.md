# PermiePortal Application Documentation

## Overview
PermiePortal is a comprehensive permaculture plant database and AI-powered gardening assistant. The application helps users discover, learn about, and manage plants in their permaculture gardens.

## Core Components

### 1. Plant Database
- Enhanced plant information storage
- Scientific and common name indexing
- Plant characteristics and requirements
- Growing zones and climate data
- Companion planting relationships
- Materialized views for common combinations

### 2. AI Integration
- Ollama-based natural language processing
- Context-aware plant recommendations
- Intelligent search capabilities
- Dynamic response generation
- Streaming support
- Optimized prompt handling

### 3. Search System
- Traditional filter-based search
- AI-powered natural language search
- Hybrid search capabilities
- Real-time search suggestions
- Optimized database queries
- Better caching strategy

## Recent Optimizations

### Plant Name Extraction
The `PlantNameExtractorService` provides efficient plant name extraction with:
- Optimized text processing
- Multiple detection strategies
- Batch database queries
- Intelligent caching
- Pattern-based matching
- Scientific name recognition

### Plant Combinations
The new materialized view system provides:
- Fast combination lookups
- Automatic view refresh
- Pattern analysis
- Usage statistics
- Performance metrics
- Better query performance

### AI Service
The optimized `OllamaClient` includes:
- Streaming support
- Better error handling
- Improved caching
- Retry mechanism
- Health checks
- Usage tracking

### Performance Improvements
Recent optimizations include:
- Reduced database queries
- Better caching strategies
- Improved error handling
- Enhanced response times
- Optimized memory usage
- Better concurrency

## API Endpoints

### Plant Search
```
GET /api/v1/plants
```
Parameters:
- `query`: Natural language search query
- `location`: User's location
- `zone`: Growing zone
- `soil`: Soil type
- `experience_level`: User's experience
- `goals`: Array of gardening goals

### AI Query
```
POST /api/v1/permie_gpt/query
```
Parameters:
- `query`: User's question
- `location`: User's location
- `zone`: Growing zone
- `soil`: Soil type
- `experience_level`: User's experience
- `goals`: Array of gardening goals

### Health Check
```
GET /health
```
Returns:
- Database status
- AI service status
- Model information
- Timestamp

## Database Structure

### Enhanced Plants
- Common name
- Scientific name
- Growing requirements
- Environmental needs
- Plant characteristics
- Usage information

### Plant Relationships
- Companion plants
- Succession planting
- Guild relationships
- Ecological functions
- Materialized combinations
- Usage statistics

## Caching Strategy

### Plant Name Extraction
- In-memory caching
- 1-hour cache expiry
- Batch processing
- Smart cache keys

### Search Results
- Response caching
- Context-aware keys
- Automatic invalidation
- Memory-efficient storage

### AI Responses
- Prompt-based caching
- Model-specific keys
- Usage tracking
- Performance metrics

## Error Handling

### AI Service
- Retry mechanism
- Fallback responses
- Error logging
- Graceful degradation
- Exponential backoff
- Health monitoring

### Database Queries
- Batch processing
- Query optimization
- Error recovery
- Connection pooling
- View refresh
- Index maintenance

## Performance Metrics

### Response Times
- AI queries: < 2 seconds
- Plant searches: < 500ms
- Name extraction: < 100ms
- Health checks: < 50ms
- Stream processing: < 100ms/chunk
- View refresh: < 5 seconds

### Resource Usage
- Memory: Optimized caching
- CPU: Efficient processing
- Database: Reduced queries
- Network: Batch operations
- Storage: Materialized views
- Cache: Smart invalidation

## Maintenance Tasks

### Plant Combinations
```bash
# Refresh materialized view
rake plant_combinations:refresh

# Analyze patterns
rake plant_combinations:analyze
```

### Database Maintenance
```bash
# Reindex tables
rake db:reindex

# Vacuum analyze
rake db:vacuum
```

## Future Improvements
- Enhanced AI capabilities
- More plant data
- Better user experience
- Additional features
- Performance optimizations
- Better monitoring

## Contributing
Please refer to CONTRIBUTING.md for guidelines on how to contribute to the project.

## License
This project is licensed under the MIT License - see LICENSE.md for details. 