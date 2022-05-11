import csv
import math

import libpyAI as ai


chromosome = '100000010001010110110100010001001101000100001000001001000010101010000100001011100111000101111111100011001100100001101011101101000010011000101000111010010100010001110011110010100001001101000101101001100100100110010010010110011000010001000010001011010001110101001011110010010000000001100011000000001110100101010001010110011100'


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
    
    weights = [
                convert_genes_to_weight(chromosome[i:i + 6])
                for i in range(0, len(chromosome), 6)
            ]

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


if __name__ == "__main__":
    ai.start(AI_loop, ["-name", "NNBot", "-join", "localhost"])
