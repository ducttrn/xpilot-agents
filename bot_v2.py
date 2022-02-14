import libpyAI as ai

from object_distance import ObjectDistance
from turn_angle import TurnAngle

WALL_DIST = 450


def AI_loop():
    # Release keys
    ai.thrust(0)
    ai.turnLeft(0)
    ai.turnRight(0)
    ai.setTurnSpeed(20)
    ai.setPower(35)

    # Set variables
    heading = int(ai.selfHeadingDeg())
    tracking = int(ai.selfTrackingDeg())
    front_wall = ai.wallFeeler(2000, heading)
    left_heading_wall = ai.wallFeeler(2000, heading + 90)
    right_heading_wall = ai.wallFeeler(2000, heading - 90)
    top_wall = ai.wallFeeler(2000, 90)
    right_wall = ai.wallFeeler(2000, 0)
    left_wall = ai.wallFeeler(2000, 180)
    bottom_wall = ai.wallFeeler(2000, 270)
    track_wall = ai.wallFeeler(2000, tracking)

    enemy_id = ai.closestShipId()
    if enemy_id == -1:
        enemy_chance = 0
    else:
        enemy_distance = ObjectDistance(ai.enemyDistanceId(enemy_id))
        ai.lockClose()
        enemy_angle = TurnAngle(abs(ai.selfHeadingDeg() - ai.lockHeadingDeg()))
        enemy_chance = calculate_enemy_chance(enemy_angle, enemy_distance)

    # Turn rules
    if track_wall < WALL_DIST and left_heading_wall < right_heading_wall:
        ai.turnRight(1)
    elif track_wall < WALL_DIST and left_heading_wall >= right_heading_wall:
        ai.turnLeft(1)
    elif left_heading_wall < right_heading_wall:
        ai.turnRight(1)
    else:
        ai.turnLeft(1)

    # Thrust rules
    if ai.selfSpeed() == 0 and front_wall < 300:
        ai.thrust(0)
    elif front_wall > WALL_DIST + 350 and track_wall < WALL_DIST and ai.selfSpeed() < 10:
        ai.thrust(1)
    elif front_wall > WALL_DIST and ai.selfSpeed() < 6:
        ai.thrust(1)
        ai.fireShot()
    elif top_wall < 100:
        ai.thrust(1)
    elif right_wall < 100:
        ai.thrust(1)
    elif left_wall < 100:
        ai.thrust(1)
    elif bottom_wall < 100:
        ai.thrust(1)
        
    if enemy_chance >= 10:
        ai.fireShot()


def calculate_enemy_chance(enemy_angle: TurnAngle, enemy_distance: ObjectDistance):
    high_enemy_chance_dom_one = min(enemy_angle.small_dom, enemy_distance.near_dom)
    high_enemy_chance_dom_two = min(enemy_angle.medium_dom, enemy_distance.near_dom)
    high_enemy_chance_dom_three = min(enemy_angle.small_dom, enemy_distance.medium_dom)
    high_enemy_chance_dom = (high_enemy_chance_dom_one + high_enemy_chance_dom_two + high_enemy_chance_dom_three) / 3

    avg_enemy_chance_dom_one = min(enemy_angle.large_dom, enemy_distance.near_dom)
    avg_enemy_chance_dom_two = min(enemy_angle.medium_dom, enemy_distance.medium_dom)
    avg_enemy_chance_dom_three = min(enemy_angle.small_dom, enemy_distance.far_dom)
    avg_enemy_chance_dom = (avg_enemy_chance_dom_one + avg_enemy_chance_dom_two + avg_enemy_chance_dom_three) / 3

    low_enemy_chance_dom_one = min(enemy_angle.medium_dom, enemy_distance.far_dom)
    low_enemy_chance_dom_two = min(enemy_angle.large_dom, enemy_distance.medium_dom)
    low_enemy_chance_dom_three = min(enemy_angle.large_dom, enemy_distance.far_dom)
    low_enemy_chance_dom = (low_enemy_chance_dom_one + low_enemy_chance_dom_two + low_enemy_chance_dom_three) / 3
    return calculate_centroid(low_enemy_chance_dom, avg_enemy_chance_dom, high_enemy_chance_dom)


# Function to calculate the centroid of three aggregated outputs.
# This is done in intervals of 10, and the crisp output returned is a number 0-100.
# 30 is meant to represent 0+10+20, 180 is 30+40+50+60, and 340 is the sum of the rest of the numbers through 100.
# This is divided by the amount of intervals each degree of membership had in the sum
# (ex. low has 0, 10, and 20 so low's degree of membership is divided by 3).
def calculate_centroid(low, medium, high):
    return (30 * low + 180 * medium + 340 * high) / (3 * low + 4 * medium + 4 * high)


ai.start(AI_loop, ["-name", "bot_v2", "-join", "localhost"])
