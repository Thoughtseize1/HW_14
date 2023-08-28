from datetime import datetime, timedelta, date

from fastapi import Depends
from sqlalchemy import extract, func
from sqlalchemy.orm import Session
from typing import List

from src.database.db import get_db
from src.database.models import Contact

day_for_congrats = {
    'Monday': [],
    'Tuesday': [],
    'Wednesday': [],
    'Thursday': [],
    'Friday': []
}


def get_birth_months() -> List[int]:
    db = next(get_db())
    birth_months = (
        db.query(func.date_part('month', Contact.birthdate))
        .filter(Contact.birthdate is not None).limit(10)
        .all()
    )
    return birth_months


def find_a_nearby_monday(d, weekday):
    days_ahead = weekday - d.weekday()
    if days_ahead <= 0:  # Target day already happened this week
        days_ahead += 7
    return d + timedelta(days_ahead)


if __name__ == '__main__':
    m = 10
    month = get_birth_months()
    # print(month)
    # print(type(month))
    for contact in month:
        print(type(*contact))
