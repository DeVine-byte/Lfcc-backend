import os
from fastapi import APIRouter, Depends, HTTPException
from jose import jwt, JWTError
from datetime import datetime, timedelta

from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

security = HTTPBearer()


from models import AdminLogin, db

router = APIRouter()

# =========================
# ARGON2 PASSWORD HASHER
# =========================
ph = PasswordHasher()

# =========================
# JWT CONFIG
# =========================
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")

# =========================
# PASSWORD FUNCTIONS
# =========================
def hash_password(password: str):
    return ph.hash(password)

def verify_password(plain_password, hashed_password):
    try:
        ph.verify(hashed_password, plain_password)
        return True
    except VerifyMismatchError:
        return False

# =========================
# JWT TOKEN CREATION
# =========================
def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(days=1)
    to_encode.update({"exp": expire})
    return jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

def verify_token(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):

    try:
        token = credentials.credentials

        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        username = payload.get("username")

        if username is None:
            raise HTTPException(
                status_code=401,
                detail="Invalid token"
            )

        return username

    except JWTError:

        raise HTTPException(
            status_code=401,
            detail="Token invalid or expired"
        )

# =========================
# LOGIN ROUTE
# =========================
@router.post("/login")
async def login(data: AdminLogin):

    # FIND ADMIN IN LOCAL DB
    admin = db.find_admin(data.username)

    if not admin:
        raise HTTPException(
            status_code=401,
            detail="Invalid username"
        )

    # VERIFY PASSWORD
    if not verify_password(data.password, admin["password"]):
        raise HTTPException(
            status_code=401,
            detail="Invalid password"
        )

    # CREATE TOKEN
    token = create_access_token({
        "username": admin["username"]
    })

    return {
        "access_token": token,
        "token_type": "bearer"
    }
