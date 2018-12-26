# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'actualRevUI.ui'
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

class Ui_ActRevWindow(object):
    def setupUi(self, ActRevWindow):
        ActRevWindow.setObjectName(_fromUtf8("ActRevWindow"))
        ActRevWindow.resize(1107, 278)
        self.buttonBox = QtGui.QDialogButtonBox(ActRevWindow)
        self.buttonBox.setGeometry(QtCore.QRect(480, 240, 621, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.revTable = QtGui.QTableWidget(ActRevWindow)
        self.revTable.setGeometry(QtCore.QRect(10, 80, 1091, 151))
        self.revTable.setAlternatingRowColors(True)
        self.revTable.setObjectName(_fromUtf8("revTable"))
        self.revTable.setColumnCount(0)
        self.revTable.setRowCount(0)
        self.dateEditBox = QtGui.QDateEdit(ActRevWindow)
        self.dateEditBox.setGeometry(QtCore.QRect(10, 30, 131, 27))
        self.dateEditBox.setCurrentSection(QtGui.QDateTimeEdit.MonthSection)
        self.dateEditBox.setCalendarPopup(True)
        self.dateEditBox.setObjectName(_fromUtf8("dateEditBox"))
        self.line = QtGui.QFrame(ActRevWindow)
        self.line.setGeometry(QtCore.QRect(10, 60, 1091, 16))
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName(_fromUtf8("line"))
        self.dateLabel = QtGui.QLabel(ActRevWindow)
        self.dateLabel.setGeometry(QtCore.QRect(10, 10, 161, 17))
        self.dateLabel.setObjectName(_fromUtf8("dateLabel"))

        self.retranslateUi(ActRevWindow)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), ActRevWindow.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), ActRevWindow.reject)
        QtCore.QMetaObject.connectSlotsByName(ActRevWindow)

    def retranslateUi(self, ActRevWindow):
        ActRevWindow.setWindowTitle(_translate("ActRevWindow", "Actual Revenue", None))
        self.dateEditBox.setDisplayFormat(_translate("ActRevWindow", "MMMM yyyy", None))
        self.dateLabel.setText(_translate("ActRevWindow", "Select month", None))

