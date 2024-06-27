from ..models.student import Student
from ..models.grade import Grade
from fastapi import APIRouter, HTTPException, Response
from ..config.db import get_db_connection
import sqlite3
from uuid import UUID, uuid4
import json

# pour créer un étudiant avec ses notes
def add_student(body: Student): 
    try:
        body.identifier = uuid4()
        conn = get_db_connection()
        cursor = conn.cursor()

        # Insert the student into the student table
        cursor.execute(
            '''INSERT INTO student (id, first_name, last_name, email) VALUES (?, ?, ?, ?)''',
            (str(body.identifier), body.first_name, body.last_name, body.email)
        )

        if body.grades is not None:

            for grade in body.grades:
                grade.identifier =  uuid4()
                cursor.execute(
                    '''INSERT INTO grade (id, student_id, course, score) VALUES (?, ?, ?, ?)''',
                    (str(grade.identifier), str(body.identifier), grade.course, grade.score)
                )

        conn.commit()
        conn.close()

    except sqlite3.Error as e:
        print(e)
        raise HTTPException(status_code=500, detail="An error occurred while inserting the student into the database.")

# pour voir un étudiant avec ses notes
def get_student_by_identifier(identifier: str):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Récupérer l'étudiant par son identifiant
        cursor.execute(
            '''SELECT id, first_name, last_name, email FROM student WHERE id = ?''',
            (identifier,)
        )

        result = cursor.fetchone()
        if result is None:
            raise HTTPException(status_code=404, detail="Student not found")

        # Créer un objet Student avec les données récupérées
        student = {
            "id": result['id'],
            "first_name": result['first_name'],
            "last_name": result['last_name'],
            "email": result['email'],
            "grades": []
        }

        # Récupérer les grades de l'étudiant
        cursor.execute(
            '''SELECT id, course, score FROM grade WHERE student_id = ?''',
            (identifier,)
        )

        grades = []
        for row in cursor.fetchall():
            grade = {
                "id": row['id'],
                "course": row['course'],
                "score": row['score']
            }
            grades.append(grade)

        conn.close()

        # Ajouter les grades à l'objet Student
        student["grades"] = grades

        return student

    except sqlite3.Error as e:
        raise HTTPException(status_code=500, detail="An error occurred while retrieving the student and grades from the database")

# supprimer un étudiant par son identifiant
def delete_student_by_identifier(identifier: str):
    # Vérifier d'abord si l'étudiant existe
    if not check_student_exists(str(identifier)):
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
                (identifier,)
            )
            grades_deleted = cursor.rowcount

            # Ensuite, supprimer l'étudiant
            cursor.execute(
                '''DELETE FROM student WHERE id = ?''',
                (identifier,)
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

# voir une note d'un étudient
def get_grade_by_student(student_id: str, grade_id: str):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Récupérer le grade spécifique par son identifiant et celui de l'étudiant
        cursor.execute(
            '''SELECT id, student_id, course, score FROM grade WHERE student_id = ? AND id = ?''',
            (student_id, grade_id)
        )

        result = cursor.fetchone()
        conn.close()

        if result is None:
            raise HTTPException(status_code=404, detail="Grade not found")

        # Créer un objet Grade avec les données récupérées
        grade = Grade(
            identifier=result['id'],  # Assurez-vous d'utiliser 'identifier' ici
            student_id=result['student_id'],
            course=result['course'],
            score=result['score']
        )

        return grade

    except sqlite3.Error as e:
        raise HTTPException(status_code=500, detail="An error occurred while retrieving the grade from the database")
    
def delete_grade_by_student(student_id: str, grade_id: str):
      # Vérifier si l'étudiant existe
    if not check_student_exists(student_id):
        response = Response(content=json.dumps({"message": "Student not found"}), media_type='application/json')
        response.status_code = 404
        return response

    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Vérifier si la note existe et appartient à l'étudiant
        cursor.execute(
            '''SELECT id FROM grade WHERE id = ? AND student_id = ?''',
            (str(grade_id), str(student_id))
        )
        result = cursor.fetchone()

        if result is None:
            response = Response(content=json.dumps({"message": "Grade not found"}), media_type='application/json')
            response.status_code = 404
            return response

        # Supprimer la note
        cursor.execute(
            '''DELETE FROM grade WHERE id = ?''',
            (str(grade_id),)
        )
        conn.commit()
        conn.close()

        return {
            "message": f"Grade with id {grade_id} for student {student_id} has been deleted successfully"
        }

    except sqlite3.Error as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail="An error occurred while deleting the grade from the database")

    finally:
        conn.close()


# pour check si un étudiant existe
def check_student_exists(identifier: str):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        '''SELECT id FROM student WHERE id = ?''',
        (identifier,)
    )
    result = cursor.fetchone()
    conn.close()
    return result is not None



