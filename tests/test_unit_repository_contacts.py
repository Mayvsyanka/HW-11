import unittest
from unittest.mock import MagicMock

from sqlalchemy.orm import Session

from datetime import date

from src.database.models import User, Contact
from src.schemas import ContactModel, ContactUpdate, ContactResponse
from src.repository.contacts import (
    get_contact,
    get_contacts,
    create_contact,
    remove_contact,
    update_contact,
    get_birthdays,
    find_contacts
)


class TestContacts(unittest.IsolatedAsyncioTestCase):

    def setUp(self):
        self.session = MagicMock(spec=Session)
        self.user = User(id=1)

    async def test_get_contacts(self):
        contacts = [Contact(), Contact(), Contact()]
        self.session.query().filter().offset().limit().all.return_value = contacts
        result = await get_contacts(skip=0, limit=10, user=self.user, db=self.session)
        self.assertEqual(result, contacts)

    async def test_get_contact_found(self):
        contact = Contact()
        self.session.query().filter().first.return_value = contact
        result = await get_contact(note_id=1, user=self.user, db=self.session)
        self.assertEqual(result, contact)

    async def test_get_contact_not_found(self):
        self.session.query().filter().first.return_value = None
        result = await get_contact(note_id=1, user=self.user, db=self.session)
        self.assertIsNone(result)

    async def test_create_contact(self):
        body = ContactModel(firstname="example", lastname="test", phone_number="0123456789",
                            email="test@example.net", date_of_birth=date('2023-07-10'), relationships="test")
        result = await create_contact(body=body, user=self.user, db=self.session)
        self.assertEqual(result.firstname, body.firstname)
        self.assertEqual(result.lastname, body.lastname)
        self.assertEqual(result.phone_number, body.phone_number)
        self.assertEqual(result.email, body.email)
        self.assertEqual(result.date_of_birth, body.date_of_birth)
        self.assertEqual(result.relationships, body.relationships)
        self.assertTrue(hasattr(result, "id"))

    async def test_remove_contact_found(self):
        contact = Contact()
        self.session.query().filter().first.return_value = contact
        result = await remove_contact(note_id=1, user=self.user, db=self.session)
        self.assertEqual(result, contact)

    async def test_remove_contact_not_found(self):
        self.session.query().filter().first.return_value = None
        result = await remove_contact(note_id=1, user=self.user, db=self.session)
        self.assertIsNone(result)


if __name__ == '__main__':
    unittest.main()
