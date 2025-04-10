import os
from typing import Annotated
from openai.types import CreateEmbeddingResponse
from pydantic import BaseModel, ConfigDict
from openai import AsyncOpenAI
from fastapi import Depends

from dotenv import load_dotenv

from app.services.openai.openai_client import OpenAIClientDep, SyncOpenAIClientDep

load_dotenv()


class EmbeddingService(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    openai_client: OpenAIClientDep
    sync_openai_client: SyncOpenAIClientDep

    async def generate_embedding(self, text: str) -> list[float]:
        response: CreateEmbeddingResponse = await self.openai_client.embeddings.create(
            input=text, model="text-embedding-v3", dimensions=1024
        )
        return response.data[0].embedding

    def generate_embedding_sync(self, text: str) -> list[float]:
        response: CreateEmbeddingResponse = self.sync_openai_client.embeddings.create(
            input=text, model="text-embedding-v3", dimensions=1024
        )
        return response.data[0].embedding


EmbeddingServiceDep = Annotated[EmbeddingService, Depends(EmbeddingService)]
