import os

from pymongo import MongoClient
from pydantic import BaseModel
from dotenv import load_dotenv

# =========================
# LOAD ENV VARIABLES
# =========================
load_dotenv()

# =========================
# MONGODB CONNECTION
# =========================
MONGO_URL = os.getenv("MONGO_URL")

if not MONGO_URL:
    raise ValueError("MONGO_URL is missing in .env")

client = MongoClient(MONGO_URL)

db = client["LFCC"]

admins_collection = db["admins"]

# =========================
# ADMIN MODEL
# =========================
class AdminLogin(BaseModel):
    username: str
    password: str
