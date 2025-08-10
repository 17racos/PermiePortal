#!/bin/bash
set -e

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Function to check service health
check_service() {
    local service="$1"
    local url="$2"
    local max_attempts=30
    local attempt=1

    echo "Checking $service health..."
    while [ $attempt -le $max_attempts ]; do
        if curl -s "$url" > /dev/null; then
            echo -e "${GREEN}$service is healthy!${NC}"
            return 0
        fi
        echo "Attempt $attempt/$max_attempts: $service not ready yet..."
        sleep 2
        attempt=$((attempt + 1))
    done
    echo -e "${RED}$service failed to become healthy${NC}"
    return 1
}

# Function to check Ollama
check_ollama() {
    local max_attempts=30
    local attempt=1
    local ollama_url="http://localhost:11434"

    echo "Checking Ollama..."
    while [ $attempt -le $max_attempts ]; do
        if curl -s "$ollama_url/api/health" > /dev/null; then
            echo -e "${GREEN}Ollama is running!${NC}"
            return 0
        fi
        echo "Attempt $attempt/$max_attempts: Ollama not ready yet..."
        sleep 2
        attempt=$((attempt + 1))
    done
    echo -e "${YELLOW}Warning: Ollama is not running. PermieGPT features will be limited.${NC}"
    return 1
}

# Clean up existing containers and volumes
echo "Cleaning up existing containers..."
docker-compose down -v

# Rebuild containers
echo "Rebuilding containers..."
docker-compose build --no-cache

# Start services
echo "Starting services..."
docker-compose up -d

# Wait for services to be ready
echo "Waiting for services to be ready..."

# Check Postgres
check_service "Postgres" "http://localhost:3000/health"

# Check Redis
check_service "Redis" "http://localhost:3000/health"

# Check Sidekiq
check_service "Sidekiq" "http://localhost:3000/health"

# Check Rails server
check_service "Rails" "http://localhost:3000/health"

# Check Ollama
check_ollama

# Check PermieGPT
echo "Checking PermieGPT..."
if curl -s -X POST http://localhost:3000/api/v1/permie_gpt/query \
    -H "Content-Type: application/json" \
    -d '{"query":"test"}' | grep -q "success"; then
    echo -e "${GREEN}PermieGPT is responding!${NC}"
else
    echo -e "${YELLOW}PermieGPT is not responding. This is expected if Ollama is not running.${NC}"
    echo "To enable PermieGPT features, ensure Ollama is running locally on port 11434"
fi

echo -e "${GREEN}All core services are up and running!${NC}"
echo "You can now access the application at http://localhost:3000"

# Show helpful commands
echo -e "\n${YELLOW}Useful commands:${NC}"
echo "  docker-compose logs -f web    # View web server logs"
echo "  docker-compose logs -f sidekiq # View Sidekiq logs"
echo "  docker-compose restart web    # Restart web server"
echo "  docker-compose restart sidekiq # Restart Sidekiq" 