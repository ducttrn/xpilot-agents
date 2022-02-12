import libpyAI as ai
from wall_distance import WallDistance
from speed import Speed


def AI_loop():
    ai.thrust(0)
    ai.turnLeft(0)
    ai.turnRight(0)

    tracking = int(ai.SelfTrackingDeg())
    track_wall = ai.wallFeeler(2000, tracking)
    wall_dist = WallDistance(track_wall)
    bot_speed = Speed(ai.selfSpeed())

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

    wall_danger = (30*low_danger_dom + 180*avg_danger_dom + 340*high_danger_dom) / (3*low_danger_dom + 4*avg_danger_dom + 4*high_danger_dom)