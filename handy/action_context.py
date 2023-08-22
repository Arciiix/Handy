from homeassistant_api import Client


class ActionContext:
    def __init__(self, confidency: float, home_assistant: Client):
        self.confidency = confidency
        self.hass_client = home_assistant
