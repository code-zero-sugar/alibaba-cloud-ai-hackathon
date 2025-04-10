from typing import Type
from datetime import datetime

from app.model.base_dto import BaseDto
from app.schemas.chat_session import SessionType, ChatSession

import uuid


class ChatSessionCreateDto(BaseDto):
    _orm_model: Type[ChatSession] = ChatSession

    sessionType: SessionType


class ChatSessionDto(ChatSessionCreateDto):

    id: int
    created_by: uuid.UUID
    created_at: datetime
    updated_at: datetime
