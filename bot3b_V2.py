# Tyler Maguire, Bill Tran, William Mears
import libpyAI as ai
from turn_model import predict_turn


def AI_loop():
    # Release keys
    ai.thrust(0)
    ai.turnLeft(0)
    ai.turnRight(0)
    ai.setTurnSpeed(20)
    ai.setPower(70)

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

    WALL_DIST = 450

    # Turn rules
    turning_data = [leftWall, rightWall, frontWall, ai.selfSpeed()]
    turn = predict_turn(turning_data)

    if turn == 0:
        ai.turnRight(1)
    else:
        ai.turnLeft(1)

    if ai.selfSpeed() == 0 and frontWall < 300:
        ai.thrust(0)
    elif frontWall > WALL_DIST + 350 and trackWall < WALL_DIST and ai.selfSpeed() < 10:
        ai.thrust(1)
    elif frontWall > WALL_DIST and ai.selfSpeed() < 6:
        ai.thrust(1)
    elif topWall < 110:
        ai.thrust(1)
    elif RWall < 110:
        ai.thrust(1)
    elif LWall < 110:
        ai.thrust(1)
    elif bottomWall < 110:
        ai.thrust(1)

    ai.fireShot()


ai.start(AI_loop, ["-name", "Dumbo", "-join", "localhost"])
