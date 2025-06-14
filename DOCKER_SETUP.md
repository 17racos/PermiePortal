# 🐳 PermieBro Docker Setup with Ollama

This guide will help you set up the complete PermieBro AI system using Docker containers, including local AI processing with Ollama.

## 🚀 Quick Start

### Prerequisites
- Docker and Docker Compose installed
- At least 8GB RAM available for Ollama
- 10GB+ free disk space for models

### Option 1: GPU-Enabled Setup (Recommended)
If you have an NVIDIA GPU with Docker GPU support:

```bash
# Start all services
docker-compose up -d

# Wait for services to start, then run setup
docker-compose exec web ./scripts/docker_setup_permie_bro.sh
```

### Option 2: CPU-Only Setup
For systems without GPU support:

```bash
# Start all services with CPU-only configuration
docker-compose -f docker-compose.cpu.yml up -d

# Wait for services to start, then run setup
docker-compose exec web ./scripts/docker_setup_permie_bro.sh
```

## 📋 Services Overview

The Docker setup includes:

- **web**: Rails application (Port 3000)
- **db**: PostgreSQL database (Port 5432)
- **redis**: Redis cache (Port 6379)
- **ollama**: Local AI model server (Port 11434)
- **sidekiq**: Background job processor

## 🦙 Ollama Configuration

### Models Included
- **llama3.1:8b**: Primary model for plant consultation
- **llama3.1:latest**: Latest version for optimal performance

### Model Management
```bash
# List available models
docker-compose exec ollama ollama list

# Pull additional models
docker-compose exec ollama ollama pull mistral:7b

# Test a model
docker-compose exec ollama ollama run llama3.1:8b "What are companion plants for tomatoes?"
```

## 🌱 PermieBro Setup Commands

### Initial Setup
```bash
# Complete system setup (run once)
docker-compose exec web rails permie_bro:setup
```

### Individual Setup Steps
```bash
# Generate semantic ontology
docker-compose exec web rails permie_bro:generate_ontology

# Auto-tag existing plants
docker-compose exec web rails permie_bro:auto_tag_plants

# Setup vector search
docker-compose exec web rails permie_bro:setup_vector_search

# Test AI responses
docker-compose exec web rails permie_bro:test_ai
```

## 🧪 Testing the System

### Health Checks
```bash
# Check all services
curl http://localhost:3000/health

# Check Ollama directly
curl http://localhost:11434/api/tags
```

### Test PermieBro AI
```bash
# Run example queries
docker-compose exec web ruby examples/permie_bro_examples.rb

# Interactive Rails console
docker-compose exec web rails console
```

### Example Usage in Console
```ruby
# Initialize PermieBro
permie_bro = PermieBroService.new(llm_provider: :ollama)

# Ask a question
result = permie_bro.ask(
  "What are good companion plants for tomatoes?",
  context: { zone: "7a" }
)

puts result[:answer]
result[:plants].each { |plant| puts "- #{plant.common_name}" }
```

## 📊 System Statistics
```bash
# View system stats
docker-compose exec web rails permie_bro:stats

# Monitor resource usage
docker stats
```

## 🔧 Troubleshooting

### Common Issues

#### Ollama Models Not Loading
```bash
# Check Ollama logs
docker-compose logs ollama

# Manually pull models
docker-compose exec ollama ollama pull llama3.1:8b
```

#### Database Connection Issues
```bash
# Check database status
docker-compose exec db pg_isready -U postgres

# Reset database
docker-compose exec web rails db:drop db:create db:migrate
```

#### Memory Issues
```bash
# Check memory usage
docker stats

# Reduce Ollama memory limit in docker-compose.yml
# deploy:
#   resources:
#     limits:
#       memory: 4G
```

### Performance Optimization

#### For Limited Resources
1. Use smaller models: `llama3.1:7b` instead of `llama3.1:8b`
2. Reduce memory limits in docker-compose.yml
3. Disable vector search: `use_vector_search: false`

#### For Better Performance
1. Use GPU-enabled setup
2. Increase memory allocation
3. Use SSD storage for Docker volumes

## 🔄 Development Workflow

### Making Changes
```bash
# Rebuild after code changes
docker-compose build web

# Restart specific service
docker-compose restart web

# View logs
docker-compose logs -f web
```

### Database Operations
```bash
# Run migrations
docker-compose exec web rails db:migrate

# Seed data
docker-compose exec web rails db:seed

# Database console
docker-compose exec db psql -U postgres -d permieportal_development
```

## 🛑 Stopping Services

```bash
# Stop all services
docker-compose down

# Stop and remove volumes (WARNING: deletes data)
docker-compose down -v

# Stop and remove images
docker-compose down --rmi all
```

## 📈 Monitoring

### Service Health
- Web app: http://localhost:3000/health
- Ollama API: http://localhost:11434/api/tags
- Database: `docker-compose exec db pg_isready -U postgres`

### Logs
```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f web
docker-compose logs -f ollama
```

## 🔐 Security Notes

- Default passwords are used for development
- Change credentials for production deployment
- Ollama API is exposed on localhost only
- Consider firewall rules for production

## 📚 Additional Resources

- [Ollama Documentation](https://ollama.ai/docs)
- [Docker Compose Reference](https://docs.docker.com/compose/)
- [PermieBro Examples](examples/permie_bro_examples.rb)

## 🆘 Support

If you encounter issues:
1. Check the troubleshooting section above
2. Review service logs: `docker-compose logs`
3. Verify system requirements (RAM, disk space)
4. Test individual components separately 