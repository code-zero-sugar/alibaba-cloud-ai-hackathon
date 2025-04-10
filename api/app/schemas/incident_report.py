from datetime import datetime
import uuid
from sqlalchemy import UUID, DateTime, Integer, String, func, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.schemas import Base


class IncidentReport(Base):
    __tablename__ = "incident_report"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    desc: Mapped[str] = mapped_column(String, nullable=False)
    explanation: Mapped[str] = mapped_column(String, nullable=False)
    action: Mapped[str] = mapped_column(String, nullable=False)
    reported_by: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    chat_session_id: Mapped[int] = mapped_column(Integer, unique=True, nullable=True)

    # chat_session = relationship("ChatSession", back_populates="incident_report")
