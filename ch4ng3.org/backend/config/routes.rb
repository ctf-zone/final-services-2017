Rails.application.routes.draw do
  scope ENV['PREFIX'] || '' do
    post 'auth/login',          to: 'authentication#authenticate'
    get  'auth/third_party',    to: 'authentication#third_party'
    post 'signup',              to: 'users#create'
    get  'users/:id',           to: 'users#get'
    get  'me',                  to: 'users#profile'

    get  'petitions',             to: 'petitions#list'
    post 'petitions',             to: 'petitions#create'
    get  'petitions/:id',         to: 'petitions#list'
    post 'petitions/:id/sign',    to: 'petitions#sign'
    get  'petitions/:id/signers', to: 'petitions#signers'
    post 'petitions/import',      to: 'petitions#import'

    get  'stats', to: 'stats#stats'
  end
end
