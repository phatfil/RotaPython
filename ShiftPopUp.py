from PyQt4 import QtGui
from ShiftPopUpWindow import Ui_ShiftPopUpWindow
import TimePadPopUp
from PyQt4.QtCore import pyqtSignal
import DB
import time
import Employees

class ShiftPopUp(QtGui.QDialog, QtGui.QLabel):
    trigger = pyqtSignal()
    senderBUT = str()
    def __init__(self, cellcol, cellrow, dateList, results, shiftTypes, departments, empID):
        super(ShiftPopUp, self).__init__()

        self.uip = Ui_ShiftPopUpWindow()
        self.uip.setupUi(self)

        self.cellcol = cellcol
        self.cellrow = cellrow
        self.dateList = dateList
        self.results2 = results
        self.shiftTypes = shiftTypes
        self.departments = departments
        self.empID = empID

        self.ShiftDate = None
        self.Name = ()
        self.StAM = float()
        self.StartAMConcat = ()
        self.FinAM = float()
        self.FinAMConcat = ()
        self.BrkAM = float()
        self.BrkAMConcat = ()
        self.StPM = float()
        self.StartPMConcat = ()
        self.FinPM = float()
        self.FinPMConcat = ()
        self.BrkPM = float()
        self.BrkPMConcat = ()
        self.TotalHours = float()
        self.ConcatShift = str()
        self.fetched = ()
        self.shiftsID = int()
        self.EmpID = int()
        self.shiftTypeAM = 0
        self.shiftTypePM = 0
        self.EmployeeDep = 0

        # set as standard department
        self.AmDepartmentType = self.results2[self.cellrow][11]
        self.PmDepartmentType = self.results2[self.cellrow][11]

        self.retrieveAutoShiftTimes()

        # 1 Populate variables from Main Window data
        ShiftPopUp.populatesVariablesfromMain(self)

        # 2 Query DB and populate class variables
        ShiftPopUp.queryShiftandEmployeeTbl(self)

        # 2.1 Query Emp Class Tables
        self.queryEmpClassTables()

        # 2.2 define emp class
        self.emp = Employees.employees(self.empTable, self.salTable, self.depTable, self.bonusTable, self.holsTable,
                                       self.salorHourlyTable)

        # 3 Set Name box as selected employee
        self.uip.EmpNameBox.setText(self.Name)

        # 4 Sets the Popup date box to retrieved date
        self.uip.ShiftDate.setDate(self.ShiftDate)

        # 4.5 Populate drop downs
        self.populateShiftTypeDropDowns()
        self.populateDepCombo()

        # 4.7 Define trigger slots
        self.defineTriggerSlots()

        # 4.8 Set Tab
        self.setTabToEmployeeRole()

        if self.fetched == ():
            # 5 populate variables with blanks if blank cell is clicked
            self.blankcellpopulate()
        else:
            # 5 Call PopulateVariables Modules to populate class variables from fetched data
            self.populateVariables()

            # 6 Convert decimal hours to time format for buttons
            ShiftPopUp.buttonDectoTimeConvertion(self)

            # 7 Set buttons to relevant times
            ShiftPopUp.writeTimetoButton(self)

            # 8 Concatenate the fetched times
            ShiftPopUp.concatenateShiftEngine(self)

            # 9 Calculate Total Hours
            ShiftPopUp.calculateHours(self)

            # 10 Have the dropdown selection adjust according to shift data
            self.setSelectedIteminShiftTypeDropDownBox()

    def changeDepComboSelection(self, depIndex):
        depAM = self.uip.DepAMCombo
        depPM = self.uip.DepPMCombo
        depAM.setCurrentIndex(depIndex)
        depPM.setCurrentIndex(depIndex)

    def populateStandardWeek(self):
        self.shiftIDList = []
        self.shiftTypeList = []

        for a in range(7):
            date = str(self.dateList[a])
            data = DB.Querydb('''
                            SELECT shiftsID, shiftTypeAM, shiftTypePM
                            FROM`shifts`
                            WHERE Date = %s AND EmployeeID = %s
                            ''', (date, self.EmpID)).fetchAllRecordswithFormatting()
            if data == ():
                self.shiftIDList.append("")
                self.shiftTypeList.append(["", ""])
            else:
                self.shiftIDList.append(data[0][0])
                self.shiftTypeList.append([data[0][1], data[0][2]])
        print (self.shiftTypeList)
        empDep = self.emp.empDepID(self.empID)
        foh = ['self.uip.FOHBut1.click()', 'self.uip.FOHBut2.click()', 'self.uip.FOHBut3.click()', 'self.uip.FOHBut4.click()',
               'self.uip.FOHBut5.click()', 'self.uip.FOHBut6.click()', 'self.uip.FOHBut7.click()']
        gen = ['self.uip.GenBut1.click()', 'self.uip.GenBut2.click()', 'self.uip.GenBut3.click()', 'self.uip.GenBut4.click()',
               'self.uip.GenBut5.click()', 'self.uip.GenBut6.click()', 'self.uip.GenBut7.click()']
        kit = ['self.uip.KitBut1.click()', 'self.uip.KitBut2.click()', 'self.uip.KitBut3.click()', 'self.uip.KitBut4.click()',
               'self.uip.KitBut5.click()', 'self.uip.KitBut6.click()', 'self.uip.KitBut7.click()']
        admin = ['self.uip.AdminBut1.click()', 'self.uip.AdminBut2.click()', 'self.uip.AdminBut3.click()',
                 'self.uip.AdminBut4.click()', 'self.uip.AdminBut5.click()', 'self.uip.AdminBut6.click()',
                 'self.uip.AdminBut7.click()']

        if empDep == 4: # if emp is general
            for d in range(len(self.dateList)):
                rules = [self.emp.isEmpCurrentlyEmployed(self.empID, self.dateList[d]) is False,
                         self.shiftTypeList[d][0] == 2,
                         self.shiftTypeList[d][1] == 2,
                         self.shiftTypeList[d][0] == 5,
                         self.shiftTypeList[d][1] == 5]

                if any(rules) : # if emp is on holiday, not currently employed or Unavailable skip
                    pass
                else:
                    self.ShiftDate = self.dateList[d]
                    exec(gen[d])
                    self.changeDepComboSelection(2)
                    if self.shiftIDList[d] == "":
                        self.HolidayUsageEntitlementDailyCalc()
                        self.insertNewShiftintoDB()
                    else:
                        self.shiftsID = self.shiftIDList[d]
                        self.HolidayUsageEntitlementDailyCalc()
                        self.updateRecordinDB()

        elif empDep == 2: # if emp is kit
            for d in range(len(self.dateList)):
                rules = [self.emp.isEmpCurrentlyEmployed(self.empID, self.dateList[d]) is False,
                         self.shiftTypeList[d][0] == 2,
                         self.shiftTypeList[d][1] == 2,
                         self.shiftTypeList[d][0] == 5,
                         self.shiftTypeList[d][1] == 5]
                if any(rules) : # if emp is on holiday, not currently employed or Unavailable skip
                    pass
                else:
                    self.ShiftDate = self.dateList[d]
                    exec(kit[d])
                    self.changeDepComboSelection(0)
                    if self.shiftIDList[d] == "":
                        self.HolidayUsageEntitlementDailyCalc()
                        self.insertNewShiftintoDB()
                    else:
                        self.shiftsID = self.shiftIDList[d]
                        self.HolidayUsageEntitlementDailyCalc()
                        self.updateRecordinDB()

        elif empDep == 3: # if emp is foh
            for d in range(len(self.dateList)):
                rules = [self.emp.isEmpCurrentlyEmployed(self.empID, self.dateList[d]) is False,
                         self.shiftTypeList[d][0] == 2,
                         self.shiftTypeList[d][1] == 2,
                         self.shiftTypeList[d][0] == 5,
                         self.shiftTypeList[d][1] == 5]
                if any(rules) : # if emp is on holiday, not currently employed or Unavailable skip
                    pass
                else:
                    self.ShiftDate = self.dateList[d]
                    exec(foh[d])
                    self.changeDepComboSelection(1)
                    if self.shiftIDList[d] == "":
                        self.HolidayUsageEntitlementDailyCalc()
                        self.insertNewShiftintoDB()
                    else:
                        self.shiftsID = self.shiftIDList[d]
                        self.HolidayUsageEntitlementDailyCalc()
                        self.updateRecordinDB()

        elif empDep == 5: # if emp is admin
            for d in range(len(self.dateList)):
                rules = [self.emp.isEmpCurrentlyEmployed(self.empID, self.dateList[d]) is False,
                        self.shiftTypeList[d][0] == 2,
                         self.shiftTypeList[d][1] == 2,
                         self.shiftTypeList[d][0] == 5,
                         self.shiftTypeList[d][1] == 5]
                if any(rules) : # if emp is on holiday, not currently employed or Unavailable skip
                    pass
                else:
                    self.ShiftDate = self.dateList[d]
                    exec(admin[d])
                    self.changeDepComboSelection(3)
                    if self.shiftIDList[d] == "":
                        self.HolidayUsageEntitlementDailyCalc()
                        self.insertNewShiftintoDB()
                    else:
                        self.shiftsID = self.shiftIDList[d]
                        self.HolidayUsageEntitlementDailyCalc()
                        self.updateRecordinDB()
        else:
            pass

        self.emitTrigger()
        self.close()



    def setTabToEmployeeRole(self):
        if self.emp.empDepID(self.empID) == 2:
            self.uip.tabWidget.setCurrentIndex(2)
        elif self.emp.empDepID(self.empID) == 3:
            self.uip.tabWidget.setCurrentIndex(1)
        elif self.emp.empDepID(self.empID) == 4:
            self.uip.tabWidget.setCurrentIndex(0)
        elif self.emp.empDepID(self.empID) == 5:
            self.uip.tabWidget.setCurrentIndex(3)

    def defineTriggerSlots(self):
        # Set slots for time buttons
        self.uip.StAMBUT.clicked.connect(self.timePadPopUp)
        self.uip.FinAMBUT.clicked.connect(self.timePadPopUp)
        self.uip.BrkAMBUT.clicked.connect(self.timePadPopUp)
        self.uip.StPMBUT.clicked.connect(self.timePadPopUp)
        self.uip.FinPMBUT.clicked.connect(self.timePadPopUp)
        self.uip.BrkPMBUT.clicked.connect(self.timePadPopUp)
        self.uip.UdateBUT.clicked.connect(self.setOrUpdatetheDB)
        self.uip.standardWeekBUT.clicked.connect(self.populateStandardWeek)
        self.uip.UdateBUT.clicked.connect(self.emitTrigger)


        self.uip.GenBut1.pressed.connect(self.buttonPressed)
        self.uip.GenBut1.released.connect(self.buttonReleased)
        self.uip.GenBut1.clicked.connect(self.setOrClickCustomShiftButton)
        self.uip.GenBut2.pressed.connect(self.buttonPressed)
        self.uip.GenBut2.released.connect(self.buttonReleased)
        self.uip.GenBut2.clicked.connect(self.setOrClickCustomShiftButton)
        self.uip.GenBut3.pressed.connect(self.buttonPressed)
        self.uip.GenBut3.released.connect(self.buttonReleased)
        self.uip.GenBut3.clicked.connect(self.setOrClickCustomShiftButton)
        self.uip.GenBut4.pressed.connect(self.buttonPressed)
        self.uip.GenBut4.released.connect(self.buttonReleased)
        self.uip.GenBut4.clicked.connect(self.setOrClickCustomShiftButton)
        self.uip.GenBut5.pressed.connect(self.buttonPressed)
        self.uip.GenBut5.released.connect(self.buttonReleased)
        self.uip.GenBut5.clicked.connect(self.setOrClickCustomShiftButton)
        self.uip.GenBut6.pressed.connect(self.buttonPressed)
        self.uip.GenBut6.released.connect(self.buttonReleased)
        self.uip.GenBut6.clicked.connect(self.setOrClickCustomShiftButton)
        self.uip.GenBut7.pressed.connect(self.buttonPressed)
        self.uip.GenBut7.released.connect(self.buttonReleased)
        self.uip.GenBut7.clicked.connect(self.setOrClickCustomShiftButton)

        self.uip.FOHBut1.pressed.connect(self.buttonPressed)
        self.uip.FOHBut1.released.connect(self.buttonReleased)
        self.uip.FOHBut1.clicked.connect(self.setOrClickCustomShiftButton)
        self.uip.FOHBut2.pressed.connect(self.buttonPressed)
        self.uip.FOHBut2.released.connect(self.buttonReleased)
        self.uip.FOHBut2.clicked.connect(self.setOrClickCustomShiftButton)
        self.uip.FOHBut3.pressed.connect(self.buttonPressed)
        self.uip.FOHBut3.released.connect(self.buttonReleased)
        self.uip.FOHBut3.clicked.connect(self.setOrClickCustomShiftButton)
        self.uip.FOHBut4.pressed.connect(self.buttonPressed)
        self.uip.FOHBut4.released.connect(self.buttonReleased)
        self.uip.FOHBut4.clicked.connect(self.setOrClickCustomShiftButton)
        self.uip.FOHBut5.pressed.connect(self.buttonPressed)
        self.uip.FOHBut5.released.connect(self.buttonReleased)
        self.uip.FOHBut5.clicked.connect(self.setOrClickCustomShiftButton)
        self.uip.FOHBut6.pressed.connect(self.buttonPressed)
        self.uip.FOHBut6.released.connect(self.buttonReleased)
        self.uip.FOHBut6.clicked.connect(self.setOrClickCustomShiftButton)
        self.uip.FOHBut7.pressed.connect(self.buttonPressed)
        self.uip.FOHBut7.released.connect(self.buttonReleased)
        self.uip.FOHBut7.clicked.connect(self.setOrClickCustomShiftButton)

        self.uip.KitBut1.pressed.connect(self.buttonPressed)
        self.uip.KitBut1.released.connect(self.buttonReleased)
        self.uip.KitBut1.clicked.connect(self.setOrClickCustomShiftButton)
        self.uip.KitBut2.pressed.connect(self.buttonPressed)
        self.uip.KitBut2.released.connect(self.buttonReleased)
        self.uip.KitBut2.clicked.connect(self.setOrClickCustomShiftButton)
        self.uip.KitBut3.pressed.connect(self.buttonPressed)
        self.uip.KitBut3.released.connect(self.buttonReleased)
        self.uip.KitBut3.clicked.connect(self.setOrClickCustomShiftButton)
        self.uip.KitBut4.pressed.connect(self.buttonPressed)
        self.uip.KitBut4.released.connect(self.buttonReleased)
        self.uip.KitBut4.clicked.connect(self.setOrClickCustomShiftButton)
        self.uip.KitBut5.pressed.connect(self.buttonPressed)
        self.uip.KitBut5.released.connect(self.buttonReleased)
        self.uip.KitBut5.clicked.connect(self.setOrClickCustomShiftButton)
        self.uip.KitBut6.pressed.connect(self.buttonPressed)
        self.uip.KitBut6.released.connect(self.buttonReleased)
        self.uip.KitBut6.clicked.connect(self.setOrClickCustomShiftButton)
        self.uip.KitBut7.pressed.connect(self.buttonPressed)
        self.uip.KitBut7.released.connect(self.buttonReleased)
        self.uip.KitBut7.clicked.connect(self.setOrClickCustomShiftButton)

        self.uip.AdminBut1.pressed.connect(self.buttonPressed)
        self.uip.AdminBut1.released.connect(self.buttonReleased)
        self.uip.AdminBut1.clicked.connect(self.setOrClickCustomShiftButton)
        self.uip.AdminBut2.pressed.connect(self.buttonPressed)
        self.uip.AdminBut2.released.connect(self.buttonReleased)
        self.uip.AdminBut2.clicked.connect(self.setOrClickCustomShiftButton)
        self.uip.AdminBut3.pressed.connect(self.buttonPressed)
        self.uip.AdminBut3.released.connect(self.buttonReleased)
        self.uip.AdminBut3.clicked.connect(self.setOrClickCustomShiftButton)
        self.uip.AdminBut4.pressed.connect(self.buttonPressed)
        self.uip.AdminBut4.released.connect(self.buttonReleased)
        self.uip.AdminBut4.clicked.connect(self.setOrClickCustomShiftButton)
        self.uip.AdminBut5.pressed.connect(self.buttonPressed)
        self.uip.AdminBut5.released.connect(self.buttonReleased)
        self.uip.AdminBut5.clicked.connect(self.setOrClickCustomShiftButton)
        self.uip.AdminBut6.pressed.connect(self.buttonPressed)
        self.uip.AdminBut6.released.connect(self.buttonReleased)
        self.uip.AdminBut6.clicked.connect(self.setOrClickCustomShiftButton)
        self.uip.AdminBut7.pressed.connect(self.buttonPressed)
        self.uip.AdminBut7.released.connect(self.buttonReleased)
        self.uip.AdminBut7.clicked.connect(self.setOrClickCustomShiftButton)

        # combo box change monitoring
        self.uip.DepAMCombo.currentIndexChanged.connect(self.updateDepTypeVariables)
        self.uip.DepPMCombo.currentIndexChanged.connect(self.updateDepTypeVariables)

        # define the clr button
        self.uip.AmShiftCLRBut.clicked.connect(self.clearTheshiftAM)
        self.uip.PmShiftCLRBut.clicked.connect(self.clearTheshiftPM)

    def queryEmpClassTables(self):
        self.empTable = DB.Querydb("""SELECT * FROM Employee_TBL""", None).fetchAllRecordswithFormatting()
        self.salTable = DB.Querydb("""SELECT * FROM Salary""", None).fetchAllRecordswithFormatting()
        self.depTable = DB.Querydb("""SELECT * FROM departments""", None).fetchAllRecordswithFormatting()
        self.bonusTable = DB.Querydb("""SELECT * FROM Bonus""", None).fetchAllRecordswithFormatting()
        self.holsTable = DB.Querydb("""SELECT * FROM HolidayEntitlement""", None).fetchAllRecordswithFormatting()
        self.salorHourlyTable = DB.Querydb("""SELECT * FROM salorHourlyTable""", None).fetchAllRecordswithFormatting()

    def populateShiftTypeDropDowns(self):
        comboAM = self.uip.AmShiftTypeCombo
        comboPM = self.uip.PmShiftTypeCombo
        for a in range(len(self.shiftTypes)):
            comboAM.addItem(self.shiftTypes[a][1])
            comboPM.addItem(self.shiftTypes[a][1])

    def populateDepCombo(self):
        # Populate the department drop downs
        depAM = self.uip.DepAMCombo
        depPM = self.uip.DepPMCombo
        for a in range(len(self.departments)):
            depAM.addItem(self.departments[a][1])
            depPM.addItem(self.departments[a][1])

        # Set the department combo boxes to the data from the shift DB,
        # if not present set to Employee's standard department info
        if self.fetched == ():
            DepTypeAM = [depType for (ID, depType) in self.departments if ID == self.EmployeeDep]
            index = depAM.findText(DepTypeAM[0])
            depAM.setCurrentIndex(index)
        else:
            DepTypeAM = [depType for (ID, depType) in self.departments if ID == self.fetched[0][13]]
            index = depAM.findText(DepTypeAM[0])
            depAM.setCurrentIndex(index)

        if self.fetched == ():
            DepTypePM = [depType for (ID, depType) in self.departments if ID == self.EmployeeDep]
            index = depPM.findText(DepTypePM[0])
            depPM.setCurrentIndex(index)
        else:
            DepTypePM = [depType for (ID, depType) in self.departments if ID == self.fetched[0][14]]
            index = depPM.findText(DepTypePM[0])
            depPM.setCurrentIndex(index)

    def clearTheshiftAM(self):
        self.StAM = int()
        self.FinAM = int()
        self.BrkAM = int()
        self.uip.AmShiftTypeCombo.setCurrentIndex(0)

        ShiftPopUp.buttonDectoTimeConvertion(self)
        ShiftPopUp.writeTimetoButton(self)
        ShiftPopUp.concatenateShiftEngine(self)
        ShiftPopUp.calculateHours(self)

    def clearTheshiftPM(self):
        self.StPM = int()
        self.FinPM = int()
        self.BrkPM = int()
        self.uip.PmShiftTypeCombo.setCurrentIndex(0)

        ShiftPopUp.buttonDectoTimeConvertion(self)
        ShiftPopUp.writeTimetoButton(self)
        ShiftPopUp.concatenateShiftEngine(self)
        ShiftPopUp.calculateHours(self)

    def retrieveAutoShiftTimes(self):
        auto = DB.Querydb("SELECT * FROM AutoShiftTimes", None).fetchAllRecordswithFormatting()
        self.autoButtons = {auto[a][1]: [auto[a][2], auto[a][3], auto[a][4], auto[a][5], auto[a][6],
                                         auto[a][7], auto[a][8], auto[a][9], auto[a][10]] for a in range(len(auto))}
        self.setAutoButtons()

    def setAutoButtons(self):

        self.uip.GenBut1.setText(self.autoButtons['GenBut1'][0])
        self.uip.GenBut2.setText(self.autoButtons['GenBut2'][0])
        self.uip.GenBut3.setText(self.autoButtons['GenBut3'][0])
        self.uip.GenBut4.setText(self.autoButtons['GenBut4'][0])
        self.uip.GenBut5.setText(self.autoButtons['GenBut5'][0])
        self.uip.GenBut6.setText(self.autoButtons['GenBut6'][0])
        self.uip.GenBut7.setText(self.autoButtons['GenBut7'][0])
        self.uip.FOHBut1.setText(self.autoButtons['FOHBut1'][0])
        self.uip.FOHBut2.setText(self.autoButtons['FOHBut2'][0])
        self.uip.FOHBut3.setText(self.autoButtons['FOHBut3'][0])
        self.uip.FOHBut4.setText(self.autoButtons['FOHBut4'][0])
        self.uip.FOHBut5.setText(self.autoButtons['FOHBut5'][0])
        self.uip.FOHBut6.setText(self.autoButtons['FOHBut6'][0])
        self.uip.FOHBut7.setText(self.autoButtons['FOHBut7'][0])
        self.uip.KitBut1.setText(self.autoButtons['KitBut1'][0])
        self.uip.KitBut2.setText(self.autoButtons['KitBut2'][0])
        self.uip.KitBut3.setText(self.autoButtons['KitBut3'][0])
        self.uip.KitBut4.setText(self.autoButtons['KitBut4'][0])
        self.uip.KitBut5.setText(self.autoButtons['KitBut5'][0])
        self.uip.KitBut6.setText(self.autoButtons['KitBut6'][0])
        self.uip.KitBut7.setText(self.autoButtons['KitBut7'][0])
        self.uip.AdminBut1.setText(self.autoButtons['AdminBut1'][0])
        self.uip.AdminBut2.setText(self.autoButtons['AdminBut2'][0])
        self.uip.AdminBut3.setText(self.autoButtons['AdminBut3'][0])
        self.uip.AdminBut4.setText(self.autoButtons['AdminBut4'][0])
        self.uip.AdminBut5.setText(self.autoButtons['AdminBut5'][0])
        self.uip.AdminBut6.setText(self.autoButtons['AdminBut6'][0])
        self.uip.AdminBut7.setText(self.autoButtons['AdminBut7'][0])

    def populatesVariablesfromMain(self):
        # Populate date variable from main window variable
        self.ShiftDate = self.dateList[int(self.cellcol) - 1]

        # Populate Name variable from main window results
        self.Name = self.results2[self.cellrow][0]

        # Populate the EmpID variable from main Window results
        self.EmpID = self.results2[self.cellrow][8]

        # Populate the Employee department
        self.EmployeeDep = self.results2[self.cellrow][11]

    def queryShiftandEmployeeTbl(self):

        self.fetched = DB.Querydb('''
                SELECT EmployeeID, Employee_TBL.Name, `Date`, StartAM, FinAM, BrkAM, 
                StartPM, FinPM, BrkPM, shiftTypeAM, shiftTypePM, shiftsID, Employee_TBL.departmentID, DepAM, DepPM
                FROM`shifts`
                INNER JOIN `Employee_TBL`on shifts.EmployeeID = idEmployee_TBL
                WHERE Date = %s AND Employee_TBL.Name = %s
                ''', (str(self.ShiftDate), self.Name)).fetchAllRecordswithFormatting()

    def populateVariables(self):
        # Populate variables from query
        self.StAM = self.fetched[0][3]
        self.FinAM = self.fetched[0][4]
        self.BrkAM = self.fetched[0][5]
        self.StPM = self.fetched[0][6]
        self.FinPM = self.fetched[0][7]
        self.BrkPM = self.fetched[0][8]
        self.shiftTypeAM = self.fetched[0][9]
        self.shiftTypePM = self.fetched[0][10]
        self.shiftsID = self.fetched[0][11]
        self.AmDepartmentType = self.fetched[0][13]
        self.PmDepartmentType = self.fetched[0][14]

    def blankcellpopulate(self):
        self.StAM = int()
        self.FinAM = int()
        self.BrkAM = int()
        self.StPM = int()
        self.FinPM = int()
        self.BrkPM = int()
        self.shiftTypeAM = 0
        self.shiftTypePM = 0

        # [ID for (ID, shiftType) in self.shiftTypes if shiftType == self.uip.AmShiftTypeCombo.currentText()]
        # [ID for (ID, shiftType) in self.shiftTypes if shiftType == self.uip.PmShiftTypeCombo.currentText()]

    def calculateHours(self):
        # Calculate total hours
        self.TotalHours = (float(self.FinAM) + float(self.FinPM)) - \
                                (float(self.StAM) + float(self.StPM)) - (float(self.BrkAM) + float(self.BrkPM))
        self.AMHours = (float(self.FinAM)) - (float(self.StAM)) - (float(self.BrkAM))
        self.PMHours = (float(self.FinPM)) - (float(self.StPM)) - (float(self.BrkPM))

    def HolidayUsageEntitlementDailyCalc(self):

        # TODO: I need to build in a stop/warning to prevent over booking of holidays
        # TODO: Compassionate leave etc?


        salOrHourly = self.emp.empSalaryOrHourlyID(self.empID)
        AM = self.shiftTypeAM
        PM = self.shiftTypePM
        hours = self.TotalHours

        holidayCalcPercentage = 0.13

        self.days_hours = [0, 0]

        # if employee is salaried
        if salOrHourly == 0:

            # if salaried and OT selected return extra 1/13th of the hours worked
            if AM == 6:
                self.days_hours[0] += (self.AMHours * holidayCalcPercentage)

            if PM == 6:
                self.days_hours[0] += (self.PMHours * holidayCalcPercentage)

            # if salaried and holiday selected then deduct one days holiday
            if AM == 2 or PM == 2:
                self.days_hours[1] -= 1
            else:
                pass


        # FIXME: deal with the am pm calc of hours rather than total hours for the hourly paid staff in the scenario that
        # FIXME: is holiday in the AM and working in the PM
        # if employee is hourly paid
        elif salOrHourly == 1:

            # if employee is hourly paid and work or OT is selected return 1/13th of the hours worked into col 2
            if AM == 1 or PM == 1 or AM == 6 or PM == 6:
                self.days_hours[0] += hours * holidayCalcPercentage

            # if hourly and holiday selected deduct the hours worked from col 2
            if AM == 2 or PM == 2:
                self.days_hours[0] -= hours

            else:
                pass

        else:
            pass

        print ('holiday days and hours', self.days_hours)
    def buttonDectoTimeConvertion(self):
        self.StartAMConcat = self.concatT(self.StAM)
        self.FinAMConcat = self.concatT(self.FinAM)
        self.BrkAMConcat = self.concatT(self.BrkAM)
        self.StartPMConcat = self.concatT(self.StPM)
        self.FinPMConcat = self.concatT(self.FinPM)
        self.BrkPMConcat = self.concatT(self.BrkPM)

    def concatenateShiftEngine(self):
        # Concat the times and shift Type into 1 string

        # convert shiftype ID into the name of shifts
        self.shiftTypeAMName = [shiftType for (ID, shiftType) in self.shiftTypes if
                            ID == self.shiftTypeAM]
        self.shiftTypePMName = [shiftType for (ID, shiftType) in self.shiftTypes if
                            ID == self.shiftTypePM]

        # concatenate all the elements with formating for writing to the buttons
        if self.StPM == 0 and self.FinPM == 0 and self.StAM == 0 and self.FinAM == 0:
            self.ConcatShift = ""
        elif self.StAM == 0 and self.FinAM == 0:
            self.ConcatShift = '.' + (' ' * 20) + '  |  ' + str(self.StartPMConcat) + "-" + str(self.FinPMConcat) \
                               + "\n" + (' ' * 27) + str(self.shiftTypePMName[0])
        elif self.StPM == 0 and self.FinPM == 0:
            self.ConcatShift = str(self.StartAMConcat) + "-" + str(self.FinAMConcat) + "  |  " + (' ' * 20) + '.' \
                               + "\n" + str(self.shiftTypeAMName[0]) + (' ' * (35 - len(self.shiftTypeAMName[0])))
        else:
            self.ConcatShift = str(self.StartAMConcat) + "-" + str(self.FinAMConcat) + "  |  " + \
                            str(self.StartPMConcat) + "-" + str(self.FinPMConcat) \
                               + "\n" + str(self.shiftTypeAMName[0]) + \
                               (' ' * (27 - len(self.shiftTypeAMName[0]) - len(self.shiftTypePMName[0])))\
                               + str(self.shiftTypePMName[0])

    def writeTimetoButton(self):
        # Set button labels to relevant times
        self.uip.StAMBUT.setText(self.StartAMConcat)
        self.uip.FinAMBUT.setText(self.FinAMConcat)
        self.uip.BrkAMBUT.setText(self.BrkAMConcat)
        self.uip.StPMBUT.setText(self.StartPMConcat)
        self.uip.FinPMBUT.setText(self.FinPMConcat)
        self.uip.BrkPMBUT.setText(self.BrkPMConcat)

    def setSelectedIteminShiftTypeDropDownBox(self):
        StTypeAM = [shiftType for (ID, shiftType) in self.shiftTypes if ID == self.shiftTypeAM]
        comboAM = self.uip.AmShiftTypeCombo
        index = comboAM.findText(StTypeAM[0])
        if index >= 0:
            comboAM.setCurrentIndex(index)
        else:
            pass

        StTypePM = [shiftType for (ID, shiftType) in self.shiftTypes if ID == self.shiftTypePM]
        comboPM = self.uip.PmShiftTypeCombo
        index = comboPM.findText(StTypePM[0])
        if index >= 0:
            comboPM.setCurrentIndex(index)
        else:
            pass

    def concatT(self, time):
        hours = int(time)
        mins = (time * 60) % 60
        return "%02d:%02d" % (hours, mins)

    def timePadPopUp(self):
        self.senderBUT = self.sender().objectName()
        self.pad = TimePadPopUp.TimePadPopUp(self.StAM, self.FinAM, self.BrkAM, self.StPM, self.FinPM, self.BrkPM)
        self.pad.show()
        self.pad.uip.setBut.clicked.connect(self.timePadSetBUTClicked)

    def timePadSetBUTClicked(self):
        # use Button clicked sender information to assign info to relevant variable from Time pad
        if str(self.senderBUT[0:-3]) == "StAM":
            self.StAM = TimePadPopUp.TimePadPopUp.a
        elif str(self.senderBUT[0:-3]) == "FinAM":
            self.FinAM = TimePadPopUp.TimePadPopUp.a
        elif str(self.senderBUT[0:-3]) == "BrkAM":
            self.BrkAM = TimePadPopUp.TimePadPopUp.a
        elif str(self.senderBUT[0:-3]) == "StPM":
            self.StPM = TimePadPopUp.TimePadPopUp.a
        elif str(self.senderBUT[0:-3]) == "FinPM":
            self.FinPM = TimePadPopUp.TimePadPopUp.a
        elif str(self.senderBUT[0:-3]) == "BrkPM":
            self.BrkPM = TimePadPopUp.TimePadPopUp.a

        self.buttonDectoTimeConvertion()

        self.concatenateShiftEngine()

        self.writeTimetoButton()

        self.calculateHours()

        self.pad.close()

    def updateShiftTypeVariables(self):
        self.shiftTypeAM = [ID for (ID, shiftType) in self.shiftTypes if shiftType == self.uip.AmShiftTypeCombo.currentText()][0]
        self.shiftTypePM = [ID for (ID, shiftType) in self.shiftTypes if shiftType == self.uip.PmShiftTypeCombo.currentText()][0]

    def updateDepTypeVariables(self):
        self.AmDepartmentType = [ID for (ID, DepType) in self.departments if DepType == self.uip.DepAMCombo.currentText()][0]
        self.PmDepartmentType = [ID for (ID, DepType) in self.departments if DepType == self.uip.DepPMCombo.currentText()][0]

    def setOrUpdatetheDB(self):
        # Determine if the info for the DB is an update or a new record

        # update the variables for shift types
        self.updateShiftTypeVariables()
        self.concatenateShiftEngine()

        # Calc the holiday columns
        self.HolidayUsageEntitlementDailyCalc()

        if self.StAM == 0 and self.FinAM == 0 and self.StPM == 0 and self.FinPM == 0:
            pass
        else:
            if self.shiftsID == int():
                self.insertNewShiftintoDB()
            else:
                self.updateRecordinDB()

    def updateRecordinDB(self):
        DB.Querydb('''
                  UPDATE shifts
                  SET StartAM = %s, 
                  FinAM = %s, 
                  BrkAM = %s, 
                  StartPM = %s, 
                  FinPM = %s, 
                  BrkPM = %s, 
                  ConcatShift = %s, 
                  TotalHours = %s,
                  shiftTypeAM = %s,
                  shiftTypePM = %s,
                  DepAM = %s,
                  DepPM = %s,
                  HolidayHours = %s,
                  HolidayDays = %s
                  WHERE shiftsID = %s;
                        ''', (self.StAM, self.FinAM, self.BrkAM,
                              self.StPM, self.FinPM, self.BrkPM, self.ConcatShift, self.TotalHours,
                              self.shiftTypeAM, self.shiftTypePM, self.AmDepartmentType,
                              self.PmDepartmentType, self.days_hours[0], self.days_hours[1], self.shiftsID)).InsertOneExecutewithFormatting()
        self.close()

    def insertNewShiftintoDB(self):
        # Writing new shift records to the DB
        DB.Querydb('''
                INSERT INTO shifts (EmployeeID, Date, StartAM, FinAM, BrkAM, StartPM, FinPM, BrkPM, 
                ConcatShift, TotalHours, shiftTypeAM, shiftTypePM, EmployeeDep, DepAM, DepPM, HolidayHours, HolidayDays)
                VALUE (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
                        ''', (self.EmpID, str(self.ShiftDate), self.StAM, self.FinAM, self.BrkAM, self.StPM,
                              self.FinPM, self.BrkPM, self.ConcatShift, self.TotalHours, self.shiftTypeAM, self.shiftTypePM,
                              self.EmployeeDep, self.AmDepartmentType, self.PmDepartmentType, self.days_hours[0],
                              self.days_hours[1])).InsertOneExecutewithFormatting()
        self.close()

    def emitTrigger(self):
        self.trigger.emit()

    def buttonPressed(self):
       self.timepressed = time.time()

    def buttonReleased(self):
        self.timereleased = time.time()

    def setOrClickCustomShiftButton(self):
        self.senderAutoShiftBUT = self.sender().objectName()
        a = self.timereleased - self.timepressed
        if a > 1:
            # update the shift type variables
            self.updateShiftTypeVariables()
            self.concatenateShiftEngine()


            DB.Querydb('''UPDATE AutoShiftTimes
                        SET StAM = %s,
                        FinAM = %s,
                        BrkAM = %s,
                        StPM = %s,
                        FinPM = %s,
                        BrkPM = %s,
                        ConcatShift = %s,
                        AMShiftType = %s,
                        PMShiftType = %s
                        WHERE ButtonReference = %s;
                        ''', (self.StAM, self.FinAM, self.BrkAM, self.StPM, self.FinPM,
                              self.BrkPM, self.ConcatShift, self.shiftTypeAM, self.shiftTypePM, self.senderAutoShiftBUT)).InsertOneExecutewithFormatting()
            if self.sender().objectName() == "GenBut1":
                self.uip.GenBut1.setText(self.ConcatShift)
            elif self.sender().objectName() == "GenBut2":
                self.uip.GenBut2.setText(self.ConcatShift)
            elif self.sender().objectName() == "GenBut3":
                self.uip.GenBut3.setText(self.ConcatShift)
            elif self.sender().objectName() == "GenBut4":
                self.uip.GenBut4.setText(self.ConcatShift)
            elif self.sender().objectName() == "GenBut5":
                self.uip.GenBut5.setText(self.ConcatShift)
            elif self.sender().objectName() == "GenBut6":
                self.uip.GenBut6.setText(self.ConcatShift)
            elif self.sender().objectName() == "GenBut7":
                self.uip.GenBut7.setText(self.ConcatShift)

            elif self.sender().objectName() == "FOHBut1":
                self.uip.FOHBut1.setText(self.ConcatShift)
            elif self.sender().objectName() == "FOHBut2":
                self.uip.FOHBut2.setText(self.ConcatShift)
            elif self.sender().objectName() == "FOHBut3":
                self.uip.FOHBut3.setText(self.ConcatShift)
            elif self.sender().objectName() == "FOHBut4":
                self.uip.FOHBut4.setText(self.ConcatShift)
            elif self.sender().objectName() == "FOHBut5":
                self.uip.FOHBut5.setText(self.ConcatShift)
            elif self.sender().objectName() == "FOHBut6":
                self.uip.FOHBut6.setText(self.ConcatShift)
            elif self.sender().objectName() == "FOHBut7":
                self.uip.FOHBut7.setText(self.ConcatShift)

            elif self.sender().objectName() == "KitBut1":
                self.uip.KitBut1.setText(self.ConcatShift)
            elif self.sender().objectName() == "KitBut2":
                self.uip.KitBut2.setText(self.ConcatShift)
            elif self.sender().objectName() == "KitBut3":
                self.uip.KitBut3.setText(self.ConcatShift)
            elif self.sender().objectName() == "KitBut4":
                self.uip.KitBut4.setText(self.ConcatShift)
            elif self.sender().objectName() == "KitBut5":
                self.uip.KitBut5.setText(self.ConcatShift)
            elif self.sender().objectName() == "KitBut6":
                self.uip.KitBut6.setText(self.ConcatShift)
            elif self.sender().objectName() == "KitBut7":
                self.uip.KitBut7.setText(self.ConcatShift)

            elif self.sender().objectName() == "AdminBut1":
                self.uip.AdminBut1.setText(self.ConcatShift)
            elif self.sender().objectName() == "AdminBut2":
                self.uip.AdminBut2.setText(self.ConcatShift)
            elif self.sender().objectName() == "AdminBut3":
                self.uip.AdminBut3.setText(self.ConcatShift)
            elif self.sender().objectName() == "AdminBut4":
                self.uip.AdminBut4.setText(self.ConcatShift)
            elif self.sender().objectName() == "AdminBut5":
                self.uip.AdminBut5.setText(self.ConcatShift)
            elif self.sender().objectName() == "AdminBut6":
                self.uip.AdminBut6.setText(self.ConcatShift)
            elif self.sender().objectName() == "AdminBut7":
                self.uip.AdminBut7.setText(self.ConcatShift)
            self.retrieveAutoShiftTimes()

        else:
            self.StAM = self.autoButtons[str(self.senderAutoShiftBUT)][1]
            self.FinAM = self.autoButtons[str(self.senderAutoShiftBUT)][2]
            self.BrkAM = self.autoButtons[str(self.senderAutoShiftBUT)][3]
            self.StPM = self.autoButtons[str(self.senderAutoShiftBUT)][4]
            self.FinPM = self.autoButtons[str(self.senderAutoShiftBUT)][5]
            self.BrkPM = self.autoButtons[str(self.senderAutoShiftBUT)][6]
            self.shiftTypeAM = self.autoButtons[str(self.senderAutoShiftBUT)][7]
            self.shiftTypePM = self.autoButtons[str(self.senderAutoShiftBUT)][8]

            self.calculateHours()
            self.buttonDectoTimeConvertion()
            self.concatenateShiftEngine()
            self.writeTimetoButton()
            self.setSelectedIteminShiftTypeDropDownBox()




