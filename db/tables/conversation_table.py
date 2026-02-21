from .table import Table

class ConversationTable(Table):
  def __init__(self):
    super().__init__(
      "Conversation",
      [
        "id SERIAL PRIMARY KEY",
        "user_id INT NOT NULL",
        "title VARCHAR(255) DEFAULT 'New Conversation'",
        "created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP",
        "updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP",
        'FOREIGN KEY (user_id) REFERENCES "User"(id)'
      ]
    )
