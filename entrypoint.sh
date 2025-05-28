#!/bin/bash
set -e

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

# Then exec the container's main process (what's set as CMD in the Dockerfile)
exec "$@" 