# PermiePortal Schema Enhancement Recommendations

## 1. Advanced Tagging System

### Semantic Tags Table
```sql
CREATE TABLE semantic_tags (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  name VARCHAR(100) NOT NULL UNIQUE,
  category VARCHAR(50) NOT NULL, -- 'trait', 'use', 'habitat', 'season', 'maintenance'
  synonyms TEXT[], -- Alternative terms for NLP matching
  parent_tag_id UUID REFERENCES semantic_tags(id),
  weight DECIMAL(3,2) DEFAULT 1.0, -- Importance for search ranking
  created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE plant_semantic_tags (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  enhanced_plant_id UUID REFERENCES enhanced_plants(id),
  semantic_tag_id UUID REFERENCES semantic_tags(id),
  confidence_score DECIMAL(3,2) DEFAULT 1.0,
  source VARCHAR(50), -- 'manual', 'extracted', 'inferred'
  created_at TIMESTAMP DEFAULT NOW(),
  UNIQUE(enhanced_plant_id, semantic_tag_id)
);
```

### Hierarchical Tag Categories
```sql
-- Examples of semantic tag hierarchy
INSERT INTO semantic_tags (name, category, synonyms) VALUES
('drought_tolerant', 'trait', ARRAY['drought resistant', 'xerophytic', 'water wise']),
('pollinator_friendly', 'trait', ARRAY['bee friendly', 'attracts pollinators', 'nectar rich']),
('fast_growing', 'trait', ARRAY['rapid growth', 'quick establishment']),
('low_maintenance', 'trait', ARRAY['easy care', 'self sufficient']);
```

## 2. GPT-Optimized Data Structure

### Natural Language Query Mapping
```sql
CREATE TABLE query_patterns (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  pattern TEXT NOT NULL, -- "drought tolerant shrubs for zone {zone}"
  intent VARCHAR(50), -- 'search', 'recommend', 'compare'
  parameters JSONB, -- {"zone": "numeric", "plant_type": "enum"}
  tag_mappings JSONB, -- Maps to semantic_tags
  created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE plant_descriptions_nlp (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  enhanced_plant_id UUID REFERENCES enhanced_plants(id),
  description_type VARCHAR(50), -- 'summary', 'detailed', 'care_instructions'
  content TEXT NOT NULL,
  keywords TEXT[], -- Extracted keywords for matching
  embedding VECTOR(1536), -- For semantic similarity (if pgvector available)
  language VARCHAR(5) DEFAULT 'en',
  created_at TIMESTAMP DEFAULT NOW()
);
```

### Context-Aware Plant Data
```sql
CREATE TABLE plant_contexts (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  enhanced_plant_id UUID REFERENCES enhanced_plants(id),
  context_type VARCHAR(50), -- 'climate', 'garden_style', 'experience_level'
  context_value VARCHAR(100),
  suitability_score DECIMAL(3,2), -- 0.0 to 1.0
  notes TEXT,
  created_at TIMESTAMP DEFAULT NOW()
);
```

## 3. Advanced Search Optimization

### Full-Text Search Enhancement
```sql
-- Add tsvector columns for fast text search
ALTER TABLE enhanced_plants ADD COLUMN search_vector tsvector;
ALTER TABLE plant_descriptions_nlp ADD COLUMN search_vector tsvector;

-- Create indexes
CREATE INDEX idx_plants_search_vector ON enhanced_plants USING gin(search_vector);
CREATE INDEX idx_descriptions_search_vector ON plant_descriptions_nlp USING gin(search_vector);

-- Update triggers
CREATE OR REPLACE FUNCTION update_plant_search_vector() RETURNS trigger AS $$
BEGIN
  NEW.search_vector := 
    setweight(to_tsvector('english', COALESCE(NEW.common_name, '')), 'A') ||
    setweight(to_tsvector('english', COALESCE(NEW.scientific_name, '')), 'A') ||
    setweight(to_tsvector('english', COALESCE(NEW.family, '')), 'B') ||
    setweight(to_tsvector('english', COALESCE(NEW.description_detailed, '')), 'C');
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER update_plant_search_vector_trigger
  BEFORE INSERT OR UPDATE ON enhanced_plants
  FOR EACH ROW EXECUTE FUNCTION update_plant_search_vector();
```

### Composite Indexes for Multi-Parameter Queries
```sql
-- Zone and plant type combinations
CREATE INDEX idx_plants_zone_type ON enhanced_plants (plant_type) 
  INCLUDE (id) WHERE plant_type IS NOT NULL;

CREATE INDEX idx_env_requirements_zone_sun ON environmental_requirements 
  (zone_min, zone_max, sunlight_requirements);

-- Tag-based searching
CREATE INDEX idx_plant_tags_category ON plant_semantic_tags (semantic_tag_id) 
  INCLUDE (enhanced_plant_id, confidence_score);
```

## 4. Offline Access Optimization

### Data Synchronization Tables
```sql
CREATE TABLE sync_metadata (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  table_name VARCHAR(100) NOT NULL,
  last_sync TIMESTAMP DEFAULT NOW(),
  sync_version INTEGER DEFAULT 1,
  checksum VARCHAR(64), -- For data integrity
  record_count INTEGER DEFAULT 0
);

CREATE TABLE change_log (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  table_name VARCHAR(100) NOT NULL,
  record_id UUID NOT NULL,
  operation VARCHAR(10) NOT NULL, -- 'INSERT', 'UPDATE', 'DELETE'
  changed_at TIMESTAMP DEFAULT NOW(),
  sync_version INTEGER,
  data_snapshot JSONB -- For conflict resolution
);
```

### Materialized Views for Performance
```sql
-- Pre-computed plant summaries for offline use
CREATE MATERIALIZED VIEW plant_summaries AS
SELECT 
  ep.id,
  ep.common_name,
  ep.scientific_name,
  ep.plant_type,
  ep.life_cycle,
  er.zone_min,
  er.zone_max,
  er.sunlight_requirements,
  er.water_requirements,
  ARRAY_AGG(DISTINCT uc.name) as uses,
  ARRAY_AGG(DISTINCT st.name) as traits,
  COUNT(DISTINCT pr.plant_b_id) as companion_count
FROM enhanced_plants ep
LEFT JOIN environmental_requirements er ON ep.id = er.enhanced_plant_id
LEFT JOIN plant_uses pu ON ep.id = pu.enhanced_plant_id
LEFT JOIN use_categories uc ON pu.use_category_id = uc.id
LEFT JOIN plant_semantic_tags pst ON ep.id = pst.enhanced_plant_id
LEFT JOIN semantic_tags st ON pst.semantic_tag_id = st.id
LEFT JOIN plant_relationships pr ON ep.id = pr.plant_a_id
GROUP BY ep.id, ep.common_name, ep.scientific_name, ep.plant_type, 
         ep.life_cycle, er.zone_min, er.zone_max, er.sunlight_requirements, 
         er.water_requirements;

CREATE UNIQUE INDEX ON plant_summaries (id);
```

## 5. Scalability Enhancements

### Partitioning Strategy
```sql
-- Partition large tables by region or climate zone
CREATE TABLE plant_observations (
  id UUID DEFAULT gen_random_uuid(),
  enhanced_plant_id UUID REFERENCES enhanced_plants(id),
  user_id UUID,
  location POINT,
  climate_zone INTEGER,
  observation_date DATE,
  notes TEXT,
  photos TEXT[],
  PRIMARY KEY (id, climate_zone)
) PARTITION BY RANGE (climate_zone);

-- Create partitions for different climate zones
CREATE TABLE plant_observations_zones_1_3 PARTITION OF plant_observations
  FOR VALUES FROM (1) TO (4);
CREATE TABLE plant_observations_zones_4_6 PARTITION OF plant_observations
  FOR VALUES FROM (4) TO (7);
-- etc.
```

### Caching Strategy
```sql
CREATE TABLE search_cache (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  query_hash VARCHAR(64) UNIQUE NOT NULL,
  query_text TEXT NOT NULL,
  parameters JSONB,
  result_ids UUID[],
  result_count INTEGER,
  created_at TIMESTAMP DEFAULT NOW(),
  expires_at TIMESTAMP DEFAULT NOW() + INTERVAL '1 hour'
);

CREATE INDEX idx_search_cache_hash ON search_cache (query_hash);
CREATE INDEX idx_search_cache_expires ON search_cache (expires_at);
```

## 6. Data Quality and Validation

### Constraint and Validation Tables
```sql
CREATE TABLE data_validation_rules (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  table_name VARCHAR(100) NOT NULL,
  column_name VARCHAR(100) NOT NULL,
  rule_type VARCHAR(50), -- 'range', 'enum', 'pattern', 'relationship'
  rule_definition JSONB,
  error_message TEXT,
  severity VARCHAR(20) DEFAULT 'error', -- 'warning', 'error', 'critical'
  active BOOLEAN DEFAULT true
);

CREATE TABLE data_quality_issues (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  table_name VARCHAR(100) NOT NULL,
  record_id UUID NOT NULL,
  rule_id UUID REFERENCES data_validation_rules(id),
  issue_description TEXT,
  detected_at TIMESTAMP DEFAULT NOW(),
  resolved_at TIMESTAMP,
  resolution_notes TEXT
);
```

## 7. Performance Monitoring

### Query Performance Tracking
```sql
CREATE TABLE query_performance (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  query_type VARCHAR(50),
  query_text TEXT,
  execution_time_ms INTEGER,
  result_count INTEGER,
  user_id UUID,
  executed_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_query_perf_type_time ON query_performance (query_type, executed_at);
```

## Implementation Priority

1. **Phase 1**: Semantic tagging system and NLP descriptions
2. **Phase 2**: Full-text search optimization and caching
3. **Phase 3**: Offline sync capabilities and materialized views
4. **Phase 4**: Partitioning and advanced scalability features
5. **Phase 5**: Data quality monitoring and performance tracking

## Migration Strategy

```sql
-- Example migration for adding semantic tags
BEGIN;

-- Create new tables
-- (semantic_tags and plant_semantic_tags from above)

-- Migrate existing data
INSERT INTO semantic_tags (name, category, synonyms)
SELECT DISTINCT 
  unnest(string_to_array(lower(name), ' ')) as tag_name,
  'use' as category,
  ARRAY[]::text[] as synonyms
FROM use_categories
WHERE name IS NOT NULL;

-- Create plant-tag relationships from existing uses
INSERT INTO plant_semantic_tags (enhanced_plant_id, semantic_tag_id, confidence_score, source)
SELECT DISTINCT
  pu.enhanced_plant_id,
  st.id,
  0.8,
  'migrated'
FROM plant_uses pu
JOIN use_categories uc ON pu.use_category_id = uc.id
JOIN semantic_tags st ON lower(st.name) = lower(uc.name)
WHERE st.category = 'use';

COMMIT;
```

This enhanced schema provides:
- **Flexible semantic tagging** for GPT integration
- **Optimized search performance** with composite indexes
- **Offline capability** with sync tables and materialized views
- **Scalability** through partitioning and caching
- **Data quality** monitoring and validation
- **Performance tracking** for optimization

The design maintains backward compatibility while adding powerful new capabilities for natural language processing and advanced search functionality. lsof
