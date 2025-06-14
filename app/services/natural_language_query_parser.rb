# frozen_string_literal: true
class NaturalLanguageQueryParser
  ZONE_PATTERN = /zone\s*(\d+(?:-\d+)?)/i
  PLANT_TYPE_PATTERN = /(tree|shrub|herb|herbaceous|vine|ground\s*cover|grass)/i

  # Semantic tag patterns with synonyms
  TAG_PATTERNS = {
    drought_tolerant: /drought[_\s-]?(tolerant|resistant)|water[_\s-]?wise|xerophytic|dry[_\s-]?conditions/i,
    pollinator_friendly: /(pollinator[_\s-]?friendly|bee[_\s-]?friendly|attracts?\s+pollinators?|nectar[_\s-]?rich|butterfly[_\s-]?plant)/i,
    fast_growing: /(fast[_\s-]?growing|quick[_\s-]?growing|rapid[_\s-]?growth|vigorous)/i,
    low_maintenance: /(low[_\s-]?maintenance|easy[_\s-]?care|minimal[_\s-]?care|self[_\s-]?sufficient)/i,
    edible: /(edible|food|fruit|vegetable|culinary)/i,
    medicinal: /(medicinal|medicine|healing|therapeutic)/i,
    shade_tolerant: /(shade[_\s-]?tolerant|partial[_\s-]?shade|low[_\s-]?light)/i,
    full_sun: /(full[_\s-]?sun|sunny|bright[_\s-]?light|direct[_\s-]?sun)/i,
    nitrogen_fixing: /(nitrogen[_\s-]?fixing|fixes[_\s-]?nitrogen|legume|soil[_\s-]?improvement)/i,
    ground_cover: /(ground[_\s-]?cover|spreading|low[_\s-]?growing|carpet)/i,
    climbing: /(climbing|vine|climber|twining)/i,
    pest_resistant: /(pest[_\s-]?resistant|repels[_\s-]?pests|naturally[_\s-]?resistant)/i,
    disease_resistant: /(disease[_\s-]?resistant|disease[_\s-]?tolerant|hardy|robust)/i,
    wildlife_habitat: /(wildlife|bird[_\s-]?food|habitat|attracts[_\s-]?birds)/i,
    ornamental: /(ornamental|decorative|beautiful|landscape)/i,
    aromatic: /(aromatic|fragrant|scented|perfumed|sweet[_\s-]?smell)/i,
    evergreen: /(evergreen|year[_\s-]?round[_\s-]?foliage|persistent[_\s-]?leaves)/i,
    deciduous: /(deciduous|loses[_\s-]?leaves|seasonal[_\s-]?foliage)/i,
    container_suitable: /(container[_\s-]?suitable|pot[_\s-]?friendly|container[_\s-]?gardening|good[_\s-]?for[_\s-]?pots)/i,
    deer_resistant: /(deer[_\s-]?resistant|deer[_\s-]?proof|deer[_\s-]?avoid)/i,
    cold_hardy: /(cold[_\s-]?hardy|winter[_\s-]?hardy|frost[_\s-]?tolerant|freeze[_\s-]?resistant)/i,
    self_seeding: /(self[_\s-]?seeding|self[_\s-]?sowing|reseeds[_\s-]?itself|naturalizes)/i,
    invasive: /(invasive|aggressive[_\s-]?spreader|hard[_\s-]?to[_\s-]?control|weedy)/i,
    native: /(native|indigenous|native[_\s-]?species|naturally[_\s-]?occurring)/i,
    tropical: /(tropical|warm[_\s-]?climate|heat[_\s-]?loving|tropical[_\s-]?species)/i,
    compact: /(compact|dwarf|small[_\s-]?form|dense[_\s-]?growth)/i,
    spreading: /(spreading|wide[_\s-]?spreading|horizontal[_\s-]?growth|mat[_\s-]?forming)/i,
    spring_blooming: /(spring[_\s-]?blooming|spring[_\s-]?flowers|early[_\s-]?flowers)/i,
    summer_blooming: /(summer[_\s-]?blooming|summer[_\s-]?flowers|mid[_\s-]?season[_\s-]?blooms)/i,
    fall_blooming: /(fall[_\s-]?blooming|autumn[_\s-]?blooming|fall[_\s-]?flowers)/i
  }.freeze

  def initialize(query)
    @query = query.downcase
    @parsed_data = {}
  end

  def parse
    extract_zones
    extract_plant_types
    extract_semantic_tags
    extract_uses
    extract_keywords

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
      # Map common terms to database enum values
      type_mapping = {
        'herb' => 'herbaceous',
        'herbs' => 'herbaceous',
        'ground_cover' => 'herbaceous' # Most ground covers are herbaceous
      }
      @parsed_data[:plant_type] = type_mapping[type] || type
    end
  end

  def extract_semantic_tags
    matched_tags = []

    TAG_PATTERNS.each do |tag_name, pattern|
      if @query.match?(pattern)
        matched_tags << tag_name.to_s
      end
    end

    @parsed_data[:semantic_tags] = matched_tags unless matched_tags.empty?
  end

  def extract_uses
    uses = []
    uses << 'edible' if @query.match?(/edible|food|fruit|vegetable/i)
    uses << 'medicinal' if @query.match?(/medicinal|medicine|healing/i)
    uses << 'ornamental' if @query.match?(/ornamental|decorative|beautiful/i)
    @parsed_data[:uses] = uses unless uses.empty?
  end

  def extract_keywords
    # Remove semantic tag matches and common words to get remaining keywords
    cleaned_query = @query.dup

    TAG_PATTERNS.each do |tag_name, pattern|
      cleaned_query.gsub!(pattern, ' ')
    end

    # Remove zone and plant type patterns
    cleaned_query.gsub!(ZONE_PATTERN, ' ')
    cleaned_query.gsub!(PLANT_TYPE_PATTERN, ' ')

    # Remove common words
    stop_words = %w[for that with and or the a an in on at to from plants plant]
    words = cleaned_query.split(/\W+/).reject(&:blank?)
    meaningful_words = words - stop_words

    @parsed_data[:keywords] = meaningful_words.join(' ') unless meaningful_words.empty?
  end
end