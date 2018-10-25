class CreatePetitions < ActiveRecord::Migration[5.1]
  def change
    create_table :petitions do |t|
      t.string :title
      t.string :text
      t.references :user, foreign_key: true

    end
    add_index :petitions, [:user_id] unless index_exists?(:petitions, :user_id)
  end
end
