# This file is auto-generated from the current state of the database. Instead
# of editing this file, please use the migrations feature of Active Record to
# incrementally modify your database, and then regenerate this schema definition.
#
# This file is the source Rails uses to define your schema when running `bin/rails
# db:schema:load`. When creating a new database, `bin/rails db:schema:load` tends to
# be faster and is potentially less error prone than running all of your
# migrations from scratch. Old migrations may fail to apply correctly if those
# migrations use external dependencies or application code.
#
# It's strongly recommended that you check this file into your version control system.

ActiveRecord::Schema[7.1].define(version: 2025_06_26_162404) do
  # These are extensions that must be enabled in order to support this database
  enable_extension "pg_trgm"
  enable_extension "pgcrypto"
  enable_extension "plpgsql"

  # Custom types defined in this database.
  # Note that some types may not work with other database engines. Be careful if changing database.
  create_enum "evidence_type_enum", ["scientific", "traditional", "observational", "theoretical"]
  create_enum "invasiveness_risk_enum", ["none", "low", "moderate", "high", "severe"]
  create_enum "legal_status_enum", ["unrestricted", "restricted", "prohibited", "permit_required"]
  create_enum "life_cycle_enum", ["annual", "biennial", "perennial", "short_lived_perennial"]
  create_enum "light_requirement_enum", ["full_shade", "partial_shade", "partial_sun", "full_sun"]
  create_enum "name_type_enum", ["common", "regional", "traditional", "trade", "historical"]
  create_enum "pest_relationship_type_enum", ["susceptible", "resistant", "immune", "attracts", "repels"]
  create_enum "pest_type_enum", ["insect", "disease", "fungal", "bacterial", "viral", "nematode", "mammal", "bird"]
  create_enum "plant_type_enum", ["tree", "shrub", "herbaceous", "vine", "grass", "fern", "moss", "aquatic"]
  create_enum "soil_drainage_enum", ["poor", "moderate", "good", "excellent"]
  create_enum "soil_fertility_enum", ["poor", "moderate", "rich", "very_rich"]
  create_enum "trait_data_type_enum", ["numeric", "categorical", "boolean", "text"]

  create_table "ai_query_cache", id: :uuid, default: -> { "gen_random_uuid()" }, force: :cascade do |t|
    t.text "query_text", null: false
    t.string "query_hash", limit: 64, null: false
    t.jsonb "response_data"
    t.jsonb "plant_ids", default: []
    t.integer "hit_count", default: 1
    t.datetime "last_accessed_at"
    t.datetime "created_at", null: false
    t.datetime "updated_at", null: false
    t.index ["last_accessed_at"], name: "index_ai_query_cache_on_last_accessed_at"
    t.index ["plant_ids"], name: "index_ai_query_cache_on_plant_ids", using: :gin
    t.index ["query_hash"], name: "index_ai_query_cache_on_query_hash", unique: true
  end

  create_table "enhanced_plants", force: :cascade do |t|
    t.string "common_name", null: false
    t.string "scientific_name"
    t.string "family"
    t.text "description"
    t.string "growth_habit"
    t.string "habitat"
    t.string "edibility"
    t.string "medicinal_uses"
    t.string "toxicity"
    t.string "plant_type"
    t.string "life_cycle"
    t.datetime "created_at", null: false
    t.datetime "updated_at", null: false
    t.string "slug"
    t.float "data_quality_score"
    t.integer "mature_height_min_cm"
    t.integer "mature_height_max_cm"
    t.integer "mature_width_min_cm"
    t.integer "mature_width_max_cm"
    t.text "description_detailed"
    t.index "to_tsvector('english'::regconfig, (((((COALESCE(common_name, ''::character varying))::text || ' '::text) || (COALESCE(scientific_name, ''::character varying))::text) || ' '::text) || (COALESCE(family, ''::character varying))::text))", name: "enhanced_plants_search_idx", using: :gin
    t.index ["slug"], name: "index_enhanced_plants_on_slug"
  end

  create_table "environmental_requirements", force: :cascade do |t|
    t.bigint "enhanced_plant_id", null: false
    t.integer "temp_optimal_min"
    t.integer "temp_optimal_max"
    t.float "ph_min"
    t.float "ph_max"
    t.datetime "created_at", null: false
    t.datetime "updated_at", null: false
    t.integer "temp_min_survival"
    t.integer "temp_max_survival"
    t.integer "hardiness_zone_min"
    t.integer "hardiness_zone_max"
    t.integer "heat_zone_min"
    t.integer "heat_zone_max"
    t.float "drought_tolerance_score"
    t.float "flood_tolerance_score"
    t.string "soil_drainage"
    t.string "soil_fertility"
    t.string "light_requirement"
    t.float "soil_ph_min"
    t.float "soil_ph_max"
    t.float "ideal_temp_min"
    t.float "ideal_temp_max"
    t.index ["enhanced_plant_id"], name: "index_environmental_requirements_on_enhanced_plant_id"
  end

  create_table "friendly_id_slugs", force: :cascade do |t|
    t.string "slug", null: false
    t.integer "sluggable_id", null: false
    t.string "sluggable_type", limit: 50
    t.string "scope"
    t.datetime "created_at"
    t.index ["slug", "sluggable_type", "scope"], name: "index_friendly_id_slugs_on_slug_and_sluggable_type_and_scope", unique: true
    t.index ["slug", "sluggable_type"], name: "index_friendly_id_slugs_on_slug_and_sluggable_type"
    t.index ["sluggable_type", "sluggable_id"], name: "index_friendly_id_slugs_on_sluggable_type_and_sluggable_id"
  end

  create_table "guides", force: :cascade do |t|
    t.string "title"
    t.text "body"
    t.string "image"
    t.string "slug"
    t.datetime "created_at", null: false
    t.datetime "updated_at", null: false
    t.index ["slug"], name: "index_guides_on_slug", unique: true
  end

  create_table "pests", force: :cascade do |t|
    t.string "name", null: false
    t.string "slug", null: false
    t.string "picture"
    t.string "scientific_name"
    t.text "description"
    t.text "characteristics"
    t.jsonb "control_methods", default: {}
    t.jsonb "natural_enemies", default: []
    t.datetime "created_at", null: false
    t.datetime "updated_at", null: false
    t.index ["name"], name: "index_pests_on_name", unique: true
    t.index ["slug"], name: "index_pests_on_slug", unique: true
  end

  create_table "plant_contexts", force: :cascade do |t|
    t.bigint "enhanced_plant_id", null: false
    t.string "context_type", null: false
    t.text "content", null: false
    t.datetime "created_at", null: false
    t.datetime "updated_at", null: false
    t.index ["context_type"], name: "index_plant_contexts_on_context_type"
    t.index ["enhanced_plant_id", "context_type"], name: "index_plant_contexts_on_enhanced_plant_id_and_context_type", unique: true
    t.index ["enhanced_plant_id"], name: "index_plant_contexts_on_enhanced_plant_id"
  end

  create_table "plant_semantic_tags", id: :uuid, default: -> { "gen_random_uuid()" }, force: :cascade do |t|
    t.bigint "enhanced_plant_id", null: false
    t.uuid "semantic_tag_id", null: false
    t.decimal "confidence_score", precision: 3, scale: 2, default: "1.0"
    t.string "source", limit: 50, default: "manual"
    t.text "notes"
    t.datetime "created_at", null: false
    t.datetime "updated_at", null: false
    t.index ["enhanced_plant_id", "semantic_tag_id"], name: "idx_plant_semantic_tags_unique", unique: true
    t.index ["semantic_tag_id"], name: "index_plant_semantic_tags_on_semantic_tag_id"
  end

  create_table "plant_traits", force: :cascade do |t|
    t.string "name"
    t.text "description"
    t.datetime "created_at", null: false
    t.datetime "updated_at", null: false
    t.bigint "enhanced_plant_id", null: false
    t.index ["enhanced_plant_id"], name: "index_plant_traits_on_enhanced_plant_id"
  end

  create_table "plant_uses", force: :cascade do |t|
    t.bigint "enhanced_plant_id", null: false
    t.bigint "use_category_id", null: false
    t.float "effectiveness_score", default: 0.0, null: false
    t.float "confidence_score", default: 0.0, null: false
    t.datetime "created_at", null: false
    t.datetime "updated_at", null: false
    t.index ["enhanced_plant_id", "use_category_id"], name: "index_plant_uses_on_enhanced_plant_id_and_use_category_id", unique: true
    t.index ["enhanced_plant_id"], name: "index_plant_uses_on_enhanced_plant_id"
    t.index ["use_category_id"], name: "index_plant_uses_on_use_category_id"
  end

  create_table "query_patterns", id: :uuid, default: -> { "gen_random_uuid()" }, force: :cascade do |t|
    t.text "pattern", null: false
    t.string "intent", limit: 50
    t.jsonb "parameters", default: {}
    t.jsonb "tag_mappings", default: {}
    t.integer "usage_count", default: 0
    t.datetime "created_at", null: false
    t.datetime "updated_at", null: false
    t.index ["intent"], name: "index_query_patterns_on_intent"
    t.index ["parameters"], name: "index_query_patterns_on_parameters", using: :gin
  end

  create_table "resources", force: :cascade do |t|
    t.string "title"
    t.text "description"
    t.text "content"
    t.bigint "user_id", null: false
    t.datetime "created_at", null: false
    t.datetime "updated_at", null: false
    t.index ["user_id"], name: "index_resources_on_user_id"
  end

  create_table "rotten_articles", force: :cascade do |t|
    t.string "title"
    t.text "body"
    t.string "slug"
    t.string "image"
    t.boolean "is_published", default: true
    t.datetime "created_at", null: false
    t.datetime "updated_at", null: false
    t.index ["slug"], name: "index_rotten_articles_on_slug", unique: true
  end

  create_table "semantic_ontology", id: :uuid, default: -> { "gen_random_uuid()" }, force: :cascade do |t|
    t.string "name", limit: 100, null: false
    t.string "ontology_category", null: false
    t.uuid "parent_id"
    t.text "synonyms", default: [], array: true
    t.text "nlp_keywords", default: [], array: true
    t.decimal "ai_weight", precision: 3, scale: 2, default: "0.5"
    t.boolean "include_in_nlp", default: true
    t.text "description"
    t.jsonb "metadata", default: {}
    t.integer "usage_count", default: 0
    t.datetime "created_at", null: false
    t.datetime "updated_at", null: false
    t.index ["ai_weight"], name: "index_semantic_ontology_on_ai_weight"
    t.index ["metadata"], name: "index_semantic_ontology_on_metadata", using: :gin
    t.index ["name"], name: "index_semantic_ontology_on_name"
    t.index ["nlp_keywords"], name: "index_semantic_ontology_on_nlp_keywords", using: :gin
    t.index ["ontology_category"], name: "index_semantic_ontology_on_ontology_category"
    t.index ["parent_id"], name: "index_semantic_ontology_on_parent_id"
    t.index ["synonyms"], name: "index_semantic_ontology_on_synonyms", using: :gin
  end

  create_table "semantic_tags", id: :uuid, default: -> { "gen_random_uuid()" }, force: :cascade do |t|
    t.string "name", limit: 100, null: false
    t.string "category", limit: 50, null: false
    t.text "synonyms", default: [], array: true
    t.uuid "parent_tag_id"
    t.decimal "weight", precision: 3, scale: 2, default: "1.0"
    t.text "description"
    t.datetime "created_at", null: false
    t.datetime "updated_at", null: false
    t.index ["category"], name: "index_semantic_tags_on_category"
    t.index ["name"], name: "index_semantic_tags_on_name", unique: true
    t.index ["parent_tag_id"], name: "index_semantic_tags_on_parent_tag_id"
  end

  create_table "use_categories", force: :cascade do |t|
    t.string "name", null: false
    t.datetime "created_at", null: false
    t.datetime "updated_at", null: false
    t.index ["name"], name: "index_use_categories_on_name", unique: true
  end

  create_table "users", force: :cascade do |t|
    t.string "email", default: "", null: false
    t.string "encrypted_password", default: "", null: false
    t.string "reset_password_token"
    t.datetime "reset_password_sent_at"
    t.datetime "remember_created_at"
    t.datetime "created_at", null: false
    t.datetime "updated_at", null: false
    t.index ["email"], name: "index_users_on_email", unique: true
    t.index ["reset_password_token"], name: "index_users_on_reset_password_token", unique: true
  end

  add_foreign_key "environmental_requirements", "enhanced_plants"
  add_foreign_key "plant_contexts", "enhanced_plants"
  add_foreign_key "plant_semantic_tags", "enhanced_plants"
  add_foreign_key "plant_semantic_tags", "semantic_tags"
  add_foreign_key "plant_traits", "enhanced_plants"
  add_foreign_key "plant_uses", "enhanced_plants"
  add_foreign_key "plant_uses", "use_categories"
  add_foreign_key "resources", "users"
  add_foreign_key "semantic_ontology", "semantic_ontology", column: "parent_id"
  add_foreign_key "semantic_tags", "semantic_tags", column: "parent_tag_id"
end
