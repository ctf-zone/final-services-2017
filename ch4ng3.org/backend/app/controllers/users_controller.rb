class UsersController < ApplicationController
  skip_before_action :authorize_request, :only => [:create,:get]
  # POST /signup
  # return authenticated token upon signup
  def create
    return json_response({message: 'User already exists'}, :conflict) if User.exists?(:email => user_params['email'])
    user = User.create!(user_params)
    auth_token = AuthenticateUser.new(user.email, user.password).call
    response = { message: Message.account_created, auth_token: auth_token }
    json_response(response, :created)
  end

  def get
    user = User.find(params[:id])
    json_response({
      id: user.id,
      name: user.name,
      email: user.email
    })
  end

  def profile
    json_response({
      id: current_user.id,
      name: current_user.name,
      email: current_user.email,
      phone: current_user.phone
    })
  end


  private

  def user_params
    params.permit(
      :name,
      :email,
      :phone,
      :password,
      :password_confirmation
    )
  end
end
