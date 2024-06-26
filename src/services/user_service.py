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

def get_current_user(authorization: str = Header(None)):
    if authorization is None:
        raise HTTPException(status_code=401, detail="Missing authorization header")
    parts = authorization.split()
    print(len(parts))
    if parts[0].lower() != "bearer":
        print('get current user')
        raise HTTPException(status_code=401, detail="Invalid authorization header")
        
    elif len(parts) == 1:
        raise HTTPException(status_code=401, detail="Token not found")
    elif len(parts) > 3:
        raise HTTPException(status_code=401, detail="Invalid authorization header")
    return 'ok'
