# Semantic Tagging System Implementation Guide

## Overview
This guide provides step-by-step implementation of a sophisticated tagging system that enables natural language queries like "drought-tolerant shrubs for zone 8 that attract pollinators."

## 1. Database Migration for Semantic Tags

### Create Migration File
```ruby
# db/migrate/20250116000000_create_semantic_tagging_system.rb
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
      t.uuid :enhanced_plant_id, null: false
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
```

## 2. Model Implementation

### SemanticTag Model
```ruby
# app/models/semantic_tag.rb
class SemanticTag < ApplicationRecord
  has_many :plant_semantic_tags, dependent: :destroy
  has_many :enhanced_plants, through: :plant_semantic_tags
  belongs_to :parent_tag, class_name: 'SemanticTag', optional: true
  has_many :child_tags, class_name: 'SemanticTag', foreign_key: 'parent_tag_id'
  
  validates :name, presence: true, uniqueness: true, length: { maximum: 100 }
  validates :category, presence: true, inclusion: { 
    in: %w[trait use habitat season maintenance growth_habit resistance] 
  }
  validates :weight, numericality: { in: 0.0..1.0 }
  
  scope :by_category, ->(category) { where(category: category) }
  scope :root_tags, -> { where(parent_tag_id: nil) }
  scope :with_synonyms, ->(term) { 
    where("name ILIKE ? OR ? = ANY(synonyms)", "%#{term}%", term.downcase) 
  }
  
  # Find tags by natural language terms
  def self.find_by_natural_language(terms)
    terms = Array(terms).map(&:downcase)
    
    where(
      terms.map { |term|
        "(name ILIKE '%#{sanitize_sql_like(term)}%' OR '#{sanitize_sql_like(term)}' = ANY(synonyms))"
      }.join(' OR ')
    )
  end
  
  # Get all descendants including self
  def descendants
    return [self] if child_tags.empty?
    [self] + child_tags.flat_map(&:descendants)
  end
  
  # Get semantic similarity score with another tag
  def similarity_score(other_tag)
    return 1.0 if self == other_tag
    return 0.8 if parent_tag == other_tag.parent_tag && parent_tag.present?
    return 0.6 if category == other_tag.category
    0.0
  end
end
```

### PlantSemanticTag Model
```ruby
# app/models/plant_semantic_tag.rb
class PlantSemanticTag < ApplicationRecord
  belongs_to :enhanced_plant
  belongs_to :semantic_tag
  
  validates :confidence_score, numericality: { in: 0.0..1.0 }
  validates :source, inclusion: { in: %w[manual extracted inferred user_generated] }
  validates :enhanced_plant_id, uniqueness: { scope: :semantic_tag_id }
  
  scope :high_confidence, -> { where('confidence_score >= ?', 0.7) }
  scope :by_source, ->(source) { where(source: source) }
  
  # Bulk assign tags to plants
  def self.bulk_assign(plant_ids, tag_ids, options = {})
    confidence = options[:confidence] || 0.8
    source = options[:source] || 'bulk_assigned'
    
    records = plant_ids.product(tag_ids).map do |plant_id, tag_id|
      {
        enhanced_plant_id: plant_id,
        semantic_tag_id: tag_id,
        confidence_score: confidence,
        source: source,
        created_at: Time.current,
        updated_at: Time.current
      }
    end
    
    insert_all(records, unique_by: [:enhanced_plant_id, :semantic_tag_id])
  end
end
```

### Enhanced Plant Model Updates
```ruby
# Add to app/models/enhanced_plant.rb
class EnhancedPlant < ApplicationRecord
  # ... existing associations ...
  
  has_many :plant_semantic_tags, dependent: :destroy
  has_many :semantic_tags, through: :plant_semantic_tags
  
  # Tag-based scopes
  scope :with_tags, ->(tag_names) {
    joins(:semantic_tags)
      .where(semantic_tags: { name: tag_names })
      .distinct
  }
  
  scope :with_tag_categories, ->(categories) {
    joins(:semantic_tags)
      .where(semantic_tags: { category: categories })
      .distinct
  }
  
  # Get plants with similar tags
  def similar_plants(limit: 10)
    tag_ids = semantic_tags.pluck(:id)
    return EnhancedPlant.none if tag_ids.empty?
    
    EnhancedPlant
      .joins(:plant_semantic_tags)
      .where(plant_semantic_tags: { semantic_tag_id: tag_ids })
      .where.not(id: id)
      .group('enhanced_plants.id')
      .order('COUNT(plant_semantic_tags.id) DESC')
      .limit(limit)
  end
  
  # Add tags with confidence scoring
  def add_semantic_tag(tag_name, confidence: 1.0, source: 'manual')
    tag = SemanticTag.find_or_create_by(name: tag_name.downcase) do |t|
      t.category = 'trait' # default category
    end
    
    plant_semantic_tags.find_or_create_by(semantic_tag: tag) do |pst|
      pst.confidence_score = confidence
      pst.source = source
    end
  end
  
  # Get tags by category
  def tags_by_category
    semantic_tags.group_by(&:category)
  end
end
```

## 3. Natural Language Query Processing

### Query Parser Service
```ruby
# app/services/natural_language_query_parser.rb
class NaturalLanguageQueryParser
  ZONE_PATTERN = /zone\s*(\d+(?:-\d+)?)/i
  PLANT_TYPE_PATTERN = /(tree|shrub|herb|vine|ground\s*cover|grass)/i
  TRAIT_PATTERNS = {
    drought: /drought[_\s-]?(tolerant|resistant)/i,
    pollinator: /(pollinator[_\s-]?friendly|bee[_\s-]?friendly|attracts?\s+pollinators?)/i,
    fast_growing: /(fast[_\s-]?growing|quick[_\s-]?growing|rapid[_\s-]?growth)/i,
    low_maintenance: /(low[_\s-]?maintenance|easy[_\s-]?care)/i,
    edible: /(edible|food|fruit|vegetable)/i,
    medicinal: /(medicinal|medicine|healing)/i,
    shade_tolerant: /(shade[_\s-]?tolerant|partial[_\s-]?shade)/i,
    full_sun: /(full[_\s-]?sun|sunny)/i
  }
  
  def initialize(query)
    @query = query.downcase
    @parsed_data = {}
  end
  
  def parse
    extract_zones
    extract_plant_types
    extract_traits
    extract_uses
    
    @parsed_data
  end
  
  private
  
  def extract_zones
    if match = @query.match(ZONE_PATTERN)
      zone_str = match[1]
      if zone_str.include?('-')
        min_zone, max_zone = zone_str.split('-').map(&:to_i)
        @parsed_data[:zone_range] = (min_zone..max_zone)
      else
        zone = zone_str.to_i
        @parsed_data[:zone_range] = (zone..zone)
      end
    end
  end
  
  def extract_plant_types
    if match = @query.match(PLANT_TYPE_PATTERN)
      type = match[1].gsub(/\s+/, '_')
      @parsed_data[:plant_type] = type
    end
  end
  
  def extract_traits
    traits = []
    TRAIT_PATTERNS.each do |trait_name, pattern|
      traits << trait_name.to_s if @query.match?(pattern)
    end
    @parsed_data[:traits] = traits unless traits.empty?
  end
  
  def extract_uses
    uses = []
    uses << 'edible' if @query.match?(/edible|food|fruit|vegetable/i)
    uses << 'medicinal' if @query.match?(/medicinal|medicine|healing/i)
    uses << 'ornamental' if @query.match?(/ornamental|decorative|beautiful/i)
    @parsed_data[:uses] = uses unless uses.empty?
  end
end
```

### Enhanced Search Service with NLP
```ruby
# app/services/enhanced_plant_search_service.rb (updated)
class EnhancedPlantSearchService
  # ... existing code ...
  
  def natural_language_search(query, options = {})
    parser = NaturalLanguageQueryParser.new(query)
    parsed = parser.parse
    
    # Convert parsed data to search parameters
    search_params = {
      query: extract_keywords(query),
      zone_range: parsed[:zone_range],
      plant_type: parsed[:plant_type],
      traits: parsed[:traits],
      uses: parsed[:uses]
    }
    
    # Use existing search with parsed parameters
    search(search_params[:query], search_params.except(:query))
  end
  
  private
  
  def extract_keywords(query)
    # Remove common words and extract meaningful terms
    stop_words = %w[for that with and or the a an in on at to from]
    words = query.downcase.split(/\W+/)
    meaningful_words = words - stop_words
    meaningful_words.join(' ')
  end
  
  def search_by_semantic_tags(tag_names, options = {})
    return EnhancedPlant.none if tag_names.blank?
    
    # Find tags by name or synonyms
    tags = SemanticTag.find_by_natural_language(tag_names)
    return EnhancedPlant.none if tags.empty?
    
    # Include descendant tags for hierarchical search
    all_tag_ids = tags.flat_map(&:descendants).map(&:id).uniq
    
    plants = EnhancedPlant
      .joins(:plant_semantic_tags)
      .where(plant_semantic_tags: { semantic_tag_id: all_tag_ids })
      .where('plant_semantic_tags.confidence_score >= ?', options[:min_confidence] || 0.5)
      .group('enhanced_plants.id')
      .order('AVG(plant_semantic_tags.confidence_score) DESC')
    
    apply_additional_filters(plants, options)
  end
end
```

## 4. Seed Data for Common Tags

### Create Seed File
```ruby
# db/seeds/semantic_tags.rb
def create_semantic_tags
  # Trait categories
  drought_tolerance = SemanticTag.create!(
    name: 'drought_tolerant',
    category: 'trait',
    synonyms: ['drought resistant', 'xerophytic', 'water wise', 'low water'],
    description: 'Plants that can survive with minimal water'
  )
  
  pollinator_friendly = SemanticTag.create!(
    name: 'pollinator_friendly',
    category: 'trait',
    synonyms: ['bee friendly', 'attracts pollinators', 'nectar rich', 'butterfly plant'],
    description: 'Plants that attract and support pollinators'
  )
  
  fast_growing = SemanticTag.create!(
    name: 'fast_growing',
    category: 'growth_habit',
    synonyms: ['rapid growth', 'quick establishment', 'vigorous'],
    description: 'Plants that establish and grow quickly'
  )
  
  # Use categories
  edible_tag = SemanticTag.create!(
    name: 'edible',
    category: 'use',
    synonyms: ['food', 'culinary', 'edible parts'],
    description: 'Plants with edible parts'
  )
  
  # Create subcategories
  SemanticTag.create!(
    name: 'edible_fruit',
    category: 'use',
    parent_tag: edible_tag,
    synonyms: ['fruit', 'berry', 'fruiting'],
    description: 'Plants with edible fruits'
  )
  
  SemanticTag.create!(
    name: 'edible_leaves',
    category: 'use',
    parent_tag: edible_tag,
    synonyms: ['leafy greens', 'salad', 'herbs'],
    description: 'Plants with edible leaves'
  )
  
  # Resistance traits
  pest_resistant = SemanticTag.create!(
    name: 'pest_resistant',
    category: 'resistance',
    synonyms: ['pest deterrent', 'naturally resistant'],
    description: 'Plants that naturally resist common pests'
  )
  
  disease_resistant = SemanticTag.create!(
    name: 'disease_resistant',
    category: 'resistance',
    synonyms: ['disease tolerant', 'hardy'],
    description: 'Plants resistant to common diseases'
  )
  
  puts "Created #{SemanticTag.count} semantic tags"
end

# Run in seeds.rb
create_semantic_tags if SemanticTag.count == 0
```

## 5. Auto-Tagging Service

### Automatic Tag Assignment
```ruby
# app/services/auto_tagging_service.rb
class AutoTaggingService
  def self.tag_all_plants
    EnhancedPlant.find_each do |plant|
      new(plant).assign_tags
    end
  end
  
  def initialize(plant)
    @plant = plant
  end
  
  def assign_tags
    assign_trait_tags
    assign_use_tags
    assign_growth_habit_tags
    assign_environmental_tags
  end
  
  private
  
  def assign_trait_tags
    # Extract from existing plant uses
    @plant.plant_uses.includes(:use_category).each do |plant_use|
      use_name = plant_use.use_category.name.downcase
      
      # Map use categories to semantic tags
      tag_mappings = {
        'drought tolerant' => 'drought_tolerant',
        'pollinator plant' => 'pollinator_friendly',
        'fast growing' => 'fast_growing',
        'low maintenance' => 'low_maintenance'
      }
      
      if tag_name = tag_mappings[use_name]
        assign_tag(tag_name, confidence: 0.8, source: 'extracted')
      end
    end
    
    # Extract from descriptions
    extract_from_description
  end
  
  def assign_use_tags
    @plant.plant_uses.includes(:use_category).each do |plant_use|
      use_name = plant_use.use_category.name.downcase
      
      case use_name
      when /edible|food|fruit|vegetable/
        assign_tag('edible', confidence: 0.9, source: 'extracted')
      when /medicinal|medicine|healing/
        assign_tag('medicinal', confidence: 0.9, source: 'extracted')
      when /ornamental|decorative/
        assign_tag('ornamental', confidence: 0.9, source: 'extracted')
      end
    end
  end
  
  def assign_growth_habit_tags
    case @plant.plant_type
    when 'tree'
      assign_tag('woody', confidence: 1.0, source: 'inferred')
    when 'shrub'
      assign_tag('woody', confidence: 1.0, source: 'inferred')
      assign_tag('compact', confidence: 0.7, source: 'inferred')
    when 'ground_cover'
      assign_tag('low_growing', confidence: 1.0, source: 'inferred')
      assign_tag('spreading', confidence: 0.8, source: 'inferred')
    end
  end
  
  def assign_environmental_tags
    return unless @plant.environmental_requirements
    
    env = @plant.environmental_requirements
    
    # Water requirements
    case env.water_requirements
    when 'low'
      assign_tag('drought_tolerant', confidence: 0.8, source: 'inferred')
    when 'high'
      assign_tag('water_loving', confidence: 0.8, source: 'inferred')
    end
    
    # Sunlight requirements
    case env.sunlight_requirements
    when 'full_sun'
      assign_tag('full_sun', confidence: 1.0, source: 'inferred')
    when 'partial_shade', 'shade'
      assign_tag('shade_tolerant', confidence: 0.9, source: 'inferred')
    end
  end
  
  def extract_from_description
    return unless @plant.description_detailed
    
    description = @plant.description_detailed.downcase
    
    # Pattern matching for traits
    patterns = {
      'drought_tolerant' => /drought[_\s-]?(tolerant|resistant)|water[_\s-]?wise|xerophytic/,
      'pollinator_friendly' => /pollinator|bee[_\s-]?friendly|nectar|butterfly/,
      'fast_growing' => /fast[_\s-]?growing|rapid[_\s-]?growth|vigorous/,
      'invasive' => /invasive|aggressive|spreads?\s+rapidly/,
      'fragrant' => /fragrant|aromatic|scented/
    }
    
    patterns.each do |tag_name, pattern|
      if description.match?(pattern)
        assign_tag(tag_name, confidence: 0.7, source: 'extracted')
      end
    end
  end
  
  def assign_tag(tag_name, confidence:, source:)
    tag = SemanticTag.find_by(name: tag_name)
    return unless tag
    
    @plant.plant_semantic_tags.find_or_create_by(semantic_tag: tag) do |pst|
      pst.confidence_score = confidence
      pst.source = source
    end
  end
end
```

## 6. Usage Examples

### Controller Integration
```ruby
# app/controllers/plants_controller.rb (updated)
def index
  if params[:nl_query].present?
    # Natural language search
    @plants = EnhancedPlantSearchService.new.natural_language_search(
      params[:nl_query], 
      limit: 50
    )
  else
    # Regular search
    @plants = EnhancedPlantSearchService.new.search(
      params[:query], 
      search_options
    )
  end
  
  # ... rest of method
end

private

def search_options
  {
    traits: params[:traits],
    uses: params[:uses],
    zone_range: parse_zone_range(params[:zones]),
    plant_type: params[:plant_type],
    limit: params[:limit] || 50
  }
end
```

### API Endpoint for Natural Language Queries
```ruby
# config/routes.rb
namespace :api do
  namespace :v1 do
    resources :plants do
      collection do
        get :natural_search
      end
    end
  end
end

# app/controllers/api/v1/plants_controller.rb
class Api::V1::PlantsController < ApplicationController
  def natural_search
    query = params[:q] || params[:query]
    
    if query.blank?
      render json: { error: 'Query parameter required' }, status: 400
      return
    end
    
    plants = EnhancedPlantSearchService.new.natural_language_search(query)
    
    render json: {
      query: query,
      count: plants.count,
      plants: plants.map { |plant| plant_summary(plant) }
    }
  end
  
  private
  
  def plant_summary(plant)
    {
      id: plant.id,
      common_name: plant.common_name,
      scientific_name: plant.scientific_name,
      plant_type: plant.plant_type,
      tags: plant.semantic_tags.pluck(:name),
      zone_range: plant.environmental_requirements&.zone_range,
      uses: plant.plant_uses.joins(:use_category).pluck('use_categories.name')
    }
  end
end
```

This implementation provides:
- **Hierarchical tagging** with parent-child relationships
- **Synonym support** for flexible matching
- **Confidence scoring** for tag reliability
- **Auto-tagging** from existing data
- **Natural language processing** for user queries
- **API integration** for external applications

The system can handle complex queries like:
- "drought tolerant shrubs for zone 8"
- "fast growing trees that attract pollinators"
- "edible ground cover for partial shade"
- "low maintenance plants for beginners" 