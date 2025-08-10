namespace :plant_combinations do
  desc "Refresh the common plant combinations materialized view"
  task refresh: :environment do
    puts "Refreshing common plant combinations materialized view..."
    
    start_time = Time.current
    ActiveRecord::Base.connection.execute("REFRESH MATERIALIZED VIEW CONCURRENTLY common_plant_combinations;")
    end_time = Time.current
    
    duration = end_time - start_time
    puts "Refresh completed in #{duration.round(2)} seconds"
    
    # Log refresh statistics
    stats = ActiveRecord::Base.connection.execute(<<-SQL).first
      SELECT 
        COUNT(*) as total_combinations,
        MAX(co_occurrence_count) as max_occurrences,
        AVG(co_occurrence_count) as avg_occurrences,
        MAX(last_updated) as last_refresh
      FROM common_plant_combinations;
    SQL
    
    puts "\nRefresh Statistics:"
    puts "Total combinations: #{stats['total_combinations']}"
    puts "Max occurrences: #{stats['max_occurrences']}"
    puts "Average occurrences: #{stats['avg_occurrences'].round(2)}"
    puts "Last refresh: #{stats['last_refresh']}"
  end

  desc "Analyze plant combination patterns"
  task analyze: :environment do
    puts "Analyzing plant combination patterns..."
    
    # Get top combinations
    top_combinations = ActiveRecord::Base.connection.execute(<<-SQL)
      SELECT 
        plant1,
        plant2,
        co_occurrence_count
      FROM common_plant_combinations
      ORDER BY co_occurrence_count DESC
      LIMIT 10;
    SQL
    
    puts "\nTop 10 Plant Combinations:"
    top_combinations.each do |combo|
      puts "#{combo['plant1']} + #{combo['plant2']} (#{combo['co_occurrence_count']} occurrences)"
    end
    
    # Get combination patterns by plant type
    patterns = ActiveRecord::Base.connection.execute(<<-SQL)
      WITH plant_types AS (
        SELECT 
          p.common_name,
          pt.name as type
        FROM enhanced_plants p
        JOIN plant_traits pt ON pt.id = ANY(p.trait_ids)
      )
      SELECT 
        t1.type as type1,
        t2.type as type2,
        COUNT(*) as combination_count
      FROM common_plant_combinations cpc
      JOIN plant_types t1 ON t1.common_name = cpc.plant1
      JOIN plant_types t2 ON t2.common_name = cpc.plant2
      GROUP BY t1.type, t2.type
      ORDER BY combination_count DESC
      LIMIT 10;
    SQL
    
    puts "\nTop Plant Type Combinations:"
    patterns.each do |pattern|
      puts "#{pattern['type1']} + #{pattern['type2']} (#{pattern['combination_count']} combinations)"
    end
  end
end 