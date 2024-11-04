from pydantic import BaseModel, EmailStr, constr, ValidationError
from typing import Optional

class UserBase(BaseModel):
    first_name: constr(min_length=1, max_length=50)
    last_name: constr(min_length=1, max_length=50)
    email: EmailStr
    access_level: constr(regex='^(admin|common)$')
    status: Optional[constr(regex='^(active|canceled)$')] = 'active'

class UserCreate(UserBase):
    password: constr(min_length=6)

class UserUpdate(BaseModel):
    first_name: Optional[constr(min_length=1, max_length=50)]
    last_name: Optional[constr(min_length=1, max_length=50)]
    email: Optional[EmailStr]
    password: Optional[constr(min_length=6)]
    access_level: Optional[constr(regex='^(admin|common)$')]
    status: Optional[constr(regex='^(active|canceled)$')]

class UserResponse(UserBase):
    id: int

    class Config:
        orm_mode = True
