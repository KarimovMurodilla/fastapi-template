import json
import redis

from fastapi import APIRouter
from fastapi_cache.decorator import cache

from api.dependencies import UOWDep

from schemas.users import UserSchemaEdit
from services.products import BillzService
from utils.cache import Cache


router = APIRouter(
    prefix="/products",
    tags=["Products"],
)

@router.get("")
# @cache(expire=60)
async def get_products(
    limit: int,
    page: int,
):
    start = (page - 1) * limit
    end = start + limit

    cache = Cache()
    data = await cache.redis_client.lrange("products", start, end-1)
    products = [json.loads(item) for item in data]

    if not products:
        products = await BillzService().get_products()
        await cache.set("count", len(products))
        for item in products:
            await cache.redis_client.rpush("products", json.dumps(item))
        await cache.redis_client.expire("products", 600)
        products = products[start:end]

    result = {}
    count = await cache.get("count")
    result["count"] = int(count)
    result["products"] = products

    return result

@router.get("/search")
async def get_products_by_name(
    product_name: str
):
    cache = Cache()
    data = await cache.redis_client.lrange("products", 0, -1)
    all_products = [json.loads(item) for item in data]

    if not all_products:
        products = await BillzService().get_products()
        await cache.set("count", len(products))
        for item in products:
            await cache.redis_client.rpush("products", json.dumps(item))
        await cache.redis_client.expire("products", 600)

    products = [item for item in all_products if item["name"].lower().startswith(product_name.lower())]

    result = {}
    count = await cache.get("count")
    result["count"] = int(count)
    result["products"] = products

    return result

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