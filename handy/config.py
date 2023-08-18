import json
import logging
from os import path

def load_config(file: str, default_config: dict[str, int | str | bool]):
    if not path.exists(file):
        logging.warn("Base config doesn't exist - using the default one")
        return default_config
    
    with open(file, 'r') as json_file:
        data = json.load(json_file)

        return {**default_config, **data}

default_config = {
    "UDP_PORT": 30001,
    "MAX_PACKET_SIZE": 65507    
}

CONFIG = load_config("config.json", default_config)