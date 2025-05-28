class ResponseTimeMiddleware
  def initialize(app)
    @app = app
  end

  def call(env)
    return @app.call(env) if Rails.env.test?

    start = Time.now
    status, headers, response = @app.call(env)
    
    # Only track metrics in development
    if Rails.env.development? && defined?(HTTP_RESPONSE_TIME)
      HTTP_RESPONSE_TIME.increment
    end

    [status, headers, response]
  end
end 