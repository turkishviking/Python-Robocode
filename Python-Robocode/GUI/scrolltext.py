   
from PyQt4.QtCore import SIGNAL
from PyQt4 import QtGui
class scrolltext(QtGui.QTextEdit):

    def __init__(self, parent=None):
        QtGui.QSlider.__init__(self, parent)
 

    def wheelEvent(self, event):
        self.emit(SIGNAL("scrol(int)"), event.delta()/120)
        print "e"
