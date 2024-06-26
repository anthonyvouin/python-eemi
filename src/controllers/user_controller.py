
from fastapi import APIRouter,HTTPException, Response
from ..models.user import User
from uuid import UUID, uuid4
from ..config.db import get_db_connection
import sqlite3
import bcrypt
import json
router = APIRouter()

@router.post("/")
def createAccount(body: User):
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
      response = Response(content=json.dumps({"message": "created user"}), media_type='application/json')
      response.status_code = 201
      return response
   except sqlite3.Error as e:
        print(e)
        raise HTTPException(status_code=500, detail="An error occurred while inserting the student into the database.")


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
            return {"message": "Login successful"}
        else:
            raise HTTPException(status_code=401, detail="Invalid credentials")

    except sqlite3.Error as e:
        print(e)
        raise HTTPException(status_code=500, detail="An error occurred while querying the database.")
    finally:
        conn.close()
