# PermieBro Enhanced Database Schema Design

## Overview
This document outlines an improved database schema for PermieBro that supports flexible searching, semantic queries, and GPT integration while maintaining offline functionality.

## Core Design Principles

1. **Trait-Based Architecture**: Move from binary tags to weighted traits and descriptive attributes
2. **Semantic Richness**: Include natural language descriptions that can be embedded for vector search
3. **Relationship Modeling**: Explicit modeling of plant relationships and guild compatibility
4. **Regional Adaptability**: Support for location-specific data and climate variations
5. **Multilingual Support**: Accommodate regional names and descriptions
6. **Fuzzy Matching**: Enable partial matches and similarity scoring

## Enhanced Schema Structure

### 1. Core Plant Entity

```sql
CREATE TABLE plants (
    id SERIAL PRIMARY KEY,
    uuid UUID UNIQUE DEFAULT gen_random_uuid(),
    
    -- Basic Identification
    common_name VARCHAR(255) NOT NULL,
    scientific_name VARCHAR(255) NOT NULL,
    family VARCHAR(100),
    genus VARCHAR(100),
    species VARCHAR(100),
    
    -- Taxonomic and Classification
    plant_type ENUM('tree', 'shrub', 'herbaceous', 'vine', 'grass', 'fern', 'moss', 'aquatic'),
    life_cycle ENUM('annual', 'biennial', 'perennial', 'short_lived_perennial'),
    
    -- Physical Characteristics (for fuzzy matching)
    mature_height_min_cm INTEGER,
    mature_height_max_cm INTEGER,
    mature_width_min_cm INTEGER,
    mature_width_max_cm INTEGER,
    
    -- Semantic Description Fields (for embedding)
    description_short TEXT, -- 1-2 sentences for quick reference
    description_detailed TEXT, -- Full botanical description
    growing_notes TEXT, -- Practical growing advice
    cultural_significance TEXT, -- Traditional uses and cultural context
    
    -- Timestamps and Metadata
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    data_quality_score FLOAT DEFAULT 0.0, -- For ranking search results
    
    -- Search Optimization
    search_vector TSVECTOR, -- Full-text search
    embedding_vector VECTOR(1536), -- For semantic search (OpenAI ada-002 dimensions)
    
    UNIQUE(scientific_name)
);
```

### 2. Regional Names and Aliases

```sql
CREATE TABLE plant_names (
    id SERIAL PRIMARY KEY,
    plant_id INTEGER REFERENCES plants(id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL,
    name_type ENUM('common', 'regional', 'traditional', 'trade', 'historical'),
    language_code VARCHAR(5), -- ISO 639-1 codes (en, es, fr, etc.)
    region VARCHAR(100), -- Geographic region where name is used
    confidence_score FLOAT DEFAULT 1.0, -- How certain we are about this name
    source VARCHAR(255), -- Where this name came from
    
    INDEX(plant_id),
    INDEX(name),
    INDEX(language_code, region)
);
```

### 3. Trait System (Replaces Binary Tags)

```sql
CREATE TABLE trait_categories (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) UNIQUE NOT NULL,
    description TEXT,
    data_type ENUM('numeric', 'categorical', 'boolean', 'text'),
    unit VARCHAR(20), -- For numeric traits (cm, kg, pH, etc.)
    
    -- For fuzzy matching
    synonyms JSON, -- Alternative terms for this trait
    search_keywords JSON -- Keywords that should match this trait
);

CREATE TABLE plant_traits (
    id SERIAL PRIMARY KEY,
    plant_id INTEGER REFERENCES plants(id) ON DELETE CASCADE,
    trait_category_id INTEGER REFERENCES trait_categories(id),
    
    -- Flexible value storage
    numeric_value FLOAT,
    numeric_min FLOAT,
    numeric_max FLOAT,
    categorical_value VARCHAR(100),
    boolean_value BOOLEAN,
    text_value TEXT,
    
    -- Confidence and context
    confidence_score FLOAT DEFAULT 1.0,
    context VARCHAR(255), -- "in ideal conditions", "drought stress", etc.
    source VARCHAR(255),
    notes TEXT,
    
    INDEX(plant_id),
    INDEX(trait_category_id),
    INDEX(categorical_value),
    INDEX(numeric_value)
);
```

### 4. Environmental Requirements (Enhanced)

```sql
CREATE TABLE environmental_requirements (
    id SERIAL PRIMARY KEY,
    plant_id INTEGER REFERENCES plants(id) ON DELETE CASCADE,
    
    -- Climate Zones (more flexible than simple range)
    hardiness_zone_min INTEGER,
    hardiness_zone_max INTEGER,
    heat_zone_min INTEGER,
    heat_zone_max INTEGER,
    
    -- Temperature (in Celsius for consistency)
    temp_min_survival FLOAT,
    temp_max_survival FLOAT,
    temp_optimal_min FLOAT,
    temp_optimal_max FLOAT,
    
    -- Precipitation and Water
    annual_rainfall_min_mm INTEGER,
    annual_rainfall_max_mm INTEGER,
    drought_tolerance_score FLOAT, -- 0-1 scale
    flood_tolerance_score FLOAT, -- 0-1 scale
    
    -- Soil Requirements
    soil_ph_min FLOAT,
    soil_ph_max FLOAT,
    soil_drainage ENUM('poor', 'moderate', 'good', 'excellent'),
    soil_fertility ENUM('poor', 'moderate', 'rich', 'very_rich'),
    
    -- Light Requirements
    light_requirement ENUM('full_shade', 'partial_shade', 'partial_sun', 'full_sun'),
    light_tolerance JSON, -- Array of acceptable light conditions
    
    -- Semantic descriptions for fuzzy matching
    climate_description TEXT, -- "thrives in hot, dry summers"
    soil_description TEXT, -- "prefers well-drained, sandy loam"
    
    INDEX(plant_id),
    INDEX(hardiness_zone_min, hardiness_zone_max),
    INDEX(drought_tolerance_score),
    INDEX(light_requirement)
);
```

### 5. Functional Uses (Enhanced)

```sql
CREATE TABLE use_categories (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) UNIQUE NOT NULL,
    parent_category_id INTEGER REFERENCES use_categories(id),
    description TEXT,
    search_terms JSON -- Alternative terms that should match this use
);

CREATE TABLE plant_uses (
    id SERIAL PRIMARY KEY,
    plant_id INTEGER REFERENCES plants(id) ON DELETE CASCADE,
    use_category_id INTEGER REFERENCES use_categories(id),
    
    -- Detailed information about the use
    plant_part VARCHAR(100), -- roots, leaves, flowers, etc.
    preparation_method TEXT, -- how to prepare/process
    effectiveness_score FLOAT, -- 0-1 scale for how effective this use is
    safety_notes TEXT,
    traditional_knowledge TEXT,
    
    -- Seasonal and timing information
    harvest_season JSON, -- ["spring", "summer"]
    processing_time VARCHAR(100),
    
    -- Source and confidence
    confidence_score FLOAT DEFAULT 1.0,
    source VARCHAR(255),
    
    INDEX(plant_id),
    INDEX(use_category_id),
    INDEX(plant_part),
    INDEX(effectiveness_score)
);
```

### 6. Plant Relationships and Guilds

```sql
CREATE TABLE relationship_types (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) UNIQUE NOT NULL,
    description TEXT,
    is_beneficial BOOLEAN,
    strength_scale VARCHAR(50) -- "weak", "moderate", "strong"
);

CREATE TABLE plant_relationships (
    id SERIAL PRIMARY KEY,
    plant_a_id INTEGER REFERENCES plants(id) ON DELETE CASCADE,
    plant_b_id INTEGER REFERENCES plants(id) ON DELETE CASCADE,
    relationship_type_id INTEGER REFERENCES relationship_types(id),
    
    -- Relationship details
    strength_score FLOAT, -- 0-1 scale
    mechanism TEXT, -- How the relationship works
    distance_optimal_cm INTEGER, -- Optimal planting distance
    distance_max_cm INTEGER, -- Maximum effective distance
    
    -- Conditions where relationship applies
    climate_conditions JSON,
    soil_conditions JSON,
    
    -- Evidence and confidence
    confidence_score FLOAT DEFAULT 1.0,
    evidence_type ENUM('scientific', 'traditional', 'observational', 'theoretical'),
    source VARCHAR(255),
    notes TEXT,
    
    INDEX(plant_a_id),
    INDEX(plant_b_id),
    INDEX(relationship_type_id),
    INDEX(strength_score),
    UNIQUE(plant_a_id, plant_b_id, relationship_type_id)
);

CREATE TABLE plant_guilds (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    climate_suitability JSON, -- Zones/climates where this guild works
    space_requirement_sqm FLOAT,
    
    -- Semantic description for GPT queries
    guild_purpose TEXT,
    management_notes TEXT,
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE guild_members (
    id SERIAL PRIMARY KEY,
    guild_id INTEGER REFERENCES plant_guilds(id) ON DELETE CASCADE,
    plant_id INTEGER REFERENCES plants(id) ON DELETE CASCADE,
    role VARCHAR(100), -- "nitrogen_fixer", "canopy", "ground_cover", etc.
    importance_score FLOAT, -- How critical this plant is to the guild
    planting_order INTEGER, -- Sequence for establishing the guild
    
    INDEX(guild_id),
    INDEX(plant_id),
    UNIQUE(guild_id, plant_id)
);
```

### 7. Regional Adaptations

```sql
CREATE TABLE regions (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    country_code VARCHAR(3),
    climate_type VARCHAR(100),
    latitude_min FLOAT,
    latitude_max FLOAT,
    longitude_min FLOAT,
    longitude_max FLOAT,
    
    -- Climate characteristics
    avg_temp_min FLOAT,
    avg_temp_max FLOAT,
    avg_rainfall_mm INTEGER,
    growing_season_days INTEGER,
    
    INDEX(country_code),
    INDEX(climate_type)
);

CREATE TABLE plant_regional_data (
    id SERIAL PRIMARY KEY,
    plant_id INTEGER REFERENCES plants(id) ON DELETE CASCADE,
    region_id INTEGER REFERENCES regions(id) ON DELETE CASCADE,
    
    -- Regional performance
    performance_score FLOAT, -- How well it grows in this region
    invasiveness_risk ENUM('none', 'low', 'moderate', 'high', 'severe'),
    legal_status ENUM('unrestricted', 'restricted', 'prohibited', 'permit_required'),
    
    -- Regional growing notes
    planting_season JSON,
    harvest_season JSON,
    special_considerations TEXT,
    local_varieties TEXT,
    
    -- Local names and cultural info
    regional_names JSON,
    cultural_uses TEXT,
    traditional_knowledge TEXT,
    
    INDEX(plant_id),
    INDEX(region_id),
    INDEX(invasiveness_risk),
    INDEX(performance_score)
);
```

### 8. Pest and Disease Relationships

```sql
CREATE TABLE pests_diseases (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    scientific_name VARCHAR(255),
    type ENUM('insect', 'disease', 'fungal', 'bacterial', 'viral', 'nematode', 'mammal', 'bird'),
    description TEXT,
    
    -- Identification help
    symptoms TEXT,
    identification_notes TEXT,
    
    INDEX(type),
    INDEX(name)
);

CREATE TABLE plant_pest_relationships (
    id SERIAL PRIMARY KEY,
    plant_id INTEGER REFERENCES plants(id) ON DELETE CASCADE,
    pest_disease_id INTEGER REFERENCES pests_diseases(id) ON DELETE CASCADE,
    
    relationship_type ENUM('susceptible', 'resistant', 'immune', 'attracts', 'repels'),
    severity_score FLOAT, -- 0-1 scale
    
    -- Management information
    prevention_methods JSON,
    treatment_methods JSON,
    biological_controls JSON,
    
    -- Conditions
    climate_factors JSON,
    seasonal_timing JSON,
    
    confidence_score FLOAT DEFAULT 1.0,
    source VARCHAR(255),
    
    INDEX(plant_id),
    INDEX(pest_disease_id),
    INDEX(relationship_type),
    UNIQUE(plant_id, pest_disease_id)
);
```

## Search and Query Optimization

### 1. Full-Text Search Setup

```sql
-- Create search index combining multiple text fields
CREATE INDEX plants_search_idx ON plants USING GIN(search_vector);

-- Function to update search vector
CREATE OR REPLACE FUNCTION update_plant_search_vector()
RETURNS TRIGGER AS $$
BEGIN
    NEW.search_vector := 
        setweight(to_tsvector('english', COALESCE(NEW.common_name, '')), 'A') ||
        setweight(to_tsvector('english', COALESCE(NEW.scientific_name, '')), 'A') ||
        setweight(to_tsvector('english', COALESCE(NEW.description_short, '')), 'B') ||
        setweight(to_tsvector('english', COALESCE(NEW.description_detailed, '')), 'C') ||
        setweight(to_tsvector('english', COALESCE(NEW.growing_notes, '')), 'D');
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Trigger to automatically update search vector
CREATE TRIGGER plants_search_vector_update
    BEFORE INSERT OR UPDATE ON plants
    FOR EACH ROW EXECUTE FUNCTION update_plant_search_vector();
```

### 2. Semantic Search Preparation

```sql
-- Index for vector similarity search (requires pgvector extension)
CREATE INDEX plants_embedding_idx ON plants USING ivfflat (embedding_vector vector_cosine_ops);

-- Function to find similar plants by embedding
CREATE OR REPLACE FUNCTION find_similar_plants(
    query_embedding VECTOR(1536),
    similarity_threshold FLOAT DEFAULT 0.7,
    max_results INTEGER DEFAULT 10
)
RETURNS TABLE(
    plant_id INTEGER,
    common_name VARCHAR(255),
    similarity_score FLOAT
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        p.id,
        p.common_name,
        1 - (p.embedding_vector <=> query_embedding) AS similarity
    FROM plants p
    WHERE 1 - (p.embedding_vector <=> query_embedding) > similarity_threshold
    ORDER BY p.embedding_vector <=> query_embedding
    LIMIT max_results;
END;
$$ LANGUAGE plpgsql;
```

## Example Data Entries

### Example 1: Tomato with Enhanced Structure

```json
{
  "plant": {
    "common_name": "Tomato",
    "scientific_name": "Solanum lycopersicum",
    "family": "Solanaceae",
    "plant_type": "herbaceous",
    "life_cycle": "annual",
    "description_short": "Popular warm-season fruit vegetable with red, juicy fruits",
    "description_detailed": "Tomato is a tender, warm-season vegetable that produces edible fruits in various sizes, colors, and shapes. Plants can be determinate (bush) or indeterminate (vining) types.",
    "growing_notes": "Requires warm soil, consistent moisture, and support for vining varieties. Benefits from mulching and regular feeding.",
    "mature_height_min_cm": 30,
    "mature_height_max_cm": 200
  },
  "names": [
    {"name": "Tomate", "language_code": "es", "name_type": "common"},
    {"name": "Love Apple", "name_type": "historical"},
    {"name": "Pomodoro", "language_code": "it", "name_type": "common"}
  ],
  "traits": [
    {
      "category": "fruit_color",
      "categorical_value": "red",
      "confidence_score": 0.9
    },
    {
      "category": "days_to_maturity",
      "numeric_min": 60,
      "numeric_max": 90,
      "context": "from transplant"
    },
    {
      "category": "flavor_profile",
      "text_value": "sweet, acidic, umami-rich",
      "confidence_score": 0.8
    }
  ],
  "environmental_requirements": {
    "hardiness_zone_min": 3,
    "hardiness_zone_max": 11,
    "temp_optimal_min": 18,
    "temp_optimal_max": 29,
    "light_requirement": "full_sun",
    "soil_ph_min": 6.0,
    "soil_ph_max": 6.8,
    "drought_tolerance_score": 0.3,
    "climate_description": "thrives in warm, sunny conditions with consistent moisture"
  },
  "uses": [
    {
      "category": "culinary_fresh",
      "plant_part": "fruit",
      "effectiveness_score": 1.0,
      "harvest_season": ["summer", "fall"]
    },
    {
      "category": "culinary_preserved",
      "plant_part": "fruit",
      "preparation_method": "canning, drying, sauce-making",
      "effectiveness_score": 0.9
    }
  ]
}
```

### Example 2: Comfrey with Relationship Data

```json
{
  "plant": {
    "common_name": "Comfrey",
    "scientific_name": "Symphytum officinale",
    "family": "Boraginaceae",
    "plant_type": "herbaceous",
    "life_cycle": "perennial",
    "description_short": "Deep-rooted perennial herb excellent for soil improvement and medicinal use",
    "description_detailed": "Comfrey is a robust perennial with large, hairy leaves and bell-shaped flowers. Its deep taproot mines nutrients from subsoil layers.",
    "growing_notes": "Once established, very difficult to remove. Harvest leaves regularly for best growth. Avoid internal consumption.",
    "mature_height_min_cm": 60,
    "mature_height_max_cm": 120
  },
  "traits": [
    {
      "category": "root_depth",
      "numeric_value": 300,
      "unit": "cm",
      "confidence_score": 0.9
    },
    {
      "category": "nutrient_accumulation",
      "text_value": "potassium, phosphorus, nitrogen",
      "confidence_score": 0.95
    },
    {
      "category": "growth_rate",
      "categorical_value": "fast",
      "confidence_score": 0.8
    }
  ],
  "relationships": [
    {
      "partner_plant": "fruit_trees",
      "relationship_type": "beneficial_companion",
      "mechanism": "dynamic accumulator provides nutrients when chopped and dropped",
      "strength_score": 0.8,
      "distance_optimal_cm": 100
    },
    {
      "partner_plant": "vegetables",
      "relationship_type": "mulch_provider",
      "mechanism": "leaves provide high-nitrogen mulch",
      "strength_score": 0.9
    }
  ],
  "uses": [
    {
      "category": "soil_improvement",
      "plant_part": "leaves",
      "preparation_method": "chop and drop, compost ingredient",
      "effectiveness_score": 0.95
    },
    {
      "category": "medicinal_topical",
      "plant_part": "leaves",
      "preparation_method": "poultice, salve",
      "effectiveness_score": 0.8,
      "safety_notes": "external use only, contains pyrrolizidine alkaloids"
    }
  ]
}
```

## Implementation Strategy for GPT Integration

### 1. Embedding Generation
- Generate embeddings for plant descriptions, uses, and growing notes
- Update embeddings when plant data changes
- Store embeddings in the database for fast similarity search

### 2. Query Processing Pipeline
```python
def process_natural_query(query: str) -> List[Plant]:
    # 1. Extract intent and entities
    intent = extract_intent(query)  # "find", "compare", "recommend"
    entities = extract_entities(query)  # plant names, traits, conditions
    
    # 2. Generate query embedding
    query_embedding = generate_embedding(query)
    
    # 3. Multi-modal search
    semantic_results = semantic_search(query_embedding)
    keyword_results = full_text_search(entities)
    trait_results = trait_based_search(entities)
    
    # 4. Combine and rank results
    combined_results = combine_search_results(
        semantic_results, keyword_results, trait_results
    )
    
    return ranked_results
```

### 3. Fuzzy Trait Matching
```sql
-- Example: Find plants good for "dry heat"
SELECT DISTINCT p.*, 
       (er.drought_tolerance_score * 0.4 + 
        CASE WHEN er.temp_optimal_max > 30 THEN 0.6 ELSE 0.2 END) as suitability_score
FROM plants p
JOIN environmental_requirements er ON p.id = er.plant_id
WHERE er.drought_tolerance_score > 0.6
   OR er.climate_description ILIKE '%dry%'
   OR er.climate_description ILIKE '%heat%'
ORDER BY suitability_score DESC;
```

## Benefits of This Enhanced Schema

1. **Flexible Trait System**: Supports fuzzy matching and weighted scoring
2. **Rich Relationships**: Models complex plant interactions and guild dynamics
3. **Regional Adaptability**: Accounts for geographic and climate variations
4. **Semantic Search Ready**: Structured for embedding-based similarity search
5. **Multilingual Support**: Accommodates regional names and cultural knowledge
6. **Confidence Scoring**: Allows for data quality assessment and ranking
7. **Extensible**: Easy to add new trait categories and relationship types

## Migration Strategy

1. **Phase 1**: Create new schema alongside existing tables
2. **Phase 2**: Migrate existing data with confidence scores
3. **Phase 3**: Generate embeddings for all plant descriptions
4. **Phase 4**: Build search APIs and GPT integration layer
5. **Phase 5**: Deprecate old schema once new system is validated

This enhanced schema provides the foundation for sophisticated plant search capabilities while maintaining the practical focus that makes PermieBro valuable for permaculture practitioners. 