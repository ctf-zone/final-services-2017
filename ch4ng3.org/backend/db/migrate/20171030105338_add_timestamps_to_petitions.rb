class AddTimestampsToPetitions < ActiveRecord::Migration[5.1]
  def change
    add_column :petitions, :created_at, :string
    add_column :petitions, :updated_at, :string
  end
end
