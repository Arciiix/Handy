import time
import cv2
import mediapipe as mp

from config import CONFIG
from angle import calculate_angle

mp_drawing = mp.solutions.drawing_utils
mp_holistic = mp.solutions.holistic


def handle_frame(frame: cv2.typing.MatLike, holistic):
    start_time = time.time()
    # Resize frame
    frame = cv2.resize(frame, (CONFIG.resize_width, CONFIG.resize_height))

    # Recolor Feed
    image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    image.flags.writeable = False

    # Make Detections
    results = holistic.process(image)
    # print(results.face_landmarks)

    # face_landmarks, pose_landmarks, left_hand_landmarks, right_hand_landmarks

    # Recolor image back to BGR for rendering
    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    # # 1. Draw face landmarks
    # mp_drawing.draw_landmarks(image, results.face_landmarks, mp_holistic.FACEMESH_TESSELATION,
    #                          mp_drawing.DrawingSpec(color=(80,110,10), thickness=1, circle_radius=1),
    #                          mp_drawing.DrawingSpec(color=(80,256,121), thickness=1, circle_radius=1)
    #                          )

    # # 2. Right hand
    # mp_drawing.draw_landmarks(image, results.right_hand_landmarks, mp_holistic.HAND_CONNECTIONS,
    #                          mp_drawing.DrawingSpec(color=(80,22,10), thickness=1, circle_radius=2),
    #                          mp_drawing.DrawingSpec(color=(80,44,121), thickness=1, circle_radius=1)
    #                          )

    # # 3. Left Hand
    # mp_drawing.draw_landmarks(image, results.left_hand_landmarks, mp_holistic.HAND_CONNECTIONS,
    #                          mp_drawing.DrawingSpec(color=(121,22,76), thickness=1, circle_radius=2),
    #                          mp_drawing.DrawingSpec(color=(121,44,250), thickness=1, circle_radius=1)
    #                          )

    # 4. Pose Detections
    mp_drawing.draw_landmarks(
        image,
        results.pose_landmarks,
        mp_holistic.POSE_CONNECTIONS,
        mp_drawing.DrawingSpec(color=(245, 117, 66), thickness=1, circle_radius=2),
        mp_drawing.DrawingSpec(color=(245, 66, 230), thickness=1, circle_radius=1),
    )
    if results.pose_landmarks is not None:
        print("START")
        shoulder = results.pose_landmarks.landmark[
            mp_holistic.PoseLandmark.RIGHT_SHOULDER
        ]
        elbow = results.pose_landmarks.landmark[mp_holistic.PoseLandmark.RIGHT_ELBOW]
        wrist = results.pose_landmarks.landmark[mp_holistic.PoseLandmark.RIGHT_WRIST]

        angle = calculate_angle(
            (shoulder.x, shoulder.y), (elbow.x, elbow.y), (wrist.x, wrist.y)
        )
        cv2.putText(
            image,
            str(angle),
            (
                int(shoulder.x * CONFIG.resize_width),
                int(shoulder.y * CONFIG.resize_height),
            ),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (255, 0, 0),
            2,
            cv2.LINE_AA,
        )
        print("END")
    else:
        print("NONE")

    cv2.imshow("Handy", image)
    print(time.time() - start_time)
