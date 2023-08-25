from datetime import datetime, timedelta, time
import json
import logging
from os import path

from logger import logger


def load_config(
    file: str, default_config: dict[str, int | str | bool]
) -> dict[str, int | str | bool]:
    if not path.exists(file):
        logger.warn("Base config doesn't exist - using the default one")
        return default_config

    with open(file, "r") as json_file:
        data = json.load(json_file)

        return {**default_config, **data}


class ActionEntitiesConfig:
    media_player = "media_player.mpd"
    play_pause = "media_player.volumio"
    volume = "media_player.volumio"
    weather = "weather.openweathermap"
    next_playlist_item = "media_player.mpd"

    def __init__(
        self,
        media_player=None,
        play_pause=None,
        volume=None,
        weather=None,
        next_playlist_item=None,
    ):
        self.media_player = media_player or self.media_player
        self.play_pause = play_pause or self.play_pause or media_player
        self.volume = volume or self.play_pause
        self.weather = weather or self.weather
        self.next_playlist_item = next_playlist_item or self.media_player

    def to_dict(self) -> dict[str, str]:
        return {
            "MEDIA_PLAYER_HASS_ENTITY_ID": self.media_player,
            "PLAYER_PLAYPAUSE_HASS_ENTITY_ID": self.play_pause,
            "PLAYER_VOLUME_HASS_ENTITY_ID": self.volume,
            "WEATHER_HASS_ENTITY_ID": self.weather,
            "PLAYER_NEXTPLAYLISTITEM_HASS_ENTITY_ID": self.next_playlist_item,
        }


class Config:
    stream_url = "udp://127.0.0.1:12345"
    home_assistant_token = None

    fps_idle = 0.5
    fps = 5
    resize_width = 960
    resize_height = 540
    is_dev = True
    home_assistant_ip = "http://homeassistant.local:8123"
    detections_to_keep = 20
    minimal_detections = 10
    action_block_delay = timedelta(seconds=5)
    fast_mode_duration = timedelta(seconds=3)
    required_troi_percent_change = (
        0.005  # Note that it's in range 0-1, whereas the dict value is 0-100%
    )
    get_numeric_value_interval = timedelta(seconds=1)
    numeric_value_max_waiting_time = timedelta(seconds=8)
    language = "en"
    min_arm_angle_for_numeric_value_change = 70
    working_hours = (time(8, 0), time(21, 0))
    socket_io_port = 4001

    entities = ActionEntitiesConfig()

    def __init__(self):
        config = load_config(
            path.join(path.dirname(__file__), "config.json"),
            self.to_dict(),
        )
        self.from_dict(config)

    def from_dict(self, dict: dict[str, int]):
        self.stream_url = dict["STREAM_URL"]
        self.home_assistant_token = dict["HOME_ASSISTANT_TOKEN"]

        self.fps_idle = dict["FPS_IDLE"]
        self.fps = dict["FPS"]
        self.resize_width = dict["RESIZE_WIDTH"]
        self.resize_height = dict["RESIZE_HEIGHT"]
        self.is_dev = dict["ENV"] == "DEV"
        self.home_assistant_ip = dict["HOME_ASSISTANT_IP"]
        self.detections_to_keep = dict["DETECTIONS_TO_KEEP"]
        self.minimal_detections = dict["MINIMAL_DETECTIONS"]
        self.action_block_delay = timedelta(seconds=dict["ACTION_BLOCK_DELAY_SECONDS"])
        self.fast_mode_duration = timedelta(seconds=dict["FAST_MODE_DURATION_SECONDS"])
        self.required_troi_percent_change = dict["REQUIRED_TROI_PERCENT_CHANGE"] / 100
        self.numeric_value_max_waiting_time = timedelta(
            seconds=dict["NUMERIC_VALUE_MAX_WAITING_TIME_SECONDS"]
        )
        self.get_numeric_value_interval = timedelta(
            seconds=dict["GET_NUMERIC_VALUE_INTERVAL_SECONDS"]
        )
        self.language = dict["LANGUAGE"]
        self.min_arm_angle_for_numeric_value_change = dict[
            "MIN_ARM_ANGLE_FOR_NUMERIC_VALUE_CHANGE"
        ]
        self.working_hours = (
            time(
                dict["TIME_START_MINUTES_AFTER_MIDNIGHT"] // 60,
                dict["TIME_START_MINUTES_AFTER_MIDNIGHT"] % 60,
            ),
            time(
                dict["TIME_END_MINUTES_AFTER_MIDNIGHT"] // 60,
                dict["TIME_END_MINUTES_AFTER_MIDNIGHT"] % 60,
            ),
        )
        self.socket_io_port = dict["SOCKET_IO_PORT"]

        self.entities = ActionEntitiesConfig(
            media_player=dict["MEDIA_PLAYER_HASS_ENTITY_ID"],
            play_pause=dict["PLAYER_PLAYPAUSE_HASS_ENTITY_ID"],
            volume=dict["PLAYER_VOLUME_HASS_ENTITY_ID"],
            weather=dict["WEATHER_HASS_ENTITY_ID"],
            next_playlist_item=dict["PLAYER_NEXTPLAYLISTITEM_HASS_ENTITY_ID"],
        )

    def to_dict(self):
        return {
            "STREAM_URL": self.stream_url,
            "HOME_ASSISTANT_TOKEN": self.home_assistant_token,
            "FPS_IDLE": self.fps_idle,
            "FPS": self.fps,
            "RESIZE_WIDTH": self.resize_width,
            "RESIZE_HEIGHT": self.resize_height,
            "ENV": "DEV" if self.is_dev else "PROD",
            "HOME_ASSISTANT_IP": self.home_assistant_ip,
            "DETECTIONS_TO_KEEP": self.detections_to_keep,
            "MINIMAL_DETECTIONS": self.minimal_detections,
            "ACTION_BLOCK_DELAY_SECONDS": self.action_block_delay.total_seconds(),
            "FAST_MODE_DURATION_SECONDS": self.fast_mode_duration.total_seconds(),
            "REQUIRED_TROI_PERCENT_CHANGE": self.required_troi_percent_change * 100,
            "NUMERIC_VALUE_MAX_WAITING_TIME_SECONDS": self.numeric_value_max_waiting_time.total_seconds(),
            "GET_NUMERIC_VALUE_INTERVAL_SECONDS": self.get_numeric_value_interval.total_seconds(),
            "LANGUAGE": self.language,
            "MIN_ARM_ANGLE_FOR_NUMERIC_VALUE_CHANGE": self.min_arm_angle_for_numeric_value_change,
            "TIME_START_MINUTES_AFTER_MIDNIGHT": self.working_hours[0].hour * 60
            + self.working_hours[0].minute,
            "TIME_END_MINUTES_AFTER_MIDNIGHT": self.working_hours[1].hour * 60
            + self.working_hours[1].minute,
            "SOCKET_IO_PORT": self.socket_io_port,
            **(self.entities.to_dict()),
        }


HANDY_WINDOW = "Handy"
HANDY_MODEL_WINDOW = "Handy - model"
HANDY_TROI_WINDOW = "Handy - T-ROI"

ROI = None
try:
    with open(path.join(path.dirname(__file__), "ROI.json")) as f:
        ROI = json.load(f)
        if not all(key in ROI for key in ("x1", "y1", "x2", "y2")):
            logger.error("Invalid ROI.json file! Using no ROI")
            ROI = None
        else:
            logger.info(
                f"ROI ({ROI['x1']}, {ROI['y1']}), ({ROI['x2']}, {ROI['y2']}) loaded"
            )

except FileNotFoundError:
    logger.warning(
        "ROI.json doesn't exist - the whole area of image will be considered in gesture detection. Consider checking the Select_ROI.ipynb notebook in handy/utils"
    )


TROI = None
try:
    with open(path.join(path.dirname(__file__), "TROI.json")) as f:
        TROI = json.load(f)
        if not all(key in TROI for key in ("x1", "y1", "x2", "y2")):
            logger.error("Invalid TROI.json file! Using no T-ROI")
            TROI = None
        else:
            logger.info(
                f"T-ROI ({TROI['x1']}, {TROI['y1']}), ({TROI['x2']}, {TROI['y2']}) loaded"
            )

except FileNotFoundError:
    logger.warning(
        "TROI.json doesn't exist - the Handy video feed will run in low FPS all the time unless the gesture is detected. Consider checking the Select_ROI.ipynb notebook in handy/utils"
    )

GROI = None
try:
    with open(path.join(path.dirname(__file__), "GROI.json")) as f:
        GROI = json.load(f)
        if not all(key in GROI for key in ("x1", "y1", "x2", "y2")):
            logger.error("Invalid GROI.json file! Using no G-ROI")
            GROI = None
        else:
            logger.info(
                f"G-ROI ({GROI['x1']}, {GROI['y1']}), ({GROI['x2']}, {GROI['y2']}) loaded"
            )

except FileNotFoundError:
    logger.warning(
        "GROI.json doesn't exist - the Handy video feed will run in low FPS all the time unless the gesture is detected. Consider checking the Select_ROI.ipynb notebook in handy/utils"
    )

CONFIG = Config()


def validate_config():
    if not CONFIG.home_assistant_token:
        logger.error(
            "No Home Assistant long-lived access token was provided in the config! See README for more information."
        )
        exit(-1)


validate_config()


SOUND_SUCCESS = "Handy_success.mp3"
