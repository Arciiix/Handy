from datetime import timedelta
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


class Config:
    stream_url = "udp://127.0.0.1:12345"
    home_assistant_token = None

    fps_idle = 0.5
    fps = 5
    resize_width = 960
    resize_height = 540
    is_dev = True
    home_assistant_ip = "http://homeassistant.local:8123"
    media_player_hass_entity_id = None
    detections_to_keep = 20
    minimal_detections = 10
    action_block_delay = timedelta(seconds=5)
    fast_mode_duration = timedelta(seconds=3)
    required_troi_percent_change = (
        0.003  # Note that it's in range 0-1, whereas the dict value is 0-100%
    )

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
        self.media_player_hass_entity_id = dict["MEDIA_PLAYER_HASS_ENTITY_ID"]
        self.detections_to_keep = dict["DETECTIONS_TO_KEEP"]
        self.minimal_detections = dict["MINIMAL_DETECTIONS"]
        self.action_block_delay = timedelta(seconds=dict["ACTION_BLOCK_DELAY_SECONDS"])
        self.fast_mode_duration = timedelta(seconds=dict["FAST_MODE_DURATION_SECONDS"])
        self.required_troi_percent_change = dict["REQUIRED_TROI_PERCENT_CHANGE"] / 100

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
            "MEDIA_PLAYER_HASS_ENTITY_ID": self.media_player_hass_entity_id,
            "DETECTIONS_TO_KEEP": self.detections_to_keep,
            "MINIMAL_DETECTIONS": self.minimal_detections,
            "ACTION_BLOCK_DELAY_SECONDS": self.action_block_delay.total_seconds(),
            "FAST_MODE_DURATION_SECONDS": self.fast_mode_duration.total_seconds(),
            "REQUIRED_TROI_PERCENT_CHANGE": self.required_troi_percent_change * 100,
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

CONFIG = Config()


def validate_config():
    if not CONFIG.home_assistant_token:
        logger.error(
            "No Home Assistant long-lived access token was provided in the config! See README for more information."
        )
        exit(-1)


validate_config()


SOUND_SUCCESS = "Handy_success.mp3"
