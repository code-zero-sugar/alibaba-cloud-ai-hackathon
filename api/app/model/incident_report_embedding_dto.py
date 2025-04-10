from app.model.base_dto import BaseDto
from app.schemas.models import IncidentReportEmbedding


class IncidentReportEmbeddingDto(BaseDto):
    _orm_model = IncidentReportEmbedding

    id: int
    incident_report_id: int
    content: str
    embedding: list[float]
