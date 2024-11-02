class Resource < ApplicationRecord
  belongs_to :user
# app/models/resource.rb
include PgSearch::Model
pg_search_scope :search_by_title_and_description,
                against: [:title, :description]
end
