import numpy as np


def calculate_angle_from_obj(a, b, c):
    a = (a.x, a.y)  # First
    b = (b.x, b.y)  # Mid - the angle corner
    c = (c.x, c.y)  # End

    return calculate_angle(a, b, c)


def calculate_angle(a, b, c):
    a = np.array(a)  # First
    b = np.array(b)  # Mid - the angle corner
    c = np.array(c)  # End

    radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(
        a[1] - b[1], a[0] - b[0]
    )
    angle = np.abs(radians * 180.0 / np.pi)

    if angle > 180.0:
        angle = 360 - angle

    return angle