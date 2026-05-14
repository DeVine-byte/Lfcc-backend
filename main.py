from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.auth import router as auth_router, hash_password
from app.models import db
from app.cms import router as cms_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
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
    if not db.find_admin("admin"):
        db.create_admin(
            username="admin",
            password=hash_password("admin")
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
