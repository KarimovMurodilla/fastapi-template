import uvicorn
from fastapi import FastAPI

from api.routers import all_routers

app = FastAPI(title="Users")

for router in all_routers:
    if isinstance(router, dict):
        app.include_router(**router)

    else:
        app.include_router(router)


if __name__ == "__main__":
    uvicorn.run(app="main:app", reload=True)
