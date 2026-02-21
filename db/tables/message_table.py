from .table import Table

class MessageTable(Table):
  def __init__(self):
    super().__init__(
      "Message",
      [
        "id SERIAL PRIMARY KEY",
        "conversation_id INT NOT NULL",
        "role VARCHAR(20) NOT NULL CHECK (role IN ('user', 'assistant', 'system'))",
        "content TEXT NOT NULL",
        "created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP",
        'FOREIGN KEY (conversation_id) REFERENCES "Conversation"(id) ON DELETE CASCADE'
      ]
    )
