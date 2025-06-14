# frozen_string_literal: true
class CreateEnhancedSemanticOntology < ActiveRecord::Migration[7.1]
  def change
    # Enable vector extension for embeddings (if using pgvector)
    # enable_extension 'vector' # Uncomment if using pgvector

    # Enhanced semantic ontology table
    create_table :semantic_ontology, id: :uuid do |t|
      t.string :name, null: false, limit: 100
      t.string :ontology_category, null: false
      t.uuid :parent_id, null: true

      # AI and NLP fields
      t.text :synonyms, array: true, default: []
      t.text :nlp_keywords, array: true, default: []
      t.decimal :ai_weight, precision: 3, scale: 2, default: 0.5
      t.boolean :include_in_nlp, default: true

      # Vector embedding for semantic search (uncomment if using pgvector)
      # t.vector :embedding_vector, limit: 1536 # OpenAI ada-002 dimensions

      # Metadata
      t.text :description
      t.jsonb :metadata, default: {}
      t.integer :usage_count, default: 0

      t.timestamps
    end

    # Indexes
    add_index :semantic_ontology, :name
    add_index :semantic_ontology, :ontology_category
    add_index :semantic_ontology, :parent_id
    add_index :semantic_ontology, :ai_weight
    add_index :semantic_ontology, :synonyms, using: :gin
    add_index :semantic_ontology, :nlp_keywords, using: :gin
    add_index :semantic_ontology, :metadata, using: :gin

    # Vector index (uncomment if using pgvector)
    # add_index :semantic_ontology, :embedding_vector, using: :ivfflat, opclass: :vector_cosine_ops

    # Foreign key constraint
    add_foreign_key :semantic_ontology, :semantic_ontology, column: :parent_id

    # Plant-ontology association table
    create_table :plant_ontology_tags, id: :uuid do |t|
      t.bigint :plant_id, null: false
      t.uuid :semantic_ontology_id, null: false

      # AI confidence and context
      t.decimal :confidence_score, precision: 3, scale: 2, default: 1.0
      t.string :source, limit: 50, default: 'manual'
      t.string :context, limit: 100 # e.g., 'companion_planting', 'edible_use'
      t.jsonb :ai_metadata, default: {}

      t.text :notes
      t.timestamps
    end

    # Indexes for plant associations
    add_index :plant_ontology_tags, [:plant_id, :semantic_ontology_id],
              unique: true, name: 'idx_plant_ontology_unique'
    add_index :plant_ontology_tags, :semantic_ontology_id
    add_index :plant_ontology_tags, :confidence_score
    add_index :plant_ontology_tags, :source
    add_index :plant_ontology_tags, :context
    add_index :plant_ontology_tags, :ai_metadata, using: :gin

    # Foreign keys
    add_foreign_key :plant_ontology_tags, :plants
    add_foreign_key :plant_ontology_tags, :semantic_ontology, column: :semantic_ontology_id

    # Query cache for AI responses
    create_table :ai_query_cache, id: :uuid do |t|
      t.text :query_text, null: false
      t.string :query_hash, null: false, limit: 64
      t.jsonb :response_data
      t.jsonb :plant_ids, default: []
      t.integer :hit_count, default: 1
      t.datetime :last_accessed_at

      t.timestamps
    end

    add_index :ai_query_cache, :query_hash, unique: true
    add_index :ai_query_cache, :last_accessed_at
    add_index :ai_query_cache, :plant_ids, using: :gin
  end
end