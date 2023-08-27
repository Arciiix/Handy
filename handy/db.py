from enum import Enum
from peewee import *

from logger import logger

db = SqliteDatabase("handy.db")


class PlaylistTypes(Enum):
    LOCAL = 0
    YOUTUBE = 1

    @classmethod
    def next(self, current):
        """
        Get the next item in enum

        Args:
            current: current item

        Returns:
            next_item: next item
        """
        members = list(self)
        idx = members.index(current)
        next_idx = (idx + 1) % len(members)
        return members[next_idx]


class PlaylistItem(Model):
    id = UUIDField(primary_key=True)
    name = CharField()
    pronunciation = CharField()
    url = CharField()

    type = SmallIntegerField()  # Value from enum PlaylistTypes

    class Meta:
        database = db

    def to_dict(self):
        return {
            "id": str(self.id),
            "name": self.name,
            "pronunciation": self.pronunciation,
            "url": self.url,
            "type": PlaylistTypes(self.type).name,
        }


db.connect()
logger.info("Connected to the db")
db.create_tables([PlaylistItem])
