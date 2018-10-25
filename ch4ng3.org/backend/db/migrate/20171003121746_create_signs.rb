class CreateSigns < ActiveRecord::Migration[5.1]
  def change
    create_table :signs do |t|
      t.references :petition, foreign_key: true
      t.references :user, foreign_key: true

    end
    add_index :signs, [:user_id] unless index_exists?(:signs, :user_id)
  end
end
