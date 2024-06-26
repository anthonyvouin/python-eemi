from fastapi import APIRouter, HTTPException
from ..models.student import Student
from ..config.db import get_db_connection
from uuid import UUID, uuid4
import sqlite3

router = APIRouter()




# create a student
@router.post("/")
def read_root(body: Student):

    body.identifier = uuid4()

    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Insert the student into the student table
        cursor.execute(
            '''INSERT INTO student (id, first_name, last_name, email) VALUES (?, ?, ?, ?)''',
            (str(body.identifier), body.first_name, body.last_name, body.email)
        )

        conn.commit()
        conn.close()

    except sqlite3.Error as e:
        raise HTTPException(status_code=500, detail="An error occurred while inserting the student into the database.")

    return body.identifier


#return a student by id
@router.get("/")
def read_root():
   return "coucou"