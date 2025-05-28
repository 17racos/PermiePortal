require 'prometheus/client'

# Create a new registry
prometheus = Prometheus::Client.registry

# Define metrics
prometheus.counter(
  :http_requests_total,
  docstring: 'A counter of HTTP requests made',
  labels: [:method, :path, :status]
)

prometheus.histogram(
  :http_request_duration_seconds,
  docstring: 'A histogram of the HTTP request durations',
  labels: [:method, :path]
)

prometheus.counter(
  :app_errors_total,
  docstring: 'Total number of application errors'
)

prometheus.counter(
  :content_views_total,
  docstring: 'Total number of content views'
)

prometheus.histogram(
  :search_duration_seconds,
  docstring: 'Search operation duration'
) 