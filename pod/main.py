from app.my_config import get_settings
from app.my_database import DBSession, UserModel, init_db
from sqlalchemy import select
from app.my_redis import cache_manager

from contextlib import asynccontextmanager

from fastapi import FastAPI
from prometheus_fastapi_instrumentator import Instrumentator

settings = get_settings()


@asynccontextmanager
async def app_lifespan(_: FastAPI):
    await init_db()
    instrumentator.expose(app)
    yield


app: FastAPI = FastAPI(lifespan=app_lifespan)
instrumentator = Instrumentator().instrument(app)


@app.get(path="/")
async def entity() -> dict:
    await cache_manager.incr()
    return {
        "message": "Kronk Deployment!",
        "DB_URL": settings.DB_URL,
        "REDIS_URL": settings.REDIS_URL,
        "Total visits": await cache_manager.total_visits()
    }


@app.get(path="/healthy")
async def root(session: DBSession) -> dict:
    users = (await session.execute(select(UserModel))).scalars().all()
    return {
        "redis_ready": "🚀",
        "users usernames(sqlalchemy)": [user.username for user in users]
    }
