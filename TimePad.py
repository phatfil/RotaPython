# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'TimePad.ui'
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

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName(_fromUtf8("Dialog"))
        Dialog.resize(172, 344)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Dialog.sizePolicy().hasHeightForWidth())
        Dialog.setSizePolicy(sizePolicy)
        Dialog.setMinimumSize(QtCore.QSize(172, 344))
        Dialog.setMaximumSize(QtCore.QSize(172, 344))
        self.gridLayoutWidget = QtGui.QWidget(Dialog)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(1, 15, 169, 289))
        self.gridLayoutWidget.setObjectName(_fromUtf8("gridLayoutWidget"))
        self.gridLayout = QtGui.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.pushButton25 = QtGui.QPushButton(self.gridLayoutWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton25.sizePolicy().hasHeightForWidth())
        self.pushButton25.setSizePolicy(sizePolicy)
        self.pushButton25.setMaximumSize(QtCore.QSize(33, 27))
        self.pushButton25.setSizeIncrement(QtCore.QSize(33, 27))
        self.pushButton25.setCheckable(True)
        self.pushButton25.setObjectName(_fromUtf8("pushButton25"))
        self.gridLayout.addWidget(self.pushButton25, 6, 0, 1, 1)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 7, 0, 1, 1)
        self.pushButton5 = QtGui.QPushButton(self.gridLayoutWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton5.sizePolicy().hasHeightForWidth())
        self.pushButton5.setSizePolicy(sizePolicy)
        self.pushButton5.setMaximumSize(QtCore.QSize(33, 27))
        self.pushButton5.setSizeIncrement(QtCore.QSize(33, 27))
        self.pushButton5.setCheckable(True)
        self.pushButton5.setObjectName(_fromUtf8("pushButton5"))
        self.gridLayout.addWidget(self.pushButton5, 1, 0, 1, 1)
        self.pushButton17 = QtGui.QPushButton(self.gridLayoutWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton17.sizePolicy().hasHeightForWidth())
        self.pushButton17.setSizePolicy(sizePolicy)
        self.pushButton17.setMaximumSize(QtCore.QSize(33, 27))
        self.pushButton17.setSizeIncrement(QtCore.QSize(33, 27))
        self.pushButton17.setCheckable(True)
        self.pushButton17.setObjectName(_fromUtf8("pushButton17"))
        self.gridLayout.addWidget(self.pushButton17, 4, 0, 1, 1)
        self.pushButton6 = QtGui.QPushButton(self.gridLayoutWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton6.sizePolicy().hasHeightForWidth())
        self.pushButton6.setSizePolicy(sizePolicy)
        self.pushButton6.setMaximumSize(QtCore.QSize(33, 27))
        self.pushButton6.setSizeIncrement(QtCore.QSize(33, 27))
        self.pushButton6.setCheckable(True)
        self.pushButton6.setObjectName(_fromUtf8("pushButton6"))
        self.gridLayout.addWidget(self.pushButton6, 1, 1, 1, 1)
        self.pushButton13 = QtGui.QPushButton(self.gridLayoutWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton13.sizePolicy().hasHeightForWidth())
        self.pushButton13.setSizePolicy(sizePolicy)
        self.pushButton13.setMaximumSize(QtCore.QSize(33, 27))
        self.pushButton13.setSizeIncrement(QtCore.QSize(33, 27))
        self.pushButton13.setCheckable(True)
        self.pushButton13.setObjectName(_fromUtf8("pushButton13"))
        self.gridLayout.addWidget(self.pushButton13, 3, 0, 1, 1)
        self.pushButton16 = QtGui.QPushButton(self.gridLayoutWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton16.sizePolicy().hasHeightForWidth())
        self.pushButton16.setSizePolicy(sizePolicy)
        self.pushButton16.setMaximumSize(QtCore.QSize(33, 27))
        self.pushButton16.setSizeIncrement(QtCore.QSize(33, 27))
        self.pushButton16.setCheckable(True)
        self.pushButton16.setObjectName(_fromUtf8("pushButton16"))
        self.gridLayout.addWidget(self.pushButton16, 3, 3, 1, 1)
        self.pushButton11 = QtGui.QPushButton(self.gridLayoutWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton11.sizePolicy().hasHeightForWidth())
        self.pushButton11.setSizePolicy(sizePolicy)
        self.pushButton11.setMaximumSize(QtCore.QSize(33, 27))
        self.pushButton11.setSizeIncrement(QtCore.QSize(33, 27))
        self.pushButton11.setCheckable(True)
        self.pushButton11.setObjectName(_fromUtf8("pushButton11"))
        self.gridLayout.addWidget(self.pushButton11, 2, 2, 1, 1)
        self.pushButton14 = QtGui.QPushButton(self.gridLayoutWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton14.sizePolicy().hasHeightForWidth())
        self.pushButton14.setSizePolicy(sizePolicy)
        self.pushButton14.setMaximumSize(QtCore.QSize(33, 27))
        self.pushButton14.setSizeIncrement(QtCore.QSize(33, 27))
        self.pushButton14.setCheckable(True)
        self.pushButton14.setObjectName(_fromUtf8("pushButton14"))
        self.gridLayout.addWidget(self.pushButton14, 3, 1, 1, 1)
        self.pushButton0000 = QtGui.QPushButton(self.gridLayoutWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton0000.sizePolicy().hasHeightForWidth())
        self.pushButton0000.setSizePolicy(sizePolicy)
        self.pushButton0000.setMaximumSize(QtCore.QSize(33, 27))
        self.pushButton0000.setSizeIncrement(QtCore.QSize(33, 27))
        self.pushButton0000.setAutoFillBackground(False)
        self.pushButton0000.setCheckable(True)
        self.pushButton0000.setObjectName(_fromUtf8("pushButton0000"))
        self.gridLayout.addWidget(self.pushButton0000, 9, 0, 1, 1)
        self.pushButton3 = QtGui.QPushButton(self.gridLayoutWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton3.sizePolicy().hasHeightForWidth())
        self.pushButton3.setSizePolicy(sizePolicy)
        self.pushButton3.setMinimumSize(QtCore.QSize(33, 27))
        self.pushButton3.setMaximumSize(QtCore.QSize(33, 27))
        self.pushButton3.setCheckable(True)
        self.pushButton3.setObjectName(_fromUtf8("pushButton3"))
        self.gridLayout.addWidget(self.pushButton3, 0, 2, 1, 1)
        self.pushButton20 = QtGui.QPushButton(self.gridLayoutWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton20.sizePolicy().hasHeightForWidth())
        self.pushButton20.setSizePolicy(sizePolicy)
        self.pushButton20.setMaximumSize(QtCore.QSize(33, 27))
        self.pushButton20.setSizeIncrement(QtCore.QSize(33, 27))
        self.pushButton20.setCheckable(True)
        self.pushButton20.setObjectName(_fromUtf8("pushButton20"))
        self.gridLayout.addWidget(self.pushButton20, 4, 3, 1, 1)
        self.pushButton0015 = QtGui.QPushButton(self.gridLayoutWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton0015.sizePolicy().hasHeightForWidth())
        self.pushButton0015.setSizePolicy(sizePolicy)
        self.pushButton0015.setMaximumSize(QtCore.QSize(33, 27))
        self.pushButton0015.setSizeIncrement(QtCore.QSize(33, 27))
        self.pushButton0015.setCheckable(True)
        self.pushButton0015.setObjectName(_fromUtf8("pushButton0015"))
        self.gridLayout.addWidget(self.pushButton0015, 9, 1, 1, 1)
        self.pushButton18 = QtGui.QPushButton(self.gridLayoutWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton18.sizePolicy().hasHeightForWidth())
        self.pushButton18.setSizePolicy(sizePolicy)
        self.pushButton18.setMaximumSize(QtCore.QSize(33, 27))
        self.pushButton18.setSizeIncrement(QtCore.QSize(33, 27))
        self.pushButton18.setCheckable(True)
        self.pushButton18.setObjectName(_fromUtf8("pushButton18"))
        self.gridLayout.addWidget(self.pushButton18, 4, 1, 1, 1)
        self.pushButtonCLR = QtGui.QPushButton(self.gridLayoutWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButtonCLR.sizePolicy().hasHeightForWidth())
        self.pushButtonCLR.setSizePolicy(sizePolicy)
        self.pushButtonCLR.setMaximumSize(QtCore.QSize(33, 27))
        self.pushButtonCLR.setSizeIncrement(QtCore.QSize(33, 27))
        self.pushButtonCLR.setCheckable(True)
        self.pushButtonCLR.setObjectName(_fromUtf8("pushButtonCLR"))
        self.gridLayout.addWidget(self.pushButtonCLR, 6, 3, 1, 1)
        self.pushButton24 = QtGui.QPushButton(self.gridLayoutWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton24.sizePolicy().hasHeightForWidth())
        self.pushButton24.setSizePolicy(sizePolicy)
        self.pushButton24.setMaximumSize(QtCore.QSize(33, 27))
        self.pushButton24.setSizeIncrement(QtCore.QSize(33, 27))
        self.pushButton24.setCheckable(True)
        self.pushButton24.setObjectName(_fromUtf8("pushButton24"))
        self.gridLayout.addWidget(self.pushButton24, 5, 3, 1, 1)
        self.pushButton9 = QtGui.QPushButton(self.gridLayoutWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton9.sizePolicy().hasHeightForWidth())
        self.pushButton9.setSizePolicy(sizePolicy)
        self.pushButton9.setMaximumSize(QtCore.QSize(33, 27))
        self.pushButton9.setSizeIncrement(QtCore.QSize(33, 27))
        self.pushButton9.setCheckable(True)
        self.pushButton9.setObjectName(_fromUtf8("pushButton9"))
        self.gridLayout.addWidget(self.pushButton9, 2, 0, 1, 1)
        self.pushButton10 = QtGui.QPushButton(self.gridLayoutWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton10.sizePolicy().hasHeightForWidth())
        self.pushButton10.setSizePolicy(sizePolicy)
        self.pushButton10.setMaximumSize(QtCore.QSize(33, 27))
        self.pushButton10.setSizeIncrement(QtCore.QSize(33, 27))
        self.pushButton10.setCheckable(True)
        self.pushButton10.setObjectName(_fromUtf8("pushButton10"))
        self.gridLayout.addWidget(self.pushButton10, 2, 1, 1, 1)
        self.pushButton26 = QtGui.QPushButton(self.gridLayoutWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton26.sizePolicy().hasHeightForWidth())
        self.pushButton26.setSizePolicy(sizePolicy)
        self.pushButton26.setMaximumSize(QtCore.QSize(33, 27))
        self.pushButton26.setSizeIncrement(QtCore.QSize(33, 27))
        self.pushButton26.setCheckable(True)
        self.pushButton26.setObjectName(_fromUtf8("pushButton26"))
        self.gridLayout.addWidget(self.pushButton26, 6, 1, 1, 1)
        self.pushButton22 = QtGui.QPushButton(self.gridLayoutWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton22.sizePolicy().hasHeightForWidth())
        self.pushButton22.setSizePolicy(sizePolicy)
        self.pushButton22.setMaximumSize(QtCore.QSize(33, 27))
        self.pushButton22.setSizeIncrement(QtCore.QSize(33, 27))
        self.pushButton22.setCheckable(True)
        self.pushButton22.setObjectName(_fromUtf8("pushButton22"))
        self.gridLayout.addWidget(self.pushButton22, 5, 1, 1, 1)
        self.pushButton0030 = QtGui.QPushButton(self.gridLayoutWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton0030.sizePolicy().hasHeightForWidth())
        self.pushButton0030.setSizePolicy(sizePolicy)
        self.pushButton0030.setMaximumSize(QtCore.QSize(33, 27))
        self.pushButton0030.setSizeIncrement(QtCore.QSize(33, 27))
        self.pushButton0030.setCheckable(True)
        self.pushButton0030.setObjectName(_fromUtf8("pushButton0030"))
        self.gridLayout.addWidget(self.pushButton0030, 9, 2, 1, 1)
        self.pushButton12 = QtGui.QPushButton(self.gridLayoutWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton12.sizePolicy().hasHeightForWidth())
        self.pushButton12.setSizePolicy(sizePolicy)
        self.pushButton12.setMaximumSize(QtCore.QSize(33, 27))
        self.pushButton12.setSizeIncrement(QtCore.QSize(33, 27))
        self.pushButton12.setCheckable(True)
        self.pushButton12.setObjectName(_fromUtf8("pushButton12"))
        self.gridLayout.addWidget(self.pushButton12, 2, 3, 1, 1)
        self.pushButton2 = QtGui.QPushButton(self.gridLayoutWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton2.sizePolicy().hasHeightForWidth())
        self.pushButton2.setSizePolicy(sizePolicy)
        self.pushButton2.setMinimumSize(QtCore.QSize(33, 27))
        self.pushButton2.setMaximumSize(QtCore.QSize(33, 27))
        self.pushButton2.setCheckable(True)
        self.pushButton2.setObjectName(_fromUtf8("pushButton2"))
        self.gridLayout.addWidget(self.pushButton2, 0, 1, 1, 1)
        self.pushButton4 = QtGui.QPushButton(self.gridLayoutWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton4.sizePolicy().hasHeightForWidth())
        self.pushButton4.setSizePolicy(sizePolicy)
        self.pushButton4.setMinimumSize(QtCore.QSize(33, 27))
        self.pushButton4.setMaximumSize(QtCore.QSize(33, 27))
        self.pushButton4.setCheckable(True)
        self.pushButton4.setObjectName(_fromUtf8("pushButton4"))
        self.gridLayout.addWidget(self.pushButton4, 0, 3, 1, 1)
        self.pushButton8 = QtGui.QPushButton(self.gridLayoutWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton8.sizePolicy().hasHeightForWidth())
        self.pushButton8.setSizePolicy(sizePolicy)
        self.pushButton8.setMaximumSize(QtCore.QSize(33, 27))
        self.pushButton8.setSizeIncrement(QtCore.QSize(33, 27))
        self.pushButton8.setCheckable(True)
        self.pushButton8.setObjectName(_fromUtf8("pushButton8"))
        self.gridLayout.addWidget(self.pushButton8, 1, 3, 1, 1)
        self.pushButton19 = QtGui.QPushButton(self.gridLayoutWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton19.sizePolicy().hasHeightForWidth())
        self.pushButton19.setSizePolicy(sizePolicy)
        self.pushButton19.setMaximumSize(QtCore.QSize(33, 27))
        self.pushButton19.setSizeIncrement(QtCore.QSize(33, 27))
        self.pushButton19.setCheckable(True)
        self.pushButton19.setObjectName(_fromUtf8("pushButton19"))
        self.gridLayout.addWidget(self.pushButton19, 4, 2, 1, 1)
        self.pushButton0045 = QtGui.QPushButton(self.gridLayoutWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton0045.sizePolicy().hasHeightForWidth())
        self.pushButton0045.setSizePolicy(sizePolicy)
        self.pushButton0045.setMaximumSize(QtCore.QSize(33, 27))
        self.pushButton0045.setSizeIncrement(QtCore.QSize(33, 27))
        self.pushButton0045.setCheckable(True)
        self.pushButton0045.setObjectName(_fromUtf8("pushButton0045"))
        self.gridLayout.addWidget(self.pushButton0045, 9, 3, 1, 1)
        self.pushButton7 = QtGui.QPushButton(self.gridLayoutWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton7.sizePolicy().hasHeightForWidth())
        self.pushButton7.setSizePolicy(sizePolicy)
        self.pushButton7.setMaximumSize(QtCore.QSize(33, 27))
        self.pushButton7.setSizeIncrement(QtCore.QSize(33, 27))
        self.pushButton7.setCheckable(True)
        self.pushButton7.setObjectName(_fromUtf8("pushButton7"))
        self.gridLayout.addWidget(self.pushButton7, 1, 2, 1, 1)
        self.pushButton23 = QtGui.QPushButton(self.gridLayoutWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton23.sizePolicy().hasHeightForWidth())
        self.pushButton23.setSizePolicy(sizePolicy)
        self.pushButton23.setMaximumSize(QtCore.QSize(33, 27))
        self.pushButton23.setSizeIncrement(QtCore.QSize(33, 27))
        self.pushButton23.setCheckable(True)
        self.pushButton23.setObjectName(_fromUtf8("pushButton23"))
        self.gridLayout.addWidget(self.pushButton23, 5, 2, 1, 1)
        self.pushButton1 = QtGui.QPushButton(self.gridLayoutWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton1.sizePolicy().hasHeightForWidth())
        self.pushButton1.setSizePolicy(sizePolicy)
        self.pushButton1.setMinimumSize(QtCore.QSize(33, 27))
        self.pushButton1.setMaximumSize(QtCore.QSize(33, 27))
        self.pushButton1.setCheckable(True)
        self.pushButton1.setObjectName(_fromUtf8("pushButton1"))
        self.gridLayout.addWidget(self.pushButton1, 0, 0, 1, 1)
        self.pushButton21 = QtGui.QPushButton(self.gridLayoutWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton21.sizePolicy().hasHeightForWidth())
        self.pushButton21.setSizePolicy(sizePolicy)
        self.pushButton21.setMaximumSize(QtCore.QSize(33, 27))
        self.pushButton21.setSizeIncrement(QtCore.QSize(33, 27))
        self.pushButton21.setCheckable(True)
        self.pushButton21.setObjectName(_fromUtf8("pushButton21"))
        self.gridLayout.addWidget(self.pushButton21, 5, 0, 1, 1)
        self.pushButton15 = QtGui.QPushButton(self.gridLayoutWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton15.sizePolicy().hasHeightForWidth())
        self.pushButton15.setSizePolicy(sizePolicy)
        self.pushButton15.setMaximumSize(QtCore.QSize(33, 27))
        self.pushButton15.setSizeIncrement(QtCore.QSize(33, 27))
        self.pushButton15.setCheckable(True)
        self.pushButton15.setObjectName(_fromUtf8("pushButton15"))
        self.gridLayout.addWidget(self.pushButton15, 3, 2, 1, 1)
        self.label_2 = QtGui.QLabel(self.gridLayoutWidget)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout.addWidget(self.label_2, 8, 0, 1, 1, QtCore.Qt.AlignBottom)
        self.setBut = QtGui.QPushButton(Dialog)
        self.setBut.setGeometry(QtCore.QRect(21, 311, 131, 27))
        self.setBut.setObjectName(_fromUtf8("setBut"))
        self.label = QtGui.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(10, 0, 56, 17))
        self.label.setObjectName(_fromUtf8("label"))

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Time", None))
        self.pushButton25.setText(_translate("Dialog", "25:", None))
        self.pushButton5.setText(_translate("Dialog", "05:", None))
        self.pushButton17.setText(_translate("Dialog", "17:", None))
        self.pushButton6.setText(_translate("Dialog", "06:", None))
        self.pushButton13.setText(_translate("Dialog", "13:", None))
        self.pushButton16.setText(_translate("Dialog", "16:", None))
        self.pushButton11.setText(_translate("Dialog", "11:", None))
        self.pushButton14.setText(_translate("Dialog", "14:", None))
        self.pushButton0000.setText(_translate("Dialog", ":00", None))
        self.pushButton3.setText(_translate("Dialog", "03:", None))
        self.pushButton20.setText(_translate("Dialog", "20:", None))
        self.pushButton0015.setText(_translate("Dialog", ":15", None))
        self.pushButton18.setText(_translate("Dialog", "18:", None))
        self.pushButtonCLR.setText(_translate("Dialog", "CLR", None))
        self.pushButton24.setText(_translate("Dialog", "24:", None))
        self.pushButton9.setText(_translate("Dialog", "09:", None))
        self.pushButton10.setText(_translate("Dialog", "10:", None))
        self.pushButton26.setText(_translate("Dialog", "26:", None))
        self.pushButton22.setText(_translate("Dialog", "22:", None))
        self.pushButton0030.setText(_translate("Dialog", ":30", None))
        self.pushButton12.setText(_translate("Dialog", "12:", None))
        self.pushButton2.setText(_translate("Dialog", "02:", None))
        self.pushButton4.setText(_translate("Dialog", "04:", None))
        self.pushButton8.setText(_translate("Dialog", "08:", None))
        self.pushButton19.setText(_translate("Dialog", "19:", None))
        self.pushButton0045.setText(_translate("Dialog", ":45", None))
        self.pushButton7.setText(_translate("Dialog", "07:", None))
        self.pushButton23.setText(_translate("Dialog", "23:", None))
        self.pushButton1.setText(_translate("Dialog", "01:", None))
        self.pushButton21.setText(_translate("Dialog", "21:", None))
        self.pushButton15.setText(_translate("Dialog", "15:", None))
        self.label_2.setText(_translate("Dialog", "<html><head/><body><p><span style=\" font-weight:600;\">Mins</span></p></body></html>", None))
        self.setBut.setText(_translate("Dialog", "Set", None))
        self.label.setText(_translate("Dialog", "<html><head/><body><p><span style=\" font-weight:600;\">Hours</span></p></body></html>", None))

