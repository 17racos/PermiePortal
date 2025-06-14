# PermiePortal Startup Troubleshooting Guide

## 🚀 Quick Start

Use the automated startup script:
```bash
./scripts/start-app.sh
```

## 🔧 Manual Startup

If you prefer manual control:

```bash
# 1. Start with simplified configuration
docker-compose -f docker-compose.test.yml up -d web

# 2. Check status
docker-compose -f docker-compose.test.yml ps

# 3. View logs
docker-compose -f docker-compose.test.yml logs web
```

## 🐛 Common Issues & Solutions

### Issue 1: Port Already in Use
**Error:** `bind: address already in use`

**Solution:**
```bash
# Check what's using the port
sudo netstat -tlnp | grep :3000

# Option A: Use different port
sed -i 's/"3000:3000"/"3001:3000"/g' docker-compose.test.yml

# Option B: Stop conflicting service
docker stop $(docker ps -q --filter "publish=3000")
```

### Issue 2: Database Connection Failed
**Error:** `ActiveRecord::DatabaseConnectionError`

**Solution:**
```bash
# Check if PostgreSQL is running
sudo systemctl status postgresql

# Start PostgreSQL if needed
sudo systemctl start postgresql

# Or use Docker PostgreSQL
docker run -d --name postgres-dev \
  -e POSTGRES_PASSWORD=postgres \
  -e POSTGRES_DB=permieportal_development \
  -p 5432:5432 postgres:15
```

### Issue 3: Redis Connection Failed
**Error:** `Redis::CannotConnectError`

**Solution:**
```bash
# Start Redis with Docker
docker run -d --name redis-dev -p 6379:6379 redis:7-alpine

# Or install locally
sudo apt-get install redis-server
sudo systemctl start redis-server
```

### Issue 4: Build Failures
**Error:** Docker build fails

**Solution:**
```bash
# Clear Docker cache
docker system prune -a

# Rebuild without cache
docker-compose -f docker-compose.test.yml build --no-cache web

# Check Dockerfile syntax
docker build -t permieportal-test .
```

### Issue 5: Missing Dependencies
**Error:** `Gem::LoadError` or missing gems

**Solution:**
```bash
# Rebuild bundle cache
docker-compose -f docker-compose.test.yml exec web bundle install

# Or rebuild container
docker-compose -f docker-compose.test.yml build web
```

### Issue 6: Database Not Migrated
**Error:** `ActiveRecord::PendingMigrationError`

**Solution:**
```bash
# Run migrations
docker-compose -f docker-compose.test.yml exec web rails db:migrate

# Check migration status
docker-compose -f docker-compose.test.yml exec web rails db:migrate:status
```

### Issue 7: Ollama/AI Service Not Available
**Error:** AI search not working

**Solution:**
```bash
# Start Ollama separately
docker run -d --name ollama-dev -p 11434:11434 ollama/ollama:latest

# Test Ollama
curl http://localhost:11434/api/tags

# The app will work without Ollama (fallback mode)
```

## 🏥 Health Checks

### Quick Health Check
```bash
# Test application response
curl -s -o /dev/null -w "%{http_code}" http://localhost:3000

# Should return: 200
```

### Database Health Check
```bash
docker-compose -f docker-compose.test.yml exec web rails runner "puts EnhancedPlant.count"
```

### Search Functionality Check
```bash
docker-compose -f docker-compose.test.yml exec web rails runner "puts EnhancedPlantSearchService.new.natural_language_search('herbs').count"
```

### UI Component Check
```bash
curl -s http://localhost:3000/plants | grep -q "Discover Plants with AI" && echo "UI OK" || echo "UI FAILED"
```

## 🔍 Debugging Commands

### View Application Logs
```bash
docker-compose -f docker-compose.test.yml logs web -f
```

### Access Rails Console
```bash
docker-compose -f docker-compose.test.yml exec web rails console
```

### Check Environment Variables
```bash
docker-compose -f docker-compose.test.yml exec web env | grep -E "(DATABASE|REDIS|OLLAMA)"
```

### Test Database Connection
```bash
docker-compose -f docker-compose.test.yml exec web rails db:version
```

## 🛠️ Development Tools

### Reset Everything
```bash
# Nuclear option - reset everything
docker-compose -f docker-compose.test.yml down -v
docker system prune -a
./scripts/start-app.sh
```

### Performance Monitoring
```bash
# Monitor container resources
docker stats permieportal_web_1

# Check disk usage
docker system df
```

### Network Debugging
```bash
# Check container networking
docker network ls
docker network inspect permieportal_app_network
```

## 📱 Testing the New Search Interface

### Test Natural Language Search
1. Go to http://localhost:3000/plants
2. Try searches like:
   - "drought tolerant herbs"
   - "pollinator friendly trees"
   - "edible ground cover"

### Test Quick Discovery
1. Click on the colorful discovery cards
2. Verify they filter results correctly

### Test Advanced Filters
1. Click "Show Advanced Filters"
2. Select multiple functions, layers, and zones
3. Verify combined filtering works

### Test UI Responsiveness
1. Resize browser window
2. Test on mobile viewport
3. Verify animations and hover effects

## 🆘 Getting Help

If you're still having issues:

1. **Check the logs:** `docker-compose -f docker-compose.test.yml logs web`
2. **Verify environment:** Ensure Docker, PostgreSQL, and Redis are available
3. **Try the automated script:** `./scripts/start-app.sh`
4. **Reset everything:** Use the nuclear option above

## 📊 Success Indicators

When everything is working correctly, you should see:

- ✅ Application responds on http://localhost:3000
- ✅ Plants page loads with "Discover Plants with AI" header
- ✅ Search functionality returns results
- ✅ Quick discovery cards are interactive
- ✅ Advanced filters toggle properly
- ✅ Database contains 198 plants (or your expected count)

## 🔄 Regular Maintenance

### Weekly
```bash
# Update containers
docker-compose -f docker-compose.test.yml pull
docker-compose -f docker-compose.test.yml up -d web
```

### Monthly
```bash
# Clean up Docker
docker system prune
docker volume prune
``` 