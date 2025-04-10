from typing import Any, Dict, Generic, Type, TypeVar
from pydantic import BaseModel, ConfigDict
from sqlalchemy import select

from app.repository.db_session import AsyncSessionDep, SyncSessionDep

T = TypeVar("T")


class Repository(BaseModel, Generic[T]):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    _model: Type[T]
    session: AsyncSessionDep
    sync_session: SyncSessionDep

    def insert_sync(self, item: T) -> T:
        self.sync_session.add(item)
        self.sync_session.commit()
        self.sync_session.refresh(item)

        return item

    def insert_many_sync(self, items: list[T]) -> list[T]:
        self.sync_session.add_all(items)
        self.sync_session.commit()

        for item in items:
            self.sync_session.refresh(item)

        return items

    def get_by_filters_sync(self, filters: dict) -> list[T]:
        query = select(self._model)

        for key, value in filters.items():
            query = query.where(getattr(self._model, key) == value)

        result = self.sync_session.execute(query)
        return list(result.scalars().all())

    def get_by_id_sync(self, id: int) -> T:
        query = select(self._model).where(self._model.id == id)
        result = self.sync_session.execute(query)
        item = result.scalars().first()
        if not item:
            raise ValueError("Item not found")
        return item

    def get_by_ids_sync(self, ids: list[int]) -> list[T]:
        query = select(self._model).where(self._model.id.in_(ids))
        result = self.sync_session.execute(query)
        return list(result.scalars().all())

    def update_by_id_sync(self, id: int, data: Dict[str, Any]) -> T:
        existing_item = self.get_by_id_sync(id)
        for key, value in data.items():
            if hasattr(existing_item, key):
                setattr(existing_item, key, value)
        self.sync_session.commit()
        self.sync_session.refresh(existing_item)

        return existing_item

    def delete_by_id_sync(self, id: int) -> None:
        item = self.get_by_id_sync(id)
        self.sync_session.delete(item)
        self.sync_session.commit()

    ##########################################################################

    async def insert(self, item: T) -> T:
        self.session.add(item)
        await self.session.commit()
        await self.session.refresh(item)

        return item

    async def insert_many(self, items: list[T]) -> list[T]:
        self.session.add_all(items)
        await self.session.commit()

        for item in items:
            await self.session.refresh(item)

        return items

    async def get_by_filters(self, filters: dict) -> list[T]:
        query = select(self._model)

        for key, value in filters.items():
            query = query.where(getattr(self._model, key) == value)

        result = await self.session.execute(query)
        return list(result.scalars().all())

    async def get_by_id(self, id: int) -> T:
        query = select(self._model).where(self._model.id == id)
        result = await self.session.execute(query)
        item = result.scalars().first()
        if not item:
            raise ValueError("Item not found")
        return item

    async def get_by_ids(self, ids: list[int]) -> list[T]:
        query = select(self._model).where(self._model.id.in_(ids))
        result = await self.session.execute(query)
        return list(result.scalars().all())

    async def update_by_id(self, id: int, data: Dict[str, Any]) -> T:
        existing_item = await self.get_by_id(id)
        for key, value in data.items():
            if hasattr(existing_item, key):
                setattr(existing_item, key, value)
        await self.session.commit()
        await self.session.refresh(existing_item)

        return existing_item

    async def delete_by_id(self, id: int) -> None:
        item = await self.get_by_id(id)
        await self.session.delete(item)
        await self.session.commit()
