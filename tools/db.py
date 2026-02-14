from strands import tool, ToolContext
from db.db import DB
from db.queries import transaction_queries, user_queries
from datetime import datetime

# Establish a single DB connection shared by all tools
_db = DB()

@tool()
def create_user(name: str, email: str, password: str) -> str:
  """
  Creates a new user in the database given their parameters,
  only if no parameters are provided then you can create a user with default values.

  Args:
    name (str): The name of the user.
    email (str): The email address of the user.
    password (str): The password for the user account.
  """
  try:
    _db.execute_query(
      user_queries.UserQueries.create_user(name, email, password)
    )
    return f"Successfully created user: {name} with email: {email}"
  except Exception as e:
    return f"Error creating user: {e}"

@tool(context=True)
def insert_income(tool_context: ToolContext, category: str, amount: float, date: str) -> str:
  """
  Inserts a new income record into the database.
  If not enough data is provided, ask the user for more information until you have all the necessary data to insert an income record into the database.

  Args:
    category (str): The category of the income record.
    amount (float): The amount of income received.
    date (str): The date the income was received. Format the Date into this YYYY-MM-DD format.
  """

  user_id = tool_context.agent.state.get("user_id")

  query = transaction_queries.TransactionQueries.insert_income(
    amount,
    date,
    user_id,
    category
  )

  try:
    result = _db.execute_query(query)
    if result is None:
      return f"Error: Failed to insert income record into database."
    return f"Successfully inserted income record: category={category}, amount={amount}, date={date}"
  except Exception as e:
    return f"Error inserting income record: {e}"

@tool(context=True)
def insert_outcome(tool_context: ToolContext, category: str, amount: float, date: str) -> str:
  """
  Inserts a new outcome (expense) record into the database.
  If not enough data is provided, ask the user for more information until you have all the necessary data to insert an outcome record into the database.

  Args:
    category (str): The category of the outcome determined by the categorizer tool.
    amount (float): The amount of the financial outcome.
    date (str): The date of the financial outcome. Format the Date into this YYYY-MM-DD format.
  """

  user_id = tool_context.agent.state.get("user_id")

  query = transaction_queries.TransactionQueries.insert_outcome(
    amount,
    date,
    user_id,
    category
  )

  try:
    result = _db.execute_query(query)
    if result is None:
      return f"Error: Failed to insert outcome record into database."
    return f"Successfully inserted outcome record: category={category}, amount={amount}, date={date}"
  except Exception as e:
    return f"Error inserting outcome record: {e}"