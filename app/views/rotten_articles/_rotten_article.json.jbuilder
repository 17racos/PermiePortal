# frozen_string_literal: true
json.extract! rotten_article, :id, :title, :slug, :content, :tags, :published, :author, :created_at, :updated_at
json.url rotten_article_url(rotten_article, format: :json)
