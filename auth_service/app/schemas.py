from pydantic import BaseModel
from typing import Optional


class UserCreate(BaseModel):
    username: str
    password: str
    role: str
    store_id: Optional[str]
    employee_id: Optional[str]


class UserRead(BaseModel):
    id: str
    username: str
    role: str
    store_id: Optional[str]
    employee_id: Optional[str]
