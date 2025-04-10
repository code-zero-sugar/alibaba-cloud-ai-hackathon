from typing import Type
from uuid import UUID
from datetime import datetime

from app.model.base_dto import BaseDto
from app.schemas.models import IncidentReport


class IncidentReportCreateDto(BaseDto):
    _orm_model: Type[IncidentReport] = IncidentReport

    desc: str
    explanation: str
    action: str
    reported_by: UUID | None = None


class IncidentReportDto(IncidentReportCreateDto):
    id: int
    created_at: datetime
    updated_at: datetime
