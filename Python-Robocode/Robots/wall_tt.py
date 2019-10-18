import math
import random
from robot import Robot

WALL_DISTANCE = 50
FIRE_DISTANCE = 500

MOVE_STEP = 5
SCAN_STEP = 3
BULLET_POWER = 5

STATE_MOVING_UNKNOWN_DIRECTION = -1
STATE_MOVING_DOWN  = 0
STATE_MOVING_LEFT  = 1
STATE_MOVING_UP    = 2
STATE_MOVING_RIGHT = 3
STATE_MOVING_ANGLE = (0, 90, 180, 270)

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

        self.scan_angle = 0
        self.scan_dir = 1
        self.scan_dir_can_change = True

    def move_following_walls(self):
        angle = self.getHeading() % 360
        target_angle = STATE_MOVING_ANGLE[self.state]
        da = target_angle - angle
        while da < -180:
            da += 360
        while 180 < da:
            da -= 360
        if int(da) == 0:
            self.move(MOVE_STEP)
        else:
            self.turn(da / 5)
            self.gunTurn(da / 5)

    def run(self):
        pos = self.getPosition()
        angle = self.getHeading()

        if self.state == STATE_MOVING_UNKNOWN_DIRECTION:
            dis_pos = (
                self.areaSize.height() - pos.y(),
                pos.x(),
                pos.y(),
                self.areaSize.width() - pos.x())
            self.state = dis_pos.index(min(dis_pos))
        elif self.state == STATE_MOVING_UP:
            if pos.y() < WALL_DISTANCE:
                self.state = STATE_MOVING_RIGHT
        elif self.state == STATE_MOVING_DOWN:
            if self.areaSize.height() - WALL_DISTANCE < pos.y():
                self.state = STATE_MOVING_LEFT
        elif self.state == STATE_MOVING_LEFT:
            if pos.x() < WALL_DISTANCE:
                self.state = STATE_MOVING_UP
        elif self.state == STATE_MOVING_RIGHT:
            if self.areaSize.width() - WALL_DISTANCE < pos.x():
                self.state = STATE_MOVING_DOWN
        self.move_following_walls()

        scan_angle = self.getGunHeading()  - angle
        if (scan_angle < 0 or 180 < scan_angle) and self.scan_dir_can_change:
            self.scan_dir *= -1
            self.scan_dir_can_change = False
        scan_step = SCAN_STEP if self.scan_dir == 1 else 2 * SCAN_STEP
        self.gunTurn(self.scan_dir * scan_step)
        if 0 < scan_angle and scan_angle < 180:
            self.scan_dir_can_change = True
            
    def onHitWall(self):
        self.reset()
        self.move(-MOVE_STEP)

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

        gun_angle = self.getGunHeading() % 360
        enemy_angle = math.degrees(math.atan2(dy, dx)) - 90
        a = enemy_angle - gun_angle
        if a < -180:
            a += 360
        elif 180 < a:
            a -= 360
        self.gunTurn(a)

        dist = math.sqrt(dx**2 + dy**2)
        if dist < FIRE_DISTANCE and 3 * BULLET_POWER < self.health:
            self.health -= BULLET_POWER
            self.fire(BULLET_POWER)

        self.move_following_walls()

