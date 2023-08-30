import asyncio
import base64
import threading
import uuid
from aiohttp import web
import aiohttp_cors
import cv2

import socketio
from schematics.exceptions import DataError

from action_context import ActionContext
from logger import logger
from config import CONFIG
from dto import PlaylistItemCreateDto, PlaylistItemEditDto, PlaylistItemRearrangeDto
from db import PlaylistItem, PlaylistTypes, db
from services import get_services
from playlist import (
    update_playlists,
    get_playlist_items,
    switch_playlist_type,
    current_playlist_type,
    get_playlist_item_new_position,
    get_playlist_info,
    play_playlist_item_from_object,
)
from playback import get_playback_state, get_current_volume_only
from youtube import get_youtube_video_info
from utils.working_hours import is_inside_working_hours
from utils.current_image import get_current_image, get_current_image_changed_at

sio = socketio.AsyncServer(async_mode="aiohttp", cors_allowed_origins=["*"])


# Since it's a separate thread, we have to get the services again
hass_client, translations = None, None

number_of_socket_clients = 0
is_handy_enabled = True

status_change_lock = threading.Lock()


def get_is_enabled() -> bool:
    """
    Gets whether Handy is currently enabled or no

    Returns:
        bool
    """

    return is_handy_enabled


@sio.event
async def connect(sid, environ):
    global number_of_socket_clients
    number_of_socket_clients += 1
    logger.info(f"New socket connected: {sid}")


@sio.event
async def disconnect(sid):
    global number_of_socket_clients
    number_of_socket_clients -= 1
    logger.info(f"Socket {sid} disconnected")


@sio.on("handy/info")
async def get_current_info(sid, data):
    """
    Gets basic info, like playlists and current status
    """
    return {
        "isEnabled": is_handy_enabled,
        "inWorkingHours": is_inside_working_hours(),
        **get_playlist_info(),
    }


@sio.on("handy/change_status")
async def change_status(sid, data):
    is_enabled = data.get("isEnabled", True)
    with status_change_lock:
        global is_handy_enabled
        is_handy_enabled = is_enabled

    logger.info(f"Is enabled changed to {is_enabled}")

    return {"success": True, "isEnabled": is_handy_enabled}


@sio.on("handy/preview")
async def get_preview(sid, data):
    image = get_current_image()
    image_string = None
    if image is not None:
        _, image = cv2.imencode(".jpg", image, [cv2.IMWRITE_JPEG_QUALITY, 50])
        image_string = base64.b64encode(image).decode()

    return {
        "success": True,
        "preview": image_string,
        "image_mimetype": "data:image/jpeg;base64",
        "changed_at": get_current_image_changed_at().isoformat(),
    }


@sio.on("playback/state")
async def get_current_playback_state(sid, data):
    ctx = ActionContext(
        confidency=1, db=db, home_assistant=hass_client, translations=translations
    )
    try:
        logger.info("Trying to get current playback state")
        return {
            "success": True,
            "state": (await get_playback_state(ctx))[0].state,
            "volume": await get_current_volume_only(ctx),
        }
    except Exception as err:
        logger.exception(err)
        return {"success": False, "error": str(err)}


@sio.on("playlist/switch_type")
async def switch_type(sid, data):
    type = data.get("type", None)

    if type is not None:
        try:
            # Check whether user provided the correct type
            type = PlaylistTypes[type].value  # Convert to value as well
        except KeyError:
            return {
                "success": False,
                "error": f"{type} does not exist in the playlist item types enum",
            }

    ctx = ActionContext(
        confidency=1, db=db, home_assistant=hass_client, translations=translations
    )
    await switch_playlist_type(ctx, type=type)

    logger.info(f"Playlist mode changed to {current_playlist_type}")
    return {"success": True, "mode": PlaylistTypes(current_playlist_type).name}


@sio.on("playlist_item/all")
async def get_all_playlist_items(sid, data):
    type = data.get("type", None)

    if type is not None:
        try:
            # Check whether user provided the correct type
            type = PlaylistTypes[type].value  # Convert to value as well
        except KeyError:
            return {
                "success": False,
                "error": f"{type} does not exist in the playlist item types enum",
            }
    return get_playlist_items(type)


@sio.on("playlist_item/add")
async def playlist_item_add(
    sid,
    data,
):
    logger.info(f"[{sid}] Add new playlist item")
    # Validate data
    try:
        dto = PlaylistItemCreateDto(data)
        dto.validate()
    except Exception as err:
        logger.warning(err)
        return {"success": False, "error": str(err)}

    playlist_item = PlaylistItem(
        id=uuid.uuid4(),
        name=dto.name,
        pronunciation=dto.pronunciation,
        url=dto.url,
        type=PlaylistTypes[dto.type].value,
        position=get_playlist_item_new_position(PlaylistTypes[dto.type]),
    )
    playlist_item.save(force_insert=True)

    await update_playlists(sio)

    return {
        "success": True,
        "playlistItem": playlist_item.to_dict(),
        "playlists": get_playlist_items(),
    }


@sio.on("playlist_item/edit")
async def playlist_item_add(
    sid,
    data,
):
    logger.info(f"[{sid}] Edit playlist item")

    if not data.get("id", None):
        return {"success": False, "error": "No id provided"}

    # Validate data
    try:
        dto = PlaylistItemEditDto(data)
        dto.validate()
    except Exception as err:
        logger.warning(err)
        return {"success": False, "error": str(err)}

    playlist_item = PlaylistItem.get_or_none(PlaylistItem.id == data["id"])

    if playlist_item is None:
        return {"success": False, "error": "Item doesn't exist"}

    # Update the item
    if data.get("name"):
        playlist_item.name = data["name"]

    if data.get("pronunciation"):
        playlist_item.pronunciation = data["pronunciation"]

    if data.get("url"):
        playlist_item.url = data["url"]

    if data.get("type"):
        playlist_item.type = PlaylistTypes[data["type"]].value

    # Note that position isn't changed here

    playlist_item.save()

    logger.info(f"Playlist {data['id']} has been updated")
    await update_playlists(sio)

    return {
        "success": True,
        "playlistItem": playlist_item.to_dict(),
        "playlists": get_playlist_items(),
    }


@sio.on("playlist_item/delete")
async def playlist_item_remove(
    sid,
    data,
):
    logger.info(f"[{sid}] Remove playlist item")

    if not data.get("id", None):
        return {"success": False, "error": "No id provided"}

    previous_playlist = PlaylistItem.get_or_none(PlaylistItem.id == data["id"])
    if previous_playlist is None:
        return {"success": False, "error": "Item doesn't exist"}

    previous_position = previous_playlist.position

    with db.atomic():
        previous_playlist.delete_instance()
        logger.info(f"Removed playlist item {data['id']}")

        # Fix the positions
        query = PlaylistItem.update(position=PlaylistItem.position - 1).where(
            PlaylistItem.position > previous_position,
            PlaylistItem.type == previous_playlist.type,
        )

        query.execute()

        logger.info(f"Fixed the positions after item removal")

    await update_playlists(sio)

    return {"success": True, "playlists": get_playlist_items()}


@sio.on("playlist_item/rearrange")
async def rearrange_items(sid, data):
    # Validate data
    try:
        dto = PlaylistItemRearrangeDto(data)
        dto.validate()
    except Exception as err:
        logger.warning(err)
        return {"success": False, "error": str(err)}

    # Get the previous playlist
    previous_playlist_item = PlaylistItem.get_or_none(PlaylistItem.id == data["id"])
    if previous_playlist_item is None:
        return {"success": False, "error": "Item doesn't exist"}

    old_position = previous_playlist_item.position
    new_position = data["new_position"]

    # Check if the new position is even possible
    # Check it by simply obtaining the new position for the item and seeing if it's lower than the user's desired new position
    type = PlaylistTypes(previous_playlist_item.type)
    if new_position >= get_playlist_item_new_position(type):
        return {"success": False, "error": "The new position is too high"}

    with db.atomic():
        # Determine the direction of the rearrangement (up or down)
        direction = 1 if new_position < old_position else -1

        # Update positions of items in the specified range
        query = PlaylistItem.update(position=PlaylistItem.position + direction).where(
            (PlaylistItem.position >= min(old_position, new_position)),
            (PlaylistItem.position <= max(old_position, new_position)),
            (
                PlaylistItem.id != previous_playlist_item.id
            ),  # Exclude the item being moved,
            (PlaylistItem.type == previous_playlist_item.type),
        )
        query.execute()

        # Set the new position for the item
        previous_playlist_item.position = new_position
        previous_playlist_item.save()

        await update_playlists()

        logger.info(
            f"Playlist item {previous_playlist_item.id} has been moved from position {old_position} to {new_position}"
        )
    return {"success": True, "playlists": get_playlist_items()}


@sio.on("playlist_item/play")
async def playlist_item_play(
    sid,
    data,
):
    logger.info(f"[{sid}] Play playlist item")

    if not data.get("id", None):
        return {"success": False, "error": "No id provided"}

    playlist_item = PlaylistItem.get_or_none(PlaylistItem.id == data["id"])

    if playlist_item is None:
        return {"success": False, "error": "Item doesn't exist"}

    ctx = ActionContext(
        confidency=1, db=db, home_assistant=hass_client, translations=translations
    )

    current_playlist_type = await play_playlist_item_from_object(ctx, playlist_item)

    return {
        "success": True,
        "item": playlist_item.to_dict(),
        "type": current_playlist_type,
    }


@sio.on("youtube/check")
async def check_youtube_video(sid, data):
    logger.info(f"[{sid}] Check YouTube video - whether audio can be retrieved")

    if not data.get("url", None):
        return {"success": False, "error": "No YouTube URL provided"}

    info = get_youtube_video_info(data["url"])

    return {"success": info["success"] and info.get("url", None) is not None}


@sio.on("youtube/info")
async def get_youtube_video_data(sid, data):
    logger.info(f"[{sid}] Get YouTube video info")

    if not data.get("url", None):
        return {"success": False, "error": "No YouTube URL provided"}

    info = get_youtube_video_info(data["url"])

    return {"success": info["success"], **info}


async def hello_handler(request):
    return web.Response(text="Hello from Handy!")


async def init():
    global hass_client, translations

    hass_client, translations = await get_services()

    app = web.Application()
    sio.attach(app)
    app.add_routes([web.get("/", hello_handler)])

    # Thanks to: https://stackoverflow.com/a/56767323
    cors = aiohttp_cors.setup(app)
    for resource in app.router._resources:
        # Because socket.io already adds cors, if you don't skip socket.io, you get error saying, you've done this already.
        if resource.raw_match("/socket.io/"):
            continue
        cors.add(
            resource,
            {
                "*": aiohttp_cors.ResourceOptions(
                    allow_credentials=True, expose_headers="*", allow_headers="*"
                )
            },
        )

    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, port=CONFIG.socket_io_port)

    try:
        await site.start()
        logger.info(f"Socket.io started on port: {CONFIG.socket_io_port}")
        await update_playlists()
        await asyncio.Event().wait()
    except KeyboardInterrupt:
        pass
    finally:
        await runner.cleanup()


def init_socket():
    asyncio.run(init())


def get_number_of_socket_clients():
    return number_of_socket_clients
