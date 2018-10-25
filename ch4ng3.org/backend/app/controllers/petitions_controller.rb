class PetitionsController < ApplicationController
  skip_before_action :authorize_request, :only => [:list, :signers]

  def create
    petition = current_user.petitions.create!(petition_params)
    petition.signs.create!(petition_id: petition.id, user_id: current_user.id)
    json_response(petition, :created)
  end

  def list
    begin
      authorize_request
    rescue StandardError => e
    end

    user_id = current_user ? current_user.id : 0

    user_signs_subquery = Sign.
      where(:user_id => user_id).to_sql

    signs_count_subquery = Sign.
      select('COUNT(id) AS count').
      select(:petition_id).
      group(:petition_id).to_sql

    per_page = params[:per_page] ? params[:page] : 10
    page = params[:page] ? params[:page] : 1

    if params['order'] == nil
      order = 'petitions.id DESC'
    else
      order = 'signature_count DESC'
    end

    petitions = Petition.
      select('petitions.*').
      select('signs_count.count AS signature_count').
      select('users.name AS creator').
      select('user_signs.id IS NOT NULL as already_signed').
      joins(:user).
      left_outer_joins(:signs).
      joins("LEFT JOIN (#{user_signs_subquery}) AS user_signs ON user_signs.petition_id = petitions.id").
      joins("LEFT JOIN (#{signs_count_subquery}) AS signs_count ON signs_count.petition_id = petitions.id").
      group(:id, 'signs_count.count', 'users.name', 'users.id', 'user_signs.id').
      paginate(per_page: per_page, page: page).
      order(order)

    if params[:author_id]
      petitions = petitions.where(:user_id => params[:author_id])
    end

    if params[:signer_id]
      petitions = petitions.where('signs.user_id' => params[:signer_id])
    end

    if params[:id]
      petitions = petitions.find(params[:id])
    end

    json_response(petitions)
  end

  def signers
    signers = Petition.
      find(params[:id]).
      signs.
      joins(:user).
      select('users.id').
      select('users.name')

    json_response(signers)
  end

  def sign
    petition = Petition.find(params[:id])

    if petition.signs.exists?(:user_id => current_user.id)
      json_response({message: 'You have already signed this petition'}, :conflict)
      return
    end

    sign = petition.signs.create!(petition_id: petition.id, user_id: current_user.id)
    json_response(sign)
  end

  def import
    yaml = Base64.decode64(params[:petition])
    begin
      petition = YAML.load(yaml)
    rescue Psych::SyntaxError => e
      json_response({message: e.message}, 500)
      return
    end
    if petition['created_at']
      petition = current_user.petitions.create!(text: petition['text'], title: petition['title'], created_at: petition['created_at'])
    else
      petition = current_user.petitions.create!(text: petition['text'], title: petition['title'])
    end
    petition.signs.create!(petition_id: petition.id, user_id: current_user.id)
    json_response(petition)
  end

  private

  def petition_params
    @petition = params.permit(:text, :title, :created_at)
  end

end
