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
@router.get("/{identifier}")
def get_student(identifier: UUID):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Convertir l'UUID en chaîne
        identifier_str = str(identifier)

        # Récupérer l'étudiant par son identifiant
        cursor.execute(
            '''SELECT id, first_name, last_name, email FROM student WHERE id = ?''',
            (identifier_str,)
        )

        result = cursor.fetchone()
        conn.close()

        if result is None:
            raise HTTPException(status_code=404, detail="Student not found")

        # Créer un objet Student avec les données récupérées
        student = Student(
            identifier=UUID(result[0]),
            first_name=result[1],
            last_name=result[2],
            email=result[3]
        )

        return student

    except sqlite3.Error as e:
        raise HTTPException(status_code=500, detail="An error occurred while retrieving the student from the database")