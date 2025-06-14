# frozen_string_literal: true
class CreateSemanticTaggingSystem < ActiveRecord::Migration[7.1]
  def change
    # Enable UUID extension if not already enabled
    enable_extension 'pgcrypto' unless extension_enabled?('pgcrypto')

    # Semantic tags table
    create_table :semantic_tags, id: :uuid do |t|
      t.string :name, null: false, limit: 100
      t.string :category, null: false, limit: 50
      t.text :synonyms, array: true, default: []
      t.uuid :parent_tag_id
      t.decimal :weight, precision: 3, scale: 2, default: 1.0
      t.text :description
      t.timestamps
    end

    add_index :semantic_tags, :name, unique: true
    add_index :semantic_tags, :category
    add_index :semantic_tags, :parent_tag_id
    add_foreign_key :semantic_tags, :semantic_tags, column: :parent_tag_id

    # Plant-tag relationships
    create_table :plant_semantic_tags, id: :uuid do |t|
      t.bigint :enhanced_plant_id, null: false
      t.uuid :semantic_tag_id, null: false
      t.decimal :confidence_score, precision: 3, scale: 2, default: 1.0
      t.string :source, limit: 50, default: 'manual'
      t.text :notes
      t.timestamps
    end

    add_index :plant_semantic_tags, [:enhanced_plant_id, :semantic_tag_id],
              unique: true, name: 'idx_plant_semantic_tags_unique'
    add_index :plant_semantic_tags, :semantic_tag_id
    add_foreign_key :plant_semantic_tags, :enhanced_plants
    add_foreign_key :plant_semantic_tags, :semantic_tags

    # Query patterns for NLP
    create_table :query_patterns, id: :uuid do |t|
      t.text :pattern, null: false
      t.string :intent, limit: 50
      t.jsonb :parameters, default: {}
      t.jsonb :tag_mappings, default: {}
      t.integer :usage_count, default: 0
      t.timestamps
    end

    add_index :query_patterns, :intent
    add_index :query_patterns, :parameters, using: :gin
  end
end
