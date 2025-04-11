import os
from typing import Annotated
from dotenv import load_dotenv
from pydantic import BaseModel, ConfigDict
from sqlalchemy import Engine, create_engine
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import Session, sessionmaker
from fastapi import Depends


load_dotenv()


class Session_Manager(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    async_connection_string: str = (
        os.getenv("DATABASE_URL", "").replace("postgresql://", "postgresql+asyncpg://")
        + "?prepared_statement_cache_size=0"
    )
    sync_connection_string: str = (
        os.getenv("DATABASE_URL", "").replace("postgresql://", "postgresql+psycopg2://")
        + "?prepared_statement_cache_size=0"
    )
    async_engine: AsyncEngine = create_async_engine(
        async_connection_string,
        echo=True,
    )
    sync_engine: Engine = create_engine(
        sync_connection_string,
        echo=True,
    )
    async_session_make: async_sessionmaker = async_sessionmaker(bind=async_engine)
    sync_session_make: sessionmaker = sessionmaker(bind=sync_engine)

    def get_async_session(self) -> AsyncSession:
        return self.async_session_make()

    def get_sync_session(self) -> Session:
        return self.sync_session_make()


async def get_async_session():
    async with Session_Manager().get_async_session() as session:
        yield session


AsyncSessionDep = Annotated[AsyncSession, Depends(get_async_session)]


def get_sync_session():
    with Session_Manager().get_sync_session() as session:
        yield session


SyncSessionDep = Annotated[Session, Depends(get_sync_session)]
