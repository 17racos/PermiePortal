# PermiePortal Application Startup Guide

## Prerequisites

### System Requirements
- Ruby 3.2.0 or higher
- PostgreSQL 13 or higher
- Redis 6.0 or higher
- Node.js 16 or higher
- Yarn 1.22 or higher
- Ollama (for AI features)
- 4GB RAM minimum
- 10GB free disk space

### Required Services
1. **PostgreSQL**
   ```bash
   # Check status
   sudo service postgresql status
   
   # Start if needed
   sudo service postgresql start
   
   # Create database user
   sudo -u postgres createuser -s $USER
   ```

2. **Redis**
   ```bash
   # Check status
   sudo service redis-server status
   
   # Start if needed
   sudo service redis-server start
   
   # Test connection
   redis-cli ping
   ```

3. **Ollama**
   ```bash
   # Check status
   curl http://localhost:11434/api/version
   
   # Start if needed
   ollama serve
   
   # Pull required model
   ollama pull mistral
   ```

## Application Setup

### 1. Clone and Dependencies
```bash
# Clone repository
git clone https://github.com/your-org/permieportal.git
cd permieportal

# Install Ruby dependencies
bundle install

# Install JavaScript dependencies
yarn install
```

### 2. Database Setup
```bash
# Create database
rails db:create

# Run migrations
rails db:migrate

# Seed initial data
rails db:seed
```

### 3. Environment Configuration
```bash
# Create .env file
cp .env.example .env

# Edit environment variables
nano .env

# Required variables
RAILS_ENV=development
DATABASE_URL=postgres://postgres:postgres@localhost:5432/permieportal_development
REDIS_URL=redis://localhost:6379/1
OLLAMA_URL=http://localhost:11434
PORT=3000
```

## Starting the Application

### 1. Kill Existing Processes
```bash
# Kill any existing Rails server
pkill -f "rails server"

# Kill any existing Ollama processes
pkill -f "ollama serve"
```

### 2. Start Services
```bash
# Start PostgreSQL
sudo service postgresql start

# Start Redis
sudo service redis-server start

# Start Ollama
ollama serve
```

### 3. Start Application
```bash
# Start Rails server with all required environment variables
RAILS_ENV=development \
DATABASE_URL=postgres://postgres:postgres@localhost:5432/permieportal_development \
REDIS_URL=redis://localhost:6379/1 \
OLLAMA_URL=http://localhost:11434 \
PORT=3000 \
bundle exec rails server
```

## Verification Steps

### 1. Database Connection
```bash
# Check database connection
rails db:version

# Verify plant data
rails runner "puts EnhancedPlant.count"
```

### 2. Redis Connection
```bash
# Test Redis connection
rails runner "puts Rails.cache.write('test', 'ok')"
rails runner "puts Rails.cache.read('test')"
```

### 3. Ollama Integration
```bash
# Test Ollama connection
curl http://localhost:11434/api/version

# Test AI response
curl -X POST http://localhost:3000/api/v1/permie_gpt/query \
  -H "Content-Type: application/json" \
  -d '{"query":"test query"}'
```

### 4. Web Interface
```bash
# Check web server
curl -s -o /dev/null -w "%{http_code}" http://localhost:3000

# Should return: 200
```

## Troubleshooting

### 1. Database Issues
```bash
# Reset database
rails db:drop db:create db:migrate db:seed

# Check logs
tail -f log/development.log

# Verify connection
rails dbconsole
```

### 2. Redis Issues
```bash
# Check Redis logs
tail -f /var/log/redis/redis-server.log

# Test Redis
redis-cli ping

# Clear Redis
redis-cli flushall
```

### 3. Ollama Issues
```bash
# Check Ollama status
curl http://localhost:11434/api/version

# Restart Ollama
pkill -f "ollama serve"
ollama serve

# Pull model again
ollama pull mistral
```

### 4. Application Issues
```bash
# Check Rails logs
tail -f log/development.log

# Clear temporary files
rails tmp:clear

# Restart application
pkill -f "rails server"
RAILS_ENV=development bundle exec rails server
```

## Performance Optimization

### 1. Database
```bash
# Analyze database
rails db:analyze

# Optimize indexes
rails db:optimize_indexes
```

### 2. Cache
```bash
# Clear cache
rails tmp:cache:clear

# Warm cache
rails cache:warm
```

### 3. Assets
```bash
# Precompile assets
rails assets:precompile

# Clean and recompile
rails assets:clean assets:precompile
```

## Monitoring

### 1. Application Logs
```bash
# View Rails logs
tail -f log/development.log

# View PostgreSQL logs
tail -f /var/log/postgresql/postgresql-*.log

# View Redis logs
tail -f /var/log/redis/redis-server.log
```

### 2. System Resources
```bash
# Check system resources
htop

# Monitor database
pg_stat_activity

# Check Redis memory
redis-cli info memory
```

## Common Issues

### 1. Port Conflicts
```bash
# Find process using port
lsof -i :3000

# Kill process
kill -9 <PID>

# Or use different port
PORT=3001 rails server
```

### 2. Memory Issues
```bash
# Check memory usage
free -h

# Clear system cache
sudo sync && sudo sysctl -w vm.drop_caches=3
```

### 3. Permission Issues
```bash
# Fix permissions
sudo chown -R $USER:$USER .

# Fix database permissions
sudo chown -R postgres:postgres /var/lib/postgresql
```

## Maintenance

### 1. Regular Updates
```bash
# Update dependencies
bundle update
yarn upgrade

# Run migrations
rails db:migrate
```

### 2. Backup
```bash
# Backup database
rails db:backup

# Backup assets
rails assets:backup
```

### 3. Cleanup
```bash
# Clean temporary files
rails tmp:clear

# Clean logs
rails log:clear
```

## Support

### Getting Help
1. Check the logs for error messages
2. Review the documentation
3. Search existing issues
4. Create a new issue with:
   - Error message
   - Steps to reproduce
   - Environment details
   - Log files

### Resources
- [Rails Documentation](https://guides.rubyonrails.org)
- [PostgreSQL Documentation](https://www.postgresql.org/docs)
- [Redis Documentation](https://redis.io/documentation)
- [Ollama Documentation](https://ollama.ai/docs) 