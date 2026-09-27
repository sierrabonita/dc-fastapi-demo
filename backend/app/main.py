from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.todos import router as todos_router
from app.core.db import create_db_and_tables


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield


app = FastAPI(title="Backend API", version="1.0.0", lifespan=lifespan)
app.include_router(todos_router)


@app.get("/")
def read_root():
    return {"message": "Welcome to FastAPI Backend"}
