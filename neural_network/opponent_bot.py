import libpyAI as ai


def headingFromPred():
    for i in range(4):
        if ai.aimdir(i) != -1 and -1000 < ai.aimdir(i) < 1000 \
                and -50 < ai.selfHeadingDeg() - ai.aimdir(i) < 50:
            ai.turnToDeg(ai.aimdir(i) - 90)


# prod system controlling prey
def AI_Prey():
    ai.turnLeft(0)
    ai.turnRight(0)
    ai.setPower(5)

    if ai.selfSpeed() == 0:
        ai.thrust(1)

    heading = int(ai.selfHeadingDeg())

    frontWall = ai.wallFeeler(800, heading)

    leftWall = ai.wallFeeler(800, heading + 45)

    rightWall = ai.wallFeeler(800, heading - 45)

    leftWall90 = ai.wallFeeler(800, heading + 90)

    rightWall90 = ai.wallFeeler(800, heading - 90)

    # avoiding walls
    if frontWall <= 700 and leftWall > rightWall:
        ai.turnLeft(1)
    elif frontWall <= 700 and leftWall <= rightWall:
        ai.turnRight(1)
    elif leftWall < rightWall:
        ai.turnRight(1)
    elif rightWall > leftWall:
        ai.turnLeft(1)
    elif leftWall90 < rightWall90:
        ai.turnRight(1)
    elif rightWall90 > leftWall90:
        ai.turnLeft(1)

    # turn to enemies
    if ai.closestShipId() != -1 and -1000 < ai.aimdir(0) < 1000:
        ai.setPower(8)
        direction = ai.aimdir(0)
        ai.turnToDeg(direction)
        ai.fireShot()

    headingFromPred()


ai.start(AI_Prey, ["-name", "Enemy", "-join", "localhost"])
