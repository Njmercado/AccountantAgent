from .table import Table

class UserTable(Table):
  def __init__(self):
    super().__init__(
      "User",
      [
        "id SERIAL PRIMARY KEY",
        "name VARCHAR(255) NOT NULL",
        "email VARCHAR(255) UNIQUE NOT NULL",
        "password VARCHAR(255) NOT NULL",
        "created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP"
      ]
    )