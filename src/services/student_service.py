from ..models.student import Student
from fastapi import APIRouter, HTTPException
from ..config.db import get_db_connection
import sqlite3
from uuid import UUID, uuid4



def addStudent(body: Student): 
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Insert the student into the student table
        cursor.execute(
            '''INSERT INTO student (id, first_name, last_name, email) VALUES (?, ?, ?, ?)''',
            (str(body.identifier), body.first_name, body.last_name, body.email)
        )


        for grade in body.grades:
            print(grade)
            cursor.execute(
                '''INSERT INTO grade (id, student_id, course, score) VALUES (?, ?, ?, ?)''',
                (str(grade.identifier), str(body.identifier), grade.course, grade.score)
            )

        conn.commit()
        conn.close()

    except sqlite3.Error as e:
        print(e)
        raise HTTPException(status_code=500, detail="An error occurred while inserting the student into the database.")



# service pour check user exist
def check_student_exists(identifier: UUID):
    print(identifier)
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        '''SELECT id FROM student WHERE id = ?''',
        (str(identifier),)
    )
    result = cursor.fetchone()
    conn.close()
    return result is not None


