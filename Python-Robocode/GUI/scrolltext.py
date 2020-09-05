   
from PyQt5.QtWidgets import QSlider, QTextEdit
from PyQt5.QtCore import pyqtSignal

class scrolltext(QTextEdit):
    def __init__(self, parent=None):
        QSlider.__init__(self, parent)
        self.wheelScrollSignal = pyqtSignal(int, int)
        self.wheelScrollSignal.connect(scrollContentsBy)
 

    def wheelEvent(self, event):
        self.wheelScrollSignal.emit(0,event.delta() / 120)
        # self.emit(SIGNAL("scrol(int)"), event.delta()/120)
        print("e")
