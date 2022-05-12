import math

import libpyAI as ai


# Selected chromosome from the population
chromosome = '011111000010000101111000010110110000011100001010100110100110101010111111011000011110100111100111' \
             '100101101011111000011011101011101111101001111111010010011101000111110111000111111000101111101001' \
             '001111010100011000001101010011001001000011000101101110110110000101000111011101001100110000100010' \
             '00110000011111011000010'


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
