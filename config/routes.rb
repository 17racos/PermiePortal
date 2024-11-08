Rails.application.routes.draw do
  get "home/index"
  get "get_involved/index"
  get "community/index"
  get "plants/index"
  get "projects/index"
  devise_for :admin_users, ActiveAdmin::Devise.config
  ActiveAdmin.routes(self)
  root "home#index"
  
  devise_for :users
  
  resources :resources, only: [:index, :show]
  
  resources :forum_threads do
    resources :forum_posts, only: [:create, :destroy]
  end
  
  get "/up/", to: "up#index", as: :up
  get "/up/databases", to: "up#databases", as: :up_databases
  get 'projects', to: 'projects#index'
  get 'plants', to: 'plants#index'
  get 'community', to: 'community#index'
  get 'get_involved', to: 'get_involved#index'
end


  # Sidekiq has a web dashboard which you can enable below. It's turned off by
  # default because you very likely wouldn't want this to be available to
  # everyone in production.
  #
  # Uncomment the 2 lines below to enable the dashboard WITHOUT authentication,
  # but be careful because even anonymous web visitors will be able to see it!
  # require "sidekiq/web"
  # mount Sidekiq::Web => "/sidekiq"
  #
  # If you add Devise to this project and happen to have an admin? attribute
  # on your user you can uncomment the 4 lines below to only allow access to
  # the dashboard if you're an admin. Feel free to adjust things as needed.
  # require "sidekiq/web"
  # authenticate :user, lambda { |u| u.admin? } do
  #   mount Sidekiq::Web => "/sidekiq"
  # end

  # Learn more about this file at: https://guides.rubyonrails.org/routing.html
