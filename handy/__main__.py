import logging
from os import path
import pickle
import cv2
import mediapipe as mp
from datetime import datetime, timedelta

from config import CONFIG, HANDY_MODEL_WINDOW, HANDY_WINDOW
from frame import handle_frame
from logger import logger

mp_holistic = mp.solutions.holistic
model_path = path.join(path.dirname(__file__), "train", "handy_classifier.pkl")


def main():
    # To prevent false detections caused by accidental gestures or model inaccuracy, store the last 10 detections
    # If a gesture is detected, the app goes faster (i.e. faster than FPS limit) and gets the next detections
    # # If most of the last detections mean the same pose
    last_detections = [None] * CONFIG.detections_to_keep

    logger.info("Handy init")
    # Check if the model exists
    if not path.exists(model_path):
        logger.error("Model not found at train/handy_classifier.pkl!")
        exit(-1)

    # Init the video feed
    cap = cv2.VideoCapture(CONFIG.stream_url, cv2.CAP_FFMPEG)

    if not cap.isOpened():
        logger.error("VideoCapture not opened")
        exit(-1)
    ret = False

    while not ret:
        ret, frame = cap.read()

    logger.info("Video feed opened")

    if CONFIG.is_dev:
        cv2.namedWindow(HANDY_WINDOW)
        cv2.namedWindow(HANDY_MODEL_WINDOW)

    with mp_holistic.Holistic(
        min_detection_confidence=0.8, min_tracking_confidence=0.8
    ) as holistic, open(model_path, "rb") as f:
        # Load the model
        model = pickle.load(f)
        logger.info("Model loaded")

        last_processing_time = datetime.now()

        while True:
            ret, frame = cap.read()

            # Limit the processing to the FPS
            # TODO: The fps should be fps_idle on idle and fps when pose is detected
            if datetime.now() - last_processing_time < timedelta(
                milliseconds=1000 / CONFIG.fps_idle
            ):
                continue
            last_processing_time = datetime.now()

            if not ret or frame is None:
                logger.warning("Frame empty")
                continue

            angles, class_name, proba = handle_frame(frame, holistic, model)
            logger.debug([angles, class_name, proba])

            if CONFIG.is_dev and cv2.waitKey(1) & 0xFF == ord("q"):
                break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
