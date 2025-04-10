from typing import Annotated
from fastapi import Depends
from pydantic import BaseModel

from app.model.enquiry_response_dto import EnquiryResponseDto
from app.model.incident_report_dto import IncidentReportDto
from app.repository.incident_report_repository import IncidentReportRepositoryDep
from app.services.investigation.investigation_agent_factory import (
    InvestigationAgentFactoryDep,
)
from app.services.llms.investigation.investigation_crew import InvestigationCrewOutput


class InvestigationService(BaseModel):
    investigation_agent_factory: InvestigationAgentFactoryDep
    incident_report_repository: IncidentReportRepositoryDep

    async def enquiry(self, query: str, chat_history: str) -> EnquiryResponseDto:
        """
        Enquiry incident report
        """
        crew = self.investigation_agent_factory.create_agent()
        result: InvestigationCrewOutput = (
            await crew.kickoff_async(
                inputs={"query": query, "chat_history": chat_history}
            )
        ).pydantic

        reference_reports = await self.incident_report_repository.get_by_ids(
            result.reference_reports_ids
        )

        return EnquiryResponseDto(
            response=result.response,
            reference_incident_reports=[
                IncidentReportDto.from_orm(report) for report in reference_reports
            ],
        )


InvestigationServiceDep = Annotated[InvestigationService, Depends(InvestigationService)]
