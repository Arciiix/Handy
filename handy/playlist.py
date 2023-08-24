import asyncio
import json
from os import path

from logger import logger
from action_context import ActionContext
from announcements import say
from config import CONFIG


class PlaylistItem:
    def __init__(self, name, pronunciation, url):
        self.name = name
        self.pronunciation = pronunciation or name
        self.url = url


PLAYLIST: list[PlaylistItem] = []

current_playlist_item_index = 0


async def next_playlist_item(ctx: ActionContext):
    if len(PLAYLIST) == 0:
        logger.warn("Tried to play next playlist item but no playlist is defined!")
        return

    global current_playlist_item_index
    # Increment the current playlist item index
    current_playlist_item_index += 1
    if current_playlist_item_index >= len(PLAYLIST):
        current_playlist_item_index = 0

    # Get the item itself
    item_to_play = PLAYLIST[current_playlist_item_index]
    logger.info(
        f"About to play {item_to_play.name} (item with index {current_playlist_item_index} from playlist)"
    )

    # First say the name of the item
    await say(ctx, item_to_play.pronunciation)
    logger.info("Said next media name")

    # Let's assume it takes 0.5 second per word to say the name + 1 second
    await asyncio.sleep((0.5 * len(item_to_play.pronunciation.split())) + 1)
    logger.info("Waited 2 seconds")

    # Play the media itself
    try:
        domain = await ctx.hass_client.async_get_domain(domain_id="media_player")
        await domain.play_media(
            entity_id=CONFIG.entities.next_playlist_item,
            media_content_id=item_to_play.url,
            media_content_type="music",
            enqueue="replace",
        )
        logger.info("Played media!")
    except Exception as err:
        logger.error(f"Couldn't play media! {str(err)}")


try:
    with open(path.join(path.dirname(__file__), "playlist.json")) as f:
        loaded_playlist = json.load(f)
        for item in loaded_playlist:
            PLAYLIST.append(
                PlaylistItem(
                    item["name"],
                    item.get("pronunciation", item["name"]),
                    item[
                        "url"
                    ],  # It throws an error if the format of playlist.json is wrong
                )
            )
        logger.info(f"Loaded {len(PLAYLIST)} playlist items!")
except FileNotFoundError:
    logger.warning(
        'playlist.json doesn\'t exist - please consider creating it to make the "next playlist item" action work'
    )
