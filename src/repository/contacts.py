'''Module for direct operations, adding, getting, updating, changing and deleting contacts inside the database'''

from typing import List

from sqlalchemy.orm import Session

from sqlalchemy import and_

from src.database.models import Contact, User
from src.schemas import ContactModel, ContactUpdate

from datetime import datetime, timedelta


async def get_contacts(user: User, skip: int, limit: int, db: Session) -> List[Contact]:
    """
    The get_contacts function returns a list of contacts for the specified user.
        
    
    :param user: User: Get the user_id of the logged in user
    :param skip: int: Skip a certain number of contacts in the database
    :param limit: int: Limit the number of contacts returned
    :param db: Session: Pass the database session to the function
    :return: A list of contacts
    """
    return db.query(Contact).filter(Contact.user_id == user.id).offset(skip).limit(limit).all()


async def get_contact(user: User, contact_id: int, db: Session) -> Contact: 
    """
    The get_contact function returns a contact from the database.
        Args:
            user (User): The user who owns the contact.
            contact_id (int): The id of the desired Contact object. 
            db (Session): A database session to use for querying data from the database.
    
    :param user: User: Get the user from the database
    :param contact_id: int: Filter the database query
    :param db: Session: Pass the database session to the function
    :return: A contact object
    """
    return db.query(Contact).filter(and_(Contact.id == contact_id, Contact.user_id == user.id)).first()


async def create_contact(body: ContactModel, user: User, db: Session) -> Contact:
    """
    The create_contact function creates a new contact in the database.
        
    
    :param body: ContactModel: Pass the json body of the request to the function
    :param user: User: Get the user id from the token
    :param db: Session: Access the database
    :return: The contact object that was created
    :doc-author: Trelent
    """
    contact = Contact(firstname=body.firstname,
                      lastname=body.lastname, phone_number=body.phone_number, email=body.email, date_of_birth=body.date_of_birth, relationships=body.relationships, user=user)
    db.add(contact)
    db.commit()
    db.refresh(contact)
    return contact


async def remove_contact(user:User, contact_id: int, db: Session) -> Contact | None:
    """
    The remove_contact function removes a contact from the database.
        Args:
            user (User): The user who owns the contact to be removed.
            contact_id (int): The id of the contact to be removed.
            db (Session): A connection to our database, used for querying and deleting contacts.
        Returns: 
            Contact | None: If successful, returns a Contact object representing the deleted record; otherwise returns None.
    
    :param user:User: Specify the user that is logged in
    :param contact_id: int: Specify which contact to delete
    :param db: Session: Pass the database session to the function
    :return: The contact object that was deleted
    :doc-author: Trelent
    """
    contact = db.query(Contact).filter(
        and_(Contact.id == contact_id, Contact.user_id == user.id)).first()
    if contact:
        db.delete(contact)
        db.commit()
    return contact


async def update_contact(user:User, contact_id: int, body: ContactUpdate, db: Session) -> Contact | None:
    """
    The update_contact function updates a contact in the database.
        Args:
            user (User): The user who is making the request.
            contact_id (int): The id of the contact to be updated.
            body (ContactUpdate): A ContactUpdate object containing all fields that can be updated for a given Contact object, including firstname, lastname, phone_number, email and date_of_birth. 
                Note: relationships cannot be changed via this function; use add/remove relationship functions instead! 
        Returns: 
            None if no such contact exists or
    
    :param user:User: Get the user id from the database
    :param contact_id: int: Identify the contact that is being updated
    :param body: ContactUpdate: Pass in the data that will be used to update the contact
    :param db: Session: Create a database session
    :return: A contact or none
    :doc-author: Trelent
    """
    
    contact = db.query(Contact).filter(
        and_(Contact.id == contact_id, Contact.user_id == user.id)).first()
    if contact:
        contact.firstname = body.firstname
        contact.lastname = body.lastname 
        contact.phone_number = body.phone_number
        contact.email = body.email 
        contact.date_of_birth = body.date_of_birth
        contact.relationships = body.relationships
        db.commit()
    return contact


async def get_birthdays(user:User, db: Session) -> List[Contact]:
    """
    The get_birthdays function returns a list of contacts whose birthdays are within the next 7 days.
        Args:
            user (User): The user object for which we want to get the nearest birthdays.
            db (Session): A database session object that is used to query the database.
    
    :param user:User: Get the user id of the current user
    :param db: Session: Pass the database session to the function
    :return: A list of contacts who have birthdays in the next 7 days
    :doc-author: Trelent
    """
    
    contacts = db.query(Contact).filter(Contact.user_id == user.id).all()
    today = datetime.now().date()
    end_date = today + timedelta(days=7)
    nearest_birthdays = []
    for contact in contacts:
        contact_bday_this_year = contact.date_of_birth.replace(
            year=today.year)
        if today <= contact_bday_this_year <= end_date:
            nearest_birthdays.append(contact)
    return nearest_birthdays


async def find_contacts(
        db: Session,
        user: User,
        firstname: str = None,
        lastname: str = None,
        email: str = None,

) -> List[Contact]:
    """
    The find_contacts function is used to search for contacts in the database.
        The function takes a user object, and optional firstname, lastname, and email parameters.
        If any of these are provided they will be used as filters on the query.
    
    :param db: Session: Pass the database session to the function
    :param user: User: Identify the user who is making the request
    :param firstname: str: Filter the contacts by firstname
    :param lastname: str: Search for a contact by lastname
    :param email: str: Search for a contact by email
    :param : Filter the contacts by firstname, lastname and email
    :return: A list of contacts
    :doc-author: Trelent
    """
    query = db.query(Contact).filter(Contact.user_id == user.id)

    if firstname:
        query = query.filter(Contact.firstname.ilike(f"%{firstname}%"))
    if lastname:
        query = query.filter(Contact.lastname.ilike(f"%{lastname}%"))
    if email:
        query = query.filter(Contact.email.ilike(f"%{email}%"))

    contact = query.all()
    return contact
