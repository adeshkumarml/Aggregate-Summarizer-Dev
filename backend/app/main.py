from fastapi import FastAPI
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
from app.storage.redis_client import redis_client
from app.api.routes.upload import router as upload_router
from app.api.routes.status import router as status_router
from app.api.routes.results import router as results_router
from app.api.routes.export import router as export_router

import os
origins = os.getenv("CORS_ALLOW_ORIGINS", "").split(",")

# temporary
import time
import asyncio

async def heartbeat():
    counter = 0
    while True:
        counter += 1
        print(f"[HB {counter}] {time.strftime('%H:%M:%S')}")
        await asyncio.sleep(1)


@asynccontextmanager
async def lifespan(app: FastAPI):
    redis_okay = await redis_client.health_check()
    if not redis_okay:
        raise RuntimeError("Failed to connect to Redis.")
    print("Redis connected successfully!")

    # temporary
    heartbeat_task = asyncio.create_task(heartbeat())

    yield

    # temporary
    heartbeat_task.cancel

    await redis_client.close()
    print("Redis connection closed!")

app = FastAPI(title = "Aggregate_Summarizer", version = "1.0", lifespan = lifespan)
app.add_middleware(CORSMiddleware, allow_origins = origins, allow_credentials = True, allow_methods =["*"], allow_headers = ["*"])

app.include_router(upload_router)
app.include_router(status_router)
app.include_router(results_router)
app.include_router(export_router)

@app.get("/")
async def root():
    return {
        "message": "Aggregate Summarizer API is running. Ver. 1.0"
    }

@app.get("/health")
async def health():
    redis_status = await redis_client.health_check()
    return {
        "status": redis_status
    }
