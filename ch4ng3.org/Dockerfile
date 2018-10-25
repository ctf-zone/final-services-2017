FROM node as frontend-builder
WORKDIR /usr/src/app
COPY frontend ./
RUN yarn && yarn build

FROM ruby
WORKDIR /usr/src/app
COPY backend ./
COPY --from=frontend-builder /usr/src/app/build/ /usr/src/app/public/
RUN bundle install
ENV PREFIX /api
ENV RAILS_ENV production
ENV RAILS_SERVE_STATIC_FILES true
EXPOSE 3000
CMD bundle exec rake db:migrate && bundle exec rails s -p 3000 -b '0.0.0.0'
