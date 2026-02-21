import psycopg2
from dotenv import load_dotenv
import os
from db.tables import transaction_table, user_table, conversation_table, message_table

load_dotenv()
DB_URL = os.getenv("DATABASE_URL")

class DB:
  _connection = None

  def __init__(self):
    self._connection = self._connect_to_db()

  def _connect_to_db(self):
    try:

      if not DB_URL:
        raise ValueError(f"DB_URL environment variable is not set. {DB_URL}")
      
      if self._connection:
        print("Already connected to database.")
        return self._connection

      connection = psycopg2.connect(DB_URL)
      print("Connection to database established successfully.")

      cursor = connection.cursor()

      transaction_table_instance = transaction_table.TransactionTable()
      user_table_instance = user_table.UserTable()
      conversation_table_instance = conversation_table.ConversationTable()
      message_table_instance = message_table.MessageTable()

      cursor.execute(user_table_instance.create_table())
      cursor.execute(transaction_table_instance.create_table())
      cursor.execute(conversation_table_instance.create_table())
      cursor.execute(message_table_instance.create_table())
      connection.commit()

      return connection
    except Exception as e:
      print(f"Error connecting to database: {e}")
      return None

  def get_db_connection(self):
    return self._connection

  def execute_query(self, query: str):
    if not self._connection:
      print("No database connection available.")
      return None
    try:
      cursor = self._connection.cursor()
      cursor.execute(query)
      self._connection.commit()

      # Only fetch results for queries that return data (SELECT, RETURNING, etc.)
      if cursor.description:
        return cursor.fetchall()
      return True
    except Exception as e:
      self._connection.rollback()
      print(f"Error executing query: {e}")
      return None

  def close_db_connection(self):
    if self._connection:
      self._connection.close()
      print("Database connection closed.")
    else:
      print("No database connection to close.")
