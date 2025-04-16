from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class MessageInfo(BaseModel):
    message_id: int
    username: Optional[str] = None
    firstname: str
    lastname: Optional[str] = None
    sender_id: int
    chat_id: int
    sent_at: datetime = Field(default_factory=datetime.now)
    