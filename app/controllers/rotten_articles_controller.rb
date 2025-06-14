# frozen_string_literal: true
class RottenArticlesController < ApplicationController
  before_action :set_rotten_article, only: [:show]

  def index
    @rotten_articles = RottenArticle.where(is_published: true)  # Use plural @rotten_articles
  end

  def show
    @rotten_article = RottenArticle.friendly.find_by(slug: params[:slug])
    if @rotten_article
      custom_view = Rails.root.join('app', 'views', 'rotten_articles', "#{@rotten_article.slug}.html.erb")
      if File.exist?(custom_view)
        render template: "rotten_articles/#{@rotten_article.slug}"
      else
        render :show
      end
    else
      redirect_to rotten_articles_path, alert: 'Rotten Article not found.'
    end
  end

  private

  def set_rotten_article
    @rotten_article = RottenArticle.friendly.find_by(slug: params[:slug])
    redirect_to rotten_articles_path, alert: 'Rotten Article not found.' unless @rotten_article
  end
end
