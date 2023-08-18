'''
This script is meant to be executed on the "client" device - to stream the feed from video camera to the server
'''

import socket
import pickle
import zlib
import logging
from datetime import datetime, timedelta

import cv2

from config import CLIENT_CONFIG

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')


if __name__ == "__main__":
    cap = cv2.VideoCapture(CLIENT_CONFIG["CAMERA"])
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    logging.info("Init")
    last_sending = datetime.now()
    while True:
        ret, frame = cap.read()
        if datetime.now() - last_sending < timedelta(milliseconds=1000 // CLIENT_CONFIG["FPS"]):
            continue
        logging.info("Sending video")
        last_sending = datetime.now()
        if not ret:
            break
        logging.info("Read frame")

        # Serialize and compress the frame
        serialized_frame = pickle.dumps(frame)
        compressed_frame = zlib.compress(serialized_frame)

        # Segment the compressed frame
        segments = [compressed_frame[i:i + CLIENT_CONFIG["MAX_PACKET_SIZE"]] for i in range(0, len(compressed_frame),  CLIENT_CONFIG["MAX_PACKET_SIZE"])]

        for segment in segments:
            sock.sendto(segment, (CLIENT_CONFIG["UDP_IP"], CLIENT_CONFIG["UDP_PORT"]))

        logging.info(f"Sent video ({(datetime.now() - last_sending ).seconds} s)")
        last_sending = datetime.now()

    cap.release()
    sock.close()
