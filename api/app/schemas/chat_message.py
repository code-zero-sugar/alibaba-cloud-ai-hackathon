from sqlalchemy import Integer, String, ForeignKey, DateTime, func, UUID, Enum
from sqlalchemy.orm import mapped_column, Mapped, relationship

from app.schemas import Base

from datetime import datetime

import enum, uuid


class Role(enum.Enum):
    bot = "bot"
    user = "user"


class ChatMessage(Base):
    __tablename__ = "chat_message"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    message: Mapped[str] = mapped_column(String, nullable=False)
    role: Mapped[Role] = mapped_column(Enum(Role), nullable=False)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    created_by: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=True)

    session_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("chat_session.id"), unique=True, nullable=False
    )
    session = relationship("ChatSession", back_populates="messages")
