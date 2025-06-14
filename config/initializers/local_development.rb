# Load local development configuration when not running in Docker
if Rails.env.development? && !ENV['DOCKER_CONTAINER']
  # Check if we're running locally (not in Docker)
  # Docker containers typically have DATABASE_URL set or hostname 'db' resolves
  begin
    require 'socket'
    # If we can't resolve 'db' hostname, we're probably running locally
    Socket.getaddrinfo('db', nil)
    # If we get here, 'db' resolves, so we're probably in Docker
  rescue SocketError
    # 'db' doesn't resolve, so we're running locally
    Rails.logger.info "🏠 Detected local development environment"
    
    # Load local development configuration
    load Rails.root.join('config', 'local_development.rb')
  end
end 