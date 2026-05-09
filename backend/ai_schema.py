from pydantic import BaseModel
from typing import Optional, List


class CardOperation(BaseModel):
    """Represents a single card operation."""
    operation: str  # 'create', 'update', 'move', 'delete'
    cardId: Optional[str] = None
    title: Optional[str] = None
    details: Optional[str] = None
    columnId: Optional[str] = None


class AIResponse(BaseModel):
    """Structured response from AI for chat messages."""
    message: str  # Natural language response to user
    operations: List[CardOperation] = []  # List of Kanban operations to apply


class ChatMessage(BaseModel):
    """A single message in the conversation."""
    role: str  # 'user' or 'assistant'
    content: str  # Message text
