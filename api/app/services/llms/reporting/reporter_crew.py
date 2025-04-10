from typing import Optional

from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, before_kickoff, crew, task

from app.model.crew_output_model import ManagerResult, IncidentReport


@CrewBase
class ReporterCrew:

    agents_config: str = "config/agents.yaml"
    tasks_config: str = "config/tasks.yaml"

    def __init__(self, llm: Optional[LLM] = None):
        self.llm = llm

    @agent
    def manager_agent(self) -> Agent:
        return Agent(config=self.agents_config["manager_agent"], llm=self.llm)

    @agent
    def incident_reporter(self) -> Agent:
        return Agent(
            config=self.agents_config["incident_reporter"],
            llm=self.llm,
        )

    @agent
    def evaluation_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["evaluation_agent"],
            llm=self.llm,
        )

    @task
    def reporting_task(self) -> Task:
        return Task(
            config=self.tasks_config["reporting_task"],
            output_pydantic=IncidentReport,
        )

    @task
    def evaluation_task(self) -> Task:
        return Task(config=self.tasks_config["evaluation_task"])

    @task
    def manager_task(self) -> Task:
        return Task(config=self.tasks_config["manager_task"], output_pydantic=ManagerResult)

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            manager=self.manager_agent(),
            process=Process.sequential,
            verbose=True,
        )
