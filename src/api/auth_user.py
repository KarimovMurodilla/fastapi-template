from fastapi_users import FastAPIUsers

from auth.auth import auth_backend
from auth.manager import get_user_manager
from db.models.user import User
from schemas.user import UserSchema, UserSchemaAdd

fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)


router_jwt = {
    "router": fastapi_users.get_auth_router(auth_backend),
    "prefix": "/auth/jwt",
    "tags": ["Auth"],
}


router_auth = {
    "router": fastapi_users.get_register_router(UserSchema, UserSchemaAdd),
    "prefix": "/auth",
    "tags": ["Auth"],
}


current_user = fastapi_users.current_user()
