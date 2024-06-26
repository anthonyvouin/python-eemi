from pydantic import BaseModel, EmailStr, Field, conint
from typing import List, Optional
from uuid import UUID
from .grade import Grade  


class Student(BaseModel):
    identifier: UUID
    first_name: str
    last_name: str
    email: EmailStr
    grades: Optional[List[Grade]] = None