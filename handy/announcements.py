import asyncio
from datetime import datetime
import time

from config import CONFIG
from action_context import ActionContext
from utils.math import clamp
from logger import logger


async def say_current_time(ctx: ActionContext):
    now = datetime.now()

    formatted_time = now.strftime("%H:%M")
    formatted_date = now.strftime("%d.%m.%Y")

    sentence = ctx.translations.get_translation(
        "current_time", {"time": formatted_time, "date": formatted_date}
    )

    await say(ctx, sentence, 8)


async def say(ctx: ActionContext, sentence_to_say: str, estimated_time_seconds: float):
    entity_id = CONFIG.entities.media_player

    # Get the previous played media
    state = await ctx.hass_client.async_get_state(entity_id=entity_id)
    logger.info("Got the previous state")

    # Say the sentence
    tts = await ctx.hass_client.async_get_domain("tts")

    time_now = time.time()
    domain = await ctx.hass_client.async_get_domain(domain_id="media_player")
    await tts.google_translate_say(entity_id=entity_id, message=sentence_to_say)

    await asyncio.sleep(1)
    new_state = await ctx.hass_client.async_get_state(entity_id=entity_id)
    if new_state.state != "playing":
        try:
            await domain.media_play(entity_id=entity_id)
        except Exception as err:
            logger.warning(str(err))
    logger.info("Said the sentence")

    time_taken = time.time() - time_now
    time_to_wait = max(estimated_time_seconds - (time_taken / 1000), 0)
    logger.info(f"Additional wait: {time_to_wait}, it took {time_taken / 1000}s")
    if time_to_wait != 0:
        await asyncio.sleep(time_to_wait)

    # Play the previous sound
    try:
        await domain.play_media(
            entity_id=entity_id,
            media_content_id=state.attributes["media_content_id"],
            media_content_type=state.attributes["media_content_type"],
            enqueue="replace",
            extra={
                "current_time": state.attributes["media_position"],
                "media_position": state.attributes["media_position"],
            },
        )
        logger.info("Played the previous sound")
    except Exception as err:
        logger.warning(str(err))

    # Restore the previous state
    try:
        if state.state == "playing":
            # Get whether the current state isn't playing anyway
            new_state = await ctx.hass_client.async_get_state(entity_id=entity_id)
            if new_state != "playing":
                await domain.media_play(entity_id=CONFIG.entities.play_pause)
        else:
            await domain.media_pause(entity_id=CONFIG.entities.play_pause)
        logger.info(f"Restored the previous state ({state.state})")
    except Exception as err:
        logger.warning(str(err))
