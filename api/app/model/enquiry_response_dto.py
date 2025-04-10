from pydantic import BaseModel, ConfigDict

from app.model.incident_report_dto import IncidentReportDto


class EnquiryResponseDto(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    response: str
    reference_incident_reports: list[IncidentReportDto]
