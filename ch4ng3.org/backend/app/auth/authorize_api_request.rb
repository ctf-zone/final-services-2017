class AuthorizeApiRequest
  def initialize(headers = {})
    @headers = headers
  end

  # Service entry point - return valid user object
  def call()
    {
      user: user()
    }
  end

  private

  attr_reader :headers

  def user()
    # check if user is in the database
    # memoize user object
    @user ||= User.find(decoded_auth_token()[:user_id]) if decoded_auth_token()
    # handle user not found
  rescue ActiveRecord::RecordNotFound => e
    # raise custom error
    raise(
      ExceptionHandler::InvalidToken,
      ("#{Message.invalid_token} #{e.message}")
    )
  end

  # decode authentication token
  def decoded_auth_token()
    token, algorithm = http_auth_header()
    @decoded_auth_token ||= JsonWebToken.decode(token, algorithm)
  end

  # check for token in `Authorization` header
  def http_auth_header
    if headers['Authorization'].present?
      auth = headers['Authorization'].split(' ').last
      algorithm = JSON.parse(Base64.decode64(auth.split('.').first))['alg']
      return auth, algorithm
    end
      raise(ExceptionHandler::MissingToken, Message.missing_token)
  end
  rescue
    raise(
      ExceptionHandler::InvalidToken,
      ("#{Message.invalid_token}")
    )
end
