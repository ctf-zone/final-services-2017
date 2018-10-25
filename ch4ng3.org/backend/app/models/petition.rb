class Petition < ApplicationRecord
  belongs_to :user

  has_many :signs
end
