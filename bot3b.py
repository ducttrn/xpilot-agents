# Tyler Maguire, Bill Tran, WIll
import libpyAI as ai
import csv
from csv import writer
from turn_model import predict_turn
from thrust_model import predict_thrust


def AI_loop():
    # Release keys
    ai.thrust(0)
    ai.turnLeft(0)
    ai.turnRight(0)
    ai.setTurnSpeed(20)
    ai.setPower(70);

    enId = ai.closestShipId()

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

    turn_dir = 0
    thrust_on = 0

    # Turn rules
    turning_data = [leftWall, rightWall, frontWall, ai.selfSpeed()]
    turn = predict_turn(turning_data)

    if turn == 0:
        ai.turnRight(1)
    else:
        ai.turnLeft(1)

    # if leftWall < rightWall:
    #  ai.turnRight(1)
    #  turn_dir = 0    #turn right class 0
    # else:
    #  ai.turnLeft(1)
    #  turn_dir = 1.0       #turn left class 1.0

    # Thrust rules
    thrusting_data = [ai.selfSpeed(), frontWall, trackWall, topWall, RWall, LWall, bottomWall]
    thruster = predict_thrust(thrusting_data)
    if thruster == 0:
        ai.thrust(0)
    else:
        ai.thrust(1)

    ai.fireShot()

    # if ai.selfSpeed() == 0 and frontWall < 300:
    #  ai.thrust(0)
    # elif frontWall > WALL_DIST+350 and trackWall < WALL_DIST and ai.selfSpeed() < 10:
    #  ai.thrust(1)
    #  thrust_on = 1.0
    # elif frontWall > WALL_DIST and ai.selfSpeed() < 6:
    #  ai.thrust(1)
    #  thrust_on = 1.0
    #  ai.fireShot()
    # elif topWall < 100:
    #  ai.thrust(1)
    #  thrust_on = 1.0
    # elif RWall < 100:
    #  ai.thrust(1)
    #  thrust_on = 1.0
    # elif LWall < 100:
    #  ai.thrust(1)
    #  thrust_on = 1.0
    # elif bottomWall < 100:
    #  ai.thrust(1)
    #  thrust_on = 1.0
    # else:
    #  ai.fireShot()

    # Ai will shoot when it is not in danger of a wall


ai.start(AI_loop, ["-name", "Dumbo", "-join", "localhost"])
