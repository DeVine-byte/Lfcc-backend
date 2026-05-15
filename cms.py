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

    db.broadcasts.insert_one(data)

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

    db.messages.delete_many({})

    db.messages.insert_one(data)

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

    db.events.insert_one(data)

    return {
        "message": "Event uploaded"
    }


# =========================
# GET BROADCASTS
# =========================
@router.get("/broadcasts")
def get_broadcasts():

    broadcasts = list(
        db.broadcasts.find({}, {"_id": 0})
    )

    return broadcasts


# =========================
# GET MESSAGES
# =========================
@router.get("/messages")
def get_messages():

    messages = list(
        db.messages.find({}, {"_id": 0})
    )

    return messages


# =========================
# GET EVENTS
# =========================
@router.get("/events")
def get_events():

    events = list(
        db.events.find({}, {"_id": 0})
    )

    return events
