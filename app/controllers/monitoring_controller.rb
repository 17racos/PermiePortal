class MonitoringController < ApplicationController
  before_action :authenticate

  def metrics
    metrics = Prometheus::Client.registry.metrics.map do |metric|
      {
        name: metric.name,
        type: metric.type,
        docstring: metric.docstring,
        values: metric.values
      }
    end
    
    render json: metrics
  end

  private

  def authenticate
    # Basic auth for metrics endpoint
    authenticate_or_request_with_http_basic do |username, password|
      # Use environment variables for credentials
      ActiveSupport::SecurityUtils.secure_compare(username, ENV['METRICS_USER']) &
      ActiveSupport::SecurityUtils.secure_compare(password, ENV['METRICS_PASSWORD'])
    end
  end
end 