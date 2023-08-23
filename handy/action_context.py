from homeassistant_api import Client

from translations import Translations


class ActionContext:
    def __init__(
        self, confidency: float, home_assistant: Client, translations: Translations
    ):
        self.confidency = confidency
        self.hass_client = home_assistant
        self.translations = translations
