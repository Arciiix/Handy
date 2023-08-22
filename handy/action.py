from typing import Awaitable, Callable, Optional

from playback import toggle_playback_state
from action_context import ActionContext


class Action:
    should_gather_numeric_value = False

    def __init__(
        self,
        handler: Callable[[ActionContext], Awaitable[None]],
        should_gather_numeric_value=False,
    ):
        # If true, after user does the gesture, Handy will then ask to indicate a numeric value with the hand
        # TODO
        self.handler = handler
        self.should_gather_numeric_value = should_gather_numeric_value


# A dict of all the actions. The key is the class_name and value is the action
ACTIONS: dict[int, Optional[Action]] = {1: Action(handler=toggle_playback_state)}
