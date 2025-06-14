#!/bin/bash

# PermiePortal Application Startup Script
# This script handles common startup issues and provides a reliable way to start the application

set -e

echo "🌱 Starting PermiePortal Application..."

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker first."
    exit 1
fi

# Clean up any existing containers
echo "🧹 Cleaning up existing containers..."
docker-compose -f docker-compose.test.yml down --remove-orphans 2>/dev/null || true

# Check for port conflicts and suggest solutions
echo "🔍 Checking for port conflicts..."
if netstat -tlnp 2>/dev/null | grep -q ":3000 "; then
    echo "⚠️  Port 3000 is in use. Trying port 3001..."
    sed -i 's/"3000:3000"/"3001:3000"/g' docker-compose.test.yml
    PORT=3001
else
    PORT=3000
fi

# Start the application
echo "🚀 Starting application on port $PORT..."
docker-compose -f docker-compose.test.yml up -d web

# Wait for application to be ready
echo "⏳ Waiting for application to start..."
for i in {1..30}; do
    if curl -s -o /dev/null -w "%{http_code}" http://localhost:$PORT | grep -q "200"; then
        echo "✅ Application is ready!"
        break
    fi
    if [ $i -eq 30 ]; then
        echo "❌ Application failed to start within 30 seconds"
        echo "📋 Checking logs..."
        docker-compose -f docker-compose.test.yml logs web
        exit 1
    fi
    sleep 1
done

# Run basic health checks
echo "🏥 Running health checks..."

# Check database connection
echo "  📊 Testing database connection..."
if docker-compose -f docker-compose.test.yml exec -T web rails runner "puts EnhancedPlant.count" > /dev/null 2>&1; then
    echo "  ✅ Database connection: OK"
else
    echo "  ❌ Database connection: FAILED"
    exit 1
fi

# Check search functionality
echo "  🔍 Testing search functionality..."
if docker-compose -f docker-compose.test.yml exec -T web rails runner "puts EnhancedPlantSearchService.new.natural_language_search('herbs').count" > /dev/null 2>&1; then
    echo "  ✅ Search functionality: OK"
else
    echo "  ❌ Search functionality: FAILED"
    exit 1
fi

# Check web interface
echo "  🌐 Testing web interface..."
if curl -s http://localhost:$PORT/plants | grep -q "Discover Plants with AI"; then
    echo "  ✅ Web interface: OK"
else
    echo "  ❌ Web interface: FAILED"
    exit 1
fi

echo ""
echo "🎉 PermiePortal is ready!"
echo "📱 Access the application at: http://localhost:$PORT"
echo "🌱 Plants page: http://localhost:$PORT/plants"
echo ""
echo "🛠️  Useful commands:"
echo "   View logs: docker-compose -f docker-compose.test.yml logs web"
echo "   Stop app:  docker-compose -f docker-compose.test.yml down"
echo "   Restart:   ./scripts/start-app.sh"
echo "" 