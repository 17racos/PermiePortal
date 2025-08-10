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

# Function to check if Ollama is running
check_ollama() {
    if ! curl -s http://localhost:11434/api/version > /dev/null; then
        print_warning "Ollama is not running. AI features will be limited."
        print_warning "Please start Ollama with: ollama serve"
    fi
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

# Main execution
print_status "Starting development environment setup..."

# Check prerequisites
check_docker
check_docker_compose
check_ollama

# Stop any running containers
stop_containers

# Clean up Docker resources
cleanup_docker

# Build and start containers
print_status "Building and starting containers..."
docker-compose build
docker-compose up -d

# Wait for services to be healthy
print_status "Waiting for services to be healthy..."
sleep 10

# Run database migrations
print_status "Running database migrations..."
docker-compose exec web bundle exec rails db:migrate

# Seed the database
print_status "Seeding the database..."
docker-compose exec web bundle exec rails db:seed

# Compile assets
print_status "Compiling assets..."
docker-compose exec web bundle exec rails assets:precompile

# Show container status
print_status "Container status:"
docker-compose ps

# Show logs
print_status "Showing logs (Ctrl+C to exit)..."
docker-compose logs -f

# Cleanup on exit
trap 'docker-compose down' EXIT 