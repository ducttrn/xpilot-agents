# Wall distance
def calculate_dom_near_wall(dist):
    if 0 <= dist <= 200:
        dom = 1
    elif 200 < dist <= 250:
        dom = (-1 / 50) * dist + 5
    else:
        dom = 0
    return dom


def calculate_dom_medium_wall(dist):
    if 200 <= dist <= 300:
        dom = (1 / 100) * dist - 2
    elif 300 < dist <= 400:
        dom = (-1 / 100) * dist + 4
    else:
        dom = 0
    return dom


def calculate_dom_far_wall(dist):
    if 350 < dist <= 450:
        dom = (1 / 100) * dist - 3.5
    elif dist > 450:
        dom = 1
    else:
        dom = 0
    return dom


# spd
def calculate_dom_low_spd(spd):
    if 0 <= spd <= 4:
        dom = 1
    elif 4 < spd <= 6:
        dom = (-1 / 2) * spd + 3
    else:
        dom = 0
    return dom


def calculate_dom_medium_spd(spd):
    if 5 <= spd <= 6:
        dom = spd - 5
    elif 6 <= spd <= 7:
        dom = 1
    elif 7 <= spd <= 8:
        dom = -spd + 8
    else:
        dom = 0
    return dom


def calculate_dom_fast_spd(spd):
    if 7 <= spd <= 10:
        dom = (1 / 3) * spd - (7 / 3)
    elif spd >= 10:
        dom = 1
    else:
        dom = 0
    return dom
