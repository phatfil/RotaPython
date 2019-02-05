# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'reportWindow.ui'
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

class Ui_reportingWindow(object):
    def setupUi(self, reportingWindow):
        reportingWindow.setObjectName(_fromUtf8("reportingWindow"))
        reportingWindow.resize(893, 713)
        self.gridLayout_2 = QtGui.QGridLayout(reportingWindow)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.reportTableWidget = QtGui.QTableWidget(reportingWindow)
        self.reportTableWidget.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.reportTableWidget.setAlternatingRowColors(True)
        self.reportTableWidget.setObjectName(_fromUtf8("reportTableWidget"))
        self.reportTableWidget.setColumnCount(0)
        self.reportTableWidget.setRowCount(0)
        self.gridLayout.addWidget(self.reportTableWidget, 1, 1, 1, 1)
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.line_5 = QtGui.QFrame(reportingWindow)
        self.line_5.setFrameShape(QtGui.QFrame.HLine)
        self.line_5.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_5.setObjectName(_fromUtf8("line_5"))
        self.verticalLayout.addWidget(self.line_5)
        self.label = QtGui.QLabel(reportingWindow)
        self.label.setObjectName(_fromUtf8("label"))
        self.verticalLayout.addWidget(self.label)
        self.selectReportCombo = QtGui.QComboBox(reportingWindow)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.selectReportCombo.sizePolicy().hasHeightForWidth())
        self.selectReportCombo.setSizePolicy(sizePolicy)
        self.selectReportCombo.setMinimumSize(QtCore.QSize(200, 0))
        self.selectReportCombo.setMaximumSize(QtCore.QSize(100, 16777215))
        self.selectReportCombo.setObjectName(_fromUtf8("selectReportCombo"))
        self.verticalLayout.addWidget(self.selectReportCombo)
        self.line = QtGui.QFrame(reportingWindow)
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName(_fromUtf8("line"))
        self.verticalLayout.addWidget(self.line)
        self.label_2 = QtGui.QLabel(reportingWindow)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.verticalLayout.addWidget(self.label_2)
        self.fromDateEdit = QtGui.QDateEdit(reportingWindow)
        self.fromDateEdit.setCalendarPopup(True)
        self.fromDateEdit.setObjectName(_fromUtf8("fromDateEdit"))
        self.verticalLayout.addWidget(self.fromDateEdit)
        self.label_3 = QtGui.QLabel(reportingWindow)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.verticalLayout.addWidget(self.label_3)
        self.toDateEdit = QtGui.QDateEdit(reportingWindow)
        self.toDateEdit.setCalendarPopup(True)
        self.toDateEdit.setObjectName(_fromUtf8("toDateEdit"))
        self.verticalLayout.addWidget(self.toDateEdit)
        self.line_3 = QtGui.QFrame(reportingWindow)
        self.line_3.setFrameShape(QtGui.QFrame.HLine)
        self.line_3.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_3.setObjectName(_fromUtf8("line_3"))
        self.verticalLayout.addWidget(self.line_3)
        self.exAdminCheck = QtGui.QCheckBox(reportingWindow)
        self.exAdminCheck.setObjectName(_fromUtf8("exAdminCheck"))
        self.verticalLayout.addWidget(self.exAdminCheck)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.line_6 = QtGui.QFrame(reportingWindow)
        self.line_6.setFrameShape(QtGui.QFrame.HLine)
        self.line_6.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_6.setObjectName(_fromUtf8("line_6"))
        self.verticalLayout.addWidget(self.line_6)
        self.exportToCSVBUT = QtGui.QPushButton(reportingWindow)
        self.exportToCSVBUT.setObjectName(_fromUtf8("exportToCSVBUT"))
        self.verticalLayout.addWidget(self.exportToCSVBUT)
        self.line_7 = QtGui.QFrame(reportingWindow)
        self.line_7.setFrameShape(QtGui.QFrame.HLine)
        self.line_7.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_7.setObjectName(_fromUtf8("line_7"))
        self.verticalLayout.addWidget(self.line_7)
        self.printReportBut = QtGui.QPushButton(reportingWindow)
        self.printReportBut.setObjectName(_fromUtf8("printReportBut"))
        self.verticalLayout.addWidget(self.printReportBut)
        self.line_2 = QtGui.QFrame(reportingWindow)
        self.line_2.setFrameShape(QtGui.QFrame.HLine)
        self.line_2.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_2.setObjectName(_fromUtf8("line_2"))
        self.verticalLayout.addWidget(self.line_2)
        self.runReportBut = QtGui.QPushButton(reportingWindow)
        self.runReportBut.setObjectName(_fromUtf8("runReportBut"))
        self.verticalLayout.addWidget(self.runReportBut)
        self.closeBut = QtGui.QPushButton(reportingWindow)
        self.closeBut.setObjectName(_fromUtf8("closeBut"))
        self.verticalLayout.addWidget(self.closeBut)
        self.line_4 = QtGui.QFrame(reportingWindow)
        self.line_4.setFrameShape(QtGui.QFrame.HLine)
        self.line_4.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_4.setObjectName(_fromUtf8("line_4"))
        self.verticalLayout.addWidget(self.line_4)
        self.gridLayout.addLayout(self.verticalLayout, 1, 0, 1, 1)
        self.gridLayout_2.addLayout(self.gridLayout, 0, 1, 1, 1)

        self.retranslateUi(reportingWindow)
        QtCore.QMetaObject.connectSlotsByName(reportingWindow)

    def retranslateUi(self, reportingWindow):
        reportingWindow.setWindowTitle(_translate("reportingWindow", "Reporting Tool", None))
        self.reportTableWidget.setSortingEnabled(True)
        self.label.setText(_translate("reportingWindow", "Select Report", None))
        self.label_2.setText(_translate("reportingWindow", "From Date", None))
        self.label_3.setText(_translate("reportingWindow", "To Date", None))
        self.exAdminCheck.setText(_translate("reportingWindow", "Exclude Admin in Pay Calc", None))
        self.exportToCSVBUT.setText(_translate("reportingWindow", "Export To CSV", None))
        self.printReportBut.setText(_translate("reportingWindow", "Print Report", None))
        self.runReportBut.setText(_translate("reportingWindow", "Run Report", None))
        self.closeBut.setText(_translate("reportingWindow", "Close", None))

