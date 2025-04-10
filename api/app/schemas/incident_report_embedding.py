from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column
from pgvector.sqlalchemy import Vector

from app.schemas import Base


class IncidentReportEmbedding(Base):
    __tablename__ = "incident_report_embedding"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    incident_report_id: Mapped[int] = mapped_column(Integer, nullable=False, index=True)
    content: Mapped[str] = mapped_column(String, nullable=False)
    embedding: Mapped[list[float]] = mapped_column(Vector(1024), nullable=False)
