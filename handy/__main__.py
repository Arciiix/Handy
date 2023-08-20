import logging
from os import path
import pickle
from random import randint
import cv2
import mediapipe as mp
from datetime import datetime, timedelta

import numpy as np

from config import CONFIG, HANDY_MODEL_WINDOW, HANDY_WINDOW
from frame import handle_frame


mp_holistic = mp.solutions.holistic
model_path = path.join(path.dirname(__file__), "train", "handy_classifier.pkl")

# Global variables to store the starting and ending points of the rectangle
start_point = None
end_point = None
selecting = False


# Mouse callback function
def mouse_callback(event, x, y, flags, param):
    global start_point, end_point, selecting

    if event == cv2.EVENT_LBUTTONDOWN:
        start_point = (x, y)
        selecting = True
    elif event == cv2.EVENT_LBUTTONUP:
        end_point = (x, y)
        selecting = False


def main():
    if not path.exists(model_path):
        logging.error("Model not found at train/handy_classifier.pkl!")
        exit(-1)

    cap = cv2.VideoCapture(CONFIG.stream_url, cv2.CAP_FFMPEG)

    if not cap.isOpened():
        logging.error("VideoCapture not opened")
        exit(-1)

    ret = None

    cv2.namedWindow(HANDY_WINDOW)
    cv2.namedWindow(HANDY_MODEL_WINDOW)
    # Select region of interest
    cv2.setMouseCallback(HANDY_WINDOW, mouse_callback)

    while not ret:
        ret, frame = cap.read()

    with mp_holistic.Holistic(
        min_detection_confidence=0.5, min_tracking_confidence=0.5
    ) as holistic, open(model_path, "rb") as f:
        model = pickle.load(f)

        last_process = datetime.now()
        while True:
            ret, frame = cap.read()
            # DEV
            # frame = cv2.imread(f"handy/test_vid/sample{randint(1,10)}.png")

            if datetime.now() - last_process < timedelta(
                milliseconds=1000 / CONFIG.fps
            ):
                continue
            last_process = datetime.now()

            if not ret or frame is None:
                logging.warning("Frame empty")
                continue

            if start_point and end_point:
                frame = frame[
                    start_point[1] : end_point[1], start_point[0] : end_point[0]
                ]

            handle_frame(frame, holistic, model)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s"
    )
    main()
