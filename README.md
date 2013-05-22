```![alt text](https://github.com/turkishviking/Python-Robocode/blob/master/Python-Robocode/robotImages/robot.png?raw=true "Python-Robocode") Python-Robocode```
===============
 


#### A Fork of Robocode for python programming

I found this project on http://sourceforge.net/p/pythonrobocode/
I didn't seen any commit since 2012 so I have decided to develop it. Any help is welcome!

#####Need help to start? watch the [python-robocode wiki](https://github.com/turkishviking/Python-Robocode/wiki)

* Thanks to the original developers:
    
  * Michael Macdonald
  * Neil Morrison
  * Maksat Tulepov
  * Tim Storer
  * Andrew Downs
  * Stuart Glendinning
    
    
* What's New & Task list:
    - [x]  getTargetPosition()
    - [x]  getTargetName()
    - [x]  bulletPower
    - [x]  on_hit_by_bullet()
    - [ ]  bulletSize
    - [ ]  WallCollision
    - [ ]  MapSize
    - [x]  Number_Of_Enmies_Left()
    - [ ]  GameSpeed
    - [x]  on_Robot_Exit()
    - [ ]  Battle Series
    - [ ]  Batlles Statistics
    
* Bot example (charlie_lutaud.py):

```python 
# -*- coding: utf-8 -*-

import gamefile # necessary for the game


# bot's name
def name():
    return "Charlie_Robot"
    
    
# bot's color
def colour():
    return (80,10,80)
     
    
# To begin whith a specific angle (not necessary)    
def startDirection():
    return 0
       
    
# loop of bot's commands    
def commands():
    
    gamefile.lockradar("GUN") #to lock the radar with the gun
       
    gamefile.lockradar("FREE") #to unlock the radar
       
    gamefile.fire(power) #To fire (0 < power < 10) 

    gamefile.nbr_bots_left() #To know the number of alive bots
    
    gamefile.turn_left(180) #To turn left in degrees
    
    gamefile.move(180) #To go forward 180 steps
    
    gamefile.turn_right(180) #To turn Right in degrees
    
    gamefile.move(180) #To go forward 180 steps
    
    """NECESSARY for the end of the loop"""
    gamefile.done()
    
    

#when a bot is seen
def target_spotted(direction, targetBotName, targetX, targetY):
    
    gamefile.pointgun(direction) #Point the gun into the target
    
    gamefile.fire(2) #To fire
    
    
    
    
#when my bot is hit by a bullet
def on_hit_by_bullet(blastPower, blastName):
    
    print blastPower, blastName
    
    
    
#when my bot is dead    
def on_death():
    
    print "i'm dead"
    
```