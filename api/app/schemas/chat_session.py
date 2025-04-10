from sqlalchemy import Integer, String, ForeignKey, UUID, DateTime, func, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.schemas import Base
from datetime import datetime
import enum, uuid


class SessionType(enum.Enum):
    reporting = "reporting"
    investigation = "investigation"


class ChatSession(Base):

    __tablename__ = "chat_session"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    session_type: Mapped[SessionType] = mapped_column(Enum(SessionType), nullable=False)
    created_by: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    # incident_report = relationship(
    #     "IncidentReport", back_populates="chat_session", uselist=False
    # )

    messages = relationship("ChatMessage", back_populates="session")
