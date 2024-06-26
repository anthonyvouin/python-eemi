from pydantic import BaseModel, EmailStr, Field, conint
from typing import List, Optional
from uuid import UUID

class Grade(BaseModel):
    identifier: UUID
    course: str
    score: conint(ge=0, le=100)  # Score should be between 0 and 100
