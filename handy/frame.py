import base64
from os import path
import time
from typing import Optional
import cv2
import mediapipe as mp
import numpy as np
import pandas as pd

from logger import logger
from config import CONFIG
from angle import calculate_angle_from_obj
from config import HANDY_MODEL_WINDOW, HANDY_WINDOW, ROI, TROI, GROI
from socket_server import get_number_of_socket_clients, sio
from utils.current_image import set_current_image

mp_drawing = mp.solutions.drawing_utils
mp_holistic = mp.solutions.holistic


def handle_frame(
    frame: cv2.typing.MatLike, holistic, model, dont_predict_pose: bool = False
) -> tuple[Optional[list[float]], Optional[int], Optional[list[float]]]:
    """
    A function to handle a single frame

    Args:
        frame (cv2.typing.MatLike):
        holistic
        model

    Returns:
        tuple[Optional[list[float]], Optional[int], Optional[list[float]]]: (angles, class_name, predicted_proba). If no pose detected, then (None, None, None)
    """

    # To calculate the performance for processing a single frame, init a start_time variable
    start_time = time.time()

    # Resize frame
    frame = cv2.resize(frame, (CONFIG.resize_width, CONFIG.resize_height))

    input_frame = frame.copy()
    width, height = CONFIG.resize_width, CONFIG.resize_height
    x1, x2, y1, y2 = (
        GROI.get("x1", 0),
        GROI.get("x2", width),
        GROI.get("y1", 0),
        GROI.get("y2", height),
    )
    # If there's ROI, cut the frame to it
    if ROI is not None:
        input_frame = input_frame[ROI["y1"] : ROI["y2"], ROI["x1"] : ROI["x2"]]
        width = ROI["x2"] - ROI["x1"]
        height = ROI["y2"] - ROI["y1"]

        x2 = min(x2 - ROI["x1"], width)
        x1 = max(x1 - ROI["x1"], 0)
        y2 = min(y2 - ROI["y1"], height)
        y1 = max(y1 - ROI["y1"], 0)

    print(x1, x2, y1, y2)

    # Recolor feed
    image = cv2.cvtColor(input_frame, cv2.COLOR_BGR2RGB)
    image.flags.writeable = False

    # Make detections
    results = holistic.process(image)

    # Recolor image back to BGR for rendering
    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    mp_drawing.draw_landmarks(
        image,
        results.pose_landmarks,
        mp_holistic.POSE_CONNECTIONS,
        mp_drawing.DrawingSpec(color=(245, 117, 66), thickness=1, circle_radius=2),
        mp_drawing.DrawingSpec(color=(245, 66, 230), thickness=1, circle_radius=1),
    )

    # Draw the GROI on the image
    if GROI is not None:
        cv2.rectangle(image, (x1, y1), (x2, y2), (255, 0, 0), 2)

    # Draw the T-ROI (tracking ROI) on the image
    if TROI is not None:
        cv2.rectangle(
            image,
            (max(TROI["x1"] - ROI["x1"], 0), max(TROI["y1"] - ROI["y1"], 0)),
            (min(TROI["x2"] - ROI["x1"], width), min(TROI["y2"] - ROI["y1"], height)),
            (0, 0, 255),
            2,
        )

    angles, predicted_class, predicted_proba = None, None, None
    model_frame = np.zeros((560, 680, 3), dtype=np.uint8)

    # If a pose was detected in the image and it's within the ROI
    if results.pose_landmarks is not None:
        # Calculate the angles
        # See train/angles.png for more info

        landmarks = results.pose_landmarks.landmark

        # If user defined the ROI, check whether the legs fit within this ROI
        right_leg_x, right_leg_y = (
            landmarks[28].x * width,
            landmarks[28].y * height,
        )
        left_leg_x, left_leg_y = (
            landmarks[27].x * width,
            landmarks[27].y * height,
        )

        logger.debug(
            f"Legs coords: ({right_leg_x}, {right_leg_y}), ({left_leg_x}, {left_leg_y}); ROI = ({x1}, {y1}), ({x2}, {y2})"
        )

        # So when GROI isn't defined or the legs fit, start checking further
        if GROI is None or (
            x1 <= left_leg_x <= x2
            and x1 <= right_leg_x <= x2
            and y1 <= left_leg_y <= y2
            and y1 <= right_leg_y <= y2
        ):
            angles = []
            # Angle 0
            angles.append(
                calculate_angle_from_obj(landmarks[12], landmarks[14], landmarks[16])
            )
            # Angle 1
            angles.append(
                calculate_angle_from_obj(landmarks[11], landmarks[13], landmarks[15])
            )
            # Angle 2
            angles.append(
                calculate_angle_from_obj(landmarks[14], landmarks[12], landmarks[24])
            )
            # Angle 3
            angles.append(
                calculate_angle_from_obj(landmarks[13], landmarks[11], landmarks[23])
            )

            # logger.info(f"Angles: {', '.join([f'{angle:.2f}' for angle in angles])}")

            if not dont_predict_pose:
                # Try to make pose guess
                X = [angles]
                predicted_class = model.predict(X)[0]
                predicted_proba = model.predict_proba(X)[0]

                if CONFIG.is_dev:
                    model_frame = cv2.imread(
                        path.join(
                            path.dirname(__file__),
                            "train",
                            "poses",
                            f"{predicted_class}.png",
                        )
                    )
                    cv2.putText(
                        model_frame,
                        f"{predicted_class} / {(predicted_proba[predicted_class] * 100):.2f}",
                        (0, 50),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        2,
                        (255, 0, 0),
                        2,
                    )
            elif CONFIG.is_dev:
                # Indicate that no pose is being predicted
                model_frame = np.zeros((560, 680, 3), dtype=np.uint8)

                cv2.putText(
                    model_frame,
                    f"No pose is being predicted!",
                    (0, 50),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    2,
                    (0, 0, 255),
                    2,
                )
        else:
            logger.info("Detected person is not in G-ROI")
    else:
        logger.info("No pose detected in the image")

    if CONFIG.is_dev:
        if not dont_predict_pose:
            cv2.imshow(HANDY_MODEL_WINDOW, model_frame)
        cv2.imshow(HANDY_WINDOW, image)

    set_current_image(image)

    # logger.info(f"It took {time.time() - start_time}s")

    return (angles, predicted_class, predicted_proba)
