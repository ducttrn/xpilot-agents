import math

import libpyAI as ai
from object_distance import ObjectDistance
from turn_angle import TurnAngle
from wall_distance import WallDistance
from speed import Speed


def AI_loop():
    ai.thrust(0)
    ai.turnLeft(0)
    ai.turnRight(0)
    ai.setTurnSpeed(20)
    ai.setPower(35)

    # Wall Avoidance
    tracking = int(ai.SelfTrackingDeg())
    track_wall = ai.wallFeeler(2000, tracking)
    wall_dist = WallDistance(track_wall)
    bot_speed = Speed(ai.selfSpeed())
    wall_danger = calculate_wall_danger(wall_dist, bot_speed)

    # Offense
    enemy_id = ai.closestShipId()
    if enemy_id == -1:
        enemy_chance = 0
    else:
        enemy_distance = ObjectDistance(ai.enemyDistanceId(enemy_id))
        ai.lockClose()
        enemy_angle = TurnAngle(abs(ai.selfHeadingDeg() - ai.lockHeadingDeg()))
        enemy_chance = calculate_enemy_chance(enemy_angle, enemy_distance)

    # Defense
    bullet_xcoor = ai.closestItemX()
    bullet_ycoor = ai.closestItemY()
    ship_xcoor = ai.selfX()
    ship_ycoor = ai.selfY()

    # Calculating Euclidean dist between ship and bullet
    bullet_dis = math.dist([bullet_xcoor, bullet_ycoor], [ship_xcoor, ship_ycoor])

    # Calculating the angle between the ship and the bullet
    alpha = abs(ship_xcoor - bullet_xcoor) / bullet_dis
    bullet_ang = math.degrees(math.asin(alpha))

    bullet_dist = ObjectDistance(bullet_dis)
    bullet_angle = TurnAngle(bullet_ang)
    bullet_danger = calculate_bullet_danger(bullet_dist, bullet_angle)

    heading = int(ai.selfHeadingDeg())
    left_wall = ai.wallFeeler(2000, heading + 90)
    right_wall = ai.wallFeeler(2000, heading - 90)
    front_wall = ai.wallFeeler(2000, heading)
    max_rating = max(wall_danger, enemy_chance, bullet_danger)
    if wall_danger == max_rating:
        if left_wall <= right_wall:
            ai.turnRight(1)
        else:
            ai.turnLeft(1)
        if front_wall > 300:
            ai.thrust(1)
    elif enemy_chance == max_rating:
        pass
    else:
        pass


def calculate_wall_danger(wall_dist: WallDistance, bot_speed: Speed):
    wall_high_danger_dom_one = min(wall_dist.near_dom, bot_speed.fast_dom)
    wall_high_danger_dom_two = min(wall_dist.medium_dom, bot_speed.fast_dom)
    wall_high_danger_dom_three = min(wall_dist.near_dom, bot_speed.medium_dom)
    wall_high_danger_dom = (wall_high_danger_dom_one + wall_high_danger_dom_two + wall_high_danger_dom_three) / 3

    wall_avg_danger_dom_one = min(wall_dist.near_dom, bot_speed.slow_dom)
    wall_avg_danger_dom_two = min(wall_dist.medium_dom, bot_speed.medium_dom)
    wall_avg_danger_dom_three = min(wall_dist.far_dom, bot_speed.fast_dom)
    wall_avg_danger_dom = (wall_avg_danger_dom_one + wall_avg_danger_dom_two + wall_avg_danger_dom_three) / 3

    wall_low_danger_dom_one = min(wall_dist.medium_dom, bot_speed.slow_dom)
    wall_low_danger_dom_two = min(wall_dist.far_dom, bot_speed.medium_dom)
    wall_low_danger_dom_three = min(wall_dist.far_dom, bot_speed.slow_dom)
    wall_low_danger_dom = (wall_low_danger_dom_one + wall_low_danger_dom_two + wall_low_danger_dom_three) / 3

    return calculate_centroid(wall_low_danger_dom, wall_avg_danger_dom, wall_high_danger_dom)


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
    low_enemy_chance_dom = (low_enemy_chance_dom_one + low_enemy_chance_dom_two + low_enemy_chance_dom_three) / 3\

    return calculate_centroid(low_enemy_chance_dom, avg_enemy_chance_dom, high_enemy_chance_dom)


def calculate_bullet_danger(bullet_dist: ObjectDistance, bullet_angle: TurnAngle):
    bullet_high_danger_dom_one = min(bullet_dist.near_dom, bullet_angle.small_dom)
    bullet_high_danger_dom_two = min(bullet_dist.near_dom, bullet_angle.medium_dom)
    bullet_high_danger_dom_three = min(bullet_dist.medium_dom, bullet_angle.small_dom)
    bullet_high_danger_dom = (bullet_high_danger_dom_one + bullet_high_danger_dom_two + bullet_high_danger_dom_three) / 3

    bullet_med_danger_dom_one = min(bullet_dist.near_dom, bullet_angle.large_dom)
    bullet_med_danger_dom_two = min(bullet_dist.medium_dom, bullet_angle.medium_dom)
    bullet_med_danger_dom_three = min(bullet_dist.far_dom, bullet_angle.small_dom)
    bullet_med_danger_dom = (bullet_med_danger_dom_one + bullet_med_danger_dom_two + bullet_med_danger_dom_three) / 3

    bullet_low_danger_dom_one = min(bullet_dist.medium_dom, bullet_angle.large_dom)
    bullet_low_danger_dom_two = min(bullet_dist.far_dom, bullet_angle.medium_dom)
    bullet_low_danger_dom_three = min(bullet_dist.far_dom, bullet_angle.large_dom)
    bullet_low_danger_dom = (bullet_low_danger_dom_one + bullet_low_danger_dom_two + bullet_low_danger_dom_three) / 3

    return calculate_centroid(bullet_low_danger_dom, bullet_med_danger_dom, bullet_high_danger_dom)


def calculate_centroid(low, medium, high):
    return (30 * low + 180 * medium + 340 * high) / (3 * low + 4 * medium + 4 * high)
