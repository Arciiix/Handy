from os import path
import time
import cv2
import mediapipe as mp
import numpy as np
import pandas as pd

from config import CONFIG
from angle import calculate_angle_from_obj
from config import HANDY_MODEL_WINDOW, HANDY_WINDOW

mp_drawing = mp.solutions.drawing_utils
mp_holistic = mp.solutions.holistic


def handle_frame(frame: cv2.typing.MatLike, holistic, model):
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
    # If a pose was detected in the image
    if results.pose_landmarks is not None:
        # Calculate the angles
        # See train/angles.png for more info

        landmarks = results.pose_landmarks.landmark
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

        print(f"Angles: {', '.join([f'{angle:.2f}' for angle in angles])}")

        # Try to make pose guess
        X = [angles]
        body_language_class = model.predict(X)[0]
        body_language_prob = model.predict_proba(X)[0]

        if CONFIG.is_dev:
            model_frame = cv2.imread(
                path.join(
                    path.dirname(__file__),
                    "train",
                    "poses",
                    f"{body_language_class}.png",
                )
            )
            cv2.putText(
                model_frame,
                f"{body_language_class} / {(body_language_prob[body_language_class] * 100):.2f}",
                (0, 50),
                cv2.FONT_HERSHEY_SIMPLEX,
                2,
                (255, 0, 0),
                2,
            )

    else:
        print("No pose detected in the image")
        model_frame = np.zeros((560, 680, 3), dtype=np.uint8)
    if CONFIG.is_dev:
        cv2.imshow(HANDY_MODEL_WINDOW, model_frame)
        cv2.imshow(HANDY_WINDOW, image)

    print(time.time() - start_time)
