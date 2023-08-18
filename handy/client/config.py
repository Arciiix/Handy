from handy.config import load_config

default_client_config = {
    "UDP_IP": '127.0.0.1',
    "UDP_PORT": 30001,
    "MAX_PACKET_SIZE": 65507,
    "CAMERA": "/dev/video0",
    "FPS": 1
}

CLIENT_CONFIG = load_config("config.json ", default_client_config)
