from datetime import datetime

from peewee import (
    Model,
    IntegerField,
    CharField,
    DateField,
    DateTimeField,
    ForeignKeyField,
    TextField,
    FloatField
)

from database.database import db


class Search(Model):
    """Хранит информацию о поисковом запросе пользователя."""
    user_id = IntegerField()
    city = CharField()
    check_in = DateField()
    check_out = DateField()
    search_date = DateTimeField(default=datetime.now)

    class Meta:
        database = db


class SearchHotel(Model):
    """Хранит информацию об отеле, найденном в результате поиска."""
    search = ForeignKeyField(Search, backref='hotels')
    name = CharField()
    booking_url = TextField()
    description = TextField()
    price = CharField()
    photos = TextField()
    latitude = FloatField()
    longitude = FloatField()

    class Meta:
        database = db
