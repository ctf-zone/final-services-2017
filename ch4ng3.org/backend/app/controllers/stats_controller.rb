class StatsController < ApplicationController
  skip_before_action :authorize_request, :only => [:stats]

  def stats
    json_response(
      {
        members: User.count(),
        signs: Sign.count(),
        petitions: Petition.count()
      }
    )
  end
end
