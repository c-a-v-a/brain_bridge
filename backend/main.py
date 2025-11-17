"""FastAPI backend for BrainBridge app."""

import uvicorn
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from crud.mongodb_connector import MongoDBConnector
from routers.auth import router as auth_router

from crud.mongodb_connector import MongoDBConnector
from routers.auth import router as auth_router
from routers.chat import router as chat_router
from routers.ideas import router as ideas_router

app = FastAPI()
origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router, prefix="/api")
app.include_router(chat_router, prefix="/api")
app.include_router(ideas_router, prefix="/api")


@asynccontextmanager
async def lifespan():
    """Define the app lifecycle."""
    # startup code
    yield
    # shutdown code
    client = MongoDBConnector()
    client.close()


if __name__ == "__main__":
    uvicorn.run("main:app", port=8000, log_level="info")
