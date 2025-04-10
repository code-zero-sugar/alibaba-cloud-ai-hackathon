from fastapi import APIRouter

from app.repository.chat_session_repository import ChatSessionRepositoryDep
from app.repository.chat_message_repository import ChatMessageRepositoryDep
from app.model.chat_session_dto import ChatSessionCreateDto, ChatSessionDto
from app.model.chat_message_dto import ChatMessageCreateDto, ChatMessageDto


router = APIRouter()


@router.get("/chat_session/{session_id}", response_model=ChatSessionDto)
async def get_chat_session(
    session_id: str,
    chat_session_repo: ChatSessionRepositoryDep,
) -> ChatSessionDto:
    chat_session = await chat_session_repo.get_by_id(session_id)
    return ChatSessionDto.from_orm(chat_session)


@router.get("/chat_sessions", response_model=list[ChatSessionDto])
async def get_chat_sessions(
    chat_session_repo: ChatSessionRepositoryDep,
) -> list[ChatSessionDto]:
    chat_sessions = await chat_session_repo.get_all()
    return [ChatSessionDto.from_orm(session) for session in chat_sessions]


@router.get("/chat_messages/{session_id}", response_model=list[ChatMessageDto])
async def get_chat_messages(
    session_id: str,
    chat_message_repo: ChatMessageRepositoryDep,
) -> list[ChatMessageDto]:
    chat_messages = await chat_message_repo.get_by_session_id(session_id)
    return [ChatMessageDto.from_orm(message) for message in chat_messages]
