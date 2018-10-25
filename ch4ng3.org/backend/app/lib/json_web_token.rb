class JsonWebToken
  # secret to encode and decode token

  def self.encode(payload, exp = 24.hours.from_now)
    # set expiry to 24 hours from creation time
    payload[:exp] = exp.to_i
    # sign token with application secret, using RSA for stronger cryptography
    secret_key = Rails.application.secrets.secret_key_base
    secret_key = OpenSSL::PKey::RSA.new(secret_key)
    JWT.encode(payload, secret_key, 'RS256')
  end

  def self.decode(token, algorithm)
    # cant store key as ruby object in yaml file
    public_key = Rails.application.secrets.public_key_base
    if algorithm == 'RS256'
      public_key = OpenSSL::PKey::RSA.new(public_key)
    end
    # get payload; first index in decoded Array
    body = JWT.decode(token, public_key, true, {:algorithm => algorithm})[0]
    HashWithIndifferentAccess.new body
    # rescue from expiry exception
  rescue JWT::ExpiredSignature, JWT::VerificationError => e
    # raise custom error to be handled by custom handler
    raise ExceptionHandler::InvalidToken, e.message
  end
end
