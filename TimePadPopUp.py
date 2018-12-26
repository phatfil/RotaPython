from PyQt4 import QtGui
from TimePad import Ui_Dialog
import ShiftPopUp


class TimePadPopUp(QtGui.QDialog):
    a = float()  # Total hours counter variable
    #sender = str()

    def __init__(self, StAM, FinAM, BrkAM, StPM, FinPM, BrkPM):
        super(TimePadPopUp, self).__init__()
        QtGui.QWidget.__init__(self)
        self.uip = Ui_Dialog()
        self.uip.setupUi(self)
        self.StAM = StAM
        self.FinAM = FinAM
        self.BrkAM = BrkAM
        self.StPM = StPM
        self.FinPM = FinPM
        self.BrkPM = BrkPM

        # 0 the total hours counter variable 'a'
        TimePadPopUp.a = + 0
        # Connect all buttons to modules
        self.uip.pushButton1.clicked.connect(self.Button1)
        self.uip.pushButton2.clicked.connect(self.Button2)
        self.uip.pushButton3.clicked.connect(self.Button3)
        self.uip.pushButton4.clicked.connect(self.Button4)
        self.uip.pushButton5.clicked.connect(self.Button5)
        self.uip.pushButton6.clicked.connect(self.Button6)
        self.uip.pushButton7.clicked.connect(self.Button7)
        self.uip.pushButton8.clicked.connect(self.Button8)
        self.uip.pushButton9.clicked.connect(self.Button9)
        self.uip.pushButton10.clicked.connect(self.Button10)
        self.uip.pushButton11.clicked.connect(self.Button11)
        self.uip.pushButton12.clicked.connect(self.Button12)
        self.uip.pushButton13.clicked.connect(self.Button13)
        self.uip.pushButton14.clicked.connect(self.Button14)
        self.uip.pushButton15.clicked.connect(self.Button15)
        self.uip.pushButton16.clicked.connect(self.Button16)
        self.uip.pushButton17.clicked.connect(self.Button17)
        self.uip.pushButton18.clicked.connect(self.Button18)
        self.uip.pushButton19.clicked.connect(self.Button19)
        self.uip.pushButton20.clicked.connect(self.Button20)
        self.uip.pushButton21.clicked.connect(self.Button21)
        self.uip.pushButton22.clicked.connect(self.Button22)
        self.uip.pushButton23.clicked.connect(self.Button23)
        self.uip.pushButton24.clicked.connect(self.Button24)
        self.uip.pushButton25.clicked.connect(self.Button25)
        self.uip.pushButton26.clicked.connect(self.Button26)
        self.uip.pushButton0000.clicked.connect(self.Button0000)
        self.uip.pushButton0015.clicked.connect(self.Button0015)
        self.uip.pushButton0030.clicked.connect(self.Button0030)
        self.uip.pushButton0045.clicked.connect(self.Button0045)
        self.uip.pushButtonCLR.clicked.connect(self.ButtonCLR)

    def ButtonCLR(self):
        self.sender = ShiftPopUp.ShiftPopUp.senderBUT
        # Use the passed button sender information from ShiftPopUp.TimePadPopUp to assign date to relevant variable
        if str(self.sender[0:-3]) == "StAM":
            self.StAM = 0
        elif str(self.sender[0:-3]) == "FinAM":
            self.FinAM = 0
        elif str(self.sender[0:-3]) == "BrkAM":
            self.BrkAM = 0
        elif str(self.sender[0:-3]) == "StPM":
            self.StPM = 0
        elif str(self.sender[0:-3]) == "FinPM":
            self.FinPM = 0
        elif str(self.sender[0:-3]) == "BrkPM":
            self.BrkPM = 0

    def Button1(self):
        if self.uip.pushButton1.isChecked() is True:  # If button is checked increase counter by 1
            TimePadPopUp.a = TimePadPopUp.a + 1
        elif self.uip.pushButton1.isChecked() is False:  # If button is unchecked decrease counter by 1
            TimePadPopUp.a = TimePadPopUp.a - 1
        print(TimePadPopUp.a)

    def Button2(self):
        if self.uip.pushButton2.isChecked() is True:
            TimePadPopUp.a = TimePadPopUp.a + 2
        elif self.uip.pushButton2.isChecked() is False:
            TimePadPopUp.a = TimePadPopUp.a - 2
        print(TimePadPopUp.a)

    def Button3(self):
        if self.uip.pushButton3.isChecked() is True:
            TimePadPopUp.a = TimePadPopUp.a + 3
        elif self.uip.pushButton3.isChecked() is False:
            TimePadPopUp.a = TimePadPopUp.a - 3
        print(TimePadPopUp.a)

    def Button4(self):
        if self.uip.pushButton4.isChecked() is True:
            TimePadPopUp.a = TimePadPopUp.a + 4
        elif self.uip.pushButton4.isChecked() is False:
            TimePadPopUp.a = TimePadPopUp.a - 4
        print(TimePadPopUp.a)

    def Button5(self):
        if self.uip.pushButton5.isChecked() is True:
            TimePadPopUp.a = TimePadPopUp.a + 5
        elif self.uip.pushButton5.isChecked() is False:
            TimePadPopUp.a = TimePadPopUp.a - 5
        print(TimePadPopUp.a)

    def Button6(self):
        if self.uip.pushButton6.isChecked() is True:
            TimePadPopUp.a = TimePadPopUp.a + 6
        elif self.uip.pushButton6.isChecked() is False:
            TimePadPopUp.a = TimePadPopUp.a - 6
        print(TimePadPopUp.a)

    def Button7(self):
        if self.uip.pushButton7.isChecked() is True:
            TimePadPopUp.a = TimePadPopUp.a + 7
        elif self.uip.pushButton7.isChecked() is False:
            TimePadPopUp.a = TimePadPopUp.a - 7
        print(TimePadPopUp.a)

    def Button8(self):
        if self.uip.pushButton8.isChecked() is True:
            TimePadPopUp.a = TimePadPopUp.a + 8
        elif self.uip.pushButton8.isChecked() is False:
            TimePadPopUp.a = TimePadPopUp.a - 8
        print(TimePadPopUp.a)

    def Button9(self):
        if self.uip.pushButton9.isChecked() is True:
            TimePadPopUp.a = TimePadPopUp.a + 9
        elif self.uip.pushButton9.isChecked() is False:
            TimePadPopUp.a = TimePadPopUp.a - 9
        print(TimePadPopUp.a)

    def Button10(self):
        if self.uip.pushButton10.isChecked() is True:
            TimePadPopUp.a = TimePadPopUp.a + 10
        elif self.uip.pushButton10.isChecked() is False:
            TimePadPopUp.a = TimePadPopUp.a - 10
        print(TimePadPopUp.a)

    def Button11(self):
        if self.uip.pushButton11.isChecked() is True:
            TimePadPopUp.a = TimePadPopUp.a + 11
        elif self.uip.pushButton11.isChecked() is False:
            TimePadPopUp.a = TimePadPopUp.a - 11
        print(TimePadPopUp.a)

    def Button12(self):
        if self.uip.pushButton12.isChecked() is True:
            TimePadPopUp.a = TimePadPopUp.a + 12
        elif self.uip.pushButton12.isChecked() is False:
            TimePadPopUp.a = TimePadPopUp.a - 12
        print(TimePadPopUp.a)

    def Button13(self):
        if self.uip.pushButton13.isChecked() is True:
            TimePadPopUp.a = TimePadPopUp.a + 13
        elif self.uip.pushButton13.isChecked() is False:
            TimePadPopUp.a = TimePadPopUp.a - 13
        print(TimePadPopUp.a)

    def Button14(self):
        if self.uip.pushButton14.isChecked() is True:
            TimePadPopUp.a = TimePadPopUp.a + 14
        elif self.uip.pushButton14.isChecked() is False:
            TimePadPopUp.a = TimePadPopUp.a - 14
        print(TimePadPopUp.a)

    def Button15(self):
        if self.uip.pushButton15.isChecked() is True:
            TimePadPopUp.a = TimePadPopUp.a + 15
        elif self.uip.pushButton15.isChecked() is False:
            TimePadPopUp.a = TimePadPopUp.a - 15
        print(TimePadPopUp.a)

    def Button16(self):
        if self.uip.pushButton16.isChecked() is True:
            TimePadPopUp.a = TimePadPopUp.a + 16
        elif self.uip.pushButton16.isChecked() is False:
            TimePadPopUp.a = TimePadPopUp.a - 16
        print(TimePadPopUp.a)

    def Button17(self):
        if self.uip.pushButton17.isChecked() is True:
            TimePadPopUp.a = TimePadPopUp.a + 17
        elif self.uip.pushButton17.isChecked() is False:
            TimePadPopUp.a = TimePadPopUp.a - 17
        print(TimePadPopUp.a)

    def Button18(self):
        if self.uip.pushButton18.isChecked() is True:
            TimePadPopUp.a = TimePadPopUp.a + 18
        elif self.uip.pushButton18.isChecked() is False:
            TimePadPopUp.a = TimePadPopUp.a - 18
        print(TimePadPopUp.a)

    def Button19(self):
        if self.uip.pushButton19.isChecked() is True:
            TimePadPopUp.a = TimePadPopUp.a + 19
        elif self.uip.pushButton19.isChecked() is False:
            TimePadPopUp.a = TimePadPopUp.a - 19
        print(TimePadPopUp.a)

    def Button20(self):
        if self.uip.pushButton20.isChecked() is True:
            TimePadPopUp.a = TimePadPopUp.a + 20
        elif self.uip.pushButton20.isChecked() is False:
            TimePadPopUp.a = TimePadPopUp.a - 20
        print(TimePadPopUp.a)

    def Button21(self):
        if self.uip.pushButton21.isChecked() is True:
            TimePadPopUp.a = TimePadPopUp.a + 21
        elif self.uip.pushButton21.isChecked() is False:
            TimePadPopUp.a = TimePadPopUp.a - 21
        print(TimePadPopUp.a)

    def Button22(self):
        if self.uip.pushButton22.isChecked() is True:
            TimePadPopUp.a = TimePadPopUp.a + 22
        elif self.uip.pushButton22.isChecked() is False:
            TimePadPopUp.a = TimePadPopUp.a - 22
        print(TimePadPopUp.a)

    def Button23(self):
        if self.uip.pushButton23.isChecked() is True:
            TimePadPopUp.a = TimePadPopUp.a + 23
        elif self.uip.pushButton23.isChecked() is False:
            TimePadPopUp.a = TimePadPopUp.a - 23
        print(TimePadPopUp.a)

    def Button24(self):
        if self.uip.pushButton24.isChecked() is True:
            TimePadPopUp.a = TimePadPopUp.a + 24
        elif self.uip.pushButton24.isChecked() is False:
            TimePadPopUp.a = TimePadPopUp.a - 24
        print(TimePadPopUp.a)

    def Button25(self):
        if self.uip.pushButton25.isChecked() is True:
            TimePadPopUp.a = TimePadPopUp.a + 25
        elif self.uip.pushButton25.isChecked() is False:
            TimePadPopUp.a = TimePadPopUp.a - 25
        print(TimePadPopUp.a)

    def Button26(self):
        if self.uip.pushButton26.isChecked() is True:
            TimePadPopUp.a = TimePadPopUp.a + 26
        elif self.uip.pushButton26.isChecked() is False:
            TimePadPopUp.a = TimePadPopUp.a - 26
        print(TimePadPopUp.a)

    def Button0015(self):
        if self.uip.pushButton0015.isChecked() is True:
            TimePadPopUp.a = TimePadPopUp.a + 0.25
        elif self.uip.pushButton0015.isChecked() is False:
            TimePadPopUp.a = TimePadPopUp.a - 0.25
        print(TimePadPopUp.a)

    def Button0030(self):
        if self.uip.pushButton0030.isChecked() is True:
            TimePadPopUp.a = TimePadPopUp.a + 0.5
        elif self.uip.pushButton0030.isChecked() is False:
            TimePadPopUp.a = TimePadPopUp.a - 0.5
        print(TimePadPopUp.a)

    def Button0045(self):
        if self.uip.pushButton0045.isChecked() is True:
            TimePadPopUp.a = TimePadPopUp.a + 0.75
        elif self.uip.pushButton0045.isChecked() is False:
            TimePadPopUp.a = TimePadPopUp.a - 0.75
        print(TimePadPopUp.a)

    def Button0000(self):
        if self.uip.pushButton0000.isChecked() is True:
            TimePadPopUp.a = TimePadPopUp.a + 0.0
        elif self.uip.pushButton0000.isChecked() is False:
            TimePadPopUp.a = TimePadPopUp.a - 0.0
        print(TimePadPopUp.a)