from typing import List, Optional
from pydantic import BaseModel

from app.model.incident_report_dto import IncidentReportCreateDto


class ManagerResult(BaseModel):
    message: str
    incident_report: Optional[IncidentReportCreateDto] = None
