import json
from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from app.model.enquiry_response_dto import EnquiryResponseDto
from app.services.websocket.connection_manager import manager
from app.services.investigation.investigation_agent_factory import (
    InvestigationAgentFactoryDep,
)
from app.services.investigation.investigation_service import InvestigationServiceDep
from app.services.rag.rag_service import IncidentReportRAGServiceDep
from app.repository.incident_report_repository import IncidentReportRepositoryDep
from app.model.incident_report_dto import IncidentReportCreateDto, IncidentReportDto

router = APIRouter()


@router.post("/incident_report")
async def create_incident_report(
    incident_reports: list[IncidentReportCreateDto],
    incident_report_repo: IncidentReportRepositoryDep,
    incident_report_rag_service: IncidentReportRAGServiceDep,
):
    results = await incident_report_repo.insert_many(
        [incident_report.to_orm() for incident_report in incident_reports]
    )
    await incident_report_rag_service.insert_many(results)
    return {"message": "Incident reports created successfully"}


# For testing purposes
@router.get("/incident_report/rag/", response_model=list[IncidentReportDto])
async def query_incident_report(
    query: str,
    incident_report_rag_service: IncidentReportRAGServiceDep,
    incident_report_repo: IncidentReportRepositoryDep,
) -> list[IncidentReportDto]:
    results = await incident_report_rag_service.query(query)
    ids = [result.incident_report_id for result in results]

    incident_reports = await incident_report_repo.get_by_ids(ids)
    return [IncidentReportDto.from_orm(report) for report in incident_reports]


# For testing purposes
@router.get("/incident_report/chatbot/", response_model=EnquiryResponseDto)
async def enquiry_incident_report(
    query: str, investigation_service: InvestigationServiceDep
) -> EnquiryResponseDto:
    return await investigation_service.enquiry(query=query, chat_history="")


async def websocket_investigation(
    websocket: WebSocket, investigation_service: InvestigationServiceDep
):
    await manager.connect(websocket)
    try:
        while True:
            input = await websocket.receive_text()
            data = json.loads(input)
            result = await investigation_service.enquiry(
                query=data["query"], chat_history=data["chat_history"]
            )
            await websocket.send_text(result.model_dump_json())
    except WebSocketDisconnect:
        manager.disconnect(websocket)


router.add_api_websocket_route(
    "/ws/investigation", websocket_investigation, name="websocket_investigation"
)
