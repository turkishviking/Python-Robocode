import math
from robot import Robot


MOVE_STEP = 5
WALL_DISTANCE = 50
BULLET_POWER = 2

STATE_MOVING_UNKNOWN_DIRECTION = 0
STATE_MOVING_UP    = 1
STATE_MOVING_RIGHT = 2
STATE_MOVING_DOWN  = 3
STATE_MOVING_LEFT  = 4

class WallRunner(Robot):

    def init(self):
        self.setColor(180, 180, 180)
        self.setGunColor(200, 200, 200)
        self.setRadarColor(200, 100, 0)
        self.setBulletsColor(255, 255, 230)

        self.radarVisible(True)

        self.areaSize = self.getMapSize()

        self.lockRadar("gun")
        self.setRadarField("thin")

        self.state = STATE_MOVING_UNKNOWN_DIRECTION
        self.health = 100

    def myTurn(self, angle):
        self.turn(angle)
        self.gunTurn(angle)

    def run(self):
        pos = self.getPosition()
        angle = self.getHeading() % 360
        if self.state == STATE_MOVING_UNKNOWN_DIRECTION:
            self.myTurn(-angle)
            self.state = STATE_MOVING_DOWN
        elif self.state == STATE_MOVING_UP:
            if pos.y() < WALL_DISTANCE:
                self.stop()
                self.myTurn(90)
                self.state = STATE_MOVING_RIGHT
            else:
                self.move(MOVE_STEP)
        elif self.state == STATE_MOVING_DOWN:
            if self.areaSize.height() - WALL_DISTANCE < pos.y():
                self.stop()
                self.myTurn(90)
                self.state = STATE_MOVING_LEFT
            else:
                self.move(MOVE_STEP)
        elif self.state == STATE_MOVING_LEFT:
            if pos.x() < WALL_DISTANCE:
                self.stop()
                self.myTurn(90)
                self.state = STATE_MOVING_UP
            else:
                self.move(MOVE_STEP)
        elif self.state == STATE_MOVING_RIGHT:
            if self.areaSize.width() - WALL_DISTANCE < pos.x():
                self.stop()
                self.myTurn(90)
                self.state = STATE_MOVING_DOWN
            else:
                self.move(MOVE_STEP)
            
    def onHitWall(self):
        self.reset()
        self.move(-2 * MOVE_STEP)

    def sensors(self): 
        pass
        
    def onRobotHit(self, robotId, robotName):
        pass
        
    def onHitByRobot(self, robotId, robotName):
        pass

    def onHitByBullet(self, bulletBotId, bulletBotName, bulletPower):
        pass
        
    def onBulletHit(self, botId, bulletId):
        pass
        
    def onBulletMiss(self, bulletId):
        pass
        
    def onRobotDeath(self):
        pass
        
    def onTargetSpotted(self, botId, botName, botPos):
        self.fire(BULLET_POWER)

        my_angle = self.getHeading() % 360
        da = 0
        if self.state == STATE_MOVING_UP:
            da = 180-my_angle
        elif self.state == STATE_MOVING_DOWN:
            da = -my_angle
        elif self.state == STATE_MOVING_LEFT:
            da = 90-my_angle
        elif self.state == STATE_MOVING_RIGHT:
            da = 270-my_angle

        if da == 0:
            self.move(MOVE_STEP)
        else:
            self.turn(da)

