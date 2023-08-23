import asyncio
from os import path
from homeassistant_api import Client, State

from config import CONFIG, SOUND_SUCCESS
from logger import logger


class AudioIndicator:
    """
    A class that confirms the execution of an action by playing a sound effect
    """

    # TODO: Make it work
    def __init__(self, hass_client=Client):
        self.hass_client = hass_client
        self.entity_id = CONFIG.entities.media_player

    async def play_sound(
        self, sound_filename: str, length_seconds: float, restore_previous_state: bool
    ):
        # Get the previous played media
        state = await self.hass_client.async_get_state(entity_id=self.entity_id)
        logger.info("Got the previous played media")

        domain = await self.hass_client.async_get_domain(domain_id="media_player")
        # Play the sound
        await domain.play_media(
            entity_id=self.entity_id,
            media_content_id=f"media-source://media_source/local/{SOUND_SUCCESS}",
            media_content_type="music",
            enqueue="replace",
        )
        logger.info("Played the sound")

        # Set a timeout after the previous sound will be played
        await asyncio.sleep(length_seconds + 3)

        # Restore the previous playback state
        await self.hass_client.async_set_state(
            state=State(entity_id=CONFIG.entities.media_player, state=state.state)
        )

        # print(state)

        # Play the previous sound
        await domain.play_media(
            entity_id=self.entity_id,
            media_content_id=state.attributes["media_content_id"],
            media_content_type=state.attributes["media_content_type"],
            enqueue="replace",
            extra={
                "current_time": state.attributes["media_position"],
                "media_position": state.attributes["media_position"],
            },
        )

        if restore_previous_state:
            # Add some delay
            await asyncio.sleep(3)
            if state.state == "playing":
                await domain.media_play(entity_id=self.entity_id)
            else:
                await domain.media_pause(entity_id=self.entity_id)

            logger.info("Restored previous state")
        return state

    async def play_success_sound(self, restore_previous_state: bool):
        return await self.play_sound("success.wav", 1, restore_previous_state)
