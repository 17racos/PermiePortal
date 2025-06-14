# Semantic Tags System Documentation

## Overview

The semantic tags system provides enhanced search capabilities for the PermieBro plant database. It allows users to quickly filter plants by characteristics like "edible", "drought tolerant", "aromatic", etc.

## Architecture

### Models
- **SemanticTag**: Defines available semantic tags (e.g., 'edible', 'medicinal')
- **PlantSemanticTag**: Join table linking plants to semantic tags with confidence scores
- **EnhancedPlant**: Extended plant model with semantic tag associations

### Key Components
- **EnhancedPlantSearchService**: Handles semantic tag searches
- **Auto-tagging System**: Automatically assigns tags based on plant data
- **Quick Filter UI**: Provides one-click filtering by semantic tags

## Available Semantic Tags

### Primary Tags (Used in Quick Filters)
- `edible` - Plants with edible parts
- `medicinal` - Plants with medicinal properties
- `pollinator_friendly` - Plants that attract pollinators
- `drought_tolerant` - Plants that tolerate dry conditions
- `nitrogen_fixing` - Plants that fix nitrogen (legumes)
- `ground_cover` - Low-growing spreading plants
- `aromatic` - Plants with fragrant parts
- `container_suitable` - Plants suitable for container growing
- `cold_hardy` - Plants tolerant of cold temperatures

### Additional Tags
- `tropical` - Plants adapted to tropical climates
- `native` - Plants indigenous to local regions
- `invasive` - Plants with aggressive spreading tendencies
- `evergreen` - Plants that retain foliage year-round
- `deciduous` - Plants that lose leaves seasonally
- `self_seeding` - Plants that readily self-propagate
- `compact` - Plants with small, dense growth habit
- `spreading` - Plants that spread horizontally
- `spring_blooming` - Plants that flower in spring
- `summer_blooming` - Plants that flower in summer
- `fall_blooming` - Plants that flower in fall

## Maintenance Tasks

### Setup and Migration
```bash
# Full setup (includes semantic tagging)
rake enhanced_plants:full_setup

# Setup semantic tags only
rake enhanced_plants:auto_tag

# Reset and rebuild all semantic tag associations
rake enhanced_plants:reset_semantic_tags
```

### Monitoring and Validation
```bash
# Show statistics including semantic tag counts
rake enhanced_plants:stats

# Validate data integrity
rake enhanced_plants:validate

# Test search functionality
rake enhanced_plants:test_search
```

## Auto-Tagging Logic

### Manual Associations
The system includes predefined lists of plants for certain tags:

**Edible Plants:**
- Tomato, Carrot, Broccoli, Asparagus, Avocado
- Blueberry, Coconut Tree, Banana, Almond Tree, Bok Choy
- Apple, Orange, Lemon, Strawberry, Grape, Peach
- Lettuce, Spinach, Kale, Cabbage, Onion, Garlic

**Medicinal Plants:**
- Aloe, Chamomile, Calendula, Ashwagandha, Comfrey, Echinacea
- Ginseng, Turmeric, Ginger, Lavender, Peppermint, Sage

**Nitrogen Fixing Plants:**
- All plants in Fabaceae/Leguminosae families

**Ground Cover Plants:**
- Plants with names containing: Chickweed, Creeping, Moss, Ivy, Vinca, Ajuga

**Aromatic Plants:**
- Plants with names containing: mint, basil, rosemary, thyme, lavender, sage, oregano, cilantro, parsley, dill, fennel

### Algorithmic Tagging
The system also automatically tags plants based on their data:

- **Drought Tolerant**: Plants with drought_tolerance_score > 0.6
- **Pollinator Friendly**: Plants with descriptions mentioning pollinators, bees, butterflies, or flowers
- **Cold Hardy**: Plants with hardiness_zone_min ≤ 5
- **Tropical**: Plants with hardiness_zone_min ≥ 9
- **Container Suitable**: Plants with mature_height_max_cm ≤ 200

## Adding New Semantic Tags

### 1. Create the Semantic Tag
```ruby
SemanticTag.create!(
  name: 'new_tag_name',
  category: 'trait', # or 'environmental', 'use', etc.
  description: 'Description of what this tag represents'
)
```

### 2. Add Auto-Tagging Logic
Update the auto-tagging rake task in `lib/tasks/enhanced_plants.rake` to include logic for the new tag.

### 3. Add to Quick Filters (Optional)
If the tag should be available as a quick filter:

1. Update `app/controllers/plants_controller.rb` in the `quick_filter` method
2. Add a button to the plants index view
3. Update the search service if needed

### 4. Test the New Tag
```bash
# Run auto-tagging to apply the new tag
rake enhanced_plants:auto_tag

# Test search functionality
rake enhanced_plants:test_search
```

## Troubleshooting

### Quick Filters Not Working
1. Check that semantic tags exist: `SemanticTag.count`
2. Check that plant associations exist: `PlantSemanticTag.count`
3. Run auto-tagging: `rake enhanced_plants:auto_tag`
4. Check search service logs for errors

### Missing Plant Associations
1. Run reset and rebuild: `rake enhanced_plants:reset_semantic_tags`
2. Check plant data quality and completeness
3. Update auto-tagging logic if needed

### Performance Issues
1. Ensure database indexes are in place
2. Consider adding caching for frequently accessed tags
3. Monitor query performance in search service

## File Locations

- **Semantic Tags Seed**: `db/seeds/enhanced_semantic_tags.rb`
- **Auto-Tagging Tasks**: `lib/tasks/enhanced_plants.rake`
- **Search Service**: `app/services/enhanced_plant_search_service.rb`
- **Controller**: `app/controllers/plants_controller.rb`
- **Models**: `app/models/semantic_tag.rb`, `app/models/plant_semantic_tag.rb`

## Best Practices

1. **Confidence Scores**: Use appropriate confidence scores (0.7-0.9 for manual, 0.5-0.8 for auto)
2. **Source Tracking**: Always specify source ('manual', 'auto', 'user') for traceability
3. **Regular Validation**: Run validation tasks regularly to ensure data integrity
4. **Backup Before Changes**: Always backup before running reset operations
5. **Test After Updates**: Test search functionality after making changes

## Future Enhancements

- Machine learning-based auto-tagging
- User-contributed tags with moderation
- Hierarchical tag relationships
- Tag synonyms and aliases
- Confidence score-based ranking
- Regional tag variations 