class GuildMember < ApplicationRecord
  belongs_to :plant_guild
  belongs_to :enhanced_plant

  validates :enhanced_plant_id, uniqueness: { scope: :plant_guild_id }
  validates :role, presence: true

  enum role: {
    primary: 'primary',
    support: 'support',
    ground_cover: 'ground_cover',
    nitrogen_fixer: 'nitrogen_fixer',
    pest_deterrent: 'pest_deterrent',
    pollinator_attractant: 'pollinator_attractant',
    windbreak: 'windbreak',
    nurse_plant: 'nurse_plant'
  }

  scope :by_role, ->(role) { where(role: role) }
  scope :essential, -> { where(is_essential: true) }
  scope :optional, -> { where(is_essential: false) }

  def role_description
    case role
    when 'primary'
      'Main productive plant in the guild'
    when 'support'
      'Provides support services to other plants'
    when 'ground_cover'
      'Covers and protects soil'
    when 'nitrogen_fixer'
      'Fixes nitrogen for other plants'
    when 'pest_deterrent'
      'Repels harmful pests'
    when 'pollinator_attractant'
      'Attracts beneficial pollinators'
    when 'windbreak'
      'Provides wind protection'
    when 'nurse_plant'
      'Protects and nurtures other plants'
    else
      'Guild member'
    end
  end

  def planting_priority
    case role
    when 'primary', 'windbreak'
      1 # Plant first
    when 'nitrogen_fixer', 'nurse_plant'
      2 # Plant early
    when 'support', 'pest_deterrent'
      3 # Plant mid-sequence
    when 'ground_cover', 'pollinator_attractant'
      4 # Plant last
    else
      3 # Default priority
    end
  end

  def spacing_requirements
    # Return recommended spacing from other plants in meters
    plant = enhanced_plant
    
    base_spacing = if plant.mature_width_max_cm
                     plant.mature_width_max_cm / 100.0 / 2 # Half the mature width
                   else
                     case plant.plant_type
                     when 'tree'
                       3.0
                     when 'shrub'
                       1.5
                     when 'herbaceous'
                       0.5
                     when 'vine'
                       1.0
                     else
                       1.0
                     end
                   end
    
    # Adjust based on role
    case role
    when 'ground_cover'
      base_spacing * 0.5 # Closer spacing for coverage
    when 'windbreak'
      base_spacing * 0.7 # Closer for wind protection
    else
      base_spacing
    end
  end

  def contribution_score
    # Calculate how much this plant contributes to guild success
    score = 0.5 # Base score
    
    # Essential plants get higher score
    score += 0.3 if is_essential?
    
    # Primary plants get higher score
    score += 0.2 if primary?
    
    # Adjust based on plant's uses that benefit the guild
    beneficial_uses = enhanced_plant.plant_uses.joins(:use_category)
                                   .where(use_categories: { 
                                     name: ['nitrogen_fixation', 'pest_control', 'pollinator_attractant', 'soil_improvement']
                                   })
                                   .count
    
    score += beneficial_uses * 0.1
    
    [score, 1.0].min # Cap at 1.0
  end
end 