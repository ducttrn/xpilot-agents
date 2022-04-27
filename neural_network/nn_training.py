import csv
import math

import libpyAI as ai
from genetic_algorithm import evolve_one_generation


population_size = 100


def convert_genes_to_weight(genes):
    return (int(genes, 2) / 64 - 0.5) * 2


def convert_angle(angle):
    # Normalize angle to [-1, 1]
    if 0 <= angle <= 180:
        return angle / 180
    elif 180 <= angle <= 360:
        return (angle - 360) / 180


def AI_loop():
    ai.thrust(0)
    ai.turnLeft(0)
    ai.turnRight(0)
    ai.setTurnSpeed(20)
    ai.setPower(35)

    # All parameters are normalized to [-1, 1]
    heading = int(ai.selfHeadingDeg())
    vel = ai.selfSpeed() / 15
    reload_time = int(ai.selfReload()) / 12

    N = ai.wallFeeler(1000, heading) / 1000
    S = ai.wallFeeler(1000, heading - 180) / 1000
    W = ai.wallFeeler(1000, heading - 90) / 1000
    E = ai.wallFeeler(1000, heading + 90) / 1000
    NW = ai.wallFeeler(1000, heading + 45) / 1000
    NE = ai.wallFeeler(1000, heading - 45) / 1000
    SW = ai.wallFeeler(1000, heading + 135) / 1000
    SE = ai.wallFeeler(1000, heading - 135) / 1000

    enemy_dist = ai.enemyDistance(0) / 1000
    enemy_dir = convert_angle(ai.aimdir(0)) or 0
    enemy_heading = convert_angle(ai.enemyHeadingDeg(0)) or 0

    enemy_reload_time = ai.enemyReload(0) / 12
    bullet_dist = ai.shotDist(0) / 1000

    # MDB direction from Self
    x1 = ai.shotX(0)
    y1 = ai.shotY(0)
    x2 = ai.selfX()
    y2 = ai.selfY()
    delta_x = x2 - x1
    delta_y = y2 - y1
    mdb_angle = convert_angle((math.atan2(delta_y, delta_x) * 180 / math.pi) + 180)  # 0-360 with +180

    bias = 1
    data = [
        convert_angle(heading), vel, reload_time,
        N, S, W, E, NW, NE, SW, SE, enemy_dist,
        enemy_dir, enemy_heading, enemy_reload_time,
        bullet_dist, mdb_angle, bias
    ]

    global fitness
    global weights_updated
    global current_row
    global weights
    global game_score

    # Count how long alive for fitness
    if ai.selfAlive() == 1:
        fitness += 1
        weights_updated = False

    if ai.selfAlive() == 0 and weights_updated is False:
        with open('nn_population.csv', 'r') as f:
            r = csv.reader(f)
            lines = list(r)
            lines[current_row][1] = str(fitness)

        with open('nn_population.csv', 'w') as f:
            writer = csv.writer(f)
            writer.writerows(lines)

        if current_row < population_size:
            # Update weights using next chromosome
            chromosome = lines[current_row + 1][0]
            weights = [
                convert_genes_to_weight(chromosome[i:i + 6])
                for i in range(0, len(chromosome), 6)
            ]
            current_row += 1

        elif current_row == population_size:
            # Reach last chromosome in the population then evolve
            evolve_one_generation('nn_population.csv', 'nn_ga_config.json')
            weights = get_initial_weights()
            current_row = 1

        # Mark weights as updated to prevent multiple updates
        # due to the bot remains dead for a few frames
        weights_updated = True
        fitness = 0

    # Forward Propagate in a Neural Network
    # with 18 inputs and 3 outputs, 0 hidden layers
    thrust = sum([i * j for i, j in zip(data, weights[:18])])
    if thrust > 0:
        ai.thrust(1)

    shoot = sum([i * j for i, j in zip(data, weights[18:36])])
    if shoot > 0:
        ai.fireShot()

    turn = sum([i * j for i, j in zip(data, weights[37:])]) / 15
    if turn > 1:
        turn = 1
    elif turn < -1:
        turn = -1
    ai.turn(int(turn * 20))

    if ai.selfScore() > game_score:
        game_score = ai.selfScore()
        fitness += 100


def get_initial_weights():
    with open('nn_population.csv', 'r') as f:
        csv_reader = csv.reader(f)
        next(csv_reader)
        line = next(csv_reader)
        return [
            convert_genes_to_weight(line[0][i:i + 6])
            for i in range(0, len(line[0]), 6)
        ]


if __name__ == "__main__":
    fitness = 0
    weights_updated = False
    # Start from first chromosome
    weights = get_initial_weights()
    current_row = 1
    game_score = 0

    ai.start(AI_loop, ["-name", "NNBot", "-join", "localhost"])
