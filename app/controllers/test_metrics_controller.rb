# frozen_string_literal: true
class TestMetricsController < ApplicationController
  def test_error
    # This will trigger our error tracking
    raise StandardError, 'Test error for Prometheus metrics'
  end

  def test_view
    # This will increment our content views counter
    track_content_view('test', 'metrics_test')
    render plain: 'Content view tracked!'
  end

  def test_search
    # This will test our search duration tracking
    result = track_search('test_search') do
      sleep(0.5) # Simulate some work
      'Search completed'
    end
    render plain: result
  end
end