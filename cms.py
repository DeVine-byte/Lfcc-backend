from fastapi import APIRouter, Depends
from pydantic import BaseModel
from urllib.parse import urlparse, parse_qs, unquote

from models import db
from auth import verify_token

router = APIRouter()


# =========================
# CLOUDINARY MEDIA HANDLER
# =========================
def cloudinary_to_direct_url(url: str, media_type: str = None) -> str:
    """
    Converts Cloudinary embed URLs into direct playable URLs.
    Auto-detects image vs video if media_type not provided.
    """

    if not url:
        return url

    try:
        parsed = urlparse(url)

        # Already direct URL
        if "res.cloudinary.com" in parsed.netloc:
            return url

        # Only handle embed player URLs
        if "player.cloudinary.com" not in parsed.netloc:
            return url

        query = parse_qs(parsed.query)

        cloud_name = query.get("cloud_name", [None])[0]
        public_id = query.get("public_id", [None])[0]

        if not cloud_name or not public_id:
            return url

        public_id = unquote(public_id)

        # =========================
        # TYPE HANDLING
        # =========================
        if media_type == "image":
            folder = "image/upload"
        elif media_type == "video":
            folder = "video/upload"
        else:
            # fallback auto-detect
            if any(x in public_id.lower() for x in ["image", "img", "photo", "thumbnail"]):
                folder = "image/upload"
            else:
                folder = "video/upload"

        return f"https://res.cloudinary.com/{cloud_name}/{folder}/{public_id}"

    except Exception:
        return url


# =========================
# MODELS
# =========================
class Broadcast(BaseModel):
    title: str
    description: str
    videoUrl: str
    thumbnail: str


class Message(BaseModel):
    title: str
    videoUrl: str


class Event(BaseModel):
    title: str
    mediaUrl: str
    date: str


# =========================
# BROADCAST
# =========================
@router.post("/broadcast")
def save_broadcast(data: Broadcast, user=Depends(verify_token)):
    payload = data.dict()

    payload["videoUrl"] = cloudinary_to_direct_url(payload["videoUrl"], "video")
    payload["thumbnail"] = cloudinary_to_direct_url(payload["thumbnail"], "image")

    db.add_broadcast(payload)

    return {"message": "Broadcast saved"}


# =========================
# MESSAGE
# =========================
@router.post("/message")
def save_message(data: Message, user=Depends(verify_token)):
    payload = data.dict()

    payload["videoUrl"] = cloudinary_to_direct_url(payload["videoUrl"], "video")

    db.add_message(payload)

    return {"message": "Message saved"}


# =========================
# EVENT
# =========================
@router.post("/event")
def save_event(data: Event, user=Depends(verify_token)):
    payload = data.dict()

    payload["mediaUrl"] = cloudinary_to_direct_url(payload["mediaUrl"])

    db.add_event(payload)

    return {"message": "Event saved"}


# =========================
# GET BROADCASTS
# =========================
@router.get("/broadcasts")
def get_broadcasts():
    items = db.get_broadcasts()

    for item in items:
        if "videoUrl" in item:
            item["videoUrl"] = cloudinary_to_direct_url(item["videoUrl"], "video")
        if "thumbnail" in item:
            item["thumbnail"] = cloudinary_to_direct_url(item["thumbnail"], "image")

    return items


# =========================
# GET MESSAGES
# =========================
@router.get("/messages")
def get_messages():
    items = db.get_messages()

    for item in items:
        if "videoUrl" in item:
            item["videoUrl"] = cloudinary_to_direct_url(item["videoUrl"], "video")

    return items


# =========================
# GET EVENTS
# =========================
@router.get("/events")
def get_events():
    items = db.get_events()

    for item in items:
        if "mediaUrl" in item:
            item["mediaUrl"] = cloudinary_to_direct_url(item["mediaUrl"])

    return items
