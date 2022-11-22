# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'RequestForSlowResponse.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_RequestForSlowResponse(object):
    def setupUi(self, RequestForSlowResponse):
        RequestForSlowResponse.setObjectName("RequestForSlowResponse")
        RequestForSlowResponse.setFixedSize(400, 300)
        RequestForSlowResponse.setStyleSheet("background-color: #22222e")
        self.buttonBox = QtWidgets.QDialogButtonBox(RequestForSlowResponse)
        self.buttonBox.setGeometry(QtCore.QRect(90, 260, 201, 32))
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
        self.frame = QtWidgets.QFrame(RequestForSlowResponse)
        self.frame.setGeometry(QtCore.QRect(-10, -10, 411, 80))
        self.frame.setStyleSheet("background-color: #fb5b5d")
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.label_2 = QtWidgets.QLabel(self.frame)
        self.label_2.setGeometry(QtCore.QRect(20, 30, 381, 41))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(18)
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setStyleSheet("color: white")
        self.label_2.setObjectName("label_2")
        self.input_currency_2 = QtWidgets.QLineEdit(RequestForSlowResponse)
        self.input_currency_2.setGeometry(QtCore.QRect(60, 90, 271, 60))
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
        self.input_currency_3 = QtWidgets.QLineEdit(RequestForSlowResponse)
        self.input_currency_3.setGeometry(QtCore.QRect(60, 170, 271, 60))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.input_currency_3.setFont(font)
        self.input_currency_3.setStyleSheet("background-color: #22222e;\n"
"border: 2px solid #f66867;\n"
"border-radius: 30;\n"
"color: white")
        self.input_currency_3.setAlignment(QtCore.Qt.AlignCenter)
        self.input_currency_3.setObjectName("input_currency_3")

        self.retranslateUi(RequestForSlowResponse)
        self.buttonBox.accepted.connect(RequestForSlowResponse.accepted)
        self.buttonBox.rejected.connect(RequestForSlowResponse.rejected)
        QtCore.QMetaObject.connectSlotsByName(RequestForSlowResponse)

    def retranslateUi(self, RequestForSlowResponse):
        _translate = QtCore.QCoreApplication.translate
        RequestForSlowResponse.setWindowTitle(_translate("RequestForSlowResponse", "Dialog"))
        self.label_2.setText(_translate("RequestForSlowResponse", "RequestForSlowResponse"))
        

