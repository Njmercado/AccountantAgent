class Table:
  def __init__(self, name: str, columns: list[str]):
    self._name = name
    self._columns = columns

  def create_table(self):
    """
    Generates a SQL query to create a table with the specified name and columns.
    - The columns are defined as a list of strings, where each string represents a column definition
    """
    columns_with_types = ", ".join([f"{col}" for col in self._columns])
    create_table_query = f'CREATE TABLE IF NOT EXISTS "{self._name}" ({columns_with_types});'
    return create_table_query

  def delete_table(self):
    """
    Generates a SQL query to delete the table with the specified name.
    """
    delete_table_query = f'DROP TABLE IF EXISTS "{self._name}";'
    return delete_table_query

  def update_table(self, new_columns: dict):
    """
    Generates SQL queries to update the table structure by adding new columns or modifying existing ones.
    - new_columns is a dictionary where the key is the column name and the value is the data type of the column (e.g., "VARCHAR(255)", "INT", etc.).
    """
    alter_table_queries = []
    for col, dtype in new_columns.items():
      if col not in self._columns:
        alter_table_queries.append(f"ALTER TABLE {self._name} ADD COLUMN {col} {dtype};")
        self._columns[col] = dtype
      else:
        alter_table_queries.append(f"ALTER TABLE {self._name} ALTER COLUMN {col} TYPE {dtype};")
    return alter_table_queries
