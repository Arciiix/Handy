import re
from schematics.exceptions import ValidationError


patterns = {
    "url": re.compile(
        r"https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&//=]*)",
        re.IGNORECASE,
    )
}


def validate_url(url):
    if not patterns["url"].match(url):
        raise ValidationError("Invalid URL format")
