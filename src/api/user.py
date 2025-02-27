"""
Users API example
"""

from fastapi import APIRouter

from api.dependencies import UOWDep

router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


@router.get("")
async def get_users(uow: UOWDep, limit: int, page: int, search: str = None):
    pass
