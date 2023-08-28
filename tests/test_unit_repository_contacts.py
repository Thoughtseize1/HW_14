import unittest
from unittest.mock import MagicMock, AsyncMock

from fastapi import HTTPException
from sqlalchemy.orm import Session
from starlette import status

from src.database.models import Contact, User
from src.schemas import ContactModel, DeletedContactResponse, ContactBirthdaysResponse
from src.repository.contacts import (
    get_contacts,
    get_contact,
    create_contact,
    remove_contact,
    update_contact,
    search_by_some_data,
    search_birthdays
)


class TestContacts(unittest.IsolatedAsyncioTestCase):

    def setUp(self):
        self.session = MagicMock(spec=Session)
        self.user = User(id=1, username='Skin2000', email='Skin200@ukr.net', password="QWERTY1rf5",
                         avatar="https://www.gravatar.com/avatar/79497276207495cf61382900b08055c9",
                         confirmed=False)
        self.contact = Contact(id=1, first_name="BOB2", last_name='Salazar', email='Salazar2000@ukr.net',
                               phone_number='+35673332323', user_id=1)
        self.body = ContactModel(first_name="Ivan", last_name="Lopatkin", email="superIvan@ivana.net",
                                 phone_number="+3(777)987777", additional_data="Ivav is a good guy", birthdate=None)
        self.contacts = [
            Contact(user_id=1, first_name="Nikita", last_name="Sherstianykh", email="nikita@ukr.net"),
            Contact(user_id=2, first_name="Nikasan", last_name="Shameleon", email="gladiator@ukr.net"),
        ]

    async def test_get_contacts(self):
        contacts = [Contact(first_name='BOB'), Contact(first_name='Pavel'), Contact(first_name='Skin')]
        self.session.query().filter().order_by().limit().all.return_value = contacts
        result = await get_contacts(limit=10, user=self.user, db=self.session)
        self.assertEqual(result, contacts)
        self.assertTrue(hasattr(result[0], "first_name"))

    async def test_get_contact_found(self):
        contact = Contact()
        self.session.query().filter().filter_by().first.return_value = contact
        result = await get_contact(contact_id=1, user=self.user, db=self.session)
        self.assertEqual(contact, result)

    async def test_get_contact_not_found(self):
        self.session.query().filter().filter_by().first.return_value = None
        result = await get_contact(contact_id=1, user=self.user, db=self.session)
        self.assertIsNone(result)

    async def test_create_contact(self):
        self.session.query().filter().filter_by().first.return_value = None
        result = await create_contact(body=self.body, user=self.user, db=self.session)
        print(result)
        self.assertEqual(result.first_name, self.body.first_name)
        self.assertEqual(result.last_name, self.body.last_name)
        self.assertEqual(result.user_id, self.user.id)
        self.assertTrue(hasattr(result, "created_at"))

    async def test_create_contact_duplicate(self):
        self.session.query().filter().filter_by().first.return_value = Contact()
        with self.assertRaises(HTTPException) as context:
            await create_contact(self.body, self.user, self.session)
        self.assertEqual(context.exception.status_code, status.HTTP_409_CONFLICT)
        self.assertEqual(context.exception.detail, 'Duplicate data')

    async def test_remove_contact_found(self):
        contact = Contact()
        self.session.query().filter().filter_by().first.return_value = contact
        result = await remove_contact(contact_id=1, user=self.user, db=self.session)
        self.assertEqual(result, contact)

    async def test_remove_contact_not_found(self):
        self.session.query().filter().filter_by().first.return_value = None
        result = await remove_contact(contact_id=1, user=self.user, db=self.session)
        self.assertIsNone(result)

    async def test_update_contact_success(self):
        old_contact = Contact(id=1, first_name="Old", last_name="Contact", user_id=self.user.id,
                              email="old@ukr.net",
                              phone_number="654321")
        self.session.query().filter().filter_by().first.return_value = old_contact
        updated_contact = await update_contact(contact_id=1, body=self.body, user=self.user, db=self.session)
        self.assertEqual(updated_contact.first_name, self.body.first_name)
        self.assertEqual(updated_contact.last_name, self.body.last_name)
        self.assertEqual(updated_contact.email, self.body.email)
        self.assertEqual(updated_contact.phone_number, self.body.phone_number)
        self.session.commit.assert_called_once()
        self.session.refresh.assert_called_once_with(updated_contact)

    async def test_update_contact_not_found(self):
        self.session.query().filter().filter_by().first.return_value = None
        with self.assertRaises(HTTPException) as context:
            await update_contact(contact_id=1, body=self.body, user=self.user, db=self.session)
        self.assertEqual(context.exception.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(context.exception.detail, 'Contact not found')

    async def test_search_by_first_name(self):
        self.session.query().filter().filter().all.return_value = self.contacts
        result = await search_by_some_data(self.user, self.session, first_name="Nik", last_name="", email="")
        self.assertEqual(result, self.contacts)

    async def test_search_by_last_name(self):
        self.session.query().filter().filter().all.return_value = self.contacts
        result = await search_by_some_data(self.user, self.session, first_name="", last_name="Sh", email="")
        self.assertEqual(result, self.contacts)

    async def test_search_by_email(self):
        self.session.query().filter().filter().all.return_value = self.contacts
        result = await search_by_some_data(self.user, self.session, first_name="", last_name="", email="@urk.net")
        self.assertEqual(result, self.contacts)

    async def test_search_not_found(self):
        self.session.query().filter().filter().all.return_value = []
        with self.assertRaises(HTTPException) as context:
            await search_by_some_data(self.user, self.session, first_name="NonExistent", last_name="", email="")
        self.assertEqual(context.exception.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(context.exception.headers, {'details': 'NOT FOUND'})


    # async def test_update_status_note_found(self):
    #     body = NoteStatusUpdate(done=True)
    #     note = Note()
    #     self.session.query().filter().first.return_value = note
    #     self.session.commit.return_value = None
    #     result = await update_status_note(note_id=1, body=body, user=self.user, db=self.session)
    #     self.assertEqual(result, note)
    #
    # async def test_update_status_note_not_found(self):
    #     body = NoteStatusUpdate(done=True)
    #     self.session.query().filter().first.return_value = None
    #     self.session.commit.return_value = None
    #     result = await update_status_note(note_id=1, body=body, user=self.user, db=self.session)
    #     self.assertIsNone(result)
