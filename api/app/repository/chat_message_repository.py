from app.repository.repository import Repository
from app.schemas.chat_message import ChatMessage

from typing import Type, Annotated
from fastapi import Depends


class ChatMessageRepository(Repository):
    _model: Type[ChatMessage] = ChatMessage


ChatMessageRepositoryDep = Annotated[
    ChatMessageRepository, Depends(ChatMessageRepository)
]
