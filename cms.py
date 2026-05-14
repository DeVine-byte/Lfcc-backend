
from fastapi import APIRouter, Depends
from pydantic import BaseModel

from models import db
from auth import verify_token

router = APIRouter()


# =========================
# BROADCAST MODEL
# =========================
class Broadcast(BaseModel):
    title: str
    description: str
    videoUrl: str
    thumbnail: str


# =========================
# MESSAGE MODEL
# =========================
class Message(BaseModel):
    title: str
    videoUrl: str


# =========================
# EVENT MODEL
# =========================
class Event(BaseModel):
    title: str
    mediaUrl: str
    date: str

# =========================
# SAVE BROADCAST
# =========================
@router.post("/broadcast")
def save_broadcast(
    data: Broadcast,
    user=Depends(verify_token)
):
    db.add_broadcast(data.dict())

    return {
        "message": "Broadcast saved"
    }


# =========================
# SAVE MESSAGE OF WEEK
# =========================
@router.post("/message")
def save_message(
    data: Message,
    user=Depends(verify_token)
):
    db.add_message(data.dict())

    return {
        "message": "Message saved"
    }


# =========================
# SAVE EVENT
# =========================
@router.post("/event")
def save_event(
    data: Event,
    user=Depends(verify_token)
):
    db.add_event(data.dict())

    return {
        "message": "Event saved"
    }


# =========================
# GET DATA
# =========================
@router.get("/broadcasts")
def get_broadcasts():
    return db.get_broadcasts()


@router.get("/messages")
def get_messages():
    return db.get_messages()


@router.get("/events")
def get_events():
    return db.get_events()
