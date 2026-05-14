import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

from auth import router as auth_router, hash_password
from models import db
from cms import router as cms_router

# LOAD ENV VARIABLES
load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://broadcast-platform.onrender.com"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(
    cms_router,
    prefix="/cms",
    tags=["CMS"]
)

# =========================
# LOAD DEFAULT ADMIN ON START
# =========================
@app.on_event("startup")
def startup():

    ADMIN_USERNAME = os.getenv("ADMIN_USERNAME")
    ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD")

    # CREATE ADMIN ONLY IF NOT EXISTS
    if ADMIN_USERNAME and ADMIN_PASSWORD:
        if not db.find_admin(ADMIN_USERNAME):
            db.create_admin(
                username=ADMIN_USERNAME,
                password=hash_password(ADMIN_PASSWORD)
            )

# AUTH ROUTES
app.include_router(
    auth_router,
    prefix="/auth",
    tags=["Authentication"]
)

@app.get("/")
def root():
    return {
        "message": "LFCC Backend Running"
    }
