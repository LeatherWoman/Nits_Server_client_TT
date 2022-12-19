# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'RequestForFastResponse.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_RequestForFastResponse(object):
    def setupUi(self, RequestForFastResponse):
        RequestForFastResponse.setObjectName("RequestForFastResponse")
        RequestForFastResponse.setFixedSize(400, 300)
        RequestForFastResponse.setStyleSheet("background-color: #22222e")
        self.buttonBox = QtWidgets.QDialogButtonBox(RequestForFastResponse)
        self.buttonBox.setGeometry(QtCore.QRect(100, 250, 191, 32))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.buttonBox.setFont(font)
        self.buttonBox.setStyleSheet("color: white;\n"
"background-color: #fb5b5d")
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.frame = QtWidgets.QFrame(RequestForFastResponse)
        self.frame.setGeometry(QtCore.QRect(-10, -10, 411, 80))
        self.frame.setStyleSheet("background-color: #fb5b5d")
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.label = QtWidgets.QLabel(self.frame)
        self.label.setGeometry(QtCore.QRect(20, 30, 381, 41))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(18)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setStyleSheet("color: white")
        self.label.setObjectName("label")
        self.input_currency_2 = QtWidgets.QLineEdit(RequestForFastResponse)
        self.input_currency_2.setGeometry(QtCore.QRect(60, 140, 271, 60))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.input_currency_2.setFont(font)
        self.input_currency_2.setStyleSheet("background-color: #22222e;\n"
"border: 2px solid #f66867;\n"
"border-radius: 30;\n"
"color: white")
        self.input_currency_2.setAlignment(QtCore.Qt.AlignCenter)
        self.input_currency_2.setObjectName("input_currency_2")

        self.retranslateUi(RequestForFastResponse)
        self.buttonBox.accepted.connect(RequestForFastResponse.accepted)
        self.buttonBox.rejected.connect(RequestForFastResponse.rejected)
        QtCore.QMetaObject.connectSlotsByName(RequestForFastResponse)

    def retranslateUi(self, RequestForFastResponse):
        _translate = QtCore.QCoreApplication.translate
        RequestForFastResponse.setWindowTitle(_translate("RequestForFastResponse", "Dialog"))
        self.label.setText(_translate("RequestForFastResponse", "RequestForFastResponse"))
        

