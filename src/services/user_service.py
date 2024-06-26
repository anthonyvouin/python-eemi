import jwt
from fastapi import APIRouter,HTTPException, Response, Header
from datetime import datetime, timedelta

SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_jwt_token(username: str) -> str:
    payload = {"sub": username, "exp": datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)}
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return token


def get_token(authorization: str = Header(None)):
    if authorization is None:
        raise HTTPException(status_code=401, detail="Missing authorization header")
    parts = authorization.split()
    if parts[0].lower() != "bearer":
        raise HTTPException(status_code=401, detail="Invalid authorization header")
    elif len(parts) == 1:
        raise HTTPException(status_code=401, detail="Token not found")
    elif len(parts) > 2:
        raise HTTPException(status_code=401, detail="Invalid authorization header")
    token = parts[1]
    return token