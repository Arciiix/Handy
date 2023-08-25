from typing import Optional
from homeassistant_api import Client, Domain
from peewee import Database

from translations import Translations


class ActionContext:
    numeric_value = None

    def __init__(
        self,
        confidency: float,
        home_assistant: Client,
        translations: Translations,
        db: Database,
        domain=Optional[Domain],
    ):
        self.confidency = confidency
        self.hass_client = home_assistant
        self.translations = translations
        self.db = db
        self.domain = domain  # Optional, to reduce requests
