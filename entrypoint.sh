#!/bin/bash
set -e

# Function to check if a service is ready
wait_for_service() {
    local host="$1"
    local port="$2"
    local service="$3"
    local max_attempts=30
    local attempt=1

    echo "Waiting for $service to be ready..."
    while [ $attempt -le $max_attempts ]; do
        if nc -z "$host" "$port" >/dev/null 2>&1; then
            echo "$service is ready!"
            return 0
        fi
        echo "Attempt $attempt/$max_attempts: $service not ready yet..."
        sleep 2
        attempt=$((attempt + 1))
    done
    echo "Error: $service failed to become ready"
    return 1
}

# Wait for Postgres
wait_for_service "db" "5432" "Postgres"

# Wait for Redis
wait_for_service "redis" "6379" "Redis"

# Remove a potentially pre-existing server.pid for Rails
rm -f /app/tmp/pids/server.pid

# Only run migrations if SKIP_DB_MIGRATE is not set
if [ -z "$SKIP_DB_MIGRATE" ]; then
  # Create and migrate database if it doesn't exist
  if ! bundle exec rails db:version > /dev/null 2>&1; then
    echo "Database does not exist, creating..."
    bundle exec rails db:create
  fi

  bundle exec rails db:migrate
fi

# Execute the passed command
exec "$@" 