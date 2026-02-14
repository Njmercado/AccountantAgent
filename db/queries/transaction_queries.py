class TransactionQueries:
  @staticmethod
  def get_total_income_by_month(month: int, year: int) -> str:
    return f"""
      SELECT SUM(amount) AS total_income
      FROM "Transaction"
      WHERE EXTRACT(MONTH FROM date) = {month} AND EXTRACT(YEAR FROM date) = {year} AND type = 'Income';
    """

  @staticmethod
  def get_income_by_category(month: int, year: int) -> str:
    return f"""
      SELECT category, SUM(amount) AS total_amount
      FROM "Transaction"
      WHERE EXTRACT(MONTH FROM date) = {month} AND EXTRACT(YEAR FROM date) = {year} AND type = 'Income'
      GROUP BY category;
    """

  @staticmethod
  def insert_income(amount: float, date: str, user_id: int, category: str) -> str:
    """
    Inserts a new income record into the database.
    
    Args:
      amount (float): The amount of income received.
      date (str): The date the income was received, in YYYY-MM-DD format.
      user_id (int): The ID of the user associated with the income record.
      category (str): The category of the income record.
    """
    
    return f"""
      INSERT INTO "Transaction" (amount, date, user_id, type, category)
      VALUES ({amount}, '{date}', {user_id}, 'Income', '{category}');
    """

  @staticmethod
  def insert_outcome(amount: float, date: str, user_id: int, category: str) -> str:
    return f"""
      INSERT INTO "Transaction" (amount, date, user_id, type, category)
      VALUES ({amount}, '{date}', {user_id}, 'Outcome', '{category}');
    """