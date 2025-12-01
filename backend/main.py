"""FastAPI backend for BrainBridge app."""

import uvicorn
from contextlib import asynccontextmanager
from fastapi import FastAPI, UploadFile, File, HTTPException 
from fastapi.staticfiles import StaticFiles 
from uuid import uuid4 
import os
from fastapi.middleware.cors import CORSMiddleware

from crud.mongodb_connector import MongoDBConnector
from routers.auth import router as auth_router

from crud.mongodb_connector import MongoDBConnector
from routers.auth import router as auth_router
from routers.chat import router as chat_router
from routers.ideas import router as ideas_router

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
@app.post("/api/upload-image")
async def upload_image(file: UploadFile = File(...)):
   
    allowed_ext = {"jpg", "jpeg", "png", "gif", "webp"}
    ext = file.filename.split(".")[-1].lower()

    if ext not in allowed_ext:
        raise HTTPException(status_code=400, detail="Niepoprawny format pliku")


    unique_name = f"{uuid4()}.{ext}"
    file_path = os.path.join(UPLOAD_DIR, unique_name)

  
    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())

  
    return {
        "filename": unique_name,
        "url": f"/uploads/{unique_name}",
    }
app.mount("/uploads", StaticFiles(directory=UPLOAD_DIR), name="uploads")

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
