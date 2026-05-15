from fastapi import APIRouter, Depends
from app.auth import verify_token
from app.models import db

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

# =========================
# DELETE BROADCAST
# =========================
@router.delete("/broadcast/{id}")
def delete_broadcast(
    id: str,
    user=Depends(verify_token)
):

    db.delete_broadcast(id)

    return {
        "message": "Broadcast deleted"
    }

# =========================
# DELETE MESSAGE
# =========================
@router.delete("/message/{id}")
def delete_message(
    id: str,
    user=Depends(verify_token)
):

    db.delete_message(id)

    return {
        "message": "Message deleted"
    }

# =========================
# DELETE EVENT
# =========================
@router.delete("/event/{id}")
def delete_event(
    id: str,
    user=Depends(verify_token)
):

    db.delete_event(id)

    return {
        "message": "Event deleted"
    }
