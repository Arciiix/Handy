import asyncio
from collections import deque
from os import path
import pickle
import threading
import time
import cv2
from homeassistant_api import Client
import mediapipe as mp
from datetime import datetime, timedelta

import numpy as np

from config import CONFIG, HANDY_MODEL_WINDOW, HANDY_WINDOW, HANDY_TROI_WINDOW, TROI
from frame import handle_frame
from audio import AudioIndicator
from action import ACTIONS, ActionContext
from logger import logger

mp_holistic = mp.solutions.holistic
model_path = path.join(path.dirname(__file__), "train", "handy_classifier.pkl")

hass_client = Client(
    f"{CONFIG.home_assistant_ip}/api",
    CONFIG.home_assistant_token,
    use_async=True,
    async_cache_session=False,
)


async def main():
    logger.info("Handy init")

    # To prevent false detections caused by accidental gestures or model inaccuracy, store the last 10 detections
    # If a gesture is detected, the app goes faster (i.e. faster than FPS limit) and gets the next detections
    # If most of the last detections mean the same pose
    last_detections = deque([None] * CONFIG.detections_to_keep)
    is_detected_now = False  # If true, there's a person standing in ROI right now

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
        min_detection_confidence=0.6, min_tracking_confidence=0.6
    ) as holistic, open(model_path, "rb") as f:
        audio_indicator = AudioIndicator(hass_client)

        # Load the model
        model = pickle.load(f)
        logger.info("Model loaded")

        last_processing_time = datetime.now()

        # To prevent user from accidently performing the same action after they show the gesture and didn't manage to stop showing it, add some blocking delay between next action
        action_block_expire_time = datetime.now()

        # Handy can run with CONFIG.fps or CONFIG.fps_idle. This variable defines the expiration date of CONFIG.fps mode
        fast_mode_expire_time = datetime.now()

        previous_frame = None
        while True:
            is_fast_mode = fast_mode_expire_time >= datetime.now()
            ret, frame = cap.read()

            # Limit the processing to the FPS, depending whether there's a person in ROI or not
            if datetime.now() - last_processing_time < timedelta(
                milliseconds=1000 / (CONFIG.fps if is_fast_mode else CONFIG.fps_idle)
            ):
                continue
            last_processing_time = datetime.now()

            if not ret or frame is None:
                logger.warning("Frame empty")
                continue

            # Detect movement within T-ROI if fast mode isn't enabled - to enable fast mode
            if previous_frame is not None and not is_fast_mode and TROI is not None:
                curr_frame_troi = frame[
                    TROI["y1"] : TROI["y2"], TROI["x1"] : TROI["x2"]
                ]
                prev_frame_troi = previous_frame[
                    TROI["y1"] : TROI["y2"], TROI["x1"] : TROI["x2"]
                ]
                prev_frame_troi = cv2.cvtColor(prev_frame_troi, cv2.COLOR_BGR2GRAY)
                curr_frame_troi = cv2.cvtColor(curr_frame_troi, cv2.COLOR_BGR2GRAY)

                frame_diff = cv2.absdiff(prev_frame_troi, curr_frame_troi)
                _, thresh_diff = cv2.threshold(frame_diff, 30, 255, cv2.THRESH_BINARY)

                total_pixels = thresh_diff.size
                num_white_pixels = np.sum(thresh_diff == 255)
                percent_change = num_white_pixels / total_pixels
                logger.info(
                    f"Percent of ROI change since last: {(percent_change * 100):.2f})"
                )
                if percent_change > CONFIG.required_troi_percent_change:
                    fast_mode_expire_time = datetime.now() + CONFIG.fast_mode_duration
                    logger.info("Detected movement in T-ROI!")

                if CONFIG.is_dev:
                    thresh_diff = cv2.cvtColor(thresh_diff, cv2.COLOR_GRAY2BGR)
                    cv2.putText(
                        thresh_diff,
                        f"{(percent_change * 100):.2f}",
                        (0, 30),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        1,
                        (255, 0, 0),
                    )
                    cv2.imshow(HANDY_TROI_WINDOW, thresh_diff)

            angles, class_name, proba = handle_frame(frame, holistic, model)

            # If there's a person in ROI, set is_detected_now to true
            fast_mode_expire_time = (
                datetime.now() + CONFIG.fast_mode_duration
                if angles is not None
                else fast_mode_expire_time
            )

            # Update the last_detections queue
            last_detections.pop()
            last_detections.appendleft(class_name)

            # Check if there is any class that appers there the most
            most_frequent_class_name = next(
                iter(
                    [
                        element
                        for element in last_detections
                        if last_detections.count(element) > CONFIG.minimal_detections
                    ]
                ),
                None,
            )  # A fancy way of saying "get this list's first item or return None"

            # If there is a class_name which isn't 0 (default action), and the user is able to perform action, perform it
            if (
                most_frequent_class_name is not None
                and most_frequent_class_name != 0
                and action_block_expire_time <= datetime.now()
            ):
                logger.info(f"Perform class_name {most_frequent_class_name}!")
                # Clear the last detections
                last_detections = deque([None] * CONFIG.detections_to_keep)

                # await audio_indicator.play_success_sound(True)

                action_block_expire_time = datetime.now() + CONFIG.action_block_delay

                ctx = ActionContext(
                    confidency=last_detections.count(most_frequent_class_name)
                    / CONFIG.detections_to_keep,
                    home_assistant=hass_client,
                )

                if class_name in ACTIONS:
                    logger.info("Action performing - start...")
                    start_time = time.time()
                    await ACTIONS[class_name].handler(ctx)
                    logger.info(
                        f"Action performing - end, it took {time.time() - start_time}s"
                    )

            # logger.debug([angles, class_name, proba])
            previous_frame = frame

            if CONFIG.is_dev and cv2.waitKey(1) & 0xFF == ord("q"):
                break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
