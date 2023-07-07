"""Module for contact's operations"""

from typing import List

from fastapi import APIRouter, HTTPException, Depends, status, Query
from sqlalchemy.orm import Session

from src.database.db import get_db
from src.schemas import ContactModel, ContactUpdate, ContactResponse
from src.repository import contacts as repository_contacts
from src.database.models import Contact, User
from src.services.auth import auth_service

from fastapi_limiter.depends import RateLimiter


router = APIRouter(prefix='/contacts', tags=["contacts"])


@router.get("/find", response_model=List[ContactResponse])
async def find_contacts(
    db: Session = Depends(get_db),
    user: User = Depends(auth_service.get_current_user),
    firstname: str = Query(None),
    lastname: str = Query(None),
    email: str = Query(None)
) -> List[Contact]:
    """
    The find_contacts function is used to find contacts in the database.
        The function takes three optional parameters: firstname, lastname and email.
        If no parameters are provided, all contacts will be returned.
    
    :param db: Session: Get the database session
    :param user: User: Get the user id from the token
    :param firstname: str: Search for contacts by firstname
    :param lastname: str: Search for a contact by lastname
    :param email: str: Filter the contacts by email
    :return: A list of contacts
    :doc-author: Trelent
    """
    contacts = await repository_contacts.find_contacts(db, user, firstname, lastname, email)
    if contacts is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return contacts


@router.get("/nearest_birthdays", response_model=List[ContactResponse])
async def nearest_birthdays(user: User = Depends(auth_service.get_current_user), db: Session = Depends(get_db)):
    """
    The nearest_birthdays function returns the nearest birthdays of a user's contacts.
        The function takes in an optional parameter, user, which is the current logged-in user.
        If no such parameter is passed to the function, it will return all contacts' birthdays.
    
    :param user: User: Get the user from the token
    :param db: Session: Pass the database connection to the function
    :return: A list of contacts that have a birthday in the next 30 days
    :doc-author: Trelent
    """
    contacts = await repository_contacts.get_birthdays(user ,db)
    if contacts is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return contacts


@router.get("/", response_model=List[ContactResponse])
async def read_contacts(current_user: User = Depends(auth_service.get_current_user), skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    The read_contacts function returns a list of contacts for the current user.
        The function takes in three parameters:
            - skip (int): The number of contacts to skip before returning results. Default is 0.
            - limit (int): The maximum number of contacts to return per page. Default is 100, max is 1000.
    
    :param current_user: User: Get the current user from the auth_service
    :param skip: int: Skip the first n contacts in the list
    :param limit: int: Limit the number of contacts returned
    :param db: Session: Pass the database session to the repository
    :return: A list of contacts
    :doc-author: Trelent
    """
    contacts = await repository_contacts.get_contacts(current_user ,skip, limit, db)
    return contacts


@router.get("/{contact_id}", response_model=ContactResponse)
async def read_contact(contact_id: int, user: User = Depends(auth_service.get_current_user), db: Session = Depends(get_db)):
    """
    The read_contact function returns a contact by its ID.
        If the contact does not exist, it raises an HTTP 404 error.
    
    
    :param contact_id: int: Specify the contact id to be read
    :param user: User: Get the user from the auth_service
    :param db: Session: Pass the database session to the function
    :return: A contact object
    :doc-author: Trelent
    """
    contact = await repository_contacts.get_contact(user, contact_id, db)
    if contact is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return contact


@router.post("/", response_model=ContactResponse, dependencies=[Depends(RateLimiter(times=2, seconds=5))])
async def create_contact(body: ContactModel, user: User = Depends(auth_service.get_current_user), db: Session = Depends(get_db)):
    """
    The create_contact function creates a new contact in the database.
        
    
    :param body: ContactModel: Pass the data from the request body to our function
    :param user: User: Get the current user and pass it to the repository
    :param db: Session: Pass the database session to the repository layer
    :return: A contactmodel object
    :doc-author: Trelent
    """
    return await repository_contacts.create_contact(body, user, db)


@router.put("/{contact_id}", response_model=ContactResponse)
async def update_contact(contact_id: int, body: ContactUpdate, user: User = Depends(auth_service.get_current_user), db: Session = Depends(get_db)):
    """
    The update_contact function updates a contact in the database.
        
    
    :param contact_id: int: Identify the contact to be updated
    :param body: ContactUpdate: Pass in the data that will be used to update the contact
    :param user: User: Get the current user from the auth_service
    :param db: Session: Pass the database session to the repository layer
    :return: A contact object
    :doc-author: Trelent
    """
    contact = await repository_contacts.update_contact(user, contact_id, body, db)
    if contact is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return contact


@router.delete("/{contact_id}", response_model=ContactResponse)
async def remove_contact(contact_id: int, user: User = Depends(auth_service.get_current_user), db: Session = Depends(get_db)):
    """
    The remove_contact function removes a contact from the database.
        Args:
            contact_id (int): The id of the contact to be removed.
            user (User): The current user, as determined by auth_service.get_current_user().
            db (Session): A connection to the database, as determined by get_db().
    
    :param contact_id: int: Specify the id of the contact to be removed
    :param user: User: Get the user from the auth_service
    :param db: Session: Pass the database session to the repository layer
    :return: A contact object, which is the same as the one we get from get_contact
    :doc-author: Trelent
    """
    contact = await repository_contacts.remove_contact(user, contact_id, db)
    if contact is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return contact


@router.get("/bday_soon", response_model=List[ContactResponse])
async def nearest_birthdays(user: User = Depends(auth_service.get_current_user), db: Session = Depends(get_db)):
    """
    The nearest_birthdays function returns the nearest birthdays of a user's contacts.
        The function takes in an optional User object and a Session object as parameters.
        It then calls the repository_contacts.birthdays() function to get all of the user's contacts' birthdays, 
        which are returned as JSON objects.
    
    :param user: User: Get the current user from the auth_service
    :param db: Session: Pass the database session to the function
    :return: A list of contacts
    :doc-author: Trelent
    """
    contacts = await repository_contacts.birthdays(user, db)
    if contacts is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return contacts
