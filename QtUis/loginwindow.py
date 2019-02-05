# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'loginwindow.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_LoginWindow(object):
    def setupUi(self, LoginWindow):
        LoginWindow.setObjectName(_fromUtf8("LoginWindow"))
        LoginWindow.resize(337, 286)
        self.UserNamelbl = QtGui.QLabel(LoginWindow)
        self.UserNamelbl.setGeometry(QtCore.QRect(70, 40, 71, 17))
        self.UserNamelbl.setObjectName(_fromUtf8("UserNamelbl"))
        self.PasWordlbl = QtGui.QLabel(LoginWindow)
        self.PasWordlbl.setGeometry(QtCore.QRect(70, 90, 71, 17))
        self.PasWordlbl.setObjectName(_fromUtf8("PasWordlbl"))
        self.Password = QtGui.QLineEdit(LoginWindow)
        self.Password.setGeometry(QtCore.QRect(70, 110, 201, 27))
        self.Password.setInputMethodHints(QtCore.Qt.ImhNone)
        self.Password.setObjectName(_fromUtf8("Password"))
        self.Username = QtGui.QLineEdit(LoginWindow)
        self.Username.setGeometry(QtCore.QRect(70, 60, 201, 27))
        self.Username.setObjectName(_fromUtf8("Username"))
        self.LoginBUT = QtGui.QPushButton(LoginWindow)
        self.LoginBUT.setGeometry(QtCore.QRect(70, 150, 85, 27))
        self.LoginBUT.setObjectName(_fromUtf8("LoginBUT"))

        self.retranslateUi(LoginWindow)
        QtCore.QMetaObject.connectSlotsByName(LoginWindow)
        LoginWindow.setTabOrder(self.Username, self.Password)
        LoginWindow.setTabOrder(self.Password, self.LoginBUT)

    def retranslateUi(self, LoginWindow):
        LoginWindow.setWindowTitle(_translate("LoginWindow", "Login Window", None))
        self.UserNamelbl.setText(_translate("LoginWindow", "Username", None))
        self.PasWordlbl.setText(_translate("LoginWindow", "Password", None))
        self.LoginBUT.setText(_translate("LoginWindow", "Login", None))

