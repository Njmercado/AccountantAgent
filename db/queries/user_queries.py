class UserQueries:
  @staticmethod
  def create_user(name: str, email: str, password: str) -> str:
    return f"""INSERT INTO "User" (name, email, password) VALUES ('{name}', '{email}', '{password}');"""

  @staticmethod
  def get_user_by_email(email: str) -> str:
    return f"""SELECT * FROM "User" WHERE email = '{email}';"""

  @staticmethod
  def update_user_email(user_id: int, new_email: str) -> str:
    return f"""UPDATE "User" SET email = '{new_email}' WHERE id = {user_id};"""

  @staticmethod
  def delete_user(user_id: int) -> str:
    return f"""DELETE FROM "User" WHERE id = {user_id};"""

  @staticmethod
  def update_user_password(user_id: int, new_password: str) -> str:
    return f"""UPDATE "User" SET password = '{new_password}' WHERE id = {user_id};"""