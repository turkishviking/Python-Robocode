# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/charlie/python/PyQt-Robocode/Python-Robocode/GUI/RobotInfo.ui'
#
# Created: Fri May 31 15:45:44 2013
#      by: PyQt4 UI code generator 4.9.3
# Modified: Thu Oct 17 12:30:00JST 2019
#      by: hjmr
#
# WARNING! All changes made in this file will be lost!

from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QToolButton, QProgressBar
from PyQt5.QtWidgets import QSizePolicy, QVBoxLayout, QHBoxLayout
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import Qt, QSize, QMetaObject

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(180, 70)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Form.sizePolicy().hasHeightForWidth())
        Form.setSizePolicy(sizePolicy)
        Form.setMinimumSize(QSize(180, 70))
        Form.setMaximumSize(QSize(180, 80))
        Form.setContextMenuPolicy(Qt.DefaultContextMenu)
        self.verticalLayout = QVBoxLayout(Form)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setContentsMargins(0,0,0,0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.toolButton_2 = QToolButton(Form)
        self.toolButton_2.setEnabled(False)
        self.toolButton_2.setMinimumSize(QSize(30, 30))
        self.toolButton_2.setMaximumSize(QSize(30, 30))
        self.toolButton_2.setStyleSheet("background-color: rgba(255, 255, 255, 0);")
        icon = QIcon()
        icon.addPixmap(QPixmap("robotImages/small.png"), QIcon.Normal, QIcon.Off)
        icon.addPixmap(QPixmap("robotImages/small.png"), QIcon.Disabled, QIcon.Off)
        self.toolButton_2.setIcon(icon)
        self.toolButton_2.setIconSize(QSize(30, 30))
        self.toolButton_2.setCheckable(False)
        self.toolButton_2.setObjectName("toolButton_2")
        self.horizontalLayout.addWidget(self.toolButton_2)
        self.pushButton = QPushButton(Form)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton.sizePolicy().hasHeightForWidth())
        self.pushButton.setSizePolicy(sizePolicy)
        self.pushButton.setMinimumSize(QSize(130, 0))
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout.addWidget(self.pushButton)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.toolButton = QToolButton(Form)
        self.toolButton.setEnabled(False)
        self.toolButton.setMinimumSize(QSize(30, 30))
        self.toolButton.setMaximumSize(QSize(30, 30))
        self.toolButton.setStyleSheet("background-color: rgba(255, 255, 255, 0);")
        icon1 = QIcon()
        icon1.addPixmap(QPixmap("robotImages/smallRed.png"), QIcon.Normal, QIcon.Off)
        icon1.addPixmap(QPixmap("robotImages/smallRed.png"), QIcon.Disabled, QIcon.Off)
        self.toolButton.setIcon(icon1)
        self.toolButton.setIconSize(QSize(30, 30))
        self.toolButton.setCheckable(False)
        self.toolButton.setObjectName("toolButton")
        self.horizontalLayout_2.addWidget(self.toolButton)
        self.progressBar = QProgressBar(Form)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.progressBar.sizePolicy().hasHeightForWidth())
        self.progressBar.setSizePolicy(sizePolicy)
        self.progressBar.setMinimumSize(QSize(130, 0))
        self.progressBar.setProperty("value", 24)
        self.progressBar.setObjectName("progressBar")
        self.horizontalLayout_2.addWidget(self.progressBar)
        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.retranslateUi(Form)
        QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(QApplication.translate("Form", "Form"))
        self.toolButton_2.setText(QApplication.translate("Form", "..."))
        self.pushButton.setText(QApplication.translate("Form", "PushButton"))
        self.toolButton.setText(QApplication.translate("Form", "..."))


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    Form = QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())

