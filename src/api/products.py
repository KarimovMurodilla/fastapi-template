from fastapi import APIRouter
from fastapi_cache.decorator import cache

from api.dependencies import UOWDep

from schemas.users import UserSchemaEdit
from services.products import BillzService


router = APIRouter(
    prefix="/products",
    tags=["Products"],
)

@router.get("/products")
@cache(expire=60)
async def get_user(
    uow: UOWDep,
    limit: int,
    page: int,
    search: str = None
):
    products = await BillzService().get_products(limit, page, search)
    return products

# @router.get("/name/{name}")
# async def get_user_by_name(
#     uow: UOWDep,
#     name: str
# ):
#     user = await UsersService().get_user(uow, name=name)
#     return user

# @router.get("/all")
# async def get_all_users(
#     uow: UOWDep
# ):
#     users = await UsersService().get_all_users(uow)
#     return users

# @router.get("/filter")
# async def filter_users_by_name(
#     uow: UOWDep,
#     name: str
# ):
#     users = await UsersService().filter_users(uow, name=name)
#     return users

# @router.patch("/edit")
# async def edit_user(
#     id: int,
#     user: UserSchemaEdit,
#     uow: UOWDep,
# ):
#     await UsersService().edit_user(uow, id, user)
#     return {"ok": True}

# @router.delete("/delete")
# async def delete_user(
#     id: int,
#     uow: UOWDep
# ):

#     await UsersService().delete_user(uow, id)
#     return {"ok": True}