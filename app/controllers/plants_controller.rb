# frozen_string_literal: true
class PlantsController < ApplicationController
  before_action :set_plant, only: [:show]

  # GET /plants
  def index
    # Use optimized search method
    @plants = EnhancedPlant.includes(:environmental_requirements, :plant_uses, :plant_traits, :semantic_tags)
                          .advanced_search(search_params)

    respond_to do |format|
      format.html
      format.json { render json: @plants }
      format.turbo_stream do
        render turbo_stream: turbo_stream.replace(
          'plants-list',
          partial: 'plants/plants_list',
          locals: { plants: @plants }
        )
      end
    end
  end

  # GET /plants/:common_name
  def show
  end

  # GET /plants/quick/:filter
  def quick_filter
    filter_type = params[:filter]
    search_service = EnhancedPlantSearchService.new

    case filter_type
    when 'edible'
      @plants = search_service.natural_language_search('edible')
    when 'medicinal'
      @plants = search_service.natural_language_search('medicinal')
    when 'pollinator'
      @plants = search_service.natural_language_search('pollinator friendly')
    when 'drought'
      @plants = search_service.natural_language_search('drought tolerant')
    when 'nitrogen'
      @plants = search_service.natural_language_search('nitrogen fixing')
    when 'groundcover'
      @plants = search_service.natural_language_search('ground cover')
    when 'aromatic'
      @plants = search_service.natural_language_search('aromatic')
    when 'container'
      @plants = search_service.natural_language_search('container suitable')
    when 'cold_hardy'
      @plants = search_service.natural_language_search('cold hardy')
    when 'deer_resistant'
      @plants = search_service.natural_language_search('deer resistant')
    else
      @plants = EnhancedPlant.limit(200)
    end

    respond_to do |format|
      format.html { redirect_to plants_path }
      format.turbo_stream do
        render turbo_stream: turbo_stream.replace('plants-list', partial: 'plants_list', locals: { plants: @plants })
      end
    end
  end

  # GET /plants/gpt_chat
  def gpt_chat
    # Simple action to render the GPT chat interface
  end

  private

  def set_plant
    @plant = EnhancedPlant.find_by(common_name: params[:common_name])

    unless @plant
      redirect_to plants_path, alert: 'Plant not found.'
    end
  end

  def search_params
    params.permit(
      :query,
      :min_zone,
      :max_zone,
      functions: [],
      layers: []
    )
  end
end