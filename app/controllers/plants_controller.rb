class PlantsController < ApplicationController
  before_action :set_plant, only: [:show]

  # GET /plants
  def index
    @plants = Plant.all

    # Apply search filter
    if params[:query].present?
      @plants = @plants.search_by_name(params[:query])
    end

    # Apply function filters
    if params[:functions].present?
      @plants = @plants.filter_by_plant_function(params[:functions])
    end

    # Apply layer filters
    if params[:layers].present?
      @plants = @plants.filter_by_layers(params[:layers])
    end

    # Apply zone filters
    if params[:min_zone].present? || params[:max_zone].present?
      min_zone = params[:min_zone].presence || 1
      max_zone = params[:max_zone].presence || 13
      @plants = @plants.filter_by_zones([min_zone.to_s])
    end

    respond_to do |format|
      format.html
      format.json { render json: @plants }
      format.turbo_stream do
        render turbo_stream: turbo_stream.replace(
          "plants-list",
          partial: "plants/list",
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
    @plants = case params[:filter]
    when 'edible'
      Plant.edible
    when 'medicinal'
      Plant.medicinal
    when 'nitrogen'
      Plant.nitrogen_fixers
    when 'groundcover'
      Plant.groundcover
    else
      Plant.all
    end

    respond_to do |format|
      format.turbo_stream do
        render turbo_stream: turbo_stream.replace(
          "plants-list",
          partial: "plants/plants_list",
          locals: { plants: @plants }
        )
      end
    end
  end

  private

  def set_plant
    @plant = Plant.find_by_common_name(params[:common_name])
    
    unless @plant
      redirect_to plants_path, alert: "Plant not found."
    end
  end

  def search_params
    params.fetch(:search, {}).permit(
      :query,
      functions: [],
      layers: [],
      zones: []
    )
  end
end