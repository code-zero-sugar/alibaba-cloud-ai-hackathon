import asyncio
from typing import Annotated
from fastapi import Depends
from openai import embeddings
from pydantic import BaseModel, ConfigDict

from app.schemas.incident_report import IncidentReport
from app.schemas.incident_report_embedding import IncidentReportEmbedding
from app.repository.incident_report_embedding_repository import (
    IncidentReportEmbeddingRepositoryDep,
)
from app.services.rag.embedding_service import EmbeddingServiceDep


class IncidentReportRAGService(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    embedding_service: EmbeddingServiceDep
    incident_report_embedding_repository: IncidentReportEmbeddingRepositoryDep

    async def insert(self, report: IncidentReport):
        await self.insert_many([report])

    async def insert_many(self, reports: list[IncidentReport]):
        embeddings = await asyncio.gather(
            *[self._get_incident_report_embedding(report) for report in reports]
        )
        await self.incident_report_embedding_repository.insert_many(embeddings)

    async def _get_incident_report_embedding(
        self, report: IncidentReport
    ) -> IncidentReportEmbedding:
        content = "\n".join([report.desc, report.explanation, report.action])
        embedding = await self.embedding_service.generate_embedding(content)

        return IncidentReportEmbedding(
            incident_report_id=report.id, content=content, embedding=embedding
        )

    async def query(self, query: str):
        embedding = await self.embedding_service.generate_embedding(query)

        results = await self.incident_report_embedding_repository.query(embedding)

        return results

    def query_sync(self, query: str):
        embedding = self.embedding_service.generate_embedding_sync(query)

        results = self.incident_report_embedding_repository.query_sync(embedding)

        return results


IncidentReportRAGServiceDep = Annotated[
    IncidentReportRAGService, Depends(IncidentReportRAGService)
]
