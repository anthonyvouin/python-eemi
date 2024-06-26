from pydantic import BaseModel, EmailStr, Field, conint
from typing import List, Optional
from uuid import UUID

class Grade(BaseModel):
    identifier: UUID
    course: str