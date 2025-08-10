# Startup Troubleshooting Guide

## Quick Start
```bash
# Kill any existing Rails server
pkill -f "rails server"

# Start the server with required environment variables
RAILS_ENV=development \
DATABASE_URL=postgres://postgres:postgres@localhost:5432/permieportal_development \
REDIS_URL=redis://localhost:6379/1 \
OLLAMA_URL=http://localhost:11434 \
PORT=3000 \
bundle exec rails server
```

## Common Issues and Solutions

### 1. Database Connection Issues

#### Symptoms
- "Could not connect to PostgreSQL"
- "Database does not exist"
- "Connection refused"

#### Solutions
```bash
# Check PostgreSQL status
sudo service postgresql status

# Start PostgreSQL if stopped
sudo service postgresql start

# Create database if missing
rails db:create

# Run migrations
rails db:migrate

# Reset database if needed
rails db:drop db:create db:migrate db:seed
```

### 2. Redis Connection Issues

#### Symptoms
- "Could not connect to Redis"
- "Redis connection refused"
- Cache-related errors

#### Solutions
```bash
# Check Redis status
sudo service redis-server status

# Start Redis if stopped
sudo service redis-server start

# Test Redis connection
redis-cli ping
```

### 3. Ollama Integration Issues

#### Symptoms
- "Could not connect to Ollama"
- "Ollama service unavailable"
- AI responses failing

#### Solutions
```bash
# Check Ollama status
curl http://localhost:11434/api/version

# Start Ollama if stopped
ollama serve

# Pull required model
ollama pull mistral

# Verify model availability
ollama list
```

### 4. Environment Variable Issues

#### Symptoms
- "Missing required environment variable"
- Configuration errors
- Service connection failures

#### Solutions
```bash
# Create .env file
cp .env.example .env

# Edit environment variables
nano .env

# Verify environment variables
rails runner "puts ENV['DATABASE_URL']"
```

### 5. Asset Compilation Issues

#### Symptoms
- Missing JavaScript files
- CSS not loading
- Asset pipeline errors

#### Solutions
```bash
# Precompile assets
rails assets:precompile

# Clean and recompile
rails assets:clean assets:precompile

# Check asset pipeline
rails assets:check
```

### 6. Port Conflicts

#### Symptoms
- "Address already in use"
- "Port 3000 is already taken"
- Server won't start

#### Solutions
```bash
# Find process using port
lsof -i :3000

# Kill process
kill -9 <PID>

# Or use different port
PORT=3001 rails server
```

### 7. Gem Dependencies

#### Symptoms
- "Could not find gem"
- Bundle install failures
- Version conflicts

#### Solutions
```bash
# Update bundler
gem update bundler

# Install dependencies
bundle install

# Clean and reinstall
bundle clean --force
bundle install
```

### 8. JavaScript Dependencies

#### Symptoms
- "Module not found"
- JavaScript errors
- Yarn issues

#### Solutions
```bash
# Install JavaScript dependencies
yarn install

# Clean and reinstall
yarn cache clean
yarn install

# Check for updates
yarn upgrade
```

## System Requirements

### Minimum Requirements
- Ruby 3.2.0 or higher
- PostgreSQL 13 or higher
- Redis 6.0 or higher
- Node.js 16 or higher
- Yarn 1.22 or higher
- 4GB RAM minimum
- 10GB free disk space

### Recommended Requirements
- Ruby 3.2.2
- PostgreSQL 14
- Redis 7.0
- Node.js 18 LTS
- Yarn 1.22
- 8GB RAM
- 20GB free disk space

## Performance Optimization

### Database
```bash
# Analyze database performance
rails db:analyze

# Optimize indexes
rails db:optimize_indexes

# Check for slow queries
rails db:slow_queries
```

### Cache
```bash
# Clear cache
rails tmp:cache:clear

# Warm cache
rails cache:warm

# Check cache stats
rails cache:stats
```

### Assets
```bash
# Optimize images
rails assets:optimize_images

# Compress assets
rails assets:compress

# Check asset sizes
rails assets:size
```

## Monitoring

### Logs
```bash
# View Rails logs
tail -f log/development.log

# View PostgreSQL logs
tail -f /var/log/postgresql/postgresql-*.log

# View Redis logs
tail -f /var/log/redis/redis-server.log
```

### Metrics
```bash
# Check system resources
htop

# Monitor database
pg_stat_activity

# Check Redis memory
redis-cli info memory
```

## Security

### Database
```bash
# Check database security
rails db:security_check

# Audit database access
rails db:audit

# Rotate credentials
rails credentials:rotate
```

### Application
```bash
# Check for vulnerabilities
bundle audit

# Update dependencies
bundle update

# Run security checks
rails security:check
```

## Backup and Recovery

### Database
```bash
# Create backup
rails db:backup

# Restore from backup
rails db:restore

# Verify backup
rails db:verify_backup
```

### Assets
```bash
# Backup assets
rails assets:backup

# Restore assets
rails assets:restore

# Verify assets
rails assets:verify
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