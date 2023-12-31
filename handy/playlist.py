import asyncio
from datetime import datetime, timedelta
import json
from os import path
import threading
from typing import Optional

from socketio import Server

from youtube import get_youtube_video_info
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

# To prevent race condition when both the server and Handy app wants to change playlist mode
playlist_type_lock = threading.Lock()


async def play_playlist_item(
    ctx: ActionContext, item_to_play: PlaylistItem, index: int
):
    logger.info(
        f"About to play {item_to_play.name} (item with index {index} from playlist type {PlaylistTypes(item_to_play.type)})"
    )
    if item_to_play.type is PlaylistTypes.LOCAL.value:
        global current_local_playlist_item_index
        current_local_playlist_item_index = index
    elif item_to_play.type is PlaylistTypes.YOUTUBE.value:
        global current_youtube_playlist_item_index
        current_youtube_playlist_item_index = index

    # First say the name of the item
    name_to_say = (
        item_to_play.pronunciation
        if item_to_play.pronunciation is not None
        else item_to_play.name
    )
    await say(
        ctx,
        name_to_say,
    )
    logger.info("Said next media name")

    # Define another variable for it because the URL can be different for specific type of playlist items (YouTube)
    url_to_play = item_to_play.url

    # Let's assume it takes 0.5 second per word to say the name + 1 second
    time_to_wait_seconds = (0.5 * len(name_to_say.split())) + 1
    if item_to_play.type is PlaylistTypes.YOUTUBE.value:
        # If it's YouTube playlist, download the item first, then if there's need to wait more, wait
        target_time = datetime.now() + timedelta(seconds=time_to_wait_seconds)

        info = get_youtube_video_info(item_to_play.url)
        if not info["success"] or not info["url"]:
            logger.error(
                f"Couldn't get YouTube URL for playlist item {item_to_play.id} (url: {{item_to_play.url}})"
            )

            await say(ctx, ctx.translations.get_translation("youtube_fail"))
            return

        url_to_play = info["url"]
        logger.info("Got YouTube audio URL")
        # If there is any time to wait anymore
        if target_time < datetime.now():
            logger.info("Additional waiting...")

            await asyncio.sleep((target_time - datetime.now()).total_seconds())
    else:
        await asyncio.sleep(time_to_wait_seconds)
        logger.info("Waited 2 seconds")

    # Play the media itself
    try:
        domain = await ctx.hass_client.async_get_domain(domain_id="media_player")
        await domain.play_media(
            entity_id=CONFIG.entities.next_playlist_item,
            media_content_id=url_to_play,
            media_content_type="music",
            enqueue="replace",
        )
        logger.info("Played media!")
    except Exception as err:
        logger.error(f"Couldn't play media! {str(err)}")


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

    return await play_playlist_item(ctx, item_to_play, index)


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


def get_playlist_info():
    return {
        "playlists": {
            "items": get_playlist_items(),
            "current_playlist_type": current_playlist_type.name,
            "local": {
                "current_index": current_local_playlist_item_index,
            },
            "youtube": {
                "current_index": current_youtube_playlist_item_index,
            },
        },
    }


async def update_playlists(socket: Server = None):
    global LOCAL_PLAYLIST, YOUTUBE_PLAYLIST
    try:
        playlists = sorted(PlaylistItem.select(), key=lambda item: item.position)

        LOCAL_PLAYLIST = sorted(
            [
                playlist
                for playlist in playlists
                if playlist.type == PlaylistTypes.LOCAL.value
            ],
            key=lambda item: item.position,
        )
        YOUTUBE_PLAYLIST = sorted(
            [
                playlist
                for playlist in playlists
                if playlist.type == PlaylistTypes.YOUTUBE.value
            ],
            key=lambda item: item.position,
        )

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


async def play_current_item(ctx: ActionContext):
    # Get the current item index
    current_item_index = (
        current_local_playlist_item_index
        if current_playlist_type is PlaylistTypes.LOCAL
        else current_youtube_playlist_item_index
    )
    current_item = (
        LOCAL_PLAYLIST[current_item_index]
        if current_playlist_type is PlaylistTypes.LOCAL
        else YOUTUBE_PLAYLIST[current_item_index]
    )

    # Play it once again
    return await play_playlist_item(ctx, current_item, current_item_index)


async def switch_playlist_type(ctx: ActionContext, type=None):
    """
    Switches between LOCAL and YOUTUBE type

    Args:
        ctx (ActionContext)
    """
    global current_playlist_type
    with playlist_type_lock:
        if type is not None:
            current_playlist_type = type
        else:
            current_playlist_type = PlaylistTypes.next(current_playlist_type)

        # Announce the mode change
        await say(
            ctx,
            ctx.translations.get_translation(
                "mode_local"
                if current_playlist_type is PlaylistTypes.LOCAL
                else "mode_youtube"
            ),
        )

        return await play_current_item(ctx)


async def play_playlist_item_from_object(
    ctx: ActionContext, playlist_item: PlaylistItem
) -> PlaylistTypes:
    playlist_item_index = None
    for index, item in enumerate(get_playlist_items(type=playlist_item.type)):
        if str(item["id"]) == str(playlist_item.id):
            playlist_item_index = index

    type_friendly = PlaylistTypes(playlist_item.type)

    if playlist_item_index is None:
        logger.error(
            f"Playlist item index that user wants to play (id: {playlist_item.id}) is None"
        )
        return {
            "success": False,
            "error": f"Playlist item index that user wants to play (id: {playlist_item.id}) is None",
        }

    with playlist_type_lock:
        global current_playlist_type
        if current_playlist_type is not type_friendly:
            current_playlist_type = type_friendly

    await play_playlist_item(ctx, playlist_item, playlist_item_index)

    return type_friendly.name


def get_playlist_item_new_position(type: PlaylistTypes) -> int:
    """
    Since all playlist items have their position, when creating a new one, its position will be type's last one + 1

    Args:
        type (PlaylistTypes)

    Returns:
        int: New position
    """
    if type is PlaylistTypes.LOCAL:
        return len(LOCAL_PLAYLIST)
    elif type is PlaylistTypes.YOUTUBE:
        return len(YOUTUBE_PLAYLIST)
