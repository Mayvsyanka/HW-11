from datetime import date
from typing import List, Optional

from datetime import date
from pydantic import BaseModel, Field, EmailStr


class ContactModel(BaseModel):
    firstname: str = Field(max_length=50)
    lastname: str = Field(max_length=50)
    phone_number: str = Field(max_length=50)
    email: EmailStr
    date_of_birth: date
    relationship: str = Field(max_length=50)


class ContactUpdate(ContactModel):
    firstname: str = Field(max_length=50)
    lastname: str = Field(max_length=50)
    phone_number: str = Field(max_length=50)
    email: EmailStr
    date_of_birth: date
    relationship: str = Field(max_length=50)


class ContactResponse(ContactModel):
    id: int
    created_at: date
    firstname: str = Field(max_length=50)
    lastname: str = Field(max_length=50)
    phone_number: str = Field(max_length=50)
    email: EmailStr
    date_of_birth: date

    class Config:
        orm_mode = True
