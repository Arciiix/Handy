from action_context import ActionContext
from config import CONFIG
from logger import logger


async def toggle_playback_state(ctx: ActionContext):
    domain = await ctx.hass_client.async_get_domain("media_player")

    # Get current state
    state = await ctx.hass_client.async_get_state(
        entity_id=CONFIG.media_player_hass_entity_id
    )
    logger.info(f"Got the current audio state = {state.state}")
    try:
        if state.state == "playing":
            await domain.media_pause(entity_id=CONFIG.media_player_hass_entity_id)
            logger.info("Set media state to: pause")
        else:
            await domain.media_play(entity_id=CONFIG.media_player_hass_entity_id)
            logger.info("Set media state to: play")
    except Exception as err:
        print(err)