from typing import Generator
from app.db.session import MongoDataBase

def get_db() -> Generator:
    try:
        db = MongoDataBase()
        yield db
    finally:
        pass