import logging
from os import path
import pickle
import cv2
import mediapipe as mp
from datetime import datetime, timedelta

from config import CONFIG, HANDY_MODEL_WINDOW, HANDY_WINDOW
from frame import handle_frame


mp_holistic = mp.solutions.holistic
model_path = path.join(path.dirname(__file__), "train", "handy_classifier.pkl")


def main():
    # Load the model
    if not path.exists(model_path):
        logging.error("Model not found at train/handy_classifier.pkl!")
        exit(-1)
    model = pickle.load(f)

    # Init the video feed
    cap = cv2.VideoCapture(CONFIG.stream_url, cv2.CAP_FFMPEG)

    if not cap.isOpened():
        logging.error("VideoCapture not opened")
        exit(-1)
    ret = False

    while not ret:
        ret, frame = cap.read()

    if CONFIG.is_dev:
        cv2.namedWindow(HANDY_WINDOW)
        cv2.namedWindow(HANDY_MODEL_WINDOW)

    with mp_holistic.Holistic(
        min_detection_confidence=0.5, min_tracking_confidence=0.5
    ) as holistic, open(model_path, "rb") as f:
        last_processing_time = datetime.now()

        while True:
            ret, frame = cap.read()

            # Limit the processing to the FPS
            if datetime.now() - last_processing_time < timedelta(
                milliseconds=1000 / CONFIG.fps
            ):
                continue
            last_processing_time = datetime.now()

            if not ret or frame is None:
                logging.warning("Frame empty")
                continue

            handle_frame(frame, holistic, model)

            if CONFIG.is_dev and cv2.waitKey(1) & 0xFF == ord("q"):
                break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    # Set the logging level to be debug
    logging.basicConfig(
        level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s"
    )

    main()
