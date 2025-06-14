# frozen_string_literal: true
require 'test_helper'

class PlantsControllerTest < ActionDispatch::IntegrationTest
  test 'should get index' do
    get plants_url
    assert_response :success
  end
end
