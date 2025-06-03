import uuid
from passlib.context import CryptContext
from sqlmodel import SQLModel, Field
from typing import Optional

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class User(SQLModel, table=True):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    username: str = Field(index=True, unique=True)
    hashed_password: str
    role: str  # "employee", "store_manager", "network_manager"
    store_id: Optional[str] = Field(foreign_key="store.id", nullable=True)
    employee_id: Optional[str] = Field(foreign_key="employee.id", nullable=True)


def verify_password(self, password: str) -> bool:
    return pwd_context.verify(password, self.hashed_password)
