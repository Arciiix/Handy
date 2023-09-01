import cv2
from queue import Queue
from logger import logger
from threading import Thread

from config import CONFIG


class Streamer:
    def __init__(self, url):
        self.url = url
        self.latest_frame = None
        self.is_running = False

    def get_processed_frame(self):
        return self.latest_frame

    def release(self):
        logger.debug("Release the streamer")
        self.is_running = False
        self.stream.release()

    def start(self):
        logger.debug(f"Starting streamer")
        self.is_running = True
        self.stream = cv2.VideoCapture(self.url, cv2.CAP_FFMPEG)
        logger.debug(f"Streamer started")

        while self.is_running:
            ret, frame = self.stream.read()
            while not ret or frame is None:
                logger.debug(f"Empty Frame")
                continue

            frame = cv2.resize(frame, (CONFIG.resize_width, CONFIG.resize_height))
            self.latest_frame = frame
