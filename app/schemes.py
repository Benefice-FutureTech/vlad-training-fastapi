from typing import Optional
from pydantic import BaseModel



class User(BaseModel):
    username: str
    password: str
    email: Optional[str] = None


    class Config:
        orm_mode = True




class ShowUser(BaseModel):
    username: str
    email: str

    class Config:
        orm_mode = True



