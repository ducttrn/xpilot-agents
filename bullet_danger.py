import math

bullet_xcoor = ai.closestItemX()
bullet_ycoor = ai.closestItemY()
ship_xcoor = ai.selfX()
ship_ycoor = ai.selfY()

#Calculating eucliden dist between ship and bullet
bullet_dis = math.dist([bullet_xcoor,bullet_ycoor], [ship_xcoor, ship_ycoor])

#Calculating the angle between the ship and the bullet
alpha = abs(ship_xcoor-bullet_xcoor)/bullet_dis
bullet_ang = math.degrees(math.asin(alpha))

bullet_dist = ObjectDistance(bullet_dis)
bullet_angle = TurnAngle(bullet_ang)

high_danger_dom_one = min(bullet_dist.near_dom, bullet_angle.small_dom)
high_danger_dom_two = min(bullet_dist.near_dom, bullet_angle.medium_dom)
high_danger_dom_three = min(bullet_dist.medium_dom, bullet_angle.small_dom)
high_danger_dom = (high_danger_dom_one + high_danger_dom_two + high_danger_dom_three) / 3

med_danger_dom_one = min(bullet_dist.near_dom, bullet_angle.large_dom)
med_danger_dom_two = min(bullet_dist.medium_dom, bullet_angle.medium_dom)
med_danger_dom_three = min(bullet_dist.far_dom, bullet_angle.small_dom)
med_danger_dom = (med_danger_dom_one + med_danger_dom_two + med_danger_dom_three) / 3

low_danger_dom_one = min(bullet_dist.medium_dom, bullet_angle.large_dom)
low_danger_dom_two = min(bullet_dist.far_dom, bullet_angle.medium_dom)
low_danger_dom_three = min(bullet_dist.far_dom, bullet_angle.large_dom)
low_danger_dom = (low_danger_dom_one + low_danger_dom_two + low_danger_dom_three) / 3
