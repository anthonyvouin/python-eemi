from fastapi import APIRouter, HTTPException, Response
from ..models.student import Student
from ..config.db import get_db_connection

from ..services.student_service import addStudent, check_student_exists
from uuid import UUID, uuid4
import sqlite3
import json

router = APIRouter()




# create a student
@router.post("/")
def read_root(body: Student):
    if body.grades is not None:
        for grade in body.grades:
            grade.identifier =  uuid4()
            
    body.identifier = uuid4()
    addStudent(body)


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
    
   


#delete user by id  
@router.delete("/{identifier}") 
def delete_student(identifier: UUID):
    # Vérifier d'abord si l'étudiant existe
    if not check_student_exists(identifier):
        response = Response(content=json.dumps({"message": "Student not found"}), media_type='application/json')
        response.status_code = 404
        return response

    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Commencer une transaction
        conn.execute("BEGIN")

        try:
            # Supprimer d'abord les notes associées à l'étudiant
            cursor.execute(
                '''DELETE FROM grade WHERE student_id = ?''',
                (str(identifier),)
            )
            grades_deleted = cursor.rowcount

            # Ensuite, supprimer l'étudiant
            cursor.execute(
                '''DELETE FROM student WHERE id = ?''',
                (str(identifier),)
            )

            # Valider la transaction
            conn.commit()

            return {
                "message": f"Student with id {identifier} has been deleted successfully",
                "grades_deleted": grades_deleted
            }

        except sqlite3.Error as e:
            # En cas d'erreur, annuler la transaction
            conn.rollback()
            raise HTTPException(status_code=500, detail="An error occurred while deleting the student and associated grades from the database")

    finally:
        conn.close()

