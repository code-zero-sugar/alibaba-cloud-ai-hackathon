from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers.incident_report_router import router as incident_report_router
from app.routers.websocket_reporting_router import reporting_websocket
from app.routers.audio import router as audio_router

app = FastAPI()

# Add CORS middleware to allow frontend connections
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Specify your frontend origin in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(incident_report_router)
app.add_api_websocket_route("/ws/reporting", reporting_websocket)
app.include_router(audio_router)


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/test")
async def test():
    return "lol"
