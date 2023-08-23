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
from config import HANDY_MODEL_WINDOW, HANDY_WINDOW, ROI, TROI

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

    # Recolor feed
    image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
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

    # Draw the ROI on the image
    if ROI is not None and CONFIG.is_dev:
        cv2.rectangle(
            image, (ROI["x1"], ROI["y1"]), (ROI["x2"], ROI["y2"]), (255, 0, 0), 2
        )

    # Draw the T-ROI (tracking ROI) on the image
    if TROI is not None and CONFIG.is_dev:
        cv2.rectangle(
            image, (TROI["x1"], TROI["y1"]), (TROI["x2"], TROI["y2"]), (0, 0, 255), 2
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
            landmarks[28].x * CONFIG.resize_width,
            landmarks[28].y * CONFIG.resize_height,
        )
        left_leg_x, left_leg_y = (
            landmarks[27].x * CONFIG.resize_width,
            landmarks[27].y * CONFIG.resize_height,
        )
        x1, x2, y1, y2 = ROI["x1"], ROI["x2"], ROI["y1"], ROI["y2"]

        logger.debug(
            f"Legs coords: ({right_leg_x}, {right_leg_y}), ({left_leg_x}, {left_leg_y}); ROI = ({x1}, {y1}), ({x2}, {y2})"
        )

        # So when ROI isn't defined or the legs fit, start checking further
        if ROI is None or (
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
            else:
                logger.info("Detected person is not in ROI")
    else:
        logger.info("No pose detected in the image")

    if CONFIG.is_dev:
        if not dont_predict_pose:
            cv2.imshow(HANDY_MODEL_WINDOW, model_frame)
        cv2.imshow(HANDY_WINDOW, image)

    # logger.info(f"It took {time.time() - start_time}s")

    return (angles, predicted_class, predicted_proba)
