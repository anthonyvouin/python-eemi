from fastapi import APIRouter, HTTPException, Response
from ..models.student import Student
from ..models.grade import Grade
from ..config.db import get_db_connection
from ..services.student_service import add_student, check_student_exists, get_student_by_identifier, delete_student_by_identifier, get_grade_by_student, delete_grade_by_student
from uuid import UUID, uuid4
import sqlite3
import json

router = APIRouter()

# create a student
@router.post("/")
def read_root(body: Student):
    add_student(body)
    return body.identifier

#return a student by id
@router.get("/{identifier}")
def get_student(identifier: str):
   return get_student_by_identifier(identifier)
    
    

#delete user by id  
@router.delete("/{identifier}") 
def delete_student(identifier: UUID):
    return  delete_student_by_identifier(str(identifier))


# recuperer une note d'un etudiant
@router.get("/{student_id}/grades/{grade_id}", response_model=Grade)
def get_grade(student_id: str, grade_id: str):   
    return get_grade_by_student(student_id, grade_id)
   
    
#supprimer une note d'un etudiant en fonction de l'id de l"etudiant
@router.delete("/{student_id}/grades/{grade_id}")
def delete_grade(student_id: UUID, grade_id: UUID):
    return delete_grade_by_student(str(student_id), str(grade_id))
