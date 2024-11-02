class ResourcesController < ApplicationController
  def index
    if params[:query].present?
      @resources = Resource.search_by_title_and_description(params[:query])
    else
      @resources = Resource.all
    end
  end
end

