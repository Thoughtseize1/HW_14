import unittest
from unittest.mock import MagicMock, AsyncMock

from sqlalchemy.orm import Session

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

    # async def test_get_contacts(self):
    #     contacts = [Contact(first_name='BOB'), Contact(first_name='Pavel'), Contact(first_name='Skin')]
    #     self.session.query().filter().limit().order_by().all.return_value = contacts
    #     result = await get_contacts(limit=10, user=self.user, db=self.session)
    #     print(type(result), result)
    #     print(type(contacts), contacts)
    #     self.assertEqual(result[0].first_name, contacts[0].first_name)
    #     self.assertTrue(hasattr(result, "first_name"))

    async def test_get_note_found(self):
        # contact = Contact()
        # self.session.query().filter().first.return_value = contact
        result = await get_contact(contact_id=1, user=self.user, db=self.session)
        self.assertEqual(self.contact, result)

    # async def test_get_note_not_found(self):
    #     self.session.query().filter().first.return_value = None
    #     result = await get_note(note_id=1, user=self.user, db=self.session)
    #     self.assertIsNone(result)
    #
    # async def test_create_note(self):
    #     body = NoteModel(title="test", description="test note", tags=[1, 2])
    #     tags = [Tag(id=1, user_id=1), Tag(id=2, user_id=1)]
    #     self.session.query().filter().all.return_value = tags
    #     result = await create_note(body=body, user=self.user, db=self.session)
    #     self.assertEqual(result.title, body.title)
    #     self.assertEqual(result.description, body.description)
    #     self.assertEqual(result.tags, tags)
    #     self.assertTrue(hasattr(result, "id"))
    #
    # async def test_remove_note_found(self):
    #     note = Note()
    #     self.session.query().filter().first.return_value = note
    #     result = await remove_note(note_id=1, user=self.user, db=self.session)
    #     self.assertEqual(result, note)
    #
    # async def test_remove_note_not_found(self):
    #     self.session.query().filter().first.return_value = None
    #     result = await remove_note(note_id=1, user=self.user, db=self.session)
    #     self.assertIsNone(result)
    #
    # async def test_update_note_found(self):
    #     body = NoteUpdate(title="test", description="test note", tags=[1, 2], done=True)
    #     tags = [Tag(id=1, user_id=1), Tag(id=2, user_id=1)]
    #     note = Note(tags=tags)
    #     self.session.query().filter().first.return_value = note
    #     self.session.query().filter().all.return_value = tags
    #     self.session.commit.return_value = None
    #     result = await update_note(note_id=1, body=body, user=self.user, db=self.session)
    #     self.assertEqual(result, note)
    #
    # async def test_update_note_not_found(self):
    #     body = NoteUpdate(title="test", description="test note", tags=[1, 2], done=True)
    #     self.session.query().filter().first.return_value = None
    #     self.session.commit.return_value = None
    #     result = await update_note(note_id=1, body=body, user=self.user, db=self.session)
    #     self.assertIsNone(result)
    #
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


if __name__ == '__main__':
    unittest.main()
