# Database Scaling and Maintenance Best Practices for PermiePortal

## Overview
This guide provides comprehensive strategies for maintaining and scaling your PermiePortal database as it grows from hundreds to millions of plants and users.

## 1. Performance Monitoring and Optimization

### Database Performance Monitoring
```ruby
# app/services/database_performance_monitor.rb
class DatabasePerformanceMonitor
  def self.setup_monitoring
    # Enable query logging for slow queries
    ActiveRecord::Base.logger = Logger.new(Rails.root.join('log', 'database_performance.log'))
    
    # Monitor query execution times
    ActiveSupport::Notifications.subscribe('sql.active_record') do |name, start, finish, id, payload|
      duration = (finish - start) * 1000 # Convert to milliseconds
      
      if duration > 100 # Log queries taking more than 100ms
        Rails.logger.warn "Slow Query (#{duration.round(2)}ms): #{payload[:sql]}"
        
        # Store performance data
        QueryPerformance.create!(
          query_type: extract_query_type(payload[:sql]),
          query_text: payload[:sql],
          execution_time_ms: duration.round(2),
          executed_at: Time.current
        )
      end
    end
  end
  
  def self.extract_query_type(sql)
    case sql.strip.upcase
    when /^SELECT/ then 'SELECT'
    when /^INSERT/ then 'INSERT'
    when /^UPDATE/ then 'UPDATE'
    when /^DELETE/ then 'DELETE'
    else 'OTHER'
    end
  end
  
  def self.generate_performance_report
    {
      slow_queries_count: QueryPerformance.where('execution_time_ms > ?', 100).count,
      average_query_time: QueryPerformance.average(:execution_time_ms),
      most_frequent_slow_queries: QueryPerformance
        .where('execution_time_ms > ?', 100)
        .group(:query_type)
        .count,
      database_size: database_size_info,
      index_usage: index_usage_stats
    }
  end
  
  private
  
  def self.database_size_info
    result = ActiveRecord::Base.connection.execute(<<~SQL)
      SELECT 
        schemaname,
        tablename,
        pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) as size,
        pg_total_relation_size(schemaname||'.'||tablename) as size_bytes
      FROM pg_tables 
      WHERE schemaname = 'public'
      ORDER BY pg_total_relation_size(schemaname||'.'||tablename) DESC;
    SQL
    
    result.to_a
  end
  
  def self.index_usage_stats
    result = ActiveRecord::Base.connection.execute(<<~SQL)
      SELECT 
        schemaname,
        tablename,
        indexname,
        idx_tup_read,
        idx_tup_fetch,
        idx_scan
      FROM pg_stat_user_indexes
      WHERE idx_scan < 10 -- Potentially unused indexes
      ORDER BY idx_scan ASC;
    SQL
    
    result.to_a
  end
end
```

### Automated Index Optimization
```ruby
# app/services/index_optimizer.rb
class IndexOptimizer
  def self.analyze_and_suggest_indexes
    suggestions = []
    
    # Analyze slow queries for missing indexes
    slow_queries = QueryPerformance.where('execution_time_ms > ?', 200)
                                  .group(:query_text)
                                  .having('COUNT(*) > ?', 5)
                                  .pluck(:query_text)
    
    slow_queries.each do |query|
      suggestions.concat(analyze_query_for_indexes(query))
    end
    
    # Check for unused indexes
    unused_indexes = find_unused_indexes
    suggestions.concat(unused_indexes.map { |idx| "Consider removing unused index: #{idx}" })
    
    suggestions
  end
  
  def self.analyze_query_for_indexes(query)
    suggestions = []
    
    # Simple pattern matching for common optimization opportunities
    if query.match?(/WHERE.*enhanced_plants\.plant_type.*AND.*zone_min/)
      suggestions << "Consider composite index on (plant_type, zone_min, zone_max)"
    end
    
    if query.match?(/JOIN.*semantic_tags.*WHERE.*category/)
      suggestions << "Consider index on semantic_tags.category"
    end
    
    if query.match?(/ORDER BY.*created_at/)
      suggestions << "Consider index on created_at for sorting"
    end
    
    suggestions
  end
  
  def self.find_unused_indexes
    result = ActiveRecord::Base.connection.execute(<<~SQL)
      SELECT indexname 
      FROM pg_stat_user_indexes 
      WHERE idx_scan = 0 
      AND schemaname = 'public'
      AND indexname NOT LIKE '%_pkey';
    SQL
    
    result.pluck('indexname')
  end
  
  def self.create_recommended_indexes
    # Composite indexes for common search patterns
    execute_if_not_exists(<<~SQL)
      CREATE INDEX CONCURRENTLY idx_enhanced_plants_search_composite 
      ON enhanced_plants (plant_type, life_cycle) 
      INCLUDE (common_name, scientific_name);
    SQL
    
    execute_if_not_exists(<<~SQL)
      CREATE INDEX CONCURRENTLY idx_environmental_requirements_zone_composite 
      ON environmental_requirements (zone_min, zone_max, sunlight_requirements);
    SQL
    
    execute_if_not_exists(<<~SQL)
      CREATE INDEX CONCURRENTLY idx_plant_semantic_tags_confidence 
      ON plant_semantic_tags (semantic_tag_id, confidence_score) 
      WHERE confidence_score >= 0.7;
    SQL
  end
  
  private
  
  def self.execute_if_not_exists(sql)
    index_name = sql.match(/idx_\w+/)[0]
    
    unless index_exists?(index_name)
      ActiveRecord::Base.connection.execute(sql)
      Rails.logger.info "Created index: #{index_name}"
    end
  rescue => e
    Rails.logger.error "Failed to create index #{index_name}: #{e.message}"
  end
  
  def self.index_exists?(index_name)
    result = ActiveRecord::Base.connection.execute(<<~SQL)
      SELECT 1 FROM pg_indexes WHERE indexname = '#{index_name}';
    SQL
    
    result.any?
  end
end
```

## 2. Data Archival and Cleanup Strategies

### Automated Data Cleanup
```ruby
# app/services/data_cleanup_service.rb
class DataCleanupService
  def self.perform_cleanup
    cleanup_old_search_cache
    cleanup_orphaned_records
    cleanup_low_confidence_tags
    vacuum_and_analyze
  end
  
  def self.cleanup_old_search_cache
    # Remove search cache entries older than 24 hours
    expired_count = SearchCache.where('expires_at < ?', Time.current).delete_all
    Rails.logger.info "Cleaned up #{expired_count} expired search cache entries"
  end
  
  def self.cleanup_orphaned_records
    # Remove plant semantic tags for deleted plants
    orphaned_tags = PlantSemanticTag.left_joins(:enhanced_plant)
                                   .where(enhanced_plants: { id: nil })
                                   .delete_all
    Rails.logger.info "Cleaned up #{orphaned_tags} orphaned semantic tags"
    
    # Remove plant uses for deleted plants
    orphaned_uses = PlantUse.left_joins(:enhanced_plant)
                           .where(enhanced_plants: { id: nil })
                           .delete_all
    Rails.logger.info "Cleaned up #{orphaned_uses} orphaned plant uses"
  end
  
  def self.cleanup_low_confidence_tags
    # Remove auto-generated tags with very low confidence
    low_confidence_count = PlantSemanticTag
      .where('confidence_score < ? AND source = ?', 0.3, 'inferred')
      .where('created_at < ?', 30.days.ago)
      .delete_all
    
    Rails.logger.info "Cleaned up #{low_confidence_count} low confidence tags"
  end
  
  def self.vacuum_and_analyze
    # Perform database maintenance
    ActiveRecord::Base.connection.execute('VACUUM ANALYZE;')
    Rails.logger.info "Performed VACUUM ANALYZE on database"
  end
end

# Schedule with cron or sidekiq-cron
# 0 2 * * * DataCleanupService.perform_cleanup
```

### Data Archival Strategy
```ruby
# app/services/data_archival_service.rb
class DataArchivalService
  ARCHIVE_THRESHOLD = 2.years
  
  def self.archive_old_data
    archive_old_query_logs
    archive_old_chat_logs
    archive_old_performance_data
  end
  
  def self.archive_old_query_logs
    old_logs = QueryPerformance.where('executed_at < ?', ARCHIVE_THRESHOLD.ago)
    
    if old_logs.any?
      # Export to JSON for long-term storage
      archive_data = old_logs.select(:query_type, :execution_time_ms, :executed_at)
                            .group_by(&:query_type)
                            .transform_values { |logs| 
                              {
                                count: logs.count,
                                avg_time: logs.sum(&:execution_time_ms) / logs.count,
                                date_range: [logs.map(&:executed_at).min, logs.map(&:executed_at).max]
                              }
                            }
      
      # Store in archive table or external storage
      DataArchive.create!(
        archive_type: 'query_performance',
        date_range: ARCHIVE_THRESHOLD.ago..Time.current,
        data: archive_data,
        record_count: old_logs.count
      )
      
      # Delete old records
      deleted_count = old_logs.delete_all
      Rails.logger.info "Archived and deleted #{deleted_count} old query performance records"
    end
  end
  
  def self.archive_old_chat_logs
    # Similar archival for chat logs
    old_chats = ChatLog.where('created_at < ?', ARCHIVE_THRESHOLD.ago)
    
    if old_chats.any?
      # Anonymize and aggregate data
      archive_data = {
        total_interactions: old_chats.count,
        unique_users: old_chats.distinct.count(:user_id),
        common_queries: old_chats.group(:query).limit(100).count,
        functions_used: old_chats.group(:function_used).count
      }
      
      DataArchive.create!(
        archive_type: 'chat_interactions',
        date_range: ARCHIVE_THRESHOLD.ago..Time.current,
        data: archive_data,
        record_count: old_chats.count
      )
      
      old_chats.delete_all
    end
  end
end
```

## 3. Horizontal Scaling Strategies

### Read Replica Configuration
```ruby
# config/database.yml
production:
  primary:
    <<: *default
    database: permieportal_production
    host: <%= ENV['PRIMARY_DB_HOST'] %>
    
  primary_replica:
    <<: *default
    database: permieportal_production
    host: <%= ENV['REPLICA_DB_HOST'] %>
    replica: true

# app/models/application_record.rb
class ApplicationRecord < ActiveRecord::Base
  self.abstract_class = true
  
  # Use read replica for heavy read operations
  connects_to database: { 
    writing: :primary, 
    reading: :primary_replica 
  }
end

# app/models/enhanced_plant.rb
class EnhancedPlant < ApplicationRecord
  # Force read operations to use replica
  scope :for_search, -> { connected_to(role: :reading) { all } }
  scope :for_display, -> { connected_to(role: :reading) { all } }
end
```

### Database Sharding Strategy
```ruby
# app/models/concerns/shardable.rb
module Shardable
  extend ActiveSupport::Concern
  
  included do
    # Shard based on plant family or geographic region
    def self.shard_key(plant_or_id)
      if plant_or_id.is_a?(String)
        # Use plant family for sharding
        plant = find(plant_or_id)
        shard_for_family(plant.family)
      else
        shard_for_family(plant_or_id.family)
      end
    end
    
    def self.shard_for_family(family)
      # Simple hash-based sharding
      family_hash = Digest::MD5.hexdigest(family.to_s).to_i(16)
      "shard_#{family_hash % 4}" # 4 shards
    end
  end
end

# app/models/enhanced_plant.rb
class EnhancedPlant < ApplicationRecord
  include Shardable
  
  # Override connection to use appropriate shard
  def self.connection
    shard = Thread.current[:current_shard] || 'shard_0'
    connection_handler.retrieve_connection("#{shard}_#{Rails.env}")
  end
end
```

### Caching Layers
```ruby
# app/services/multi_level_cache_service.rb
class MultiLevelCacheService
  # L1: Application memory cache (Redis)
  # L2: Database query cache
  # L3: CDN for static content
  
  def self.fetch_plant_data(plant_id, options = {})
    cache_key = "plant_data:#{plant_id}:#{options.hash}"
    
    # L1 Cache: Redis
    Rails.cache.fetch(cache_key, expires_in: 1.hour) do
      # L2 Cache: Database with includes
      plant = EnhancedPlant.includes(
        :environmental_requirements,
        :plant_uses,
        :plant_traits,
        :semantic_tags
      ).find(plant_id)
      
      serialize_plant_data(plant, options)
    end
  end
  
  def self.fetch_search_results(query, filters)
    cache_key = "search:#{Digest::MD5.hexdigest("#{query}:#{filters.to_json}")}"
    
    Rails.cache.fetch(cache_key, expires_in: 30.minutes) do
      service = EnhancedPlantSearchService.new
      results = service.search(query, filters)
      
      # Cache serialized results
      results.map { |plant| serialize_plant_summary(plant) }
    end
  end
  
  def self.warm_cache_for_popular_plants
    # Pre-load cache for most viewed plants
    popular_plant_ids = ViewLog.group(:plant_id)
                              .order('COUNT(*) DESC')
                              .limit(100)
                              .pluck(:plant_id)
    
    popular_plant_ids.each do |plant_id|
      fetch_plant_data(plant_id)
    end
  end
  
  private
  
  def self.serialize_plant_data(plant, options)
    {
      id: plant.id,
      common_name: plant.common_name,
      scientific_name: plant.scientific_name,
      plant_type: plant.plant_type,
      description: plant.description_detailed,
      environmental_requirements: plant.environmental_requirements&.as_json,
      uses: plant.plant_uses.includes(:use_category).map(&:as_json),
      traits: plant.plant_traits.includes(:trait_category).map(&:as_json),
      semantic_tags: plant.semantic_tags.pluck(:name),
      cached_at: Time.current
    }
  end
end
```

## 4. Backup and Disaster Recovery

### Automated Backup Strategy
```ruby
# app/services/backup_service.rb
class BackupService
  def self.perform_backup
    timestamp = Time.current.strftime('%Y%m%d_%H%M%S')
    
    # Full database backup
    full_backup_path = perform_full_backup(timestamp)
    
    # Incremental backup of recent changes
    incremental_backup_path = perform_incremental_backup(timestamp)
    
    # Upload to cloud storage
    upload_to_cloud_storage(full_backup_path, incremental_backup_path)
    
    # Cleanup old local backups
    cleanup_old_backups
    
    # Verify backup integrity
    verify_backup_integrity(full_backup_path)
  end
  
  def self.perform_full_backup(timestamp)
    backup_path = Rails.root.join('tmp', 'backups', "full_backup_#{timestamp}.sql")
    
    system(<<~CMD)
      pg_dump #{database_url} \
        --verbose \
        --clean \
        --no-owner \
        --no-privileges \
        --format=custom \
        --file=#{backup_path}
    CMD
    
    backup_path
  end
  
  def self.perform_incremental_backup(timestamp)
    # Backup only data changed in last 24 hours
    backup_path = Rails.root.join('tmp', 'backups', "incremental_#{timestamp}.sql")
    
    tables_with_timestamps = %w[
      enhanced_plants plant_semantic_tags plant_uses 
      plant_traits environmental_requirements
    ]
    
    where_clause = "WHERE updated_at >= '#{24.hours.ago.iso8601}'"
    
    tables_with_timestamps.each do |table|
      system(<<~CMD)
        pg_dump #{database_url} \
          --table=#{table} \
          --where="#{where_clause}" \
          --data-only \
          --format=custom \
          --file=#{backup_path}_#{table}
      CMD
    end
    
    backup_path
  end
  
  def self.upload_to_cloud_storage(full_backup, incremental_backup)
    # Upload to AWS S3, Google Cloud Storage, etc.
    # Implementation depends on your cloud provider
    
    s3_client = Aws::S3::Client.new
    bucket_name = ENV['BACKUP_BUCKET_NAME']
    
    [full_backup, incremental_backup].each do |backup_file|
      next unless File.exist?(backup_file)
      
      s3_client.put_object(
        bucket: bucket_name,
        key: "database_backups/#{File.basename(backup_file)}",
        body: File.read(backup_file),
        server_side_encryption: 'AES256'
      )
    end
  end
  
  def self.verify_backup_integrity(backup_path)
    # Test restore to temporary database
    test_db_name = "permieportal_backup_test_#{Time.current.to_i}"
    
    begin
      # Create test database
      system("createdb #{test_db_name}")
      
      # Restore backup
      system("pg_restore --dbname=#{test_db_name} #{backup_path}")
      
      # Verify data integrity
      test_connection = ActiveRecord::Base.establish_connection(
        adapter: 'postgresql',
        database: test_db_name,
        host: ENV['DB_HOST']
      )
      
      plant_count = test_connection.connection.execute(
        'SELECT COUNT(*) FROM enhanced_plants'
      ).first['count']
      
      if plant_count > 0
        Rails.logger.info "Backup verification successful: #{plant_count} plants restored"
      else
        Rails.logger.error "Backup verification failed: No plants found"
      end
      
    ensure
      # Cleanup test database
      system("dropdb #{test_db_name}")
    end
  end
  
  private
  
  def self.database_url
    config = Rails.application.config.database_configuration[Rails.env]
    "postgresql://#{config['username']}:#{config['password']}@#{config['host']}/#{config['database']}"
  end
  
  def self.cleanup_old_backups
    backup_dir = Rails.root.join('tmp', 'backups')
    old_backups = Dir.glob("#{backup_dir}/*").select do |file|
      File.mtime(file) < 7.days.ago
    end
    
    old_backups.each { |file| File.delete(file) }
  end
end
```

## 5. Monitoring and Alerting

### Health Check System
```ruby
# app/services/system_health_monitor.rb
class SystemHealthMonitor
  def self.check_system_health
    health_status = {
      database: check_database_health,
      cache: check_cache_health,
      search: check_search_functionality,
      storage: check_storage_health,
      overall: 'healthy'
    }
    
    # Determine overall health
    if health_status.values.any? { |status| status == 'critical' }
      health_status[:overall] = 'critical'
    elsif health_status.values.any? { |status| status == 'warning' }
      health_status[:overall] = 'warning'
    end
    
    # Send alerts if needed
    send_alerts_if_needed(health_status)
    
    health_status
  end
  
  def self.check_database_health
    begin
      # Check connection
      ActiveRecord::Base.connection.execute('SELECT 1')
      
      # Check query performance
      start_time = Time.current
      EnhancedPlant.limit(1).first
      query_time = (Time.current - start_time) * 1000
      
      if query_time > 1000
        'critical'
      elsif query_time > 500
        'warning'
      else
        'healthy'
      end
    rescue => e
      Rails.logger.error "Database health check failed: #{e.message}"
      'critical'
    end
  end
  
  def self.check_cache_health
    begin
      # Test cache read/write
      test_key = "health_check_#{Time.current.to_i}"
      Rails.cache.write(test_key, 'test_value', expires_in: 1.minute)
      
      if Rails.cache.read(test_key) == 'test_value'
        'healthy'
      else
        'warning'
      end
    rescue => e
      Rails.logger.error "Cache health check failed: #{e.message}"
      'critical'
    end
  end
  
  def self.check_search_functionality
    begin
      # Test search service
      service = EnhancedPlantSearchService.new
      results = service.search('test', limit: 1)
      
      'healthy'
    rescue => e
      Rails.logger.error "Search health check failed: #{e.message}"
      'warning'
    end
  end
  
  def self.check_storage_health
    begin
      # Check disk space
      disk_usage = `df -h /`.split("\n")[1].split[4].to_i
      
      if disk_usage > 90
        'critical'
      elsif disk_usage > 80
        'warning'
      else
        'healthy'
      end
    rescue => e
      Rails.logger.error "Storage health check failed: #{e.message}"
      'warning'
    end
  end
  
  def self.send_alerts_if_needed(health_status)
    if health_status[:overall] == 'critical'
      AlertService.send_critical_alert(health_status)
    elsif health_status[:overall] == 'warning'
      AlertService.send_warning_alert(health_status)
    end
  end
end
```

## 6. Deployment and Migration Strategies

### Zero-Downtime Migrations
```ruby
# app/services/safe_migration_service.rb
class SafeMigrationService
  def self.perform_safe_migration(migration_class)
    # Pre-migration checks
    check_migration_safety(migration_class)
    
    # Create migration lock
    acquire_migration_lock
    
    begin
      # Perform migration with monitoring
      monitor_migration_progress(migration_class)
      
      # Post-migration validation
      validate_migration_success(migration_class)
      
    ensure
      release_migration_lock
    end
  end
  
  def self.check_migration_safety(migration_class)
    # Check for potentially dangerous operations
    migration_content = File.read(migration_class.filename)
    
    dangerous_operations = [
      'DROP TABLE',
      'DROP COLUMN',
      'ALTER COLUMN.*TYPE',
      'ADD COLUMN.*NOT NULL'
    ]
    
    dangerous_operations.each do |operation|
      if migration_content.match?(/#{operation}/i)
        raise "Potentially dangerous migration operation detected: #{operation}"
      end
    end
  end
  
  def self.monitor_migration_progress(migration_class)
    start_time = Time.current
    
    # Run migration with timeout
    Timeout::timeout(30.minutes) do
      migration_class.migrate(:up)
    end
    
    duration = Time.current - start_time
    Rails.logger.info "Migration completed in #{duration} seconds"
    
  rescue Timeout::Error
    Rails.logger.error "Migration timed out after 30 minutes"
    raise
  end
  
  def self.validate_migration_success(migration_class)
    # Verify migration was applied correctly
    version = migration_class.version
    
    unless ActiveRecord::SchemaMigration.where(version: version).exists?
      raise "Migration #{version} was not recorded in schema_migrations"
    end
    
    # Run basic data integrity checks
    check_data_integrity
  end
  
  def self.check_data_integrity
    # Verify foreign key constraints
    orphaned_records = PlantSemanticTag.left_joins(:enhanced_plant)
                                      .where(enhanced_plants: { id: nil })
                                      .count
    
    if orphaned_records > 0
      Rails.logger.warn "Found #{orphaned_records} orphaned semantic tag records"
    end
    
    # Verify required data exists
    if EnhancedPlant.count == 0
      raise "Data integrity check failed: No plants found after migration"
    end
  end
end
```

## 7. Performance Optimization Checklist

### Regular Maintenance Tasks
```ruby
# lib/tasks/maintenance.rake
namespace :maintenance do
  desc "Perform regular database maintenance"
  task :daily => :environment do
    puts "Starting daily maintenance..."
    
    # Update statistics
    ActiveRecord::Base.connection.execute('ANALYZE;')
    
    # Cleanup expired cache
    DataCleanupService.cleanup_old_search_cache
    
    # Update materialized views
    ActiveRecord::Base.connection.execute('REFRESH MATERIALIZED VIEW CONCURRENTLY plant_summaries;')
    
    # Generate performance report
    report = DatabasePerformanceMonitor.generate_performance_report
    Rails.logger.info "Performance report: #{report}"
    
    puts "Daily maintenance completed."
  end
  
  desc "Perform weekly database optimization"
  task :weekly => :environment do
    puts "Starting weekly optimization..."
    
    # Full vacuum and analyze
    DataCleanupService.vacuum_and_analyze
    
    # Reindex if needed
    IndexOptimizer.create_recommended_indexes
    
    # Archive old data
    DataArchivalService.archive_old_data
    
    # Warm cache for popular content
    MultiLevelCacheService.warm_cache_for_popular_plants
    
    puts "Weekly optimization completed."
  end
  
  desc "Perform monthly backup and health check"
  task :monthly => :environment do
    puts "Starting monthly backup..."
    
    # Full system backup
    BackupService.perform_backup
    
    # Comprehensive health check
    health_status = SystemHealthMonitor.check_system_health
    puts "System health: #{health_status[:overall]}"
    
    # Generate usage statistics
    generate_usage_statistics
    
    puts "Monthly backup completed."
  end
end

def generate_usage_statistics
  stats = {
    total_plants: EnhancedPlant.count,
    total_searches: QueryPerformance.where('executed_at > ?', 1.month.ago).count,
    active_users: ChatLog.where('created_at > ?', 1.month.ago).distinct.count(:user_id),
    database_size: DatabasePerformanceMonitor.database_size_info.sum { |table| table['size_bytes'] }
  }
  
  Rails.logger.info "Monthly usage statistics: #{stats}"
end
```

This comprehensive guide provides:

- **Performance monitoring** with automated alerts
- **Data cleanup and archival** strategies
- **Horizontal scaling** with read replicas and sharding
- **Multi-level caching** for optimal performance
- **Backup and disaster recovery** procedures
- **Health monitoring** and alerting systems
- **Safe migration** practices for zero-downtime deployments
- **Regular maintenance** tasks and optimization

These practices will ensure your PermiePortal database remains performant, reliable, and scalable as it grows from hundreds to millions of plants and users. 