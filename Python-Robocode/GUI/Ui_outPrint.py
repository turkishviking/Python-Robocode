# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/charlie/python/PyQt-Robocode/Python-Robocode/GUI/outPrint.ui'
#
# Created: Thu May 30 02:58:40 2013
#      by: PyQt4 UI code generator 4.9.3
# Modified: Thu Oct 17 12:30:00JST 2019
#      by: hjmr
#
# WARNING! All changes made in this file will be lost!


from PyQt5.QtWidgets import QApplication, QWidget, QTextEdit
from PyQt5.QtWidgets import QSizePolicy, QVBoxLayout, QHBoxLayout
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import QMetaObject

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(444, 383)
        icon = QIcon()
        icon.addPixmap(QPixmap("robotImages/small.png"), QIcon.Normal, QIcon.Off)
        Form.setWindowIcon(icon)
        self.verticalLayout = QVBoxLayout(Form)
        self.verticalLayout.setObjectName("verticalLayout")
        self.textEdit = QTextEdit(Form)
        self.textEdit.setObjectName("textEdit")
        self.verticalLayout.addWidget(self.textEdit)

        self.retranslateUi(Form)
        QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(QApplication.translate("Form", "Form"))


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    Form = QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())

