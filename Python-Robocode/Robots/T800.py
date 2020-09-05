#! /usr/bin/python
# -*- coding: utf-8 -*-

from math import cos, sin, radians
from robot import Robot  # Import a base Robot
import math

#
# Algorithm:
#   STATE_INIT:
#   Robot will first run away to nearest corner (C0X,C0Y), using his radar to search
#   the field to know initial enemies position.
#   STATE_RUN_AWAY (C1 and C2)
#   As soon as he knows one enemy position, he starts running away to furthest corners
#   and going back and forth between C1 and C2 corners (staying put is dangerous)
#   It will use his radar to continue scanning known enemy positions and record enemies moves.
#   it will update C1 and C2 corners when enemies move.
#   It will wait until the field hosts only one enemy and start shooting.
#   shooting stops when enemy moves to lower chances of bullet miss
#   shooting power is tuned with distance to enemy to maximize chances of rapid killing
#
#   robot uses delays to fire when enemy doesn't move.
#   FIXME!
#       - could avoid running through enemy ?
#       - when there is only one opponent, could turn around the enemy and fire !
#       - could team with same class robots to maximize win chances
#

MOVE_STEP = 10
MOVE_LIMIT = 50  # never get closer than 30 from the walls (hitting wall loose health)

STATE_INIT = 0
STATE_RUNNING_C0 = 1
STATE_RUNNING_C1 = 2
STATE_RUNNING_C2 = 3


class T800(Robot):  # Create a Robot

    def init(self):  # To initialise your robot

        # Set the bot color in RGB
        self.setColor(0, 255, 0)
        self.setGunColor(0, 255, 0)
        self.setRadarColor(255, 0, 0)
        self.setBulletsColor(0, 255, 0)

        # get game informations
        self.MapX = self.getMapSize().width()
        self.MapY = self.getMapSize().height()

        # initialiase some variables
        #        self.move_step = MOVE_STEP
        self.state = STATE_INIT
        self.runcounter = 0     #used to record time based on game turns for our bot
        self.last_time = 0      #used to measure delays in "game turns"

        #these ugly variables keep track of corners of the gameplay we will travel to
        #repeatedly to never stay put. These are calculated based on other enemies position.
        self.C0X = -1  # will store destination C0 X we want to reach
        self.C0Y = -1  # will store destination C0 Y we want to reach
        self.C1X = -1  # will store destination C1 X we want to reach
        self.C1Y = -1  # will store destination C1 Y we want to reach
        self.C2X = -1  # will store destination C2 X we want to reach
        self.C2Y = -1  # will store destination C2 Y we want to reach

        self.radarVisible(True)     # if True the radar field is visible
        self.lockRadar("gun")       # might be "free","base" or "gun"
        self.radarGoingAngle = 5    # step angle for radar rotation
        self.lookingForBot = 0      # botId we are looking for
        self.angleMinBot = 0        # botId of further bot when radar rotating ccw
        self.angleMaxBot = 0        # botId of further bot when radar rotating cw

        # self.enemies is a list of existing opponents and their last known location
        # onTargetSpotted() is used to update enemy list and their position
        # sensor() is used to delete missing opponents (dead)
        self.enemies = {}

    def MyMove(self, step: int):
        # MyMove takes care of not loosing health by not hitting walls.

        angle = self.getHeading()  # Returns the direction that the robot is facing
        position = self.getPosition()
        myX = position.x()
        myY = position.y()
        deltaY = step * cos(radians(angle))
        deltaX = - step * sin(radians(angle))

        move_ok = True

        if (deltaX > 0) and (myX + deltaX > self.MapX - MOVE_LIMIT):
            move_ok = False
        if (deltaX < 0) and (myX + deltaX < MOVE_LIMIT):
            move_ok = False
        if (deltaY > 0) and (myY + deltaY > self.MapY - MOVE_LIMIT):
            move_ok = False
        if (deltaY < 0) and (myY + deltaY < MOVE_LIMIT):
            move_ok = False

        if move_ok:
            self.move(step)
        else:
            # simulate wall hitting to launch appropriate actions
            self.rPrint("simulating wall hit, but stay calm, we stopped before !")
            self.onHitWall()

    def MyComputeDestAway(self):
        # compute enemy position center and deduce corners of gameplay we will run to.
        x = y = r = 0
        for robot in self.enemies:
            r += 1
            x += self.enemies[robot]["x"]
            y += self.enemies[robot]["y"]
        x = x // r
        y = y // r
        position = self.getPosition()
        myX = position.x()
        myY = position.y()

        if myX > x:
            self.C1X = self.MapX - MOVE_LIMIT * 1.5
        else:
            self.C1X = MOVE_LIMIT * 1.5
        if myY > y:
            self.C1Y = self.MapY - MOVE_LIMIT * 1.5
        else:
            self.C1Y = MOVE_LIMIT * 1.5

        if abs(self.C1X - x) > abs(self.C1Y - y):
            self.C2X = self.C1X
            self.C2Y = self.MapY - self.C1Y
        else:
            self.C2Y = self.C1Y
            self.C2X = self.MapX - self.C1X

    def MyGoto(self, x, y, step, urgency_flag) -> bool:
        """
        MyGoto move the robot to coordinates x,y moving step by step
        if urgency_flag is True, robot will start moving immediately,
        otherwise it will first turn to the right direction first and then start moving ahead

        @type step: bool
        """
        position = self.getPosition()
        myX = int(position.x())
        myY = int(position.y())

        # need MOVE_LIMIT precision
        x = x // MOVE_LIMIT
        y = y // MOVE_LIMIT
        myX = myX // MOVE_LIMIT
        myY = myY // MOVE_LIMIT

        if myX == x and myY == y:
            return True  # arrived at destination

        angle = self.getHeading() % 360  # Returns the direction that the robot is facing

        new_angle = -1
        if x > myX and y > myY: new_angle = 315
        if x > myX and y < myY: new_angle = 225
        if x < myX and y < myY: new_angle = 135
        if x < myX and y > myY: new_angle = 45
        if x > myX and y == myY: new_angle = 270
        if x < myX and y == myY: new_angle = 90
        if x == myX and y < myY: new_angle = 180
        if x == myX and y > myY: new_angle = 0

        delta_angle = new_angle - angle

        #when turning on itself, the bot stays put and is an ideal target
        #we prefer running backward (reverse) and use a lower rotation angle when it makes sens
        if delta_angle > 90:
            delta_angle = delta_angle - 180
            step = - step
        if delta_angle < -90:
            delta_angle = delta_angle + 180
            step = - step

        if abs(delta_angle) > 5:
            turn_step = 5
        else:
            turn_step = 1

        if delta_angle < 0:
            turn_step = -turn_step
            self.turn(turn_step)
        if delta_angle > 0:
            self.turn(turn_step)
        if delta_angle == 0:
            pass

        #if moving is an emergency, start immediately
        #otherwise, wait until almost set to the right direction
        if urgency_flag or abs(delta_angle) < 30:
            self.MyMove(step)

        return False

    def MyComputeBotSearch(self, botSpotted):
        # when we know all enemies positions, we compute radar seeking range
        # based on known enemy positions to avoid scanning empty space.

        #angles will store all enemies position for us
        angles = {}

        e1 = len(self.getEnemiesLeft()) - 1  # we are counted in enemiesLeft !!
        e2 = len(self.enemies)
        if e1 == e2:
            # we know all enemies position, optimise radar moves
            pos = self.getPosition()

            my_radar_angle = self.getRadarHeading() % 360

            for botId in self.enemies:
                dx = self.enemies[botId]["x"] - pos.x()
                dy = self.enemies[botId]["y"] - pos.y()
                enemy_angle = math.degrees(math.atan2(dy, dx)) - 90
                a = enemy_angle - my_radar_angle
                if a < -180:
                    a += 360
                elif 180 < a:
                    a -= 360
                angles[a] = botId

            amin = min(angles.keys())
            amax = max(angles.keys())
            self.angleMinBot = angles[amin]
            self.angleMaxBot = angles[amax]

            if len(self.enemies) == 1:  # tracking single bot mode
                if amin > 0:
                    self.radarGoingAngle = min([5, amin])
                elif amin < 0:
                    self.radarGoingAngle = -min([5, -amin])
                else:
                    self.radarGoingAngle = 1

                #called with some bot spotted ! try to shoot ...
                if botSpotted!=0 and abs(self.radarGoingAngle)<1 and self.runcounter>self.last_time:
                    dx=self.enemies[angles[amin]]["x"]-pos.x()
                    dy=self.enemies[angles[amin]]["y"]-pos.y()
                    dist=math.sqrt(dx**2+dy**2)

                    if self.runcounter-self.enemies[angles[amin]]["move"] > 2:  #shoot only if not moving since 2 rounds
                        #fire with more power if near the robot, lower power with distance
                        self.fire(int(1000/dist)+1)
                        #slow down fire rate with distance
                        self.last_time=self.runcounter+int(dist/150)

            elif self.lookingForBot == botSpotted:
                #bot spotted is the one we were looking for.
                #there are multiple enemies, go back and forth between enemies

                if self.lookingForBot == self.angleMinBot:
                    self.lookingForBot = self.angleMaxBot
                    if (self.radarGoingAngle<0):
                        self.radarGoingAngle = -self.radarGoingAngle
                else:
                    self.lookingForBot = self.angleMinBot
                    if (self.radarGoingAngle>0):
                        self.radarGoingAngle = -self.radarGoingAngle

            elif self.lookingForBot not in self.enemies:
                # lookingForBot not defined or lookingForBot is dead now
                # start seeking another one
                if self.radarGoingAngle > 0:
                    self.lookingForBot = self.angleMaxBot
#                    self.radarGoingAngle = (amax / abs(amax)) * min([5, abs(amax)])
                else:
                    self.lookingForBot = self.angleMinBot
#                   self.radarGoingAngle = (amin / abs(amin)) * min([5, abs(amin)])

    def run(self):  # main loop to command the bot
        self.runcounter += 1
        if self.state == STATE_INIT:
            position = self.getPosition()
            myX = position.x()
            myY = position.y()
            if myX < self.MapX//2:
                self.C0X = MOVE_LIMIT
                self.radarGoingAngle = -5  # step angle for radar rotation
            else:
                self.C0X = self.MapX - MOVE_LIMIT
            if myY < self.MapY//2:
                self.C0Y = MOVE_LIMIT
            else:
                self.C0Y = self.MapY - MOVE_LIMIT

            self.setRadarField("round")  # might be "normal", "large, "thin", "round"
            self.state = STATE_RUNNING_C0
            self.MyGoto(self.C0X, self.C0Y, MOVE_STEP, True)

        if self.state == STATE_RUNNING_C0:
            if self.runcounter > self.last_time + 5:    #change after first 5 rounds
                self.setRadarField("thin")  # might be "normal", "large, "thin", "round"
            self.MyComputeBotSearch(0)
            self.gunTurn(self.radarGoingAngle)
            self.MyGoto(self.C0X, self.C0Y, MOVE_STEP, True)
            if self.C1X != -1:
                self.state = STATE_RUNNING_C1

        if self.state == STATE_RUNNING_C1:
            self.setRadarField("thin")  # might be "normal", "large, "thin", "round"
            self.MyComputeBotSearch(0)
            self.gunTurn(self.radarGoingAngle)
            if self.MyGoto(self.C1X, self.C1Y, MOVE_STEP, False):
                self.state = STATE_RUNNING_C2

        if self.state == STATE_RUNNING_C2:
            self.setRadarField("thin")  # might be "normal", "large, "thin", "round"
            self.MyComputeBotSearch(0)
            self.gunTurn(self.radarGoingAngle)
            if self.MyGoto(self.C2X, self.C2Y, MOVE_STEP, False):
                self.state = STATE_RUNNING_C1

    def onHitWall(self):
        self.rPrint("ouch! a wall !")

    def sensors(self):
        # get rid of dead oppponents in our tracking list
        list = self.getEnemiesLeft()  # return a list of the enemies alive in the battle
        alive = []
        for robot in list:
            alive.append(robot["id"])
        missing = []
        for robot in self.enemies:
            if robot not in alive:
                missing.append(robot)
        for robot in missing:
            del self.enemies[robot]


    def onRobotHit(self, robotId, robotName):  # when My bot hit another
        pass

    def onHitByRobot(self, robotId, robotName):
        pass

    def onHitByBullet(self, bulletBotId, bulletBotName, bulletPower):  # NECESARY FOR THE GAME
        pass

    def onBulletHit(self, botId, bulletId):  # NECESARY FOR THE GAME
        pass

    def onBulletMiss(self, bulletId):
        pass

    def onRobotDeath(self):
        pass

    def onTargetSpotted(self, botId, botName, botPos):  # NECESARY FOR THE GAME
        #keep a list of spotted enemies with enemy coordinates recorded.
        #compute destination if new bot spotted or if known bot is moving
        # store x and y position and "date" of last seen (runcounter)
        if botId not in self.enemies:
            self.enemies[botId] = {}
            self.enemies[botId]["x"] = botPos.x()
            self.enemies[botId]["y"] = botPos.y()
            self.enemies[botId]["move"] = self.runcounter
            self.MyComputeDestAway()
        else:
            if self.enemies[botId]["x"] != botPos.x() or self.enemies[botId]["y"] != botPos.y():
                self.enemies[botId]["x"] = botPos.x()
                self.enemies[botId]["y"] = botPos.y()
                self.enemies[botId]["move"] = self.runcounter
                self.MyComputeDestAway()

        #compute radar next moves with information of botId currently aimed
        self.MyComputeBotSearch(botId)
