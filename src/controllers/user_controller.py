
from fastapi import APIRouter,HTTPException, Response, Header
from ..models.user import User
from uuid import UUID, uuid4
from ..config.db import get_db_connection
import sqlite3
import bcrypt
import json
from datetime import datetime, timedelta
import jwt

router = APIRouter()


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


@router.post("/")
def create_account(body: User):
    try:
        identifier = uuid4()

        conn = get_db_connection()
        cursor = conn.cursor()

        password_bytes = body.password.encode('utf-8')

        # Générer un sel et hacher le mot de passe
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password_bytes, salt)

        cursor.execute(
            '''INSERT INTO user (id, username, password) VALUES (?, ?, ?)''',
            (str(identifier), body.username, hashed_password)
        )

        conn.commit()
        conn.close()

        # Après la création du compte, générer un token JWT
        token = create_jwt_token(body.username)

        return {"message": "User created successfully", "access_token": token, "token_type": "bearer"}

    except sqlite3.Error as e:
        print(e)
        raise HTTPException(status_code=500, detail="An error occurred while inserting the user into the database.")



@router.post("/login")
def login(body: User):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute(
            '''SELECT id, username, password FROM user WHERE username = ?''',
            (body.username,)
        )

        user = cursor.fetchone()

        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        stored_password = user['password']  # Le mot de passe est déjà en bytes

        if bcrypt.checkpw(body.password.encode('utf-8'), stored_password):
            token = create_jwt_token(body.username)
            return {"message": "Login successful", "access_token": token, "token_type": "bearer"}
        else:
            raise HTTPException(status_code=401, detail="Invalid credentials")

    except sqlite3.Error as e:
        print(e)
        raise HTTPException(status_code=500, detail="An error occurred while querying the database.")
    finally:
        conn.close()
