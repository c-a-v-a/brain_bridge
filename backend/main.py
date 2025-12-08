"""FastAPI backend for BrainBridge app."""

import uvicorn
from contextlib import asynccontextmanager
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.staticfiles import StaticFiles
from uuid import uuid4
import os
from fastapi.middleware.cors import CORSMiddleware

from crud.ideas import get_idea, update_idea
from crud.mongodb_connector import MongoDBConnector
from routers.auth import router as auth_router
from routers.chat import router as chat_router
from routers.ideas import router as ideas_router
from typing import List

app = FastAPI()
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)
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


IMAGE_MIME_TYPES = {
    "image/png",
    "image/jpeg",
    "image/jpg",
    "image/webp",
    "image/gif",
    "image/bmp"
}


@app.post("/api/upload-images/{idea_id}")
async def upload_image(idea_id: str, images: List[UploadFile] = File(...)):
    idea = await get_idea(idea_id)

    if not idea:
        raise HTTPException(404, "Idea not found")

    saved_paths = []

    for image in images:
        if image.content_type not in IMAGE_MIME_TYPES:
            raise HTTPException(400, "File is not an image")

        ext = image.filename.split(".")[-1].lower()

        unique_name = f"{uuid4()}.{ext}"
        file_path = os.path.join(UPLOAD_DIR, unique_name)

        with open(file_path, "wb") as buffer:
            buffer.write(await image.read())

        saved_paths.append(file_path)

    idea.images = saved_paths

    await update_idea(idea_id, idea)

    return {
        "ok": True,
    }


app.mount("/api/uploads", StaticFiles(directory=UPLOAD_DIR), name="uploads")

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
