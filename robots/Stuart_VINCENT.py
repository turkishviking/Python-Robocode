import gamefile
def name():
        return "VINCENT"
def colour():
	return (255,20,147)
def commands():
        gamefile.move(200)
	gamefile.turn_left(90)
	gamefile.fire(2)
	gamefile.turn_left(90)
        gamefile.fire(2)
	gamefile.turn_left(90)
	gamefile.fire(2)
	gamefile.turn_left(90)
	gamefile.fire(2)
	gamefile.done()

def target_spotted(direction, targetBotName, targetX, targetY):
        gamefile.pointgun(direction*1.0)
        gamefile.fire(2)
        gamefile.fire(2)
