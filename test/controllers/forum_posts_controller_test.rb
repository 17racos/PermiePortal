require "test_helper"

class ForumPostsControllerTest < ActionDispatch::IntegrationTest
  test "should get create" do
    get forum_posts_create_url
    assert_response :success
  end

  test "should get destroy" do
    get forum_posts_destroy_url
    assert_response :success
  end
end
