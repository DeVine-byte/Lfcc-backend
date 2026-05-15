import os

from pymongo import MongoClient
from pydantic import BaseModel
from dotenv import load_dotenv

# LOAD ENV VARIABLES
load_dotenv()

# =========================
# MONGODB CONNECTION
# =========================
MONGO_URL = os.getenv("MONGO_URL")

client = MongoClient(MONGO_URL)

database = client["LFCC"]

admins_collection = database["admins"]
broadcasts_collection = database["broadcasts"]
messages_collection = database["messages"]
events_collection = database["events"]

# =========================
# DATABASE HELPER CLASS
# =========================
class Database:

    # ADMINS
    def find_admin(self, username):
        return admins_collection.find_one({
            "username": username
        })

    def create_admin(self, username, password):

        return admins_collection.insert_one({
            "username": username,
            "password": password
        })

    # BROADCASTS
    def add_broadcast(self, data):
        return broadcasts_collection.insert_one(data)

    def get_broadcasts(self):
        return list(
            broadcasts_collection.find(
                {},
                {"_id": 0}
            )
        )

    # MESSAGES
    def add_message(self, data):
        messages_collection.delete_many({})
        return messages_collection.insert_one(data)

    def get_messages(self):
        return list(
            messages_collection.find(
                {},
                {"_id": 0}
            )
        )

    # EVENTS
    def add_event(self, data):
        return events_collection.insert_one(data)

    def get_events(self):
        return list(
            events_collection.find(
                {},
                {"_id": 0}
            )
        )

# =========================
# DATABASE INSTANCE
# =========================
db = Database()

# =========================
# ADMIN MODEL
# =========================
class AdminLogin(BaseModel):
    username: str
    password: str
