from abc import ABC, abstractmethod
from typing import Type

from db.db import async_session_maker
from repositories.users import UserRepository


# https://github1s.com/cosmicpython/code/tree/chapter_06_uow
class IUnitOfWork(ABC):
    user: Type[UserRepository]

    @abstractmethod
    def __init__(self): ...

    @abstractmethod
    async def __aenter__(self): ...

    @abstractmethod
    async def __aexit__(self, *args): ...

    @abstractmethod
    async def commit(self): ...

    @abstractmethod
    async def rollback(self): ...


class UnitOfWork:
    session_factory = async_session_maker

    async def __aenter__(self):
        self.session = UnitOfWork.session_factory()

        self.user = UserRepository(self.session)

    async def __aexit__(self, *args):
        await self.rollback()
        await self.session.close()

    async def commit(self):
        await self.session.commit()

    async def rollback(self):
        await self.session.rollback()

    @staticmethod
    def dependency_overrides(session):
        UnitOfWork.session_factory = session
