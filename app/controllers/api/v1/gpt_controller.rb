include LlmHelper
# frozen_string_literal: true
module Api
  module V1
    class GptController < ApplicationController
      before_action :set_llm_service
      skip_before_action :verify_authenticity_token

      # POST /api/v1/gpt/query
      def query
        user_query = params.dig(:query) || params.dig('query')
        context = params[:context] || {}

        if user_query.blank?
          render json: { error: 'Query parameter is required' }, status: :bad_request
          return
        end

        result = @llm_service.process_plant_query(user_query.to_s, context: context)

        if result[:success]
          render json: {
            success: true,
            data: {
              response: result[:response],
              type: result[:type],
              model: result[:model],
              usage: result[:usage]
            }
          }
        else
          render json: {
            success: false,
            error: result[:error],
            fallback_response: result[:fallback_response]
          }, status: :service_unavailable
        end
      rescue => e
        Rails.logger.error "LLM Query Error: #{e.message}"
        Rails.logger.error "LLM Query Backtrace: #{e.backtrace.join("\n")}"
        render json: {
          error: 'Failed to process query',
          message: e.message
        }, status: :internal_server_error
      end

      # POST /api/v1/gpt/chat
      def chat
        messages = params[:messages]
        plant_context = params[:plant_context] || []

        if messages.blank? || !messages.is_a?(Array)
          render json: { error: 'Messages array is required' }, status: :bad_request
          return
        end

        # Get plant context if plant names provided
        plants = []
        if plant_context.any?
          plants = EnhancedPlant.where(common_name: plant_context)
        end

        result = @llm_service.chat_with_context(messages, plants)

        if result[:success]
          render json: {
            success: true,
            data: {
              response: result[:response],
              model: result[:model],
              usage: result[:usage]
            }
          }
        else
          render json: { 
            success: false, 
            error: result[:error] 
          }, status: :service_unavailable
        end
      rescue => e
        Rails.logger.error "LLM Chat Error: #{e.message}"
        render json: {
          error: 'Failed to process chat',
          message: e.message
        }, status: :internal_server_error
      end

      # POST /api/v1/gpt/search_plants
      def search_plants
        query = params[:query]
        criteria = params[:criteria] || {}

        if query.blank?
          render json: { error: 'Query parameter is required' }, status: :bad_request
          return
        end

        result = @llm_service.search_plants_with_ai(query, criteria)

        if result
          render json: {
            success: true,
            data: {
              ai_response: result[:ai_response],
              plants_found: result[:plants_found],
              plants: result[:plants_data]
            }
          }
        else
          render json: {
            success: false,
            error: 'Search not available - running in fallback mode'
          }, status: :service_unavailable
        end
      rescue => e
        Rails.logger.error "LLM Plant Search Error: #{e.message}"
        render json: {
          error: 'Failed to search plants',
          message: e.message
        }, status: :internal_server_error
      end

      # POST /api/v1/gpt/recommendations
      def recommendations
        criteria = params[:criteria]

        if criteria.blank?
          render json: { error: 'Criteria parameter is required' }, status: :bad_request
          return
        end

        # Use the Ollama service for recommendations
        result = @llm_service.search_plants_with_ai(criteria, {})

        if result
          render json: {
            success: true,
            data: {
              criteria: criteria,
              recommendations: result[:ai_response],
              plants_considered: result[:plants_found],
              matching_plants: result[:plants_data]
            }
          }
        else
          render json: {
            success: false,
            error: 'Recommendations not available - running in fallback mode'
          }, status: :service_unavailable
        end
      rescue => e
        Rails.logger.error "LLM Recommendations Error: #{e.message}"
        render json: {
          error: 'Failed to generate recommendations',
          message: e.message
        }, status: :internal_server_error
      end

      # GET /api/v1/gpt/relationships/:plant_name
      def relationships
        plant_name = params[:plant_name]

        if plant_name.blank?
          render json: { error: 'Plant name is required' }, status: :bad_request
          return
        end

        plant = EnhancedPlant.find_by(common_name: plant_name)
        
        if plant.nil?
          render json: { success: false, error: 'Plant not found' }, status: :not_found
          return
        end

        companions = plant.beneficial_companions.limit(10)
        antagonists = plant.antagonistic_plants.limit(5)

        # Use Ollama to explain relationships
        plants_to_analyze = [plant] + companions.to_a + antagonists.to_a
        analysis = @llm_service.analyze_plant_compatibility(plants_to_analyze.uniq)

        if analysis
          render json: {
            success: true,
            data: {
              plant: plant.common_name,
              explanation: analysis,
              companions: companions.map { |c| { name: c.common_name, scientific_name: c.scientific_name } },
              antagonists: antagonists.map { |a| { name: a.common_name, scientific_name: a.scientific_name } }
            }
          }
        else
          render json: {
            success: false,
            error: 'Relationship analysis not available - running in fallback mode'
          }, status: :service_unavailable
        end
      rescue => e
        Rails.logger.error "LLM Relationships Error: #{e.message}"
        render json: {
          error: 'Failed to explain relationships',
          message: e.message
        }, status: :internal_server_error
      end

      # POST /api/v1/gpt/analyze_compatibility
      def analyze_compatibility
        plant_names = params[:plants]

        if plant_names.blank? || !plant_names.is_a?(Array)
          render json: { error: 'Plants array is required' }, status: :bad_request
          return
        end

        plants = EnhancedPlant.where(common_name: plant_names)
        
        if plants.empty?
          render json: { error: 'No plants found' }, status: :not_found
          return
        end

        analysis = @llm_service.analyze_plant_compatibility(plants)

        if analysis
          render json: {
            success: true,
            data: {
              plants: plant_names,
              analysis: analysis
            }
          }
        else
          render json: {
            success: false,
            error: 'Analysis not available - running in fallback mode'
          }, status: :service_unavailable
        end
      rescue => e
        Rails.logger.error "Compatibility Analysis Error: #{e.message}"
        render json: {
          error: 'Failed to analyze compatibility',
          message: e.message
        }, status: :internal_server_error
      end

      # GET /api/v1/gpt/status
      def status
        llm_status = LlmHelper.status

        render json: {
          success: true,
          data: {
            llm_available: llm_status[:enabled],
            features: {
              query_processing: true,
              chat: llm_status[:enabled],
              plant_search: llm_status[:enabled],
              recommendations: llm_status[:enabled],
              relationship_explanations: llm_status[:enabled],
              compatibility_analysis: llm_status[:enabled]
            },
            fallback_mode: !llm_status[:enabled],
            provider: llm_status[:provider],
            url: llm_status[:url],
            model: llm_status[:model],
            available_models: llm_status[:available_models]
          }
        }
      end

      # GET /api/v1/gpt/models
      def models
        available_models = LlmHelper.models

        render json: {
          success: true,
          data: {
            available_models: available_models,
            current_model: ENV['OLLAMA_MODEL'] || 'llama3.1:8b',
            provider: 'Ollama'
          }
        }
      end

    private

      def set_llm_service
        @llm_service = OllamaGptService.new
      end
    end
  end
end