from fastapi import APIRouter, Depends

from app.models import db
from app.auth import verify_token

router = APIRouter()

# =========================
# SAVE BROADCAST
# =========================
@router.post("/broadcast")
def save_broadcast(data: dict, user=Depends(verify_token)):

    db.add_broadcast(data)

    return {
        "message": "Broadcast saved"
    }

# =========================
# SAVE MESSAGE OF WEEK
# =========================
@router.post("/message")
def save_message(data: dict, user=Depends(verify_token)):

    db.add_message(data)

    return {
        "message": "Message saved"
    }

# =========================
# SAVE EVENT
# =========================
@router.post("/event")
def save_event(data: dict, user=Depends(verify_token)):

    db.add_event(data)

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
