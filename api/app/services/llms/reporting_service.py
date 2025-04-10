import os
from dotenv import load_dotenv
from crewai import LLM
from typing import Annotated
from fastapi import Depends

from app.services.llms.reporting.reporter_crew import ReporterCrew


load_dotenv()

OPEN_AI_APIKEY = os.getenv("OPENAI_API_KEY")


class IncidentReportingService:

    def __init__(self):
        self._reporter_crew = ReporterCrew(
            llm=LLM(
                model="openai/qwen-plus",
                api_key=os.getenv("OPENAI_API_KEY"),
                base_url="https://dashscope-intl.aliyuncs.com/compatible-mode/v1",
            )
        ).crew()

    # def evaluate_report(self, data: str) -> dict:
    #     """
    #     Evaluate the incident report using the evaluation crew.
    #     """

    #     result = (
    #         self._report_evaluation_crew.kick_off(inputs={"data": data.model_dump_json()})
    #     ).raw
    #     # If the result is a JSON string, parse it
    #     if isinstance(result, str):
    #         try:
    #             result = json.loads(result)
    #         except json.JSONDecodeError as e:
    #             print(f"Error decoding JSON: {e}")
    #             return {"error": "Invalid JSON response"}

    #     print(f"Result: {result}")

    #     return result

    def get_incident_report(self, data: str) -> dict:
        """
        Get incident report from the data using the reporter crew.
        """
        result = self._reporter_crew.kickoff(inputs={"data": data}).raw
        print(f"Result: {result}")
        return result

    # def process_report(self, data: str) -> dict:
    #     """
    #     Get incident report embedding from the data using the reporter crew.
    #     """
    #     evaluation_result = self.evaluate_report(data)
    #     if evaluation_result["isEnoughInfo"]:
    #         # Process the info
    #         return self.get_incident_report(data)
    #     else:
    #         return evaluation_result["follow_up_questions"]


IncidentReportingServiceDep = Annotated[
    IncidentReportingService, Depends(IncidentReportingService)
]
