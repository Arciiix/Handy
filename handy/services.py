from homeassistant_api import Client

from config import CONFIG
from translations import Translations


async def get_services():
    hass_client = Client(
        f"{CONFIG.home_assistant_ip}/api",
        CONFIG.home_assistant_token,
        use_async=True,
        async_cache_session=False,
    )

    translations = Translations()
    return (hass_client, translations)
