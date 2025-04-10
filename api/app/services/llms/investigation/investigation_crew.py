import os
from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task
from dotenv import load_dotenv
from pydantic import BaseModel, Field

from app.services.llms.investigation.incident_report_retrieval_tool import (
    IncidentReportRetrievalTool,
)
from app.repository.incident_report_repository import IncidentReportRepository
from app.services.rag.rag_service import IncidentReportRAGService

load_dotenv()


class InvestigationCrewOutput(BaseModel):
    response: str = Field(..., description="The response from the crew.")
    reference_reports_ids: list[int] = Field(
        ..., description="The IDs of the reference reports used in the response."
    )


@CrewBase
class InvestigationCrew:

    agents_config: str = "config/agents.yaml"
    tasks_config: str = "config/tasks.yaml"

    def __init__(
        self,
        incident_report_rag_service: IncidentReportRAGService,
        incident_report_repository: IncidentReportRepository,
    ):
        self.llm = LLM(
            model="openai/qwen-plus",
            api_key=os.getenv("OPENAI_API_KEY"),
            base_url="https://dashscope-intl.aliyuncs.com/compatible-mode/v1",
        )
        self.incident_report_rag_service = incident_report_rag_service
        self.incident_report_repository = incident_report_repository

    def get_incident_report_retrieval_tool(self):
        return IncidentReportRetrievalTool(
            incident_report_rag_service=self.incident_report_rag_service,
            incident_report_repository=self.incident_report_repository,
        )

    @agent
    def incident_report_analyst(self) -> Agent:
        return Agent(
            config=self.agents_config["incident_report_analyst"],
            tools=[self.get_incident_report_retrieval_tool()],
            llm=self.llm,
        )

    @task
    def analyse_incident_report_task(self) -> Task:
        return Task(
            config=self.tasks_config["analyse_incident_report_task"],
            output_pydantic=InvestigationCrewOutput,
        )

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )
