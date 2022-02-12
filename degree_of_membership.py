# Degree of membership functions for wall distance
def calculate_dom_near_wall(x):
    if 0 <= x <= 200:
        y = 1
    elif 200 < x <= 250:
        y = (-1 / 50) * x + 5
    else:
        y = 0
    print(y)


def calculate_dom_medium_wall(x):
    if 200 <= x <= 300:
        y = (1 / 100) * x - 2
    elif 300 < x <= 400:
        y = (-1 / 100) * x + 4
    else:
        y = 0
    return y


def calculate_dom_far_wall(x):
    if 350 < x <= 450:
        y = (1 / 100) * x - 3.5
    elif x > 450:
        y = 1
    else:
        y = 0
    return y


# Degree of membership functions for speed
def calculate_dom_low_speed(x):
    if 0 <= x <= 4:
        y = 1
    elif 4 < x <= 6:
        y = (-1 / 2) * x + 3
    else:
        y = 0
    return y


def calculate_dom_medium_speed(x):
    if 5 <= x <= 6:
        y = x - 5
    elif 6 <= x <= 7:
        y = 1
    elif 7 <= x <= 8:
        y = -x + 8
    else:
        y = 0
    return y


def calculate_dom_fast_speed(x):
    if 7 <= x <= 10:
        y = (1 / 3) * x - (7 / 3)
    elif x >= 10:
        y = 1
    else:
        y = 0
    return y
