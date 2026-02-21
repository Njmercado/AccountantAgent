class ConversationQueries:
  @staticmethod
  def create_conversation(user_id: int, title: str = "New Conversation") -> str:
    safe_title = title.replace("'", "''")
    return f"""
      INSERT INTO "Conversation" (user_id, title)
      VALUES ({user_id}, '{safe_title}')
      RETURNING id, title, created_at;
    """

  @staticmethod
  def get_conversations_by_user(user_id: int) -> str:
    return f"""
      SELECT c.id, c.title, c.created_at, c.updated_at
      FROM "Conversation" c
      WHERE c.user_id = {user_id}
      ORDER BY c.updated_at DESC;
    """

  @staticmethod
  def get_conversation_messages(conversation_id: int) -> str:
    return f"""
      SELECT role, content, created_at
      FROM "Message"
      WHERE conversation_id = {conversation_id}
      ORDER BY created_at ASC;
    """

  @staticmethod
  def insert_message(conversation_id: int, role: str, content: str) -> str:
    safe_content = content.replace("'", "''")
    return f"""
      INSERT INTO "Message" (conversation_id, role, content)
      VALUES ({conversation_id}, '{role}', '{safe_content}');
    """

  @staticmethod
  def update_conversation_timestamp(conversation_id: int) -> str:
    return f"""
      UPDATE "Conversation"
      SET updated_at = CURRENT_TIMESTAMP
      WHERE id = {conversation_id};
    """
