from api.auth_user import router_jwt, router_auth
from api.user import router as router_user

all_routers = [
    router_jwt,
    router_auth,

    router_user
]
