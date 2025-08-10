# frozen_string_literal: true

# US Climate Zones Data
# This seed file adds detailed climate information for all US zones

module ClimateData
  US_CLIMATE_ZONES = {
    '4a' => {
      name: 'Northern Plains',
      description: 'Very cold winters with short, cool summers. Ideal for cold-hardy plants and short-season crops.',
      temperature_range: {
        summer: { min: 55, max: 80 },
        winter: { min: -30, max: -20 }
      },
      rainfall: {
        annual: 30,
        summer_months: 18,
        winter_months: 12
      },
      humidity: {
        summer: 65,
        winter: 55
      },
      growing_seasons: {
        spring: 'May to June',
        summer: 'July to August',
        fall: 'September',
        winter: 'October to April'
      },
      soil_types: [
        {
          name: 'Clay Loam',
          description: 'Heavy soil with good water retention. Common in the Northern Plains.',
          ph_range: '6.0-7.0',
          water_retention: 'High',
          nutrient_content: 'High',
          recommended_amendments: [
            'Compost',
            'Gypsum',
            'Organic matter',
            'Cover crops'
          ]
        }
      ],
      microclimate_considerations: [
        'Protection from cold winds',
        'Maximize sun exposure',
        'Frost protection',
        'Season extension techniques'
      ],
      common_challenges: [
        'Very short growing season',
        'Late spring frosts',
        'Early fall frosts',
        'Winter protection needed'
      ],
      recommended_practices: [
        'Cold frames and row covers',
        'Season extension techniques',
        'Winter mulching',
        'Hardy variety selection'
      ]
    },
    '4b' => {
      name: 'Upper Midwest',
      description: 'Cold winters with moderate summers. Good for cold-hardy plants and short-season crops.',
      temperature_range: {
        summer: { min: 60, max: 85 },
        winter: { min: -25, max: -15 }
      },
      rainfall: {
        annual: 35,
        summer_months: 20,
        winter_months: 15
      },
      humidity: {
        summer: 70,
        winter: 60
      },
      growing_seasons: {
        spring: 'April to June',
        summer: 'July to August',
        fall: 'September to October',
        winter: 'November to March'
      },
      soil_types: [
        {
          name: 'Loam',
          description: 'Rich, well-balanced soil common in the Midwest. Good water retention and drainage.',
          ph_range: '6.0-7.0',
          water_retention: 'Medium',
          nutrient_content: 'High',
          recommended_amendments: [
            'Compost',
            'Leaf mold',
            'Well-rotted manure',
            'Cover crops'
          ]
        }
      ],
      microclimate_considerations: [
        'Protection from cold winds',
        'Maximize sun exposure',
        'Frost protection',
        'Season extension techniques'
      ],
      common_challenges: [
        'Short growing season',
        'Late spring frosts',
        'Early fall frosts',
        'Winter protection needed'
      ],
      recommended_practices: [
        'Cold frames and row covers',
        'Season extension techniques',
        'Winter mulching',
        'Hardy variety selection'
      ]
    },
    '5a' => {
      name: 'Great Lakes',
      description: 'Cold winters with moderate summers. Good for a variety of cold-hardy plants.',
      temperature_range: {
        summer: { min: 65, max: 85 },
        winter: { min: -20, max: -10 }
      },
      rainfall: {
        annual: 40,
        summer_months: 22,
        winter_months: 18
      },
      humidity: {
        summer: 75,
        winter: 65
      },
      growing_seasons: {
        spring: 'April to June',
        summer: 'July to August',
        fall: 'September to October',
        winter: 'November to March'
      },
      soil_types: [
        {
          name: 'Silty Loam',
          description: 'Rich soil with good water retention. Common in the Great Lakes region.',
          ph_range: '6.0-7.0',
          water_retention: 'High',
          nutrient_content: 'High',
          recommended_amendments: [
            'Compost',
            'Leaf mold',
            'Well-rotted manure',
            'Cover crops'
          ]
        }
      ],
      microclimate_considerations: [
        'Lake effect moderation',
        'Wind protection',
        'Frost protection',
        'Season extension'
      ],
      common_challenges: [
        'Variable spring weather',
        'Late frosts',
        'High humidity',
        'Winter protection'
      ],
      recommended_practices: [
        'Wind breaks',
        'Frost protection',
        'Disease prevention',
        'Season extension'
      ]
    },
    '6a' => {
      name: 'Northeast',
      description: 'Cold winters with warm summers. Good for a wide variety of plants.',
      temperature_range: {
        summer: { min: 70, max: 90 },
        winter: { min: -15, max: -5 }
      },
      rainfall: {
        annual: 45,
        summer_months: 25,
        winter_months: 20
      },
      humidity: {
        summer: 75,
        winter: 65
      },
      growing_seasons: {
        spring: 'March to May',
        summer: 'June to August',
        fall: 'September to November',
        winter: 'December to February'
      },
      soil_types: [
        {
          name: 'Sandy Loam',
          description: 'Well-draining soil with good nutrient retention. Common in the Northeast.',
          ph_range: '5.5-6.5',
          water_retention: 'Medium',
          nutrient_content: 'Medium',
          recommended_amendments: [
            'Compost',
            'Leaf mold',
            'Pine bark',
            'Cover crops'
          ]
        }
      ],
      microclimate_considerations: [
        'Coastal influence',
        'Urban heat effects',
        'Wind protection',
        'Frost pockets'
      ],
      common_challenges: [
        'Variable spring weather',
        'High humidity',
        'Pest pressure',
        'Disease management'
      ],
      recommended_practices: [
        'Disease-resistant varieties',
        'Proper spacing',
        'Air circulation',
        'Season extension'
      ]
    },
    '7a' => {
      name: 'Mid-Atlantic',
      description: 'Moderate climate with distinct seasons. Good for a wide variety of plants.',
      temperature_range: {
        summer: { min: 70, max: 90 },
        winter: { min: 0, max: 10 }
      },
      rainfall: {
        annual: 45,
        summer_months: 25,
        winter_months: 20
      },
      humidity: {
        summer: 75,
        winter: 65
      },
      growing_seasons: {
        spring: 'March to May',
        summer: 'June to August',
        fall: 'September to November',
        winter: 'December to February'
      },
      soil_types: [
        {
          name: 'Clay Loam',
          description: 'Rich soil with good water retention. Common in the Mid-Atlantic region.',
          ph_range: '6.0-7.0',
          water_retention: 'High',
          nutrient_content: 'High',
          recommended_amendments: [
            'Compost',
            'Gypsum',
            'Organic matter',
            'Cover crops'
          ]
        }
      ],
      microclimate_considerations: [
        'Drainage management',
        'Wind protection',
        'Sun exposure optimization',
        'Heat island effects'
      ],
      common_challenges: [
        'Humidity-related diseases',
        'Soil compaction',
        'Urban heat effects',
        'Variable spring weather'
      ],
      recommended_practices: [
        'Proper drainage systems',
        'Disease-resistant varieties',
        'Seasonal crop rotation',
        'Mulching strategies'
      ]
    },
    '8a' => {
      name: 'Southeast',
      description: 'Hot, humid summers and mild winters. Excellent for long-season crops.',
      temperature_range: {
        summer: { min: 75, max: 95 },
        winter: { min: 10, max: 20 }
      },
      rainfall: {
        annual: 50,
        summer_months: 30,
        winter_months: 20
      },
      humidity: {
        summer: 80,
        winter: 70
      },
      growing_seasons: {
        spring: 'February to April',
        summer: 'May to September',
        fall: 'October to November',
        winter: 'December to January'
      },
      soil_types: [
        {
          name: 'Sandy Clay',
          description: 'Well-draining soil with good nutrient retention. Common in the Southeast.',
          ph_range: '5.5-6.5',
          water_retention: 'Medium',
          nutrient_content: 'Medium',
          recommended_amendments: [
            'Compost',
            'Pine bark',
            'Organic matter',
            'Mycorrhizal fungi'
          ]
        }
      ],
      microclimate_considerations: [
        'Afternoon shade',
        'Wind protection',
        'Drainage management',
        'Heat stress mitigation'
      ],
      common_challenges: [
        'High humidity',
        'Summer heat stress',
        'Pest pressure',
        'Disease management'
      ],
      recommended_practices: [
        'Shade structures',
        'Drip irrigation',
        'Pest monitoring',
        'Disease prevention'
      ]
    },
    '9b' => {
      name: 'Central Florida',
      description: 'Hot, humid summers with frequent afternoon thunderstorms. Mild, dry winters.',
      temperature_range: {
        summer: { min: 75, max: 95 },
        winter: { min: 45, max: 75 }
      },
      rainfall: {
        annual: 52,
        summer_months: 30,
        winter_months: 22
      },
      humidity: {
        summer: 85,
        winter: 65
      },
      growing_seasons: {
        spring: 'February to May',
        summer: 'June to September',
        fall: 'October to November',
        winter: 'December to January'
      },
      soil_types: [
        {
          name: 'Sandy Loam',
          description: 'Well-draining soil common in Central Florida. Requires regular organic matter amendments.',
          ph_range: '5.5-7.0',
          water_retention: 'Low to Medium',
          nutrient_content: 'Low',
          recommended_amendments: [
            'Compost',
            'Worm castings',
            'Biochar',
            'Mycorrhizal fungi'
          ]
        }
      ],
      microclimate_considerations: [
        'Protection from afternoon sun',
        'Wind protection for young plants',
        'Drainage management during rainy season',
        'Frost protection for sensitive plants'
      ],
      common_challenges: [
        'High humidity promoting fungal diseases',
        'Sandy soil requiring frequent fertilization',
        'Intense summer heat stress',
        'Hurricane season preparation'
      ],
      recommended_practices: [
        'Mulching to retain moisture',
        'Drip irrigation systems',
        'Companion planting for pest control',
        'Seasonal crop rotation'
      ]
    },
    '10a' => {
      name: 'Southern California',
      description: 'Mediterranean climate with mild, wet winters and hot, dry summers.',
      temperature_range: {
        summer: { min: 70, max: 90 },
        winter: { min: 30, max: 60 }
      },
      rainfall: {
        annual: 15,
        summer_months: 0,
        winter_months: 15
      },
      humidity: {
        summer: 50,
        winter: 60
      },
      growing_seasons: {
        spring: 'February to May',
        summer: 'June to September',
        fall: 'October to November',
        winter: 'December to January'
      },
      soil_types: [
        {
          name: 'Sandy Clay Loam',
          description: 'Well-draining soil with good nutrient retention. Common in Southern California.',
          ph_range: '6.0-7.5',
          water_retention: 'Medium',
          nutrient_content: 'Medium',
          recommended_amendments: [
            'Compost',
            'Worm castings',
            'Rock dust',
            'Cover crops'
          ]
        }
      ],
      microclimate_considerations: [
        'Water conservation',
        'Heat stress management',
        'Wind protection',
        'Frost protection in valleys'
      ],
      common_challenges: [
        'Drought conditions',
        'Summer heat stress',
        'Water restrictions',
        'Fire season preparation'
      ],
      recommended_practices: [
        'Drought-tolerant varieties',
        'Water-wise irrigation',
        'Mulching for moisture retention',
        'Fire-safe landscaping'
      ]
    },
    '11a' => {
      name: 'South Florida',
      description: 'Tropical climate with year-round growing season. High humidity and rainfall.',
      temperature_range: {
        summer: { min: 75, max: 95 },
        winter: { min: 50, max: 80 }
      },
      rainfall: {
        annual: 60,
        summer_months: 35,
        winter_months: 25
      },
      humidity: {
        summer: 85,
        winter: 70
      },
      growing_seasons: {
        spring: 'January to April',
        summer: 'May to September',
        fall: 'October to November',
        winter: 'December'
      },
      soil_types: [
        {
          name: 'Marl',
          description: 'Calcareous soil common in South Florida. High pH, requires acidification.',
          ph_range: '7.5-8.5',
          water_retention: 'Medium',
          nutrient_content: 'Low',
          recommended_amendments: [
            'Sulfur',
            'Compost',
            'Pine bark',
            'Mycorrhizal fungi'
          ]
        }
      ],
      microclimate_considerations: [
        'Salt spray protection',
        'Wind protection',
        'Drainage management',
        'Shade structures'
      ],
      common_challenges: [
        'High humidity',
        'Salt exposure',
        'Poor soil quality',
        'Hurricane season'
      ],
      recommended_practices: [
        'Salt-tolerant varieties',
        'Raised beds',
        'Wind breaks',
        'Seasonal planting'
      ]
    }
  }
end

# Add climate data to the database
ClimateData::US_CLIMATE_ZONES.each do |zone, data|
  ClimateZone.find_or_create_by!(zone: zone) do |cz|
    cz.name = data[:name]
    cz.description = data[:description]
    cz.temperature_range = data[:temperature_range]
    cz.rainfall = data[:rainfall]
    cz.humidity = data[:humidity]
    cz.growing_seasons = data[:growing_seasons]
    cz.soil_types = data[:soil_types]
    cz.microclimate_considerations = data[:microclimate_considerations]
    cz.common_challenges = data[:common_challenges]
    cz.recommended_practices = data[:recommended_practices]
  end
end

puts "✅ Added climate data for US zones 4a through 11a" 