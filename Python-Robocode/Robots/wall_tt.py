import math
from robot import Robot

WALL_DISTANCE = 50
FIRE_DISTANCE = 300

MOVE_STEP = 5
BULLET_POWER = 5

STATE_MOVING_UNKNOWN_DIRECTION = 0
STATE_MOVING_UP    = 1
STATE_MOVING_RIGHT = 2
STATE_MOVING_DOWN  = 3
STATE_MOVING_LEFT  = 4

class WallTargetTracker(Robot):

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

    def run(self):
        pos = self.getPosition()
        angle = self.getHeading() % 360
        if self.state == STATE_MOVING_UNKNOWN_DIRECTION:
            self.turn(-angle)
            self.state = STATE_MOVING_DOWN
        elif self.state == STATE_MOVING_UP:
            if pos.y() < WALL_DISTANCE:
                self.stop()
                self.turn(90)
                self.state = STATE_MOVING_RIGHT
            else:
                self.move(MOVE_STEP)
        elif self.state == STATE_MOVING_DOWN:
            if self.areaSize.height() - WALL_DISTANCE < pos.y():
                self.stop()
                self.turn(90)
                self.state = STATE_MOVING_LEFT
            else:
                self.move(MOVE_STEP)
        elif self.state == STATE_MOVING_LEFT:
            if pos.x() < WALL_DISTANCE:
                self.stop()
                self.turn(90)
                self.state = STATE_MOVING_UP
            else:
                self.move(MOVE_STEP)
        elif self.state == STATE_MOVING_RIGHT:
            if self.areaSize.width() - WALL_DISTANCE < pos.x():
                self.stop()
                self.turn(90)
                self.state = STATE_MOVING_DOWN
            else:
                self.move(MOVE_STEP)
        self.gunTurn(5)
            
    def onHitWall(self):
        self.reset()
        self.move(-2 * MOVE_STEP)

    def sensors(self): 
        pass
        
    def onRobotHit(self, robotId, robotName):
        self.health -= 1
        
    def onHitByRobot(self, robotId, robotName):
        self.health -= 1

    def onHitByBullet(self, bulletBotId, bulletBotName, bulletPower):
        self.health -= 3 * bulletPower
        
    def onBulletHit(self, botId, bulletId):
        self.health += 2 * BULLET_POWER
        
    def onBulletMiss(self, bulletId):
        pass
        
    def onRobotDeath(self):
        pass
        
    def onTargetSpotted(self, botId, botName, botPos):
        self.reset()
        pos = self.getPosition()
        dx = botPos.x() - pos.x()
        dy = botPos.y() - pos.y()

        my_gun_angle = self.getGunHeading() % 360
        enemy_angle = math.degrees(math.atan2(dy, dx)) - 90
        a = enemy_angle - my_gun_angle
        if a < -180:
            a += 360
        elif 180 < a:
            a -= 360
        self.gunTurn(a)

        dist = math.sqrt(dx**2 + dy**2)
        if dist < FIRE_DISTANCE and 5 * BULLET_POWER < self.health:
            self.health -= BULLET_POWER
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

