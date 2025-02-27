from typing import Optional

from schemas.users import UserSchemaAdd, UserSchemaEdit
from utils.unitofwork import IUnitOfWork

from fastapi_users.password import PasswordHelper, PasswordHelperProtocol


class UsersService:
    password_helper: PasswordHelperProtocol

    def __init__(
        self,
        password_helper: Optional[PasswordHelperProtocol] = None,
    ):
        if password_helper is None:
            self.password_helper = PasswordHelper()
        else:
            self.password_helper = password_helper  # pragma: no cover

    async def add_user(self, uow: IUnitOfWork, user: UserSchemaAdd):
        user_dict = user.model_dump()
        async with uow:
            await uow.users.add_one(user_dict)
            await uow.commit()

    async def get_user(self, uow: IUnitOfWork, **filters: dict):
        async with uow:
            user = await uow.users.find_one(**filters)
            return user

    async def get_all_users(self, uow: IUnitOfWork):
        async with uow:
            users = await uow.users.find_all()
            return users

    async def filter_users(self, uow: IUnitOfWork, **filters: dict):
        async with uow:
            users = await uow.users.find_all_by(**filters)
            return users

    async def edit_user(self, uow: IUnitOfWork, id: int, user: UserSchemaEdit):
        async with uow:
            user_dict = user.model_dump()
            password = user_dict.pop("password")
            user_dict["hashed_password"] = self.password_helper.hash(password)
            await uow.users.edit_one(id=id, data=user_dict)
            await uow.commit()

    async def delete_user(self, uow: IUnitOfWork, id: int):
        async with uow:
            await uow.users.delete_one(id=id)
            await uow.commit()
