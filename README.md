![alt text](https://github.com/turkishviking/Python-Robocode/blob/master/Python-Robocode/robotImages/robot.png?raw=true "Python-Robocode")  Python-Robocode
===============
 


#### A Fork of Robocode for python programming

I found this project on http://sourceforge.net/p/pythonrobocode/
I didn't seen any commit since 2012 so I have decided to develop it. Any help is welcome!

Need help to start? watch the [python-robocode wiki](https://github.com/turkishviking/Python-Robocode/wiki)

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

#bot's name
def name():
    return "Charlie_Robot"
#bot's color
def colour():
    return (80,10,80)
    
def startDirection():
    """ To begin whith a specific angle (not necessary)"""
    return 0
    
    
def commands():
    """ loop of bot's commands"""
        
    """to lock the radar with the gun"""
    gamefile.lockradar("GUN")
        
    """to unlock the radar"""
    gamefile.lockradar("FREE")
       
    """To fire"""  
    gamefile.fire(2)

    """To know the number of alive bot"""
    gamefile.nbr_bots_left()

    """To turn left in degrees"""
    gamefile.turn_left(180)
    
    """To go forward 180 steps"""
    gamefile.move(180)
    
    """To turn Right in degrees"""
    gamefile.turn_right(180)
    
    """To go forward 180 steps"""
    gamefile.move(180)
    
    """NECESSARY for the end of the loop"""
    gamefile.done()



def target_spotted(direction, targetBotName, targetX, targetY):
    """when a bot is seen"""
    
    """Point the gun into the target"""
    gamefile.pointgun(direction)
    
    """To fire""" 
    gamefile.fire(2)
    
    
    
def on_hit_by_bullet(blastPower, blastName):
    """when my bot is hit by a bullet"""
    print blastPower, blastName
    
    
    
    
def on_death():
    """when my bot is dead"""
    print "i'm dead"
    
```