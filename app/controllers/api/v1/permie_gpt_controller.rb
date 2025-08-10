# frozen_string_literal: true

module Api
  module V1
    class PermieGptController < ApplicationController
      include ActionController::MimeResponds
      include ActionController::Live

      # Constants
      CACHE_EXPIRY = 1.hour
      MAX_RETRIES = 3
      RETRY_DELAY = 1.second
      BATCH_SIZE = 50

      # Initialize service
      def initialize
        super
        @permie_gpt_service = PermieGptService.new
        @cache = ActiveSupport::Cache::MemoryStore.new(expires_in: CACHE_EXPIRY)
      end

      # Health check endpoint with caching
      def health
        cache_key = 'permie_gpt_health'
        cached_health = @cache.read(cache_key)

        if cached_health.present?
          render_json(cached_health)
        else
          health_data = check_health
          @cache.write(cache_key, health_data, expires_in: 5.minutes)
          render_json(health_data)
        end
      end

      # Main query endpoint with optimized error handling
      def query
        return render_error("Query parameter is required") unless params[:query].present?

        # Check cache first
        cache_key = generate_cache_key(params)
        cached_response = @cache.read(cache_key)
        return render_json(cached_response) if cached_response.present?

        # Process query with retries
        response = with_retries(max_attempts: MAX_RETRIES, base_sleep_seconds: RETRY_DELAY) do
          process_query(params)
        end

        # Cache successful response
        @cache.write(cache_key, response) if response[:success]
        render_json(response)
      rescue StandardError => e
        Rails.logger.error("PermieGPT Error: #{e.message}")
        render_error("An error occurred while processing your request")
      end

      # Stream response for long-running queries
      def stream
        response.headers['Content-Type'] = 'text/event-stream'
        response.headers['Last-Modified'] = Time.current.httpdate

        begin
          process_stream(params)
        rescue StandardError => e
          Rails.logger.error("Stream Error: #{e.message}")
          response.stream.write("data: {\"error\": \"#{e.message}\"}\n\n")
        ensure
          response.stream.close
        end
      end

      private

      # Process query with optimized context building
      def process_query(params)
        # Extract plant names
        plant_names = extract_plant_names(params[:query])
        
        # Build context with optimized data loading
        context = build_context(params, plant_names)
        
        # Generate response
        @permie_gpt_service.query(context)
      end

      # Extract plant names with improved accuracy
      def extract_plant_names(text)
        return [] unless text.present?

        # Use database function for fuzzy matching
        words = text.downcase.split(/\W+/)
        words = words.reject { |w| w.length < 3 }
        
        # Batch check existence using database function
        result = ActiveRecord::Base.connection.execute(
          "SELECT plant_name, exists FROM batch_check_plant_existence(ARRAY[?])",
          words
        )

        # Return only existing plants
        result.values.select { |_, exists| exists }.map(&:first)
      end

      # Build context with optimized data loading
      def build_context(params, plant_names)
        # Load plant data in a single query with eager loading
        plants = EnhancedPlant.includes(
          :environmental_requirements,
          :plant_uses,
          :plant_traits,
          :semantic_tags
        ).where(
          'LOWER(common_name) = ANY(ARRAY[?]) OR LOWER(scientific_name) = ANY(ARRAY[?])',
          plant_names,
          plant_names
        )

        # Get common plant combinations
        combinations = get_common_combinations(plants)

        {
          query: params[:query],
          location: params[:location],
          zone: params[:zone],
          soil: params[:soil],
          experience_level: params[:experience_level],
          goals: params[:goals],
          plants: plants,
          combinations: combinations
        }
      end

      # Get common plant combinations from materialized view
      def get_common_combinations(plants)
        return [] if plants.empty?

        plant_names = plants.map(&:common_name)
        
        ActiveRecord::Base.connection.execute(
          "SELECT plant1, plant2, co_occurrence_count 
           FROM common_plant_combinations 
           WHERE plant1 = ANY(ARRAY[?]) OR plant2 = ANY(ARRAY[?])
           ORDER BY co_occurrence_count DESC
           LIMIT 5",
          plant_names,
          plant_names
        ).values
      end

      # Process stream with optimized data handling
      def process_stream(params)
        # Extract plant names
        plant_names = extract_plant_names(params[:query])
        
        # Build context with optimized data loading
        context = build_context(params, plant_names)
        
        # Stream response
        @permie_gpt_service.stream_query(context) do |chunk|
          response.stream.write("data: #{chunk.to_json}\n\n")
        end
      end

      # Check health with optimized database query
      def check_health
        # Check database connection
        db_healthy = ActiveRecord::Base.connection.execute("SELECT 1").first.present?
        
        # Check AI service
        ai_healthy = @permie_gpt_service.health_check
        
        {
          success: true,
          data: {
            database: db_healthy,
            llm_available: ai_healthy,
            model: ENV.fetch('OLLAMA_MODEL', 'mistral'),
            timestamp: Time.current
          }
        }
      end

      # Generate cache key
      def generate_cache_key(params)
        [
          'permie_gpt',
          params[:query],
          params[:location],
          params[:zone],
          params[:soil],
          params[:experience_level],
          params[:goals]&.sort&.join(':')
        ].compact.join(':')
      end

      # Render JSON response
      def render_json(data)
        respond_to do |format|
          format.json { render json: data }
          format.html { render json: data }
        end
      end

      # Render error response
      def render_error(message)
        render_json({
          success: false,
          error: message,
          fallback_response: generate_fallback_response
        })
      end

      # Generate fallback response
      def generate_fallback_response
        {
          response: "I apologize, but I'm having trouble accessing the AI model right now. Here's a basic response based on traditional permaculture principles:\n\n" +
                    "1. Start with a site analysis\n" +
                    "2. Consider local climate and soil conditions\n" +
                    "3. Choose plants that are well-suited to your specific conditions\n" +
                    "4. Implement appropriate growing techniques\n" +
                    "5. Monitor and adjust as needed\n\n" +
                    "Would you like me to try the search again, or would you prefer to use the traditional search filters?",
          knowledge_gaps: []
        }
      end
    end
  end
end 