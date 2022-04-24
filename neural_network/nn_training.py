import csv
import math

import libpyAI as ai
from genetic_algorithm import evolve_one_generation


def convert_genes_to_weight(genes):
    return (int(genes, 2) / 64 - 0.5) * 2


def convert_angle(angle):
    if 0 <= angle <= 180:
        return angle / 180
    elif 180 <= angle <= 360:
        return (angle - 360) / 180


def AI_loop():
    ai.setTurnSpeed(20)
    ai.setPower(35)
    ai.turnRight(0)
    ai.turnLeft(0)
    ai.thrust(0)

    heading = convert_angle(int(ai.selfHeadingDeg()))

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
    enemy_dir = convert_angle(ai.aimdir(0))
    enemy_heading = convert_angle(ai.enemyHeadingDeg(0))

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
    data = [heading, vel, reload_time, N, S, W, E, NW, NE, SW, SE, enemy_dist,
            enemy_dir, enemy_heading, enemy_reload_time, bullet_dist, mdb_angle, bias]

    global survival_time
    global weights_updated
    global row_count
    global weights

    # Count how long alive for fitness
    if ai.selfAlive() == 1:
        survival_time += 1
        weights_updated = False

    if ai.selfAlive() == 0 and weights_updated is False and row_count < 514:
        with open('nn_population.csv', newline='') as f:
            r = csv.reader(f)
            lines = list(r)
            lines[row_count - 1][1] = str(survival_time)
            writer = csv.writer(f)
            writer.writerows(lines)

            chromosome = lines[row_count - 1][0]
            weights = [
                convert_genes_to_weight(chromosome[i:i + 6])
                for i in range(0, len(chromosome), 6)
            ]

        row_count += 1
        weights_updated = True
        survival_time = 0

    elif ai.selfAlive() == 0 and weights_updated is False and row_count == 514:
        evolve_one_generation('nn_population.csv', 'nn_ga_config.json')
        weights = get_initial_weights()
        row_count = 2
        weights_updated = True
        survival_time = 0

    thrust = sum([i*j for i, j in zip(data, weights[:18])])
    if thrust > 0:
        ai.thrust(1)

    shoot = sum([i*j for i, j in zip(data, weights[18:36])])
    if shoot > 0:
        ai.fireShot()

    turn = sum([i*j for i, j in zip(data, weights[37:])]) / 15
    if turn > 1:
        turn = 1
    elif turn < -1:
        turn = -1
    ai.turn(int(turn * 20))


def get_initial_weights():
    with open('nn_population.csv', newline='') as f:
        csv_reader = csv.reader(f)
        line = next(next(csv_reader))
        return [
            convert_genes_to_weight(line[0][i:i + 6])
            for i in range(0, len(line[0]), 6)
        ]


if __name__ == "__main__":
    survival_time = 0
    weights_updated = False
    row_count = 2
    weights = get_initial_weights()

    ai.start(AI_loop, ["-name", "NNBot", "-join", "localhost"])
