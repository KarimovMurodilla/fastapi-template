from api.auth_user import router_auth, router_jwt
from api.user import router as router_user

all_routers = [router_jwt, router_auth, router_user]
