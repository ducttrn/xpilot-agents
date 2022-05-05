# Import libraries, including the degree of membership libraries we created
import math
import csv

import libpyAI as ai
from object_distance import ObjectDistance
from turn_angle import TurnAngle
from wall_distance import WallDistance
from speed import Speed
from calculate_fuzzy import calculate_wall_danger, calculate_bullet_danger, calculate_enemy_chance
from genetic_algorithm import evolve_one_generation


WALL_DIST = 350
population_size = 50


def AI_loop():
    # Release keys
    global chromosome
    global generation
    global chromosome_updated
    global fitness
    global game_score
    global current_row

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
        if bottom_wall < 100:
            ai.thrust(1)
        elif ai.selfSpeed() < 4:
            ai.thrust(1)
        elif track_wall < WALL_DIST and left_wall < right_wall:
            ai.turnRight(1)
        elif track_wall < WALL_DIST and left_wall >= right_wall:
            ai.turnLeft(1)
        elif left_wall < right_wall:
            ai.turnRight(1)
        elif bottom_wall < 500 and ai.selfSpeed() < 5:
            ai.thrust(1)
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

    # Fire enemy chance rating. 
    # Statements were made so the bot turns in the direction which allows it to aim at the enemy quickest               
    elif enemy_chance == max_rating:
        enemy_deg = ai.lockHeadingDeg()
        # Shoot if enemy is within 40 degrees of heading 
        if abs(heading - enemy_deg) < 40:
            ai.fireShot()
        elif heading < 180 and enemy_deg < 180:
            if heading > enemy_deg:
                ai.turnRight(1)
            else:
                ai.turnLeft(1)
        elif heading > 180 and enemy_deg > 180:
            if enemy_deg > heading:
                ai.turnLeft(1)
            else:
                ai.turnRight(1)
        elif heading > 180 and enemy_deg < 180:
            if enemy_deg > (heading - 180):
                ai.turnRight(1)
            else:
                ai.turnLeft(1)
        else:
            if enemy_deg < (heading + 180):
                ai.turnLeft(1)
            else:
                ai.turnRight(1)

    # If bullet danger is max, thrust pilot to avoid danger.
    # Sets cap for speed so the pilot doesn't lose control
    elif bullet_danger == max_rating:
        if ai.selfSpeed() < 6:
            ai.thrust(1)

    if ai.selfAlive() == 1:
        fitness += 1
        chromosome_updated = False

    if ai.selfAlive() == 0 and chromosome_updated is False:
        with open('fuzzy_population.csv', 'r') as f:
            r = csv.reader(f)
            lines = list(r)
            lines[current_row][1] = str(fitness)

        with open('fuzzy_population.csv', 'w') as f:
            writer = csv.writer(f)
            writer.writerows(lines)

        if current_row < population_size:
            # Update weights using next chromosome
            chromosome = lines[current_row + 1][0]
            current_row += 1

        elif current_row == population_size:
            # Reach last chromosome in the population then evolve
            evolve_one_generation('fuzzy_population.csv', 'fuzzy_ga_config.json')
            chromosome = get_initial_chromosome()
            current_row = 1
            generation += 1
            print(generation)

        # Mark weights as updated to prevent multiple updates
        # due to the bot remains dead for a few frames
        chromosome_updated = True
        fitness = 0


def get_initial_chromosome():
    with open('fuzzy_population.csv', newline='') as f:
        csv_reader = csv.reader(f)
        next(csv_reader)
        line = next(csv_reader)
        return line[0]


if __name__ == '__main__':
    generation = 1
    fitness = 0
    chromosome_updated = False
    current_row = 1
    chromosome = get_initial_chromosome()
    game_score = 0

    ai.start(AI_loop, ["-name", "fuzzyBot", "-join", "localhost"])
