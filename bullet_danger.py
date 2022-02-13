import numpy as np

bullet_xcoor = int closestItemX()
bullet_ycoor = int closestItemX()
ship_xcoor = int selfX()
ship_ycoor = int selfY()

bullet_pt = np.array((1,bullet_xcoor,bullet_ycoor))
ship_pt = np.array((1,ship_xcoor, ship_ycoor))
sum_sq = np.sum(np.square(ship_pt-bullet_pt))

bullet_dist = ObjectDistance(bullet)
bullet_angle = TurnAngle(bullet)

high_danger_dom_one = min(bullet.near_dom, bullet.small_dom)
high_danger_dom_two = min(bullet.near_dom, bullet.medium_dom)
high_danger_dom_three = min(bullet.medium_dom, bullet.small_dom)
high_danger_dom = (high_danger_dom_one + high_danger_dom_two + high_danger_dom_three) / 3

med_danger_dom_one = min(bullet.near_dom, bullet.large_dom)
med_danger_dom_two = min(bullet.medium_dom, bullet.medium_dom)
med_danger_dom_three = min(bullet.far_dom, bullet.small_dom)
med_danger_dom = (med_danger_dom_one + med_danger_dom_two + med_danger_dom_three) / 3

low_danger_dom_one = min(bullet.medium_dom, bullet.large_dom)
low_danger_dom_two = min(bullet.far_dom, bullet.medium_dom)
low_danger_dom_three = min(bullet.far_dom, bullet.large_dom)
low_danger_dom = (low_danger_dom_one + low_danger_dom_two + low_danger_dom_three) / 3
