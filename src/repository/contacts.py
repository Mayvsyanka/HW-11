from typing import List

from sqlalchemy.orm import Session

from src.database.models import Contact
from src.schemas import ContactModel, ContactUpdate

from datetime import datetime, timedelta


async def get_contacts(skip: int, limit: int, db: Session) -> List[Contact]:
    return db.query(Contact).offset(skip).limit(limit).all()


async def get_contact(contact_id: int, db: Session) -> Contact:
    return db.query(Contact).filter(Contact.id == contact_id).first()


async def create_contact(body: ContactModel, db: Session) -> Contact:
    contact = Contact(firstname=body.firstname,
                      lastname=body.lastname, phone_number=body.phone_number, email=body.email, date_of_birth=body.date_of_birth, relationship=body.relationship)
    db.add(contact)
    db.commit()
    db.refresh(contact)
    return contact


async def remove_contact(contact_id: int, db: Session) -> Contact | None:
    contact = db.query(Contact).filter(Contact.id == contact_id).first()
    if contact:
        db.delete(contact)
        db.commit()
    return contact


async def update_contact(contact_id: int, body: ContactUpdate, db: Session) -> Contact | None:
    contact = db.query(Contact).filter(Contact.id == contact_id).first()
    if contact:
        contact.firstname = body.firstname
        contact.lastname = body.lastname 
        contact.phone_number = body.phone_number
        contact.email = body.email 
        contact.date_of_birth = body.date_of_birth
        contact.relationship = body.relationship
        db.commit()
    return contact


async def get_birthdays(db: Session) -> List[Contact]:
    contacts = db.query(Contact).all()
    today = datetime.now().date()
    end_date = today + timedelta(days=7)
    nearest_birthdays = []
    for contact in contacts:
        contact_bday_this_year = contact.date_of_birth.replace(
            year=today.year)
        if today <= contact_bday_this_year <= end_date:
            nearest_birthdays.append(contact)
    return nearest_birthdays
