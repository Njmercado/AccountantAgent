from typing import override
from .table import Table

class TransactionTable(Table):
  def __init__(self):
    super().__init__(
      "Transaction",
      [
        "id SERIAL PRIMARY KEY",
        "amount DECIMAL(10, 2) NOT NULL",
        "category VARCHAR(255) NOT NULL",
        "date DATE NOT NULL",
        "type VARCHAR(10) NOT NULL CHECK (type IN ('Income', 'Outcome'))",
        "user_id INT NOT NULL",
        'foreign key (user_id) references "User"(id)'
      ]
    )
