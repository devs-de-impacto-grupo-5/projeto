from pydantic import BaseModel, EmailStr
from typing import Optional

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    senha: str
    role: Optional[str] = None  # Optional role, accepts any string