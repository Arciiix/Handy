import asyncio
import uuid
from aiohttp import web
import aiohttp_cors

import socketio
from schematics.exceptions import DataError

from action_context import ActionContext
from logger import logger
from config import CONFIG
from dto import PlaylistItemCreateDto, PlaylistItemEditDto
from db import PlaylistItem, PlaylistTypes, db
from services import get_services
from playlist import (
    update_playlists,
    get_playlist_items,
    switch_playlist_type,
    current_playlist_type,
    get_playlist_item_new_position,
)
from youtube import get_youtube_video_info

sio = socketio.AsyncServer(async_mode="aiohttp", cors_allowed_origins=["*"])


# Since it's a separate thread, we have to get the services again
hass_client, translations = None, None


@sio.event
async def connect(sid, environ):
    logger.info(f"New socket connected: {sid}")


@sio.event
async def disconnect(sid):
    logger.info(f"Socket {sid} disconnected")


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
        "playlist": playlist_item.to_dict(),
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
        "playlist": playlist_item.to_dict(),
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


@sio.on("youtube/info")
async def get_youtube_video_data(sid, data):
    logger.info(f"[{sid}] Get YouTube video info")

    if not data.get("url", None):
        return {"success": False, "error": "No YouTube URL provided"}

    info = get_youtube_video_info(data["url"])

    return {"success": True, **info}


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
        await asyncio.Event().wait()
    except KeyboardInterrupt:
        pass
    finally:
        await runner.cleanup()


def init_socket():
    asyncio.run(init())
