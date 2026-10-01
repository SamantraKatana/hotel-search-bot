from database.database import db
from database.models import Search, SearchHotel


def create_tables() -> None:
    """Создаёт таблицы базы данных, если они ещё не существуют."""
    db.connect()
    db.create_tables([Search,SearchHotel])
    db.close()