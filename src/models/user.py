from pydantic import BaseModel
from typing import Optional
from uuid import UUID

class User(BaseModel):
    identifier: Optional[UUID] = None
    username: str
    password: str
