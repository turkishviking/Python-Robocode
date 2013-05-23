import gamefile
def name():
        return "Cassius"
def colour():
        return (75, 124, 255)
def commands():
        gamefile.move(200)
	gamefile.turn_right(90)
	gamefile.stop(100)
	gamefile.move(22)
	gamefile.turn_right(90)
	gamefile.fire(2)
	gamefile.done()

def target_spotted(direction, targetBotName, targetX, targetY):
        gamefile.pointgun((direction)*1.3)
        gamefile.fire(2)

def on_hit_by_bullet(blastPower, blastName):
    """print blastPower, blastName"""
	
