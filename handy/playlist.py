import asyncio
import json
from os import path
from typing import Optional

from socketio import Server

from logger import logger
from action_context import ActionContext
from announcements import say
from config import CONFIG
from db import PlaylistItem, PlaylistTypes


# YouTube playlists contains raw YouTube URLs, whereas local playlist contains URLs to raw sound files (that do not need processing)
LOCAL_PLAYLIST: list[PlaylistItem] = []
YOUTUBE_PLAYLIST: list[PlaylistItem] = []


current_local_playlist_item_index = 0
current_youtube_playlist_item_index = 0
current_playlist_type = PlaylistTypes.LOCAL


async def next_playlist_item(ctx: ActionContext):
    if (current_playlist_type is PlaylistTypes.LOCAL and len(LOCAL_PLAYLIST) == 0) or (
        current_playlist_type is PlaylistTypes.YOUTUBE and len(YOUTUBE_PLAYLIST) == 0
    ):
        logger.warn(
            "Tried to play next playlist item but there's no items in the current playlist!"
        )
        return

    global current_local_playlist_item_index, current_youtube_playlist_item_index

    index = None
    if current_playlist_type is PlaylistTypes.LOCAL:
        # Increment the current playlist item index
        current_local_playlist_item_index += 1
        if current_local_playlist_item_index >= len(LOCAL_PLAYLIST):
            current_local_playlist_item_index = 0
        index = current_local_playlist_item_index

        # Get the item itself
        item_to_play = LOCAL_PLAYLIST[current_local_playlist_item_index]
    elif current_playlist_type is PlaylistTypes.YOUTUBE:
        # Increment the current playlist item index
        current_youtube_playlist_item_index += 1
        if current_youtube_playlist_item_index >= len(YOUTUBE_PLAYLIST):
            current_youtube_playlist_item_index = 0
        index = current_youtube_playlist_item_index

        # Get the item itself
        item_to_play = YOUTUBE_PLAYLIST[current_youtube_playlist_item_index]
    else:
        logger.error(f"Couldn't find playlist type {current_playlist_type}")
        return

    logger.info(
        f"About to play {item_to_play.name} (item with index {index} from playlist type {current_playlist_type})"
    )

    # First say the name of the item
    await say(ctx, item_to_play.pronunciation)
    logger.info("Said next media name")

    # TODO: If it's YouTube playlist, download the item in the background while waiting

    # Let's assume it takes 0.5 second per word to say the name + 1 second
    await asyncio.sleep((0.5 * len(item_to_play.pronunciation.split())) + 1)
    logger.info("Waited 2 seconds")

    # Play the media itself
    try:
        domain = await ctx.hass_client.async_get_domain(domain_id="media_player")
        await domain.play_media(
            entity_id=CONFIG.entities.next_playlist_item,
            media_content_id=item_to_play.url,  # TODO: On YouTube, get the raw .mp3 URL
            media_content_type="music",
            enqueue="replace",
        )
        logger.info("Played media!")
    except Exception as err:
        logger.error(f"Couldn't play media! {str(err)}")


def get_playlist_items(type: Optional[PlaylistTypes] = None):
    return [
        playlist.to_dict()
        for playlist in (
            # Basically, if type is local, only local. If type is YouTube, only YouTube. If type is None, True (all)
            (LOCAL_PLAYLIST if type == PlaylistTypes.LOCAL.value else YOUTUBE_PLAYLIST)
            if type is not None
            else LOCAL_PLAYLIST + YOUTUBE_PLAYLIST
        )
    ]


async def update_playlists(socket: Server = None):
    global LOCAL_PLAYLIST, YOUTUBE_PLAYLIST
    try:
        playlists = PlaylistItem.select()

        LOCAL_PLAYLIST = [
            playlist
            for playlist in playlists
            if playlist.type == PlaylistTypes.LOCAL.value
        ]
        YOUTUBE_PLAYLIST = [
            playlist
            for playlist in playlists
            if playlist.type == PlaylistTypes.YOUTUBE.value
        ]

        if socket:
            await socket.emit(
                "playlist_item/update",
                {
                    "local": [playlist.to_dict() for playlist in LOCAL_PLAYLIST],
                    "youtube": [playlist.to_dict() for playlist in YOUTUBE_PLAYLIST],
                },
            )

        logger.info(
            f"Loaded {len(LOCAL_PLAYLIST)} local playlist items and {len(YOUTUBE_PLAYLIST)} YouTube playlist items!"
        )
    except Exception as err:
        logger.warning(f"Playlist couldn't be loaded from the database: {str(err)}")
