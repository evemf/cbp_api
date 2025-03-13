from pydantic import BaseModel

class UserBase(BaseModel):
    email: str

    class Config:
        from_attributes = True  

class UserCreate(UserBase):
    password: str

class UserRead(UserBase):
    id: int

    class Config:
        from_attributes = True

class UserUpdate(BaseModel): 
    email: str | None = None
    password: str | None = None

    class Config:
        from_attributes = True
