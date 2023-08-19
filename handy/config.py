import json
import logging
from os import path


def load_config(
    file: str, default_config: dict[str, int | str | bool]
) -> dict[str, int | str | bool]:
    if not path.exists(file):
        logging.warn("Base config doesn't exist - using the default one")
        return default_config

    with open(file, "r") as json_file:
        data = json.load(json_file)

        return {**default_config, **data}


class Config:
    stream_url = "udp://127.0.0.1:12345"
    fps = 10
    resize_width = 960
    resize_height = 540

    def __init__(self):
        config = load_config(
            path.join(path.dirname(__file__), "config.json"),
            self.to_dict(),
        )
        self.from_dict(config)

    def from_dict(self, dict: dict[str, int]):
        self.stream_url = dict["STREAM_URL"]
        self.fps = dict["FPS"]
        self.resize_width = dict["RESIZE_WIDTH"]
        self.resize_height = dict["RESIZE_HEIGHT"]

    def to_dict(self):
        return {
            "STREAM_URL": self.stream_url,
            "FPS": self.fps,
            "RESIZE_WIDTH": self.resize_width,
            "RESIZE_HEIGHT": self.resize_height,
        }


CONFIG = Config()
