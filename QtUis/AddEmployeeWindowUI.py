# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'AddEmployeeWindowUI.ui'
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

class Ui_AddEmpDialog(object):
    def setupUi(self, AddEmpDialog):
        AddEmpDialog.setObjectName(_fromUtf8("AddEmpDialog"))
        AddEmpDialog.resize(312, 480)
        self.gridLayout = QtGui.QGridLayout(AddEmpDialog)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.AddEmpLbl = QtGui.QLabel(AddEmpDialog)
        self.AddEmpLbl.setObjectName(_fromUtf8("AddEmpLbl"))
        self.gridLayout.addWidget(self.AddEmpLbl, 0, 0, 1, 1)
        self.groupBox = QtGui.QGroupBox(AddEmpDialog)
        self.groupBox.setTitle(_fromUtf8(""))
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.AddEmpBUT = QtGui.QPushButton(self.groupBox)
        self.AddEmpBUT.setGeometry(QtCore.QRect(0, 0, 85, 27))
        self.AddEmpBUT.setObjectName(_fromUtf8("AddEmpBUT"))
        self.AddEmpBUT.raise_()
        self.gridLayout.addWidget(self.groupBox, 1, 1, 1, 1)
        self.EmpList = QtGui.QListWidget(AddEmpDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.EmpList.sizePolicy().hasHeightForWidth())
        self.EmpList.setSizePolicy(sizePolicy)
        self.EmpList.setMinimumSize(QtCore.QSize(150, 0))
        self.EmpList.setMaximumSize(QtCore.QSize(200, 16777215))
        self.EmpList.setSelectionMode(QtGui.QAbstractItemView.MultiSelection)
        self.EmpList.setObjectName(_fromUtf8("EmpList"))
        self.gridLayout.addWidget(self.EmpList, 1, 0, 1, 1)

        self.retranslateUi(AddEmpDialog)
        QtCore.QMetaObject.connectSlotsByName(AddEmpDialog)

    def retranslateUi(self, AddEmpDialog):
        AddEmpDialog.setWindowTitle(_translate("AddEmpDialog", "Add Employee", None))
        self.AddEmpLbl.setText(_translate("AddEmpDialog", "Select Employees to be added", None))
        self.AddEmpBUT.setText(_translate("AddEmpDialog", "Add", None))
        self.EmpList.setSortingEnabled(True)

