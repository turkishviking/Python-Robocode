import math
from robot import Robot

FIRE_DISTANCE = 500
BULLET_POWER = 2

class TargetTracker(Robot):

    def init(self):
        self.setColor(180, 180, 180)
        self.setGunColor(200, 200, 200)
        self.setRadarColor(200, 100, 0)
        self.setBulletsColor(255, 255, 230)

        self.radarVisible(True)

        self.areaSize = self.getMapSize()

        self.lockRadar("gun")
        self.setRadarField("thin")

    def run(self):
        self.gunTurn(5)
            
    def onHitWall(self):
        pass

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
        if dist < FIRE_DISTANCE:
            self.fire(BULLET_POWER)
