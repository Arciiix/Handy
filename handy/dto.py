import re
from schematics.models import Model
from schematics.types import StringType, DecimalType, DateTimeType, URLType

from validators import validate_url
from db import PlaylistTypes


class PlaylistItemCreateDto(Model):
    name = StringType(required=True)
    pronunciation = StringType()
    url = StringType(required=True, validators=[validate_url])

    type = StringType(
        required=True, choices=[*PlaylistTypes.__members__.keys()]
    )  # Type is PlaylistTypes enum

    def __init__(self, *args, **kwargs):
        super(PlaylistItemCreateDto, self).__init__(*args, **kwargs)

        # Set the default value of pronunciation to be equal to the value of name
        if "name" in args[0] and not "pronunciation" in args[0]:
            self.pronunciation = args[0]["name"]


class PlaylistItemEditDto(Model):
    id = StringType(required=True)
    name = StringType()
    pronunciation = StringType()
    url = StringType(validators=[validate_url])

    type = StringType(
        choices=[PlaylistTypes.__members__.keys()]
    )  # Type is PlaylistTypes enum
