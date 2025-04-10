from typing import Annotated, Type

from fastapi import Depends
from app.repository.repository import Repository
from app.schemas.incident_report import IncidentReport


class IncidentReportRepository(Repository[IncidentReport]):
    _model: Type[IncidentReport] = IncidentReport


IncidentReportRepositoryDep = Annotated[
    IncidentReportRepository, Depends(IncidentReportRepository)
]
