from datetime import datetime

from config import CONFIG


def is_inside_working_hours() -> bool:
    """
    Checks whether the app is executing within working hours right now - there are working hours (see README)

    Returns:
        bool: If true, the app is within working hours and should execute
    """

    return (
        datetime.now().time() >= CONFIG.working_hours[0]
        and datetime.now().time() <= CONFIG.working_hours[1]
    )
