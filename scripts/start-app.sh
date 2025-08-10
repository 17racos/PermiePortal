#!/bin/bash

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print status
print_status() {
    echo -e "${GREEN}[✓]${NC} $1"
}

print_error() {
    echo -e "${RED}[✗]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[!]${NC} $1"
}

# Function to check if Docker is running
check_docker() {
    if ! docker info > /dev/null 2>&1; then
        print_error "Docker is not running. Please start Docker first."
        exit 1
    fi
}

# Function to check if required ports are available
check_ports() {
    local ports=(3000 5432 6379 11434)
    for port in "${ports[@]}"; do
        if lsof -i ":$port" > /dev/null 2>&1; then
            print_warning "Port $port is in use. Stopping any running containers..."
            docker-compose down
            break
        fi
    done
}

# Function to stop existing containers
stop_containers() {
    print_status "Stopping existing containers..."
    docker-compose down
}

# Function to clean up Docker resources
cleanup_docker() {
    print_status "Cleaning up Docker resources..."
    docker system prune -f
}

# Function to check Docker Compose version
check_docker_compose() {
    if ! docker-compose version > /dev/null 2>&1; then
        print_error "Docker Compose is not installed. Please install Docker Compose."
        exit 1
    fi
}

# Function to check Ollama service
check_ollama() {
    print_status "Checking Ollama service..."
    if ! curl -s http://localhost:11434/api/tags > /dev/null 2>&1; then
        print_error "Ollama service is not running. Please start Ollama first."
        exit 1
    fi
}

# Function to setup database
setup_database() {
    print_status "Setting up database..."
    
    # Wait for database to be ready
    until docker-compose exec db pg_isready -h localhost -p 5432 > /dev/null 2>&1; do
        sleep 1
    done
    
    # Create database if it doesn't exist
    docker-compose exec db psql -U postgres -c "SELECT 1 FROM pg_database WHERE datname='permieportal_development'" | grep -q 1 || \
    docker-compose exec db psql -U postgres -c "CREATE DATABASE permieportal_development"
    
    # Grant privileges
    docker-compose exec db psql -U postgres -c "GRANT ALL PRIVILEGES ON DATABASE permieportal_development TO postgres"
    
    # Create extension if needed
    docker-compose exec db psql -U postgres -d permieportal_development -c "CREATE EXTENSION IF NOT EXISTS pg_trgm"
}

# Function to check database migrations
check_migrations() {
    print_status "Checking database migrations..."
    docker-compose exec web bundle exec rails db:migrate:status | grep -q "^\s*down"
    if [ $? -eq 0 ]; then
        print_status "Running pending migrations..."
        docker-compose exec web bundle exec rails db:migrate
    fi
}

# Function to wait for services to be ready
wait_for_services() {
    print_status "Waiting for services to be ready..."
    
    # Wait for database
    print_status "Waiting for database..."
    until docker-compose exec db pg_isready -h localhost -p 5432 > /dev/null 2>&1; do
        sleep 1
    done
    
    # Wait for Redis
    print_status "Waiting for Redis..."
    until docker-compose exec redis redis-cli ping > /dev/null 2>&1; do
        sleep 1
    done
    
    # Wait for web service
    print_status "Waiting for web service..."
    local max_attempts=30
    local attempt=1
    
    while [ $attempt -le $max_attempts ]; do
        if curl -s http://localhost:3000/health > /dev/null 2>&1; then
            print_status "Web service is ready!"
            return 0
        fi
        
        # Check if web container is still running
        if ! docker-compose ps web | grep -q "Up"; then
            print_error "Web container failed to start. Checking logs..."
            docker-compose logs web
            return 1
        fi
        
        print_warning "Waiting for web service... (attempt $attempt/$max_attempts)"
        sleep 2
        attempt=$((attempt + 1))
    done
    
    print_error "Web service failed to start within the timeout period"
    return 1
}

# Function to check service health
check_service_health() {
    print_status "Checking service health..."
    
    # Check database
    if ! docker-compose exec web bundle exec rails runner "puts ActiveRecord::Base.connection.active?" > /dev/null 2>&1; then
        print_error "Database connection failed"
        return 1
    fi
    
    # Check Redis
    if ! docker-compose exec web bundle exec rails runner "puts Redis.new.ping" > /dev/null 2>&1; then
        print_error "Redis connection failed"
        return 1
    fi
    
    # Check web service
    if ! curl -s http://localhost:3000/health > /dev/null 2>&1; then
        print_error "Web service health check failed"
        return 1
    fi
    
    # Check Sidekiq
    if ! docker-compose exec sidekiq pgrep -f sidekiq > /dev/null 2>&1; then
        print_error "Sidekiq process not found"
        return 1
    fi
    
    # Check PermieGPT service
    if ! docker-compose exec web bundle exec rails runner "puts PermieGptService.new.respond_to?(:generate_completion)" > /dev/null 2>&1; then
        print_warning "PermieGPT service may not be fully initialized"
        return 1
    fi
    
    return 0
}

# Function to check logs for errors
check_logs() {
    print_status "Checking service logs for errors..."
    
    # Check web service logs
    if docker-compose logs web | grep -i "error\|exception\|fail" > /dev/null 2>&1; then
        print_error "Found errors in web service logs:"
        docker-compose logs web | grep -i "error\|exception\|fail"
        return 1
    fi
    
    # Check Sidekiq logs
    if docker-compose logs sidekiq | grep -i "error\|exception\|fail" > /dev/null 2>&1; then
        print_error "Found errors in Sidekiq logs:"
        docker-compose logs sidekiq | grep -i "error\|exception\|fail"
        return 1
    fi
    
    return 0
}

# Function to restart web service if needed
restart_web_service() {
    print_status "Restarting web service..."
    docker-compose restart web
    sleep 5
    
    # Wait for web service to be ready again
    local max_attempts=10
    local attempt=1
    
    while [ $attempt -le $max_attempts ]; do
        if curl -s http://localhost:3000/health > /dev/null 2>&1; then
            print_status "Web service restarted successfully!"
            return 0
        fi
        
        print_warning "Waiting for web service to restart... (attempt $attempt/$max_attempts)"
        sleep 2
        attempt=$((attempt + 1))
    done
    
    print_error "Web service failed to restart"
    return 1
}

# Function to start Rails server
start_rails_server() {
    print_status "Starting Rails server..."
    
    # Kill any existing Rails server
    pkill -f "rails server" || true
    
    # Start Rails server with proper environment variables
    RAILS_ENV=development \
    DATABASE_URL=postgres://postgres:postgres@localhost:5432/permieportal_development \
    REDIS_URL=redis://localhost:6379/1 \
    OLLAMA_URL=http://192.168.1.106:11434 \
    PORT=3000 \
    bundle exec rails server &
    
    # Wait for server to start
    local max_attempts=30
    local attempt=1
    
    while [ $attempt -le $max_attempts ]; do
        if curl -s http://localhost:3000/health > /dev/null 2>&1; then
            print_status "Rails server started successfully!"
            return 0
        fi
        
        # Check if process is still running
        if ! ps aux | grep -v grep | grep -q "rails server"; then
            print_error "Rails server process died. Checking logs..."
            tail -n 50 log/development.log
            return 1
        fi
        
        print_warning "Waiting for Rails server... (attempt $attempt/$max_attempts)"
        sleep 2
        attempt=$((attempt + 1))
    done
    
    print_error "Rails server failed to start"
    return 1
}

# Function to initialize PermieGPT service
initialize_permiegpt() {
    print_status "Initializing PermieGPT service..."
    
    # Check if Ollama is running
    if ! curl -s http://localhost:11434/api/tags > /dev/null 2>&1; then
        print_error "Ollama service is not running. Please start Ollama first."
        return 1
    fi
    
    # Wait for Rails server to be ready
    local max_attempts=30
    local attempt=1
    
    while [ $attempt -le $max_attempts ]; do
        if curl -s http://localhost:3000/health > /dev/null 2>&1; then
            break
        fi
        
        print_warning "Waiting for Rails server before initializing PermieGPT... (attempt $attempt/$max_attempts)"
        sleep 2
        attempt=$((attempt + 1))
    done
    
    if [ $attempt -gt $max_attempts ]; then
        print_error "Rails server not ready for PermieGPT initialization"
        return 1
    fi
    
    # Initialize PermieGPT service
    if ! RAILS_ENV=development \
        DATABASE_URL=postgres://postgres:postgres@localhost:5432/permieportal_development \
        REDIS_URL=redis://localhost:6379/1 \
        OLLAMA_URL=http://192.168.1.106:11434 \
        bundle exec rails runner "PermieGptService.new.initialize_service" > /dev/null 2>&1; then
        print_error "Failed to initialize PermieGPT service"
        return 1
    fi
    
    # Verify PermieGPT service
    if ! RAILS_ENV=development \
        DATABASE_URL=postgres://postgres:postgres@localhost:5432/permieportal_development \
        REDIS_URL=redis://localhost:6379/1 \
        OLLAMA_URL=http://192.168.1.106:11434 \
        bundle exec rails runner "puts PermieGptService.new.respond_to?(:generate_completion)" | grep -q "true"; then
        print_error "PermieGPT service initialization failed - generate_completion method not found"
        return 1
    fi
    
    return 0
}

# Main execution
print_status "Starting PermiePortal..."

# Check prerequisites
check_docker
check_docker_compose
check_ports
check_ollama

# Stop any running containers
stop_containers

# Clean up Docker resources
cleanup_docker

# Build and start containers
print_status "Building and starting containers..."
docker-compose build
docker-compose up -d

# Setup database
setup_database

# Wait for services to be ready
if ! wait_for_services; then
    print_error "Services failed to start properly. Attempting to restart web service..."
    if ! restart_web_service; then
        print_error "Failed to restart web service. Please check the logs for details."
        docker-compose logs
        exit 1
    fi
fi

# Check and run migrations
check_migrations

# Seed the database
print_status "Seeding the database..."
docker-compose exec web bundle exec rails db:seed

# Install JavaScript dependencies
print_status "Installing JavaScript dependencies..."
yarn install --check-files

# Build Tailwind CSS
print_status "Building Tailwind CSS..."
yarn build:css

# Start Tailwind CSS watcher in development
if [ "$RAILS_ENV" = "development" ]; then
    print_status "Starting Tailwind CSS watcher..."
    yarn watch:css &
fi

# Compile assets only in production
if [ "$RAILS_ENV" = "production" ]; then
    print_status "Compiling assets..."
    docker-compose exec web bundle exec rails assets:precompile
else
    print_status "Setting up development assets..."
    docker-compose exec web bundle exec rails assets:clobber
    docker-compose exec web bundle exec rails assets:precompile
fi

# Start Rails server
if ! start_rails_server; then
    print_error "Failed to start Rails server. Please check the logs for details."
    exit 1
fi

# Initialize PermieGPT service
if ! initialize_permiegpt; then
    print_error "Failed to initialize PermieGPT service. Please check the logs for details."
    docker-compose logs
    exit 1
fi

# Check service health
if ! check_service_health; then
    print_error "Service health checks failed. Attempting to restart web service..."
    if ! restart_web_service; then
        print_error "Failed to restart web service. Please check the logs for details."
        docker-compose logs
        exit 1
    fi
fi

# Check logs for errors
if ! check_logs; then
    print_error "Found errors in service logs. Please review the logs above."
    exit 1
fi

# Show container status
print_status "Container status:"
docker-compose ps

# Show logs
print_status "Showing logs (Ctrl+C to exit)..."
docker-compose logs -f

# Cleanup on exit
trap 'docker-compose down; pkill -f "rails server"' EXIT 