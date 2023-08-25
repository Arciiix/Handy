from peewee import *

from logger import logger

db = SqliteDatabase("handy.db")


class PlaylistItem(Model):
    id = UUIDField(primary_key=True)
    name = CharField()
    pronunciation = CharField()
    url = CharField()

    class Meta:
        database = db

    def to_dict(self):
        return {
            "id": str(self.id),
            "name": self.name,
            "pronunciation": self.pronunciation,
            "url": self.url,
        }


db.connect()
logger.info("Connected to the db")
db.create_tables([PlaylistItem])
