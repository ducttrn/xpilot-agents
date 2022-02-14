import libpyAI as ai
from object_distance import ObjectDistance
from turn_angle import TurnAngle
from wall_distance import WallDistance
from speed import Speed


def calculate_centroid(low, medium, high):
    return (30 * low + 180 * medium + 340 * high) / (3 * low + 4 * medium + 4 * high)


def AI_loop():
    ai.thrust(0)
    ai.turnLeft(0)
    ai.turnRight(0)

    tracking = int(ai.SelfTrackingDeg())
    track_wall = ai.wallFeeler(2000, tracking)
    wall_dist = WallDistance(track_wall)
    bot_speed = Speed(ai.selfSpeed())

    # Wall Avoidance
    high_danger_dom_one = min(wall_dist.near_dom, bot_speed.fast_dom)
    high_danger_dom_two = min(wall_dist.medium_dom, bot_speed.fast_dom)
    high_danger_dom_three = min(wall_dist.near_dom, bot_speed.medium_dom)
    high_danger_dom = (high_danger_dom_one + high_danger_dom_two + high_danger_dom_three) / 3

    avg_danger_dom_one = min(wall_dist.near_dom, bot_speed.slow_dom)
    avg_danger_dom_two = min(wall_dist.medium_dom, bot_speed.medium_dom)
    avg_danger_dom_three = min(wall_dist.far_dom, bot_speed.fast_dom)
    avg_danger_dom = (avg_danger_dom_one + avg_danger_dom_two + avg_danger_dom_three) / 3

    low_danger_dom_one = min(wall_dist.medium_dom, bot_speed.slow_dom)
    low_danger_dom_two = min(wall_dist.far_dom, bot_speed.medium_dom)
    low_danger_dom_three = min(wall_dist.far_dom, bot_speed.slow_dom)
    low_danger_dom = (low_danger_dom_one + low_danger_dom_two + low_danger_dom_three) / 3

    wall_danger = calculate_centroid(low_danger_dom, avg_danger_dom, high_danger_dom)

    # Offense
    enemy_id = ai.closestShipId()
    enemy_distance = ObjectDistance(ai.enemyDistanceId(enemy_id))
    ai.lockClose()
    enemy_angle = TurnAngle(abs(ai.selfHeadingDeg() - ai.lockHeadingDeg()))

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

    enemy_chance = calculate_centroid(low_enemy_chance_dom, avg_enemy_chance_dom, high_enemy_chance_dom)
