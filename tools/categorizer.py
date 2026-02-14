from strands import tool

@tool
def categorizer(description: str) -> str:
  """
  A tool that categorizes financial transactions based on provided data.
  This tool should only return the category and type of transaction(Income, Outcome) and nothing else. Do not return any explanations or additional information, only the category of the transaction.
  
  IMPORTANT: After this tool returns a category and type, you MUST immediately call the appropriate tool:
    - If the type is 'Income', call insert_income with the amount, date, and determined category.
    - If the type is 'Outcome', call insert_outcome with the amount, date, and determined category.
  Do NOT stop after categorization. Always proceed to insert the transaction.

  Args:
    description (str): A brief description of the financial transaction.
  """
  return f"The transaction '{description}' has been categorized. Now you MUST call insert_income or insert_outcome to save it to the database."
