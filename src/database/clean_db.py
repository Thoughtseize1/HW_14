from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from models import Contact  # Подставьте путь к вашим моделям
from src.database.db import DATABASE_URL

engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

# Получаем все контакты
all_contacts = session.query(Contact).all()

# Оставляем только первые 15 контактов
contacts_to_keep = all_contacts[:15]

# Удаляем остальные контакты
contacts_to_delete = set(all_contacts) - set(contacts_to_keep)
for contact in contacts_to_delete:
    session.delete(contact)

# Применяем изменения
session.commit()
