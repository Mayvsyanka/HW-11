from typing import List

from fastapi import APIRouter, HTTPException, Depends, status, Query
from sqlalchemy.orm import Session

from src.database.db import get_db
from src.schemas import ContactModel, ContactUpdate, ContactResponse
from src.repository import contacts as repository_contacts
from src.database.models import Contact, User
from src.services.auth import auth_service


router = APIRouter(prefix='/contacts', tags=["contacts"])


@router.get("/find", response_model=List[ContactResponse])
async def find_contacts(
    firstname: str = Query(None),
    lastname: str = Query(None),
    email: str = Query(None), db: Session = Depends(get_db),
    user: User = Depends(auth_service.get_current_user)
) -> List[Contact]:
    contacts = await repository_contacts.find_contacts(db, firstname, lastname, email)
    if contacts is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return contacts


@router.get("/nearest_birthdays", response_model=List[ContactResponse])
async def nearest_birthdays(user: User = Depends(auth_service.get_current_user), db: Session = Depends(get_db)):

    contacts = await repository_contacts.get_birthdays(db)
    if contacts is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return contacts


@router.get("/", response_model=List[ContactResponse])
async def read_contacts(current_user: User = Depends(auth_service.get_current_user), skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    contacts = await repository_contacts.get_contacts(current_user ,skip, limit, db)
    return contacts


@router.get("/{contact_id}", response_model=ContactResponse)
async def read_contact(contact_id: int, user: User = Depends(auth_service.get_current_user), db: Session = Depends(get_db)):
    contact = await repository_contacts.get_contact(contact_id, user, db)
    if contact is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return contact


@router.post("/", response_model=ContactResponse)
async def create_contact(body: ContactModel, user: User = Depends(auth_service.get_current_user), db: Session = Depends(get_db)):
    return await repository_contacts.create_contact(body, user, db)


@router.put("/{contact_id}", response_model=ContactResponse)
async def update_contact(body: ContactUpdate, contact_id: int, user: User = Depends(auth_service.get_current_user), db: Session = Depends(get_db)):
    contact = await repository_contacts.update_contact(contact_id, user, body, db)
    if contact is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return contact


@router.delete("/{contact_id}", response_model=ContactResponse)
async def remove_contact(contact_id: int, user: User = Depends(auth_service.get_current_user), db: Session = Depends(get_db)):
    contact = await repository_contacts.remove_contact(user, contact_id, db)
    if contact is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return contact


@router.get("/bday_soon", response_model=List[ContactResponse])
async def nearest_birthdays(user: User = Depends(auth_service.get_current_user), db: Session = Depends(get_db)):

    contacts = await repository_contacts.birthdays(user, db)
    if contacts is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return contacts
