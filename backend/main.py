"""
Test module for FastAPI backend.
"""
import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List

app = FastAPI()
origins = [ "http://localhost:5173" ]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


class Message(BaseModel):
    name: str
    message: str


messages: List[Message] = []


@app.get("/api/message")
def get_message():
    if not messages:
        raise HTTPException(status_code=204,
                            detail="No messages left on the stack")
    else:
        return messages.pop(0)


@app.post("/api/message")
def add_message(message: Message):
    messages.append(message)
    return {"status": "success", "message": message}


if __name__ == "__main__":
    uvicorn.run("main:app", port=8000, log_level="info")
