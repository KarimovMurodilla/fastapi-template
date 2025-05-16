from typing import Optional

from fastapi_users.password import PasswordHelper, PasswordHelperProtocol

from schemas.user import UserSchemaAdd, UserSchemaEdit
from utils.unitofwork import IUnitOfWork


class UserService:
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
            await uow.user.add_one(user_dict)
            await uow.commit()

    async def get_user(self, uow: IUnitOfWork, **filters: dict):
        async with uow:
            user = await uow.user.find_one(**filters)
            return user

    async def get_all_users(self, uow: IUnitOfWork):
        async with uow:
            users = await uow.user.find_all()
            return users

    async def filter_users(self, uow: IUnitOfWork, **filters: dict):
        async with uow:
            users = await uow.user.find_all_by(**filters)
            return users

    async def edit_user(self, uow: IUnitOfWork, id: int, user: UserSchemaEdit):
        async with uow:
            user_dict = user.model_dump()
            password = user_dict.pop("password")
            user_dict["hashed_password"] = self.password_helper.hash(password)
            await uow.user.edit_one(id=id, data=user_dict)
            await uow.commit()

    async def delete_user(self, uow: IUnitOfWork, id: int):
        async with uow:
            await uow.user.delete_one(id=id)
            await uow.commit()
