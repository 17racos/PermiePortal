class CreateRottenArticles < ActiveRecord::Migration[7.0]
  def change
    create_table :rotten_articles do |t|
      t.string :title
      t.text :body
      t.string :slug, unique: true
      t.string :image
      t.boolean :is_published, default: true
      
      t.timestamps
    end

    add_index :rotten_articles, :slug, unique: true
  end
end
