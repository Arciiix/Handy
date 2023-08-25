import asyncio
import uuid
from aiohttp import web
import aiohttp_cors

import socketio
from schematics.exceptions import DataError

from logger import logger
from config import CONFIG
from dto import PlaylistItemCreateDto, PlaylistItemEditDto
from db import PlaylistItem, PlaylistTypes
from playlist import update_playlists, get_playlist_items

sio = socketio.AsyncServer(async_mode="aiohttp", cors_allowed_origins=["*"])


@sio.event
async def connect(sid, environ):
    logger.info(f"New socket connected: {sid}")


@sio.event
async def disconnect(sid):
    logger.info(f"Socket {sid} disconnected")


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

    previous_playlist.delete_instance()
    await update_playlists(sio)

    logger.info(f"Removed playlist item {data['id']}")

    return {"success": True, "playlists": get_playlist_items()}


app = web.Application()
sio.attach(app)


async def hello_handler(request):
    return web.Response(text="Hello from Handy!")


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


def init_socket():
    logger.info(f"Socket.io starting on port: {CONFIG.socket_io_port}")
    web.run_app(app, port=CONFIG.socket_io_port)
