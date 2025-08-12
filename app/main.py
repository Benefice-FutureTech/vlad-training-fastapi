from fastapi import FastAPI, HTTPException, Depends
from sqlmodel import Session, select
from .database import engine, init_db
from .models import User as UserModel
from .schemes import User as UserSchema, ShowUser
from typing import List
app = FastAPI()

def get_session():
    with Session(engine) as session:
        yield session


@app.on_event("startup")
def on_startup():
    init_db()

@app.post("/users/", response_model=ShowUser)
def create_user(user: UserSchema, session: Session = Depends(get_session)):
    new_user = UserModel(username=user.username, email = user.email, password=user.password)    
    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    return new_user

@app.get("/users/", response_model=List[ShowUser])
def read_users(session: Session = Depends(get_session)):
    return session.exec(select(UserModel)).all()


@app.get("/users/{user_id}", response_model=ShowUser)
def read_user(user_id: int,session: Session = Depends(get_session)):
    user = session.get(UserModel, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.put("/users/{user_id}", response_model=ShowUser)
def update_user(user_id: int, new_data: UserSchema, session: Session = Depends(get_session)):
    user = session.get(UserModel, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user.username = new_data.username
    user.email = new_data.email
    session.commit()
    session.refresh(user)
    return user


@app.delete("/users/{user_id}")
def delete_user(user_id: int, session: Session = Depends(get_session)):
    user = session.get(UserModel, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    session.delete(user)
    session.commit()
    return {"message": "User deleted"}
