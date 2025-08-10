# frozen_string_literal: true

require 'test_helper'

class PermieGptServiceTest < ActiveSupport::TestCase
  setup do
    @service = PermieGptService.new
  end

  test "processes permaculture query and identifies knowledge gaps" do
    skip "Ollama not available" unless @service.available?

    result = @service.process_permaculture_query(
      "How do I integrate passionflower and basil in a Florida microclimate?",
      context: {
        location: "Florida",
        zone: "9b",
        soil: "Sandy loam",
        experience_level: "Intermediate",
        goals: ["Medicinal garden", "Pollinator habitat"]
      }
    )

    assert result[:success]
    assert result[:response].present?
    assert result[:knowledge_gaps].is_a?(Array)
    assert result[:plant_stubs].is_a?(Array)
  end

  test "handles unavailable Ollama gracefully" do
    service = PermieGptService.new("http://invalid-url:11434")
    result = service.process_permaculture_query("Test query")
    
    assert_not result[:success]
    assert result[:fallback_response].present?
  end
end 