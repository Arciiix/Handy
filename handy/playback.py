import asyncio
from typing import Optional

from homeassistant_api import Client, Domain
from action_context import ActionContext
from config import CONFIG
from logger import logger


async def get_playback_state(ctx: ActionContext):
    domain = await ctx.hass_client.async_get_domain("media_player")

    # Get current state
    state = await ctx.hass_client.async_get_state(entity_id=CONFIG.entities.play_pause)
    logger.info(f"Got the current audio state = {state.state}")

    return (state, domain)


async def toggle_playback_state(ctx: ActionContext):
    state, domain = await get_playback_state(ctx)
    try:
        if state.state == "playing":
            await domain.media_pause(entity_id=CONFIG.entities.play_pause)
            logger.info("Set media state to: pause")
        else:
            await domain.media_play(entity_id=CONFIG.entities.play_pause)
            logger.info("Set media state to: play")
    except Exception as err:
        logger.error(f"Error while toggling playback state: {err}")


async def get_current_volume_only(ctx: ActionContext) -> Optional[int]:
    state = await ctx.hass_client.async_get_state(entity_id=CONFIG.entities.volume)

    volume = state.attributes.get("volume_level", None)

    if volume is None:
        return None

    volume = int(float(volume) * 100)
    logger.info(f"Got volume: {volume}")

    return volume


async def get_current_volume(ctx: ActionContext) -> tuple[int, Optional[Domain]]:
    volume = await get_current_volume_only(ctx)
    domain = await ctx.hass_client.async_get_domain("media_player")

    if volume is None:
        return (None, domain)

    # Also indicate about entering volume change mode
    logger.info("Indicating about volume change mode...")
    await domain.volume_mute(entity_id=CONFIG.entities.volume, is_volume_muted=True)
    logger.info("Muted, wait 1s")
    await asyncio.sleep(1)
    await domain.volume_mute(entity_id=CONFIG.entities.volume, is_volume_muted=False)
    logger.info("Unmuted, wait 1s")
    await asyncio.sleep(1)

    return (volume, domain)


async def set_current_volume(ctx: ActionContext):
    """
    Sets the volume

    Args:
        ctx (ActionContext) - volume is in ctx.numeric_value attribute with range 0 - 100%
    """
    domain = (
        ctx.domain
        if ctx.domain is not None
        else await ctx.hass_client.async_get_domain("media_player")
    )
    try:
        await domain.volume_set(
            entity_id=CONFIG.entities.volume, volume_level=ctx.numeric_value / 100
        )
        logger.info(f"Set volume to {ctx.numeric_value}%")
    except Exception as err:
        logger.exception(err)
