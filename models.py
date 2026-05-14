
from pymongo import MongoClient
from pydantic import BaseModel

# MONGODB CONNECTION
MONGO_URL = "mongodb+srv://divine4529_db_user:Z9eVtwi8gZp5GkXp@cluster0.xkmltbd.mongodb.net/?appName=Cluster0"

client = MongoClient(MONGO_URL)

db = client["LFCC"]

admins_collection = db["admins"]

# ADMIN MODEL
class AdminLogin(BaseModel):
    username: str
    password: str
