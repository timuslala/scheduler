import uuid
from sqlmodel import SQLModel, Field, Relationship
from typing import List, Optional
from passlib.context import CryptContext
from datetime import datetime
7
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class User(SQLModel, table=True):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    username: str = Field(index=True, unique=True)
    hashed_password: str
    role: str  # "employee", "store_manager", "network_manager"
    store_id: Optional[str] = Field(foreign_key="store.id", nullable=True)
    employee_id: str = Field(foreign_key="employee.id")

def verify_password(self, password: str) -> bool:
    return pwd_context.verify(password, self.hashed_password)

class Store(SQLModel, table=True):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    name: str
    employees: List["Employee"] = Relationship(back_populates="store")
    schedules: List["Schedule"] = Relationship(back_populates="store")

class Employee(SQLModel, table=True):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    name: str
    store_id: str = Field(foreign_key="store.id")
    skills: List[str] = Field(default_factory=list)
    availability: dict = Field(default_factory=dict)
    store: Store = Relationship(back_populates="employees")
    schedules: List["Schedule"] = Relationship(back_populates="employees")

class Schedule(SQLModel, table=True):
    id: str = Field(primary_key=True)
    store_id: str = Field(foreign_key="store.id")
    employee_id: Optional[str] = Field(foreign_key="employee.id", nullable=True)
    start_time: datetime
    end_time: datetime
    status: str = Field(default="pending")  # "pending", "completed", "failed"
    store: Store = Relationship(back_populates="schedules")
    employee: Optional[Employee] = Relationship(back_populates="schedules")