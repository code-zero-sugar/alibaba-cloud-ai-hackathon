from typing import List, Optional
from pydantic import BaseModel


class IncidentReport(BaseModel):
    desc: str
    explanation: str
    action: str


class ManagerResult(BaseModel):
    message: str
    incident_report: Optional[IncidentReport] = None
