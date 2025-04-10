from app.model.base_dto import BaseDTO
from app.schemas.chat_message import ChatMessage, Role

from typing import Type


class ChatMessageCreateDTO(BaseDTO):
    _orm_model: Type[ChatMessage] = ChatMessage

    session_id: int
    message: str
    role: Role


class ChatMessageDto(ChatMessageCreateDTO):

    id: int
    created_at: str
    created_by: str
