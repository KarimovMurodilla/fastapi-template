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
async def get_products(
    limit: int,
    page: int,
    search: str = None,
):
    start = (page - 1) * limit
    end = start + limit

    cache = Cache()

    if not search:
        print("Not search")
        data = await cache.redis_client.lrange("products", start, end-1)
        products = [json.loads(item) for item in data]

        if not products:
            products = await BillzService().get_products()
            await cache.set("count", len(products))
            for item in products:
                await cache.redis_client.rpush("products", json.dumps(item))
            await cache.redis_client.expire("products", 600)
            products = products[start:end]

    else:
        print("It is search")

        data = await cache.redis_client.lrange("products", 0, -1)
        all_products = [json.loads(item) for item in data]

        if not all_products:
            products = await BillzService().get_products()
            await cache.set("count", len(products))
            for item in products:
                await cache.redis_client.rpush("products", json.dumps(item))
            await cache.redis_client.expire("products", 600)

        products = [item for item in all_products if search.lower() in item["name"].lower()]

    result = {}
    count = await cache.get("count")
    result["count"] = int(count)
    result["products"] = products

    return result
