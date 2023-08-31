import base64
from datetime import datetime
from typing import Awaitable, Callable, Optional
import cv2

from homeassistant_api import Domain
from action_context import ActionContext

from announcements import say_current_time
from playlist import next_playlist_item, switch_playlist_type
from playback import (
    toggle_playback_state,
    get_current_volume,
    set_current_volume,
)
from weather import get_weather
from config import CONFIG
from logger import logger


class Action:
    should_gather_numeric_value = False

    def __init__(
        self,
        handler: Callable[[ActionContext], Awaitable[None]],
        friendly_name: str,
        change_numeric_value=False,
        numeric_value_multiplier=1,
        numeric_value_range: Optional[tuple[int, int]] = (0, 100),
        init_value_getter: Optional[
            Callable[[ActionContext], Awaitable[tuple[int, Optional[Domain]]]]
        ] = None,
    ):
        self.handler = handler

        # Name displayed on mobile app
        self.friendly_name = friendly_name

        # If true, after user does the gesture, Handy will then ask to indicate a numeric value with the hands
        self.change_numeric_value = change_numeric_value

        # If change_numeric_value = True, this value is a multiplier of numeric value, i.e. how much value should change on single input
        self.numeric_value_multiplier = numeric_value_multiplier

        # Min and max numeric_value
        self.numeric_value_range = numeric_value_range

        # A function used to retrieve the initial numeric_value. Only useful is change_numeric_value = True
        # This function is also called at numeric_value mount, so it's a perfect place to indicate about the change
        # It returns a tuple of the initial value + optionally Home Assistant domain (to reduce further requests)
        self.init_value_getter = init_value_getter

    def to_dict(self) -> dict[str, any]:
        return {
            "name": self.friendly_name,
            "changeNumericValue": self.change_numeric_value,
            "numericValueMultiplier": self.numeric_value_multiplier,
            "numericValueRange": self.numeric_value_range,
        }


class ActionPerformed:
    """
    A class that represents the type of an already done action
    """

    def __init__(
        self,
        action: Action,
        index: int,
        image: Optional[cv2.typing.MatLike] = None,
        timestamp: datetime = datetime.now(),
    ):
        self.action = action
        self.index = index  # The action gesture index
        self.image = image
        self.timestamp = timestamp

    def to_dict(self):
        image_string = None
        if self.image is not None:
            _, image = cv2.imencode(".jpg", self.image, [cv2.IMWRITE_JPEG_QUALITY, 50])
            image_string = base64.b64encode(image).decode()
        return {
            **self.action.to_dict(),
            "index": self.index,
            "image": image_string,
            "timestamp": self.timestamp.isoformat(),
        }


actions_perform_history: list[ActionPerformed] = []


def add_action_performed(
    action: Action, gesture_index: int, frame: Optional[cv2.typing.MatLike] = None
):
    global actions_perform_history
    performed = ActionPerformed(
        action=action, index=gesture_index, image=frame, timestamp=datetime.now()
    )
    actions_perform_history.append(performed)

    if len(actions_perform_history) > CONFIG.action_performed_history_length:
        actions_perform_history.pop(0)
    logger.info("Added new performed action")


def get_actions_performed():
    return actions_perform_history


# A dict of all the actions. The key is the class_name and value is the action
ACTIONS: dict[int, Optional[Action]] = {
    1: Action(
        handler=set_current_volume,
        friendly_name="Set current volume",
        change_numeric_value=True,
        numeric_value_range=(0, 100),
        numeric_value_multiplier=5,
        init_value_getter=get_current_volume,
    ),
    2: Action(
        handler=next_playlist_item,
        friendly_name="Next playlist item",
    ),
    4: Action(
        handler=toggle_playback_state,
        friendly_name="Toggle playback state",
    ),
    5: Action(
        handler=switch_playlist_type,
        friendly_name="Switch playlist type",
    ),
    7: Action(
        handler=say_current_time,
        friendly_name="Say current time",
    ),
    8: Action(
        handler=get_weather,
        friendly_name="Say the weather",
    ),
}
