# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'option.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.setFixedSize(400, 300)
        Dialog.setStyleSheet("background-color: #22222e")
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setGeometry(QtCore.QRect(100, 250, 201, 32))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        self.buttonBox.setFont(font)
        self.buttonBox.setStyleSheet("QPushButton {\n"
"    color: white;\n"
"    background-color: #fb5b5d;\n"
"\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: #fa4244;\n"
"}")
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.checkBox = QtWidgets.QCheckBox(Dialog)
        self.checkBox.setGeometry(QtCore.QRect(80, 50, 241, 21))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.checkBox.setFont(font)
        self.checkBox.setStyleSheet("background-color: #22222e;\n"
"border-radius: 30;\n"
"color: white")
        self.checkBox.setObjectName("checkBox")
        self.input_currency_3 = QtWidgets.QLineEdit(Dialog)
        self.input_currency_3.setGeometry(QtCore.QRect(70, 120, 261, 60))
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
        self.input_currency_3.setText("")
        self.input_currency_3.setAlignment(QtCore.Qt.AlignCenter)
        self.input_currency_3.setObjectName("input_currency_3")

        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accepted)
        self.buttonBox.rejected.connect(Dialog.rejected)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.checkBox.setText(_translate("Dialog", "Auto Reconnection"))

