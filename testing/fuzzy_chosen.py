# Import libraries, including the degree of membership libraries we created
import math

import libpyAI as ai
from training.fuzzy.object_distance import ObjectDistance
from training.fuzzy.turn_angle import TurnAngle
from training.fuzzy.wall_distance import WallDistance
from training.fuzzy.speed import Speed
from training.fuzzy.calculate_fuzzy import calculate_wall_danger, calculate_bullet_danger, calculate_enemy_chance


def AI_loop():
    # Release keys
    global chromosome

    ai.thrust(0)
    ai.turnLeft(0)
    ai.turnRight(0)
    ai.setTurnSpeed(20)
    ai.setPower(35)

    # Wall Avoidance
    tracking = int(ai.selfTrackingDeg())
    track_wall = ai.wallFeeler(2000, tracking)
    wall_dist = WallDistance(track_wall, chromosome)
    bot_speed = Speed(ai.selfSpeed(), chromosome)
    wall_danger = calculate_wall_danger(wall_dist, bot_speed)
    dist_var = int(chromosome[146:155], 2)

    # Offense
    enemy_id = ai.closestShipId()
    if enemy_id != -1:
        enemy_distance = ObjectDistance(ai.enemyDistanceId(enemy_id), chromosome)
        ai.lockClose()
        enemy_angle = TurnAngle(abs(ai.selfHeadingDeg() - ai.lockHeadingDeg()), chromosome)
        enemy_chance = calculate_enemy_chance(enemy_angle, enemy_distance)
    else:
        enemy_chance = 0

    # Defense
    bullet_xcoor = ai.closestItemX()
    bullet_ycoor = ai.closestItemY()
    ship_xcoor = ai.selfX()
    ship_ycoor = ai.selfY()

    if bullet_xcoor == -1 or bullet_ycoor == -1:
        bullet_danger = 0
    else:

        # Calculating Euclidean dist between ship and bullet
        bullet_dis = math.dist([bullet_xcoor, bullet_ycoor], [ship_xcoor, ship_ycoor])

        # Calculating the angle between the ship and the bullet
        alpha = abs(ship_xcoor - bullet_xcoor) / bullet_dis
        bullet_ang = math.degrees(math.asin(alpha))

        # Give inputs and calculate bullet danger based off of aggregation and defuzzification functions
        # at the bottom of this code
        bullet_dist = ObjectDistance(bullet_dis, chromosome)
        bullet_angle = TurnAngle(bullet_ang, chromosome)
        bullet_danger = calculate_bullet_danger(bullet_dist, bullet_angle)

    heading = int(ai.selfHeadingDeg())
    left_wall = ai.wallFeeler(2000, heading + 90)
    right_wall = ai.wallFeeler(2000, heading - 90)
    front_wall = ai.wallFeeler(2000, heading)
    top_wall = ai.wallFeeler(2000, 90)
    bottom_wall = ai.wallFeeler(2000, heading - 180)

    if wall_danger == bullet_danger == enemy_chance:
        wall_danger += 1

    max_rating = max(wall_danger, bullet_danger, enemy_chance)

    # Fire wall danger with top priority
    if wall_danger == max_rating:
        if bottom_wall < int(chromosome[155:164], 2):
            ai.thrust(1)
        elif ai.selfSpeed() < int(chromosome[164:168], 2):
            ai.thrust(1)
        elif track_wall < dist_var and left_wall < right_wall:
            ai.turnRight(1)
        elif track_wall < dist_var and left_wall >= right_wall:
            ai.turnLeft(1)
        elif left_wall < right_wall:
            ai.turnRight(1)
        elif bottom_wall < int(chromosome[168:178], 2) and ai.selfSpeed() < int(chromosome[178:182], 2):
            ai.thrust(1)
        else:
            ai.turnLeft(1)

        # Thrust rules  
        if ai.selfSpeed() == 0 and front_wall < int(chromosome[182:191], 2):
            ai.thrust(0)
        elif front_wall > dist_var + int(chromosome[191:200], 2) and track_wall < dist_var and ai.selfSpeed() < int(
                chromosome[200:204], 2):
            ai.thrust(1)
        elif front_wall > dist_var and ai.selfSpeed() < int(chromosome[204:208], 2):
            ai.thrust(1)
            ai.fireShot()
        elif top_wall < int(chromosome[208:217], 2):
            ai.thrust(1)
        elif right_wall < int(chromosome[217:226], 2):
            ai.thrust(1)
        elif left_wall < int(chromosome[226:235], 2):
            ai.thrust(1)
        elif bottom_wall < int(chromosome[235:244], 2):
            ai.thrust(1)

    # Fire enemy chance rating. 
    # Statements were made so the bot turns in the direction which allows it to aim at the enemy quickest               
    elif enemy_chance > 0:
        ai.fireShot()
        enemy_deg = ai.lockHeadingDeg()
        # Shoot if enemy is within 40 degrees of heading 
        if abs(heading - enemy_deg) < int(chromosome[244:251], 2):
            ai.fireShot()
        elif heading < int(chromosome[251:258], 2) and enemy_deg < int(chromosome[258:265], 2):
            if heading > enemy_deg:
                ai.turnRight(1)
            else:
                ai.turnLeft(1)
        elif heading > int(chromosome[265:272], 2) and enemy_deg > int(chromosome[272:279], 2):
            if enemy_deg > heading:
                ai.turnLeft(1)
            else:
                ai.turnRight(1)
        elif heading > int(chromosome[279:286], 2) and enemy_deg < int(chromosome[286:293], 2):
            if enemy_deg > (heading - int(chromosome[293:300], 2)):
                ai.turnRight(1)
            else:
                ai.turnLeft(1)
        else:
            if enemy_deg < (heading + int(chromosome[300:307], 2)):
                ai.turnLeft(1)
            else:
                ai.turnRight(1)

    # If bullet danger is max, thrust pilot to avoid danger.
    # Sets cap for speed so the pilot doesn't lose control
    elif bullet_danger == max_rating:
        if ai.selfSpeed() < int(chromosome[307:311], 2):
            ai.thrust(1)


if __name__ == '__main__':
    # Selected chromosome from the population
    chromosome = '101111011101001110010100010111011011111000111100010011101101110001111000101001111100100' \
                 '111010100011000000111110111010010110101100101010100110111111001110000001111100110001001' \
                 '010001011010000000000111100110011001101100100101011010101001010010110101010010010000000' \
                 '01110100000110010011001110111010101000110010000110'

    ai.start(AI_loop, ["-name", "fuzzyBot", "-join", "localhost"])
