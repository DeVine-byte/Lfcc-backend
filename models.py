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

client = MongoClient(MONGO_URL)

database = client["LFCC"]

admins_collection = database["admins"]
broadcasts_collection = database["broadcasts"]
messages_collection = database["messages"]
events_collection = database["events"]

# =========================
# SERIALIZER
# =========================
def serialize_document(doc):

    doc["_id"] = str(doc["_id"])

    return doc

# =========================
# DATABASE HELPER CLASS
# =========================
class Database:

    # =========================
    # ADMINS
    # =========================
    def find_admin(self, username):

        return admins_collection.find_one({
            "username": username
        })

    def create_admin(
        self,
        username,
        password
    ):

        return admins_collection.insert_one({
            "username": username,
            "password": password
        })

    # =========================
    # BROADCASTS
    # =========================
    def add_broadcast(self, data):

        return broadcasts_collection.insert_one(data)

    def get_broadcasts(self):

        broadcasts = broadcasts_collection.find()

        return [
            serialize_document(b)
            for b in broadcasts
        ]

    def delete_broadcast(self, id):

        from bson import ObjectId

        return broadcasts_collection.delete_one({
            "_id": ObjectId(id)
        })

    # =========================
    # MESSAGES
    # =========================
    def add_message(self, data):

        messages_collection.delete_many({})

        return messages_collection.insert_one(data)

    def get_messages(self):

        messages = messages_collection.find()

        return [
            serialize_document(m)
            for m in messages
        ]

    def delete_message(self, id):

        from bson import ObjectId

        return messages_collection.delete_one({
            "_id": ObjectId(id)
        })

    # =========================
    # EVENTS
    # =========================
    def add_event(self, data):

        return events_collection.insert_one(data)

    def get_events(self):

        events = events_collection.find()

        return [
            serialize_document(e)
            for e in events
        ]

    def delete_event(self, id):

        from bson import ObjectId

        return events_collection.delete_one({
            "_id": ObjectId(id)
        })

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
