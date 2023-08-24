from typing import Awaitable, Callable, Optional

from homeassistant_api import Domain
from action_context import ActionContext

from announcements import say_current_time
from playlist import next_playlist_item
from playback import toggle_playback_state, get_current_volume, set_current_volume
from weather import get_weather


class Action:
    should_gather_numeric_value = False

    def __init__(
        self,
        handler: Callable[[ActionContext], Awaitable[None]],
        change_numeric_value=False,
        numeric_value_multiplier=1,
        numeric_value_range: Optional[tuple[int, int]] = (0, 100),
        init_value_getter: Optional[
            Callable[[ActionContext], Awaitable[tuple[int, Optional[Domain]]]]
        ] = None,
    ):
        self.handler = handler
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


# A dict of all the actions. The key is the class_name and value is the action
ACTIONS: dict[int, Optional[Action]] = {
    1: Action(
        handler=set_current_volume,
        change_numeric_value=True,
        numeric_value_range=(0, 100),
        numeric_value_multiplier=5,
        init_value_getter=get_current_volume,
    ),
    2: Action(handler=next_playlist_item),
    4: Action(handler=toggle_playback_state),
    7: Action(handler=say_current_time),
    8: Action(handler=get_weather),
}
