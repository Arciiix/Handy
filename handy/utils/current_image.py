from datetime import datetime
import cv2


current_image = None
changed_at = datetime.now()


def get_current_image() -> cv2.typing.MatLike:
    """
    Gets the last image frame

    Returns:
        cv2.typing.MatLike: Image frame
    """
    return current_image


def get_current_image_changed_at() -> datetime:
    return changed_at


def set_current_image(image: cv2.typing.MatLike):
    global current_image, changed_at
    current_image = image
    changed_at = datetime.now()
