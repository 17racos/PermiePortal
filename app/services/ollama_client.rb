class OllamaClient
  # Constants
  TIMEOUT = 30.seconds
  MAX_RETRIES = 3
  RETRY_DELAY = 1.second
  CHUNK_SIZE = 1024
  MAX_TOKENS = 4096
  TEMPERATURE = 0.7
  TOP_P = 0.9

  # Initialize client
  def initialize
    @base_url = ENV.fetch('OLLAMA_API_URL', 'http://localhost:11434')
    @model = ENV.fetch('OLLAMA_MODEL', 'mistral')
    @http = HTTP.timeout(write: TIMEOUT, read: TIMEOUT, connect: TIMEOUT)
    @cache = ActiveSupport::Cache::MemoryStore.new(expires_in: 1.hour)
  end

  # Generate completion with optimized processing
  def generate_completion(prompt)
    return error_response("Empty prompt") if prompt.blank?

    # Check cache first
    cache_key = generate_cache_key(prompt)
    cached_response = @cache.read(cache_key)
    return cached_response if cached_response.present?

    # Process with retries
    response = with_retries(max_attempts: MAX_RETRIES, base_sleep_seconds: RETRY_DELAY) do
      make_request(prompt)
    end

    # Cache successful response
    @cache.write(cache_key, response) if response[:success]
    response
  rescue StandardError => e
    Rails.logger.error("Ollama Error: #{e.message}")
    error_response("Failed to generate response")
  end

  # Stream completion with optimized processing
  def stream_completion(prompt, &block)
    return error_response("Empty prompt") if prompt.blank?

    # Process with retries
    with_retries(max_attempts: MAX_RETRIES, base_sleep_seconds: RETRY_DELAY) do
      stream_request(prompt, &block)
    end
  rescue StandardError => e
    Rails.logger.error("Stream Error: #{e.message}")
    error_response("Failed to stream response")
  end

  # Health check with optimized request
  def health_check
    response = @http.get("#{@base_url}/api/health")
    response.status.success?
  rescue StandardError => e
    Rails.logger.error("Health Check Error: #{e.message}")
    false
  end

  private

  # Make request with optimized parameters
  def make_request(prompt)
    response = @http.post(
      "#{@base_url}/api/generate",
      json: {
        model: @model,
        prompt: prompt,
        stream: false,
        options: {
          temperature: TEMPERATURE,
          top_p: TOP_P,
          max_tokens: MAX_TOKENS
        }
      }
    )

    if response.status.success?
      data = JSON.parse(response.body.to_s)
      {
        success: true,
        text: data['response'],
        usage: {
          prompt_tokens: data['prompt_eval_count'],
          completion_tokens: data['eval_count'],
          total_tokens: data['prompt_eval_count'] + data['eval_count']
        }
      }
    else
      error_response("Request failed with status #{response.status}")
    end
  end

  # Stream request with optimized processing
  def stream_request(prompt, &block)
    response = @http.post(
      "#{@base_url}/api/generate",
      json: {
        model: @model,
        prompt: prompt,
        stream: true,
        options: {
          temperature: TEMPERATURE,
          top_p: TOP_P,
          max_tokens: MAX_TOKENS
        }
      }
    )

    if response.status.success?
      process_stream(response, &block)
    else
      error_response("Stream request failed with status #{response.status}")
    end
  end

  # Process stream with optimized chunking
  def process_stream(response, &block)
    buffer = ""
    response.body.each do |chunk|
      begin
        data = JSON.parse(chunk)
        if data['response'].present?
          buffer << data['response']
          yield data['response'] if block_given?
        end
      rescue JSON::ParserError => e
        Rails.logger.error("Stream parsing error: #{e.message}")
        next
      end
    end

    {
      success: true,
      text: buffer,
      usage: {
        prompt_tokens: response.headers['X-Prompt-Tokens'].to_i,
        completion_tokens: response.headers['X-Completion-Tokens'].to_i,
        total_tokens: response.headers['X-Total-Tokens'].to_i
      }
    }
  end

  # Generate cache key
  def generate_cache_key(prompt)
    [
      'ollama',
      @model,
      Digest::MD5.hexdigest(prompt)
    ].join(':')
  end

  # Error response helper
  def error_response(message)
    {
      success: false,
      error: message,
      usage: {
        prompt_tokens: 0,
        completion_tokens: 0,
        total_tokens: 0
      }
    }
  end

  # Retry helper with exponential backoff
  def with_retries(max_attempts:, base_sleep_seconds:)
    attempt = 0
    begin
      attempt += 1
      yield
    rescue StandardError => e
      if attempt < max_attempts
        sleep_time = base_sleep_seconds * (2 ** (attempt - 1))
        Rails.logger.warn("Retry attempt #{attempt} after #{sleep_time} seconds: #{e.message}")
        sleep(sleep_time)
        retry
      else
        raise e
      end
    end
  end
end 