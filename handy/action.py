from typing import Optional


class Action:
    should_gather_numeric_value = False

    def __init__(self, should_gather_numeric_value=False):
        # If true, after user does the gesture, Handy will then ask to indicate a numeric value with the hand
        # TODO
        self.should_gather_numeric_value = should_gather_numeric_value


# A dict of all the actions. The key is the class_name and value is the action
ACTIONS: dict[int, Optional[Action]] = {1: Action()}
