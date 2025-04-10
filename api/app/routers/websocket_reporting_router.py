# app/routers/websocket_router.py

from fastapi import WebSocket, WebSocketDisconnect
from app.services.websocket.connection_manager import manager
from app.services.llms.reporting_service import (
    IncidentReportingService,
    IncidentReportingServiceDep,
)


# Exported function (DO NOT decorate with @app.websocket)
async def reporting_websocket(
    websocket: WebSocket, reporting_service: IncidentReportingServiceDep
):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            result = reporting_service.get_incident_report(data)
            await websocket.send_text(result)
    except WebSocketDisconnect:
        manager.disconnect(websocket)
