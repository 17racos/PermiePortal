class PlantsController < ApplicationController
  before_action :set_plant, only: [:show]

  # GET /plants
  def index
    # Start with base query
    @plants = EnhancedPlant.includes(:environmental_requirements, :plant_uses, :plant_traits)

    # Apply search filter using enhanced search service
    if params[:query].present?
      search_service = EnhancedPlantSearchService.new
      search_results = search_service.search(params[:query], limit: 200)
      # Convert to ActiveRecord relation for further filtering
      @plants = @plants.where(id: search_results.map(&:id))
    end

    # Apply function filters (map to use categories)
    if params[:functions].present? && params[:functions].any?(&:present?)
      use_category_names = params[:functions].reject(&:blank?)
      plant_ids_with_functions = PlantUse.joins(:use_category)
                                         .where(use_categories: { name: use_category_names })
                                         .pluck(:enhanced_plant_id)
                                         .uniq
      @plants = @plants.where(id: plant_ids_with_functions)
    end

    # Apply layer filters (map to plant types)
    if params[:layers].present? && params[:layers].any?(&:present?)
      layers = params[:layers].reject(&:blank?)
      layer_to_type_mapping = {
        'Canopy' => 'tree',
        'Sub-canopy' => 'tree',
        'Shrub' => 'shrub',
        'Herbaceous' => 'herbaceous',
        'Ground' => 'herbaceous',
        'Root' => 'herbaceous',
        'Vine' => 'vine',
        'Aquatic' => 'aquatic'
      }
      
      plant_types = layers.map { |layer| layer_to_type_mapping[layer] }.compact.uniq
      if plant_types.any?
        @plants = @plants.where(plant_type: plant_types)
      end
    end

    # Apply zone filters
    if (params[:min_zone].present? && params[:min_zone] != "") || 
       (params[:max_zone].present? && params[:max_zone] != "")
      min_zone = params[:min_zone].presence&.to_i || 1
      max_zone = params[:max_zone].presence&.to_i || 13
      
      # Get plant IDs that match zone requirements
      plant_ids_in_zone = EnvironmentalRequirements.where(
        'hardiness_zone_min <= ? AND hardiness_zone_max >= ?',
        max_zone, min_zone
      ).pluck(:enhanced_plant_id).uniq
      
      @plants = @plants.where(id: plant_ids_in_zone)
    end

    # Ensure we have a proper relation
    @plants = @plants.distinct

    respond_to do |format|
      format.html
      format.json { render json: @plants }
      format.turbo_stream do
        render turbo_stream: turbo_stream.replace(
          "plants-list",
          partial: "plants/plants_list",
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
    search_service = EnhancedPlantSearchService.new
    
    @plants = case params[:filter]
    when 'edible'
      search_service.search('edible food', limit: 100)
    when 'medicinal'
      search_service.search('medicinal', limit: 100)
    when 'nitrogen'
      search_service.search('nitrogen fixing', limit: 100)
    when 'groundcover'
      search_service.search('ground cover', limit: 100)
    else
      EnhancedPlant.all
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
    @plant = EnhancedPlant.find_by(common_name: params[:common_name])
    
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