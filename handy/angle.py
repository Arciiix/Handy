import numpy as np


def calculate_angle_from_obj(a, b, c):
    a = (a.x, a.y)  # First
    b = (b.x, b.y)  # Mid - the angle corner
    c = (c.x, c.y)  # End

    return calculate_angle(a, b, c)


def calculate_angle(a, b, c):
    """
    Calculates the angle ABC given (x, y) of A, B and C

    Args:
        a (x, y)
        b (x, y)
        c (x, y)

    Returns:
        float: Angle (degrees)
    """
    # Define points
    A = np.array(a)
    B = np.array(b)
    C = np.array(c)

    # Calculate vectors
    BA = A - B
    BC = C - B

    # Calculate the cosine of the angle
    cosine_angle = np.dot(BA, BC) / (np.linalg.norm(BA) * np.linalg.norm(BC))

    # Calculate the angle and convert it to degrees
    angle = np.arccos(cosine_angle)
    angle_deg = np.degrees(angle)

    return angle_deg
