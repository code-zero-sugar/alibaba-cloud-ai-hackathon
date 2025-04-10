from typing import Annotated, Type

from sqlalchemy import select
from fastapi import Depends

from app.schemas.incident_report_embedding import IncidentReportEmbedding
from app.repository.repository import Repository


class IncidentReportEmbeddingRepository(Repository[IncidentReportEmbedding]):
    _model: Type[IncidentReportEmbedding] = IncidentReportEmbedding
    _similarity_threshold: float = 0.7
    _default_limit: int = 5

    async def query(
        self, query_embedding: list[float], limit: int = _default_limit
    ) -> list[IncidentReportEmbedding]:
        result = await self.session.execute(self._get_query(query_embedding, limit))

        return list(result.scalars().all())

    def query_sync(
        self, query_embedding: list[float], limit: int = _default_limit
    ) -> list[IncidentReportEmbedding]:
        result = self.sync_session.execute(self._get_query(query_embedding, limit))

        return list(result.scalars().all())

    def _get_query(self, query_embedding: list[float], limit: int = _default_limit):
        return (
            select(
                self._model,
                self._model.embedding.cosine_distance(query_embedding).label(
                    "distance"
                ),
            )
            .filter(
                self._model.embedding.cosine_distance(query_embedding)
                < self._similarity_threshold
            )
            .order_by("distance")
            .limit(limit)
        )


IncidentReportEmbeddingRepositoryDep = Annotated[
    IncidentReportEmbeddingRepository,
    Depends(IncidentReportEmbeddingRepository),
]
