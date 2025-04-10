from typing import Type, Annotated
from fastapi import Depends

from app.schemas.chat_session import ChatSession
from app.repository.repository import Repository


class ChatSessionRepository(Repository[ChatSession]):
    _model: Type[ChatSession] = ChatSession


ChatSessionRepositoryDep = Annotated[
    ChatSessionRepository, Depends(ChatSessionRepository)
]
