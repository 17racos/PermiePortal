class ForumPost < ApplicationRecord
  belongs_to :forum_thread
  belongs_to :user
end
