from datetime import date, datetime
from typing import List, Optional

from datetime import date
from pydantic import BaseModel, Field, EmailStr


class UserModel(BaseModel):
    username: str = Field(min_length=3, max_length=16)
    email: str
    password: str = Field(min_length=6, max_length=10)


class UserDb(BaseModel):
    id: int
    username: str
    email: str
    created_at: datetime
    avatar: str

    class Config:
        orm_mode = True


class UserResponse(BaseModel):
    user: UserDb
    detail: str = "User successfully created"


class TokenModel(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class ContactModel(BaseModel):
    firstname: str = Field(max_length=50)
    lastname: str = Field(max_length=50)
    phone_number: str = Field(max_length=50)
    email: EmailStr
    date_of_birth: date
    relationships: str = Field(max_length=50)


class ContactUpdate(ContactModel):
    firstname: str = Field(max_length=50)
    lastname: str = Field(max_length=50)
    phone_number: str = Field(max_length=50)
    email: EmailStr
    date_of_birth: date
    relationships: str = Field(max_length=50)


class ContactResponse(ContactModel):
    id: int
    created_at: date
    firstname: str = Field(max_length=50)
    lastname: str = Field(max_length=50)
    phone_number: str = Field(max_length=50)
    email: EmailStr
    date_of_birth: date
    relationships: str = Field(max_length=50)

    class Config:
        orm_mode = True


class RequestEmail(BaseModel):
    email: EmailStr
