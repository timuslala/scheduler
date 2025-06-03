from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session, select
from back.models import User, Store, Employee, Schedule
from back.schemas import UserCreate, UserRead, ScheduleCreate, ScheduleRead
from back.auth import create_access_token, get_current_user
from back.crud import create_user, get_store, get_employee_schedules
from back.dependencies import get_db
from back.tasks import generate_schedule_task
from typing import List
import uuid

app = FastAPI(title="Employee Scheduling API")

@app.post("/register", response_model=UserRead)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = create_user(db, user)
    return db_user

@app.post("/token")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.exec(select(User).where(User.username == form_data.username)).first()
    if not user or not user.verify_password(form_data.password):
        raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect username or password",
        headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user.username, "role": user.role, "store_id": user.store_id})
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/schedules", response_model=ScheduleRead)
def create_schedule(
    schedule: ScheduleCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
    ):
    if current_user.role not in ["store_manager", "network_manager"]:
        raise HTTPException(status_code=403, detail="Not authorized")

    schedule_id = str(uuid.uuid4())
    task = generate_schedule_task.apply_async(
    args=[schedule_id, schedule.store_id, schedule.dict()],
    queue="schedule_queue"
    )

    db_schedule = Schedule(id=schedule_id, store_id=schedule.store_id, status="pending")
    db.add(db_schedule)
    db.commit()
    db.refresh(db_schedule)
    return db_schedule

@app.get("/schedules", response_model=List[ScheduleRead])
def get_schedules(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if current_user.role == "employee":
        return get_employee_schedules(db, current_user.employee_id)
    elif current_user.role == "store_manager":
        store = get_store(db, current_user.store_id)
        return store.schedules
    elif current_user.role == "network_manager":
        return db.exec(select(Schedule)).all()
    raise HTTPException(status_code=403, detail="Not authorized")