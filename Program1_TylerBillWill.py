# Evan Gray - January 2018
import libpyAI as ai


def AI_loop():
    # Release keys
    ai.thrust(0)
    ai.turnLeft(0)
    ai.turnRight(0)
    ai.setTurnSpeed(20)
    ai.setPower(35);

    # Set variables
    heading = int(ai.selfHeadingDeg())
    tracking = int(ai.selfTrackingDeg())
    frontWall = ai.wallFeeler(2000, heading)
    leftWall = ai.wallFeeler(2000, heading + 90)
    rightWall = ai.wallFeeler(2000, heading - 90)
    topWall = ai.wallFeeler(2000, 90)
    RWall = ai.wallFeeler(2000, 0)
    LWall = ai.wallFeeler(2000, 180)
    bottomWall = ai.wallFeeler(2000, 270)
    trackWall = ai.wallFeeler(2000, tracking)

    TRACK_WALL_DIST = 450
    WALL_DIST = 100
    MAX_SPEED = 6

    # Turn rules
    if trackWall < TRACK_WALL_DIST and leftWall < rightWall:
        ai.turnRight(1)
    elif trackWall < TRACK_WALL_DIST and leftWall >= rightWall:
        ai.turnLeft(1)
    elif leftWall < rightWall:
        ai.turnRight(1)
    else:
        ai.turnLeft(1)

    # Thrust rules
    if ai.selfSpeed() == 0 and frontWall < TRACK_WALL_DIST - 150:
        ai.thrust(0)
    elif frontWall > TRACK_WALL_DIST + 350 and trackWall < TRACK_WALL_DIST and ai.selfSpeed() < MAX_SPEED:
        ai.thrust(1)
    elif topWall < WALL_DIST:
        ai.thrust(1)
    elif RWall < WALL_DIST:
        ai.thrust(1)
    elif LWall < WALL_DIST:
        ai.thrust(1)
    elif bottomWall < WALL_DIST:
        ai.thrust(1)

    ai.fireShot()

    # Ai will shoot when it is not in danger of a wall


ai.start(AI_loop, ["-name", "GABot", "-join", "localhost"])
