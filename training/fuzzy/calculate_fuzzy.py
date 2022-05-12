# Functions for aggregation and defuzzification
# Clipping is done by taking the minimum degree of membership for two variables
# (ex. fast bot speed with 0.2 and near wall 0.4 would give degree of membership 0.2).
# Since three degrees of membership are given for each danger rating (high, avg, and low danger)
# the max of the three is returned.
from wall_distance import WallDistance
from speed import Speed
from turn_angle import TurnAngle
from object_distance import ObjectDistance


def calculate_wall_danger(wall_dist: WallDistance, bot_speed: Speed):
    wall_high_danger_dom_one = min(wall_dist.near_dom, bot_speed.fast_dom)
    wall_high_danger_dom_two = min(wall_dist.medium_dom, bot_speed.fast_dom)
    wall_high_danger_dom_three = min(wall_dist.near_dom, bot_speed.medium_dom)
    wall_high_danger_dom = max(wall_high_danger_dom_one, wall_high_danger_dom_two, wall_high_danger_dom_three)

    wall_avg_danger_dom_one = min(wall_dist.near_dom, bot_speed.slow_dom)
    wall_avg_danger_dom_two = min(wall_dist.medium_dom, bot_speed.medium_dom)
    wall_avg_danger_dom_three = min(wall_dist.far_dom, bot_speed.fast_dom)
    wall_avg_danger_dom = max(wall_avg_danger_dom_one, wall_avg_danger_dom_two, wall_avg_danger_dom_three)

    wall_low_danger_dom_one = min(wall_dist.medium_dom, bot_speed.slow_dom)
    wall_low_danger_dom_two = min(wall_dist.far_dom, bot_speed.medium_dom)
    wall_low_danger_dom_three = min(wall_dist.far_dom, bot_speed.slow_dom)
    wall_low_danger_dom = max(wall_low_danger_dom_one, wall_low_danger_dom_two, wall_low_danger_dom_three)

    return calculate_centroid(wall_low_danger_dom, wall_avg_danger_dom, wall_high_danger_dom)


def calculate_enemy_chance(enemy_angle: TurnAngle, enemy_distance: ObjectDistance):
    high_enemy_chance_dom_one = min(enemy_angle.small_dom, enemy_distance.near_dom)
    high_enemy_chance_dom_two = min(enemy_angle.medium_dom, enemy_distance.near_dom)
    high_enemy_chance_dom_three = min(enemy_angle.small_dom, enemy_distance.medium_dom)
    high_enemy_chance_dom = max(high_enemy_chance_dom_one, high_enemy_chance_dom_two, high_enemy_chance_dom_three)

    avg_enemy_chance_dom_one = min(enemy_angle.large_dom, enemy_distance.near_dom)
    avg_enemy_chance_dom_two = min(enemy_angle.medium_dom, enemy_distance.medium_dom)
    avg_enemy_chance_dom_three = min(enemy_angle.small_dom, enemy_distance.far_dom)
    avg_enemy_chance_dom = max(avg_enemy_chance_dom_one, avg_enemy_chance_dom_two, avg_enemy_chance_dom_three)

    low_enemy_chance_dom_one = min(enemy_angle.medium_dom, enemy_distance.far_dom)
    low_enemy_chance_dom_two = min(enemy_angle.large_dom, enemy_distance.medium_dom)
    low_enemy_chance_dom_three = min(enemy_angle.large_dom, enemy_distance.far_dom)
    low_enemy_chance_dom = max(low_enemy_chance_dom_one, low_enemy_chance_dom_two, low_enemy_chance_dom_three)

    return calculate_centroid(low_enemy_chance_dom, avg_enemy_chance_dom, high_enemy_chance_dom)


def calculate_bullet_danger(bullet_dist: ObjectDistance, bullet_angle: TurnAngle):
    bullet_high_danger_dom_one = min(bullet_dist.near_dom, bullet_angle.small_dom)
    bullet_high_danger_dom_two = min(bullet_dist.near_dom, bullet_angle.medium_dom)
    bullet_high_danger_dom_three = min(bullet_dist.medium_dom, bullet_angle.small_dom)
    bullet_high_danger_dom = max(bullet_high_danger_dom_one, bullet_high_danger_dom_two, bullet_high_danger_dom_three)

    bullet_med_danger_dom_one = min(bullet_dist.near_dom, bullet_angle.large_dom)
    bullet_med_danger_dom_two = min(bullet_dist.medium_dom, bullet_angle.medium_dom)
    bullet_med_danger_dom_three = min(bullet_dist.far_dom, bullet_angle.small_dom)
    bullet_med_danger_dom = max(bullet_med_danger_dom_one, bullet_med_danger_dom_two, bullet_med_danger_dom_three)

    bullet_low_danger_dom_one = min(bullet_dist.medium_dom, bullet_angle.large_dom)
    bullet_low_danger_dom_two = min(bullet_dist.far_dom, bullet_angle.medium_dom)
    bullet_low_danger_dom_three = min(bullet_dist.far_dom, bullet_angle.large_dom)
    bullet_low_danger_dom = max(bullet_low_danger_dom_one, bullet_low_danger_dom_two, bullet_low_danger_dom_three)

    return calculate_centroid(bullet_low_danger_dom, bullet_med_danger_dom, bullet_high_danger_dom)


# Function to calculate the centroid of three aggregated outputs.
# This is done in intervals of 10, and the crisp output returned is a number 0-100. 30 is meant to represent 0+10+20,
# 180 is 30+40+50+60, and 340 is the sum of the rest of the numbers through 100.
# This is divided by the amount of intervals each degree of membership had in the sum (ex. low has 0, 10, and 20
# so low's degree of membership is divided by 3).
def calculate_centroid(low, medium, high):
    if (low + medium + high) == 0:
        return 0
    else:
        return (30 * low + 180 * medium + 340 * high) / (3 * low + 4 * medium + 4 * high)