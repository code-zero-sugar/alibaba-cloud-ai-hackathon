import os
from typing import Annotated
from dotenv import load_dotenv
from pydantic import BaseModel, ConfigDict
from fastapi import Depends
from crewai import Crew

from app.repository.incident_report_repository import IncidentReportRepositoryDep
from app.services.rag.rag_service import IncidentReportRAGServiceDep
from app.services.llms.investigation.investigation_crew import InvestigationCrew

load_dotenv()


class InvestigationAgentFactory(BaseModel):
    model_config = ConfigDict(
        arbitrary_types_allowed=True,
    )
    incident_report_rag_service: IncidentReportRAGServiceDep
    incident_report_repository: IncidentReportRepositoryDep

    def create_agent(self) -> Crew:
        return InvestigationCrew(
            incident_report_rag_service=self.incident_report_rag_service,
            incident_report_repository=self.incident_report_repository,
        ).crew()


InvestigationAgentFactoryDep = Annotated[
    InvestigationAgentFactory, Depends(InvestigationAgentFactory)
]
