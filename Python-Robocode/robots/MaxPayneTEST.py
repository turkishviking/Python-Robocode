import gamefile
def name():
        return "MaxPayne"
def colour():
	return (0,0,128)
def commands():
        gamefile.move(180)
	gamefile.fire(2)
        gamefile.stop(180)
        gamefile.fire(2)
	gamefile.turn_left(120)
        gamefile.fire(2)
	gamefile.turn_right(120)
        gamefile.fire(2)
	gamefile.turn_right(120)
        gamefile.fire(2)
	gamefile.turn_left(120)
        gamefile.fire(2)
	gamefile.done()

def target_spotted(direction, targetBotName, targetX, targetY):
        gamefile.pointgun(direction*1.4)
        gamefile.fire(2)
        gamefile.fire(2)
	gamefile.fire(2)
