from fastapi import APIRouter, Depends
from auth import verify_token
from models import db

router = APIRouter()

# =========================
# CREATE BROADCAST
# =========================
@router.post("/broadcast")
def create_broadcast(
    data: dict,
    user=Depends(verify_token)
):

    db.add_broadcast(data)

    return {
        "message": "Broadcast uploaded"
    }


# =========================
# CREATE MESSAGE
# =========================
@router.post("/message")
def create_message(
    data: dict,
    user=Depends(verify_token)
):

    db.add_message(data)

    return {
        "message": "Message uploaded"
    }


# =========================
# CREATE EVENT
# =========================
@router.post("/event")
def create_event(
    data: dict,
    user=Depends(verify_token)
):

    db.add_event(data)

    return {
        "message": "Event uploaded"
    }


# =========================
# GET BROADCASTS
# =========================
@router.get("/broadcasts")
def get_broadcasts():

    return db.get_broadcasts()


# =========================
# GET MESSAGES
# =========================
@router.get("/messages")
def get_messages():

    return db.get_messages()


# =========================
# GET EVENTS
# =========================
@router.get("/events")
def get_events():

    return db.get_events()
