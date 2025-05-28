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

ActiveRecord::Schema[7.1].define(version: 2025_05_28_161241) do
  # These are extensions that must be enabled in order to support this database
  enable_extension "plpgsql"
  enable_extension "uuid-ossp"

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

  create_table "enhanced_pests_diseases", force: :cascade do |t|
    t.string "name", null: false
    t.string "scientific_name"
    t.enum "pest_type", enum_type: "pest_type_enum"
    t.text "description"
    t.text "symptoms"
    t.text "identification_notes"
    t.datetime "created_at", null: false
    t.datetime "updated_at", null: false
    t.index ["name"], name: "index_enhanced_pests_diseases_on_name"
    t.index ["pest_type"], name: "index_enhanced_pests_diseases_on_pest_type"
  end

  create_table "enhanced_plant_pest_relationships", force: :cascade do |t|
    t.bigint "enhanced_plant_id", null: false
    t.bigint "enhanced_pests_disease_id", null: false
    t.enum "relationship_type", enum_type: "pest_relationship_type_enum"
    t.float "severity_score"
    t.json "prevention_methods"
    t.json "treatment_methods"
    t.json "biological_controls"
    t.json "climate_factors"
    t.json "seasonal_timing"
    t.float "confidence_score", default: 1.0
    t.string "source"
    t.datetime "created_at", null: false
    t.datetime "updated_at", null: false
    t.index ["enhanced_pests_disease_id"], name: "idx_on_enhanced_pests_disease_id_6cbf69ae49"
    t.index ["enhanced_plant_id", "enhanced_pests_disease_id"], name: "unique_plant_pest_relationship", unique: true
    t.index ["enhanced_plant_id"], name: "index_enhanced_plant_pest_relationships_on_enhanced_plant_id"
    t.index ["relationship_type"], name: "index_enhanced_plant_pest_relationships_on_relationship_type"
  end

  create_table "enhanced_plants", force: :cascade do |t|
    t.uuid "uuid", default: -> { "gen_random_uuid()" }, null: false
    t.string "common_name", null: false
    t.string "scientific_name", null: false
    t.string "family", limit: 100
    t.string "genus", limit: 100
    t.string "species", limit: 100
    t.enum "plant_type", enum_type: "plant_type_enum"
    t.enum "life_cycle", enum_type: "life_cycle_enum"
    t.integer "mature_height_min_cm"
    t.integer "mature_height_max_cm"
    t.integer "mature_width_min_cm"
    t.integer "mature_width_max_cm"
    t.text "description_short"
    t.text "description_detailed"
    t.text "growing_notes"
    t.text "cultural_significance"
    t.float "data_quality_score", default: 0.0
    t.tsvector "search_vector"
    t.datetime "created_at", null: false
    t.datetime "updated_at", null: false
    t.string "slug"
    t.index ["common_name"], name: "index_enhanced_plants_on_common_name"
    t.index ["data_quality_score"], name: "index_enhanced_plants_on_data_quality_score"
    t.index ["family"], name: "index_enhanced_plants_on_family"
    t.index ["life_cycle"], name: "index_enhanced_plants_on_life_cycle"
    t.index ["plant_type"], name: "index_enhanced_plants_on_plant_type"
    t.index ["scientific_name"], name: "index_enhanced_plants_on_scientific_name", unique: true
    t.index ["search_vector"], name: "index_enhanced_plants_on_search_vector", using: :gin
    t.index ["slug"], name: "index_enhanced_plants_on_slug"
    t.index ["uuid"], name: "index_enhanced_plants_on_uuid", unique: true
  end

  create_table "environmental_requirements", force: :cascade do |t|
    t.bigint "enhanced_plant_id", null: false
    t.integer "hardiness_zone_min"
    t.integer "hardiness_zone_max"
    t.integer "heat_zone_min"
    t.integer "heat_zone_max"
    t.float "temp_min_survival"
    t.float "temp_max_survival"
    t.float "temp_optimal_min"
    t.float "temp_optimal_max"
    t.integer "annual_rainfall_min_mm"
    t.integer "annual_rainfall_max_mm"
    t.float "drought_tolerance_score"
    t.float "flood_tolerance_score"
    t.float "soil_ph_min"
    t.float "soil_ph_max"
    t.enum "soil_drainage", enum_type: "soil_drainage_enum"
    t.enum "soil_fertility", enum_type: "soil_fertility_enum"
    t.enum "light_requirement", enum_type: "light_requirement_enum"
    t.json "light_tolerance"
    t.text "climate_description"
    t.text "soil_description"
    t.datetime "created_at", null: false
    t.datetime "updated_at", null: false
    t.index ["drought_tolerance_score"], name: "index_environmental_requirements_on_drought_tolerance_score"
    t.index ["enhanced_plant_id"], name: "index_environmental_requirements_on_enhanced_plant_id"
    t.index ["hardiness_zone_min", "hardiness_zone_max"], name: "idx_on_hardiness_zone_min_hardiness_zone_max_37997d309b"
    t.index ["light_requirement"], name: "index_environmental_requirements_on_light_requirement"
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

  create_table "guild_members", force: :cascade do |t|
    t.bigint "plant_guild_id", null: false
    t.bigint "enhanced_plant_id", null: false
    t.string "role", limit: 100
    t.float "importance_score"
    t.integer "planting_order"
    t.datetime "created_at", null: false
    t.datetime "updated_at", null: false
    t.index ["enhanced_plant_id"], name: "index_guild_members_on_enhanced_plant_id"
    t.index ["plant_guild_id", "enhanced_plant_id"], name: "index_guild_members_on_plant_guild_id_and_enhanced_plant_id", unique: true
    t.index ["plant_guild_id"], name: "index_guild_members_on_plant_guild_id"
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

  create_table "plant_guilds", force: :cascade do |t|
    t.string "name", null: false
    t.text "description"
    t.json "climate_suitability"
    t.float "space_requirement_sqm"
    t.text "guild_purpose"
    t.text "management_notes"
    t.datetime "created_at", null: false
    t.datetime "updated_at", null: false
    t.index ["name"], name: "index_plant_guilds_on_name"
  end

  create_table "plant_names", force: :cascade do |t|
    t.bigint "enhanced_plant_id", null: false
    t.string "name", null: false
    t.enum "name_type", null: false, enum_type: "name_type_enum"
    t.string "language_code", limit: 5
    t.string "region", limit: 100
    t.float "confidence_score", default: 1.0
    t.string "source"
    t.datetime "created_at", null: false
    t.datetime "updated_at", null: false
    t.index ["enhanced_plant_id"], name: "index_plant_names_on_enhanced_plant_id"
    t.index ["language_code", "region"], name: "index_plant_names_on_language_code_and_region"
    t.index ["name"], name: "index_plant_names_on_name"
  end

  create_table "plant_pests", force: :cascade do |t|
    t.bigint "plant_id", null: false
    t.bigint "pest_id", null: false
    t.datetime "created_at", null: false
    t.datetime "updated_at", null: false
    t.index ["pest_id"], name: "index_plant_pests_on_pest_id"
    t.index ["plant_id", "pest_id"], name: "index_plant_pests_on_plant_id_and_pest_id", unique: true
    t.index ["plant_id"], name: "index_plant_pests_on_plant_id"
  end

  create_table "plant_regional_data", force: :cascade do |t|
    t.bigint "enhanced_plant_id", null: false
    t.bigint "region_id", null: false
    t.float "performance_score"
    t.enum "invasiveness_risk", enum_type: "invasiveness_risk_enum"
    t.enum "legal_status", enum_type: "legal_status_enum"
    t.json "planting_season"
    t.json "harvest_season"
    t.text "special_considerations"
    t.text "local_varieties"
    t.json "regional_names"
    t.text "cultural_uses"
    t.text "traditional_knowledge"
    t.datetime "created_at", null: false
    t.datetime "updated_at", null: false
    t.index ["enhanced_plant_id"], name: "index_plant_regional_data_on_enhanced_plant_id"
    t.index ["invasiveness_risk"], name: "index_plant_regional_data_on_invasiveness_risk"
    t.index ["performance_score"], name: "index_plant_regional_data_on_performance_score"
    t.index ["region_id"], name: "index_plant_regional_data_on_region_id"
  end

  create_table "plant_relationships", force: :cascade do |t|
    t.bigint "plant_a_id", null: false
    t.bigint "plant_b_id", null: false
    t.bigint "relationship_type_id", null: false
    t.float "strength_score"
    t.text "mechanism"
    t.integer "distance_optimal_cm"
    t.integer "distance_max_cm"
    t.json "climate_conditions"
    t.json "soil_conditions"
    t.float "confidence_score", default: 1.0
    t.enum "evidence_type", enum_type: "evidence_type_enum"
    t.string "source"
    t.text "notes"
    t.datetime "created_at", null: false
    t.datetime "updated_at", null: false
    t.index ["plant_a_id", "plant_b_id", "relationship_type_id"], name: "unique_plant_relationship", unique: true
    t.index ["plant_a_id"], name: "index_plant_relationships_on_plant_a_id"
    t.index ["plant_b_id"], name: "index_plant_relationships_on_plant_b_id"
    t.index ["relationship_type_id"], name: "index_plant_relationships_on_relationship_type_id"
    t.index ["strength_score"], name: "index_plant_relationships_on_strength_score"
  end

  create_table "plant_traits", force: :cascade do |t|
    t.bigint "enhanced_plant_id", null: false
    t.bigint "trait_category_id", null: false
    t.float "numeric_value"
    t.float "numeric_min"
    t.float "numeric_max"
    t.string "categorical_value", limit: 100
    t.boolean "boolean_value"
    t.text "text_value"
    t.float "confidence_score", default: 1.0
    t.string "context"
    t.string "source"
    t.text "notes"
    t.datetime "created_at", null: false
    t.datetime "updated_at", null: false
    t.index ["categorical_value"], name: "index_plant_traits_on_categorical_value"
    t.index ["confidence_score"], name: "index_plant_traits_on_confidence_score"
    t.index ["enhanced_plant_id"], name: "index_plant_traits_on_enhanced_plant_id"
    t.index ["numeric_value"], name: "index_plant_traits_on_numeric_value"
    t.index ["trait_category_id"], name: "index_plant_traits_on_trait_category_id"
  end

  create_table "plant_uses", force: :cascade do |t|
    t.bigint "enhanced_plant_id", null: false
    t.bigint "use_category_id", null: false
    t.string "plant_part", limit: 100
    t.text "preparation_method"
    t.float "effectiveness_score"
    t.text "safety_notes"
    t.text "traditional_knowledge"
    t.json "harvest_season"
    t.string "processing_time", limit: 100
    t.float "confidence_score", default: 1.0
    t.string "source"
    t.datetime "created_at", null: false
    t.datetime "updated_at", null: false
    t.index ["effectiveness_score"], name: "index_plant_uses_on_effectiveness_score"
    t.index ["enhanced_plant_id"], name: "index_plant_uses_on_enhanced_plant_id"
    t.index ["plant_part"], name: "index_plant_uses_on_plant_part"
    t.index ["use_category_id"], name: "index_plant_uses_on_use_category_id"
  end

  create_table "plants", force: :cascade do |t|
    t.string "picture"
    t.string "common_name", null: false
    t.string "scientific_name"
    t.text "aka", default: [], array: true
    t.string "family"
    t.int4range "zone_range"
    t.string "ideal_temp_min"
    t.string "ideal_temp_max"
    t.string "min_temp"
    t.string "max_temp"
    t.boolean "perennial"
    t.text "layers", default: [], array: true
    t.text "plant_functions", default: [], array: true
    t.text "description"
    t.text "purpose"
    t.text "avoid", default: [], array: true
    t.text "companions", default: [], array: true
    t.datetime "created_at", null: false
    t.datetime "updated_at", null: false
    t.index ["common_name"], name: "index_plants_on_common_name", unique: true
  end

  create_table "regions", force: :cascade do |t|
    t.string "name", null: false
    t.string "country_code", limit: 3
    t.string "climate_type", limit: 100
    t.float "latitude_min"
    t.float "latitude_max"
    t.float "longitude_min"
    t.float "longitude_max"
    t.float "avg_temp_min"
    t.float "avg_temp_max"
    t.integer "avg_rainfall_mm"
    t.integer "growing_season_days"
    t.datetime "created_at", null: false
    t.datetime "updated_at", null: false
    t.index ["climate_type"], name: "index_regions_on_climate_type"
    t.index ["country_code"], name: "index_regions_on_country_code"
    t.index ["name"], name: "index_regions_on_name"
  end

  create_table "relationship_types", force: :cascade do |t|
    t.string "name", limit: 100, null: false
    t.text "description"
    t.boolean "is_beneficial"
    t.string "strength_scale", limit: 50
    t.datetime "created_at", null: false
    t.datetime "updated_at", null: false
    t.index ["is_beneficial"], name: "index_relationship_types_on_is_beneficial"
    t.index ["name"], name: "index_relationship_types_on_name", unique: true
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

  create_table "trait_categories", force: :cascade do |t|
    t.string "name", limit: 100, null: false
    t.text "description"
    t.enum "data_type", null: false, enum_type: "trait_data_type_enum"
    t.string "unit", limit: 20
    t.json "synonyms"
    t.json "search_keywords"
    t.datetime "created_at", null: false
    t.datetime "updated_at", null: false
    t.index ["data_type"], name: "index_trait_categories_on_data_type"
    t.index ["name"], name: "index_trait_categories_on_name", unique: true
  end

  create_table "use_categories", force: :cascade do |t|
    t.string "name", limit: 100, null: false
    t.bigint "parent_category_id"
    t.text "description"
    t.json "search_terms"
    t.datetime "created_at", null: false
    t.datetime "updated_at", null: false
    t.index ["name"], name: "index_use_categories_on_name", unique: true
    t.index ["parent_category_id"], name: "index_use_categories_on_parent_category_id"
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

  add_foreign_key "enhanced_plant_pest_relationships", "enhanced_pests_diseases", on_delete: :cascade
  add_foreign_key "enhanced_plant_pest_relationships", "enhanced_plants", on_delete: :cascade
  add_foreign_key "environmental_requirements", "enhanced_plants", on_delete: :cascade
  add_foreign_key "guild_members", "enhanced_plants", on_delete: :cascade
  add_foreign_key "guild_members", "plant_guilds", on_delete: :cascade
  add_foreign_key "plant_names", "enhanced_plants", on_delete: :cascade
  add_foreign_key "plant_pests", "pests"
  add_foreign_key "plant_pests", "plants"
  add_foreign_key "plant_regional_data", "enhanced_plants", on_delete: :cascade
  add_foreign_key "plant_regional_data", "regions", on_delete: :cascade
  add_foreign_key "plant_relationships", "enhanced_plants", column: "plant_a_id", on_delete: :cascade
  add_foreign_key "plant_relationships", "enhanced_plants", column: "plant_b_id", on_delete: :cascade
  add_foreign_key "plant_relationships", "relationship_types"
  add_foreign_key "plant_traits", "enhanced_plants", on_delete: :cascade
  add_foreign_key "plant_traits", "trait_categories"
  add_foreign_key "plant_uses", "enhanced_plants", on_delete: :cascade
  add_foreign_key "plant_uses", "use_categories"
  add_foreign_key "resources", "users"
  add_foreign_key "use_categories", "use_categories", column: "parent_category_id"
end
