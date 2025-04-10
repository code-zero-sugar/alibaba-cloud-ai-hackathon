from typing import Type
from crewai.tools import BaseTool
from pydantic import BaseModel, Field

from app.model.incident_report_dto import IncidentReportDto
from app.repository.incident_report_repository import IncidentReportRepository
from app.services.rag.rag_service import IncidentReportRAGService


class IncidentReportRetrievelInput(BaseModel):
    query: str = Field(
        ...,
        description="The query to search for incident reports.",
    )


class IncidentReportRetrievalTool(BaseTool):
    name: str = "Incident Report Retrieval Tool"
    description: str = "This tool retrieves incident reports based on a query."
    args_schema: Type[BaseModel] = IncidentReportRetrievelInput
    return_direct: bool = True
    verbose: bool = True
    incident_report_rag_service: IncidentReportRAGService
    incident_report_repository: IncidentReportRepository

    def _run(self, query: str):
        results = self.incident_report_rag_service.query_sync(query)
        ids = [result.incident_report_id for result in results]
        incident_reports = self.incident_report_repository.get_by_ids_sync(ids)
        return [IncidentReportDto.from_orm(report) for report in incident_reports]
