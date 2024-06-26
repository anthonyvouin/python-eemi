from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from ..models.student import Student
from ..models.grade import Grade
from ..config.db import get_db_connection
from uuid import UUID, uuid4
import sqlite3
import json
import io
import csv

router = APIRouter()

# Get an export from all the data in the database
@router.get("/{format}")
def read_root(format: str):
    try:
        conn = get_db_connection()
        cursorStudent = conn.cursor()
        cursorGrade = conn.cursor()

        # Get all data from the database
        cursorStudent.execute("SELECT * FROM student")
        cursorGrade.execute("SELECT * FROM grade")

        rowsStudent = cursorStudent.fetchall()
        rowsGrade = cursorGrade.fetchall()

        # Create a list of students
        students = []
        for rowStudent in rowsStudent:
            student = dict(rowStudent) # On transforme l'élément de type Row en dictionnaire pour pouvoir l'utiliser après
            students.append(student)
        
        # Create a list of grades
        grades = []
        for rowGrade in rowsGrade:
            grade = dict(rowGrade) # On transforme l'élément de type Row en dictionnaire pour pouvoir l'utiliser après
            grades.append(grade)

        # Associate the grades with the students
        for student in students:
            student["grades"] = []
            for grade in grades:
                if student["id"] == grade["student_id"]:
                    student["grades"].append(grade["score"])

        # Return the data in the requested format
        if format == "json":
            return students
        
        elif format == "csv":
            output = io.StringIO()
            # Headers du CSV
            output.write("student_id,first_name,last_name,email,grades\n")
            # On écrit les données dans le CSV
            for student in students:
                grades_str = "|".join(map(str, student["grades"]))  # Convert list of grades to a pipe-separated string
                output.write(f"{student['id']},{student['first_name']},{student['last_name']},{student['email']},{grades_str}\n")
            output.seek(0)

            response = StreamingResponse(output, media_type="text/csv")
            response.headers["Content-Disposition"] = "attachment; filename=students.csv"
            return response

        else:
            raise HTTPException(status_code=400, detail="Invalid format")

    except sqlite3.Error as e:
        raise HTTPException(status_code=500, detail="Database error")
