# frozen_string_literal: true
Rails.application.routes.draw do

  # Suppress favicon errors
  get '/favicon.ico', to: proc { [204, {}, []] }

  # Devise routes for users
  devise_for :users

  # Root route
  root 'home#index'

  # Dynamic rotten_article routes using slugs
  resources :rotten_articles, param: :slug  # Ensures rotten_article are found by slug, not ID

  # Dynamic guides routes using slugs
  resources :guides, param: :slug  # Ensures guides are found by slug, not ID

  # Plant routes, using common_name as the URL param
  resources :plants, param: :common_name, only: [:index, :show] do
    collection do
      get 'quick/:filter', to: 'plants#quick_filter', as: :quick_filter
      get 'gpt_chat', to: 'plants#gpt_chat', as: :gpt_chat
    end
  end

  # Resources routes
  resources :resources, only: [:index] do
    get 'whatisperm', on: :collection, as: :whatisperm
    get 'whyitmatters', on: :collection, as: :whyitmatters
  end

  # Community and involvement pages
  get 'community', to: 'community#index'
  get 'get_involved', to: 'get_involved#index'

  # Pest routes
  resources :pests, param: :slug, only: [:index, :show]

  # ✅ Serve Static Images Locally (ONLY in Development)
  if Rails.env.development?
    get '/images/:filename', to: proc { |env|
      req = Rack::Request.new(env)
      filename = req.params['filename']

      # Ensure filename is present
      if filename.nil? || filename.empty?
        [400, { 'Content-Type' => 'text/plain' }, ['Bad Request: Missing filename']]
      else
        file_path = Rails.root.join('public', 'images', filename)

        if File.exist?(file_path)
          [200, { 'Content-Type' => Rack::Mime.mime_type(File.extname(file_path)) }, [File.binread(file_path)]]
        else
          [404, { 'Content-Type' => 'text/plain' }, ['Not Found']]
        end
      end
    }, constraints: { filename: /.+\.(jpg|jpeg|png|gif|webp)/ }
  end

  # Sidekiq Web UI
  authenticate :user, lambda { |u| u.admin? } do
    require 'sidekiq/web'
    mount Sidekiq::Web => '/sidekiq'
  end

  # Monitoring endpoint
  get '/metrics', to: 'monitoring#metrics'

  # API Routes
  namespace :api do
    namespace :v1 do
      resources :sync, only: [] do
        collection do
          get :manifest
          get :delta
        end
      end

      # LLM Integration routes (keeping 'gpt' namespace for compatibility)
      namespace :gpt do
        post :query
        post :chat
        post :search_plants
        post :recommendations
        post :analyze_compatibility
        get :relationships, path: 'relationships/:plant_name', action: :relationships
        get :status
        get :models
      end
    end
  end

  # Health check endpoint
  get '/health', to: 'application#health'

  # Test metrics routes
  get 'test_metrics/error', to: 'test_metrics#test_error'
  get 'test_metrics/view', to: 'test_metrics#test_view'
  get 'test_metrics/search', to: 'test_metrics#test_search'
end
