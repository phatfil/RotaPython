#!/usr/bin/python

from PyQt4 import QtGui, QtCore
from EmployeeinfoEntry import Ui_Employee, _translate
import datetime
import Employees
import DB
import WidgetTools
from PyQt4.QtCore import pyqtSignal

class EmployeePopUp(QtGui.QDialog):
    trigger = pyqtSignal()

    def __init__(self, fromDate, toDate, parent=None):
        super(EmployeePopUp, self).__init__(parent)

        self.uie = Ui_Employee()
        self.uie.setupUi(self)

        # disable add emp save and cancel buttons
        self.uie.EmployeeListSaveButt.setDisabled(1)
        self.uie.EmployeeListSaveCancelButt.setDisabled(1)

        # set focus to first tab
        self.uie.tabWidget.setCurrentIndex(0)

        # instant Variables
        self.fromDate = fromDate
        self.toDate = toDate
        self.currentID = None
        self.IDtoReturnto = None

        # first load
        self.defineTriggers()
        self.queryDB_reloadEmpModule()
        self.populateInstantVariablesWithDBData()
        self.populateNameListWidget()
        self.PopulateComboLists()
        self.populateWidgets_NotNameList()

    def defineTriggers(self):
        # define triggers
        self.uie.EmployeeListTable.currentCellChanged.connect(self.updateEmpDataToDB)
        self.uie.EmployeeListTable.currentCellChanged.connect(self.queryDB_reloadEmpModule)
        self.uie.EmployeeListTable.currentCellChanged.connect(self.getIDfromcurrentrow)
        self.uie.EmployeeListTable.currentCellChanged.connect(self.selectedEmpVariableUpdate)
        self.uie.EmployeeListTable.currentCellChanged.connect(self.populateWidgets_NotNameList)


        self.uie.UpdateEmpRecordBUT.clicked.connect(self.updateButtonclicked)

        self.uie.closeEmployeePopUpBUT.clicked.connect(self.emitTrigger)
        self.uie.empDOBbox.dateChanged.connect(self.calculateAge)

        self.uie.EmployeeListAddButt.clicked.connect(self.clearFormandSwitchtoAddEmpFormConfig)
        self.uie.EmployeeListSaveButt.clicked.connect(self.addEmployeeAction)
        self.uie.EmployeeListSaveCancelButt.clicked.connect(self.cancelAddEmployeeAction)
        self.uie.EmployeeListDelButt.clicked.connect(self.deleteEmployeeAction)

        self.uie.SalaryAddButt.clicked.connect(self.addSalary)
        self.uie.SalaryDelButt.clicked.connect(self.delSalary)
        self.uie.SalaryUpdateBUT.clicked.connect(self.updateSalary)

        self.uie.BonusAddButt.clicked.connect(self.addBonus)
        self.uie.BonusDelButt.clicked.connect(self.delBonus)
        self.uie.BonusUpdateBUT.clicked.connect(self.updateBonus)

        self.uie.holidayEntitlementAddBUT.clicked.connect(self.addHolidayEnt)
        self.uie.holidayEntitlementDelBUT.clicked.connect(self.delHolidayEnt)
        self.uie.HolidayUpdateBUT.clicked.connect(self.updateHolEntitlement)

    def updateButtonclicked(self):
        self.updateEmpDataToDB()
        self.setReturntoID()
        self.populateInstantVariablesWithDBData()
        self.populateNameListWidget()
        self.populateWidgets_NotNameList()

    def queryDB_reloadEmpModule(self):
        self.empTable = DB.Querydb("""SELECT * FROM Employee_TBL""", None).fetchAllRecordswithFormatting()
        self.salTable = DB.Querydb("""SELECT * FROM Salary""", None).fetchAllRecordswithFormatting()
        self.depTable = DB.Querydb("""SELECT * FROM departments""", None).fetchAllRecordswithFormatting()
        self.bonusTable = DB.Querydb("""SELECT * FROM Bonus""", None).fetchAllRecordswithFormatting()
        self.holsTable = DB.Querydb("""SELECT * FROM HolidayEntitlement""", None).fetchAllRecordswithFormatting()
        self.salorHourlyTable = DB.Querydb("""SELECT * FROM salorHourlyTable""", None).fetchAllRecordswithFormatting()
        self.emp = Employees.employees(self.empTable, self.salTable, self.depTable, self.bonusTable, self.holsTable,
                                       self.salorHourlyTable)

    def populateInstantVariablesWithDBData(self):
        self.updateNameListVariablewithCurrentDBData()

        # if first load or emp listOfEmployees is empty, otherwise return to emp selected before refresh
        if self.IDtoReturnto is None:
            self.currentID = None if self.listOfEmployees == [] else self.listOfEmployees[0][0]
        else:
            self.currentID = self.IDtoReturnto

        self.currentName = self.emp.empName(self.currentID)
        self.currentDOB = self.emp.empDOB(self.currentID)
        self.currentDepartmentID = self.emp.empDepID(self.currentID)
        self.currentSalorHourlyID = self.emp.empSalaryOrHourlyID(self.currentID)
        self.currentAdrs = self.emp.empAdrs(self.currentID)
        self.currentEmail = self.emp.empEmail(self.currentID)
        self.currentHome = self.emp.empHphone(self.currentID)
        self.currentMobile = self.emp.empMphone(self.currentID)
        self.currentStDate = self.emp.empStartDate(self.currentID)

    def populateWidgets_NotNameList(self):
        # populate employee data
        if self.currentID is None:
            self.calculateAge()
            self.populateSalaryTable()
            self.populateBonusTable()
            self.populateHolidayTable()

        else:
            self.uie.empNameBox.setText(self.emp.empName(self.currentID))
            self.uie.empDOBbox.setDate(self.emp.empDOB(self.currentID))
            self.uie.empAgeBox.setValue(self.emp.empAge(self.currentID, datetime.date.today()))
            self.uie.adrsBox.setText(self.emp.empAdrs(self.currentID))
            self.uie.emailBox.setText(self.emp.empEmail(self.currentID))
            self.uie.mobileBox.setText(self.emp.empMphone(self.currentID))
            self.uie.homeBox.setText(self.emp.empHphone(self.currentID))
            self.uie.empStDateBox.setDate(self.emp.empStartDate(self.currentID))
            self.calculateAge()
            self.populateSalaryTable()
            self.populateBonusTable()
            self.populateHolidayTable()
            self.setDepCombo()
            self.setSalCombo()

    def updateNameListVariablewithCurrentDBData(self):
        self.queryDB_reloadEmpModule()
        if self.emp.NameListEmpList(self.fromDate, self.toDate) is None:
            self.listOfEmployees = []
        else:
            self.listOfEmployees = self.emp.NameListEmpList(self.fromDate, self.toDate)

    def selectedEmpVariableUpdate(self):
        self.currentName = self.emp.empName(self.currentID)
        self.currentDOB = self.emp.empDOB(self.currentID)
        self.currentDepartmentID = self.emp.empDepID(self.currentID)
        self.currentSalorHourlyID = self.emp.empSalaryOrHourlyID(self.currentID)
        self.currentAdrs = self.emp.empAdrs(self.currentID)
        self.currentEmail = self.emp.empEmail(self.currentID)
        self.currentHome = self.emp.empHphone(self.currentID)
        self.currentMobile = self.emp.empMphone(self.currentID)
        self.currentStDate = self.emp.empStartDate(self.currentID)

    def clearFormandSwitchtoAddEmpFormConfig(self):
        self.clearForm()

        # enable save and cancel buttons
        self.uie.EmployeeListSaveButt.setDisabled(0)
        self.uie.EmployeeListSaveCancelButt.setDisabled(0)

        # Disable all areas of the form that are no needed for adding new employees
        self.uie.UpdateEmpRecordBUT.setDisabled(1)
        self.uie.EmployeeListAddButt.setDisabled(1)
        self.uie.EmployeeListDelButt.setDisabled(1)
        self.uie.EmployeeListTable.setDisabled(1)
        self.uie.payrollInformationTab.setDisabled(1)
        self.uie.HolidayTab.setDisabled(1)

        # shift focus to emp info tab
        self.uie.tabWidget.setCurrentIndex(0)

    def clearTables(self):
        self.uie.salaryTable.clearContents()
        self.uie.bonusTable.clearContents()
        self.uie.EmployeeListTable.clearContents()
        self.uie.holidayEntitlementTable.clearContents()

    def addEmployeeAction(self):
        empName = self.uie.empNameBox.text()
        DOB = QtCore.QDate.toPyDate(self.uie.empDOBbox.date())
        department = [ID for ID, depType in self.depTable if depType == self.uie.empDepCombo.currentText()][0]
        salorHourlyID = [ID for ID, sal in self.salorHourlyTable if sal == self.uie.empSalCombo.currentText()][0]
        adrs = self.uie.adrsBox.toPlainText()
        email = self.uie.emailBox.text()
        home = self.uie.homeBox.text()
        mobile = self.uie.mobileBox.text()
        StDate = QtCore.QDate.toPyDate(self.uie.empStDateBox.date())
        FinDate = None

        listCompiled = [name.upper() for ID, name in self.listOfEmployees]
        if str(empName).upper() in listCompiled:
            QtGui.QMessageBox.warning(QtGui.QMessageBox(), 'Warning', "Name Already Exists!", "")
            pass
        else:
            DB.Querydb('''INSERT INTO Employee_TBL 
            (Name, 
            DOB, 
            departmentID, 
            SalOrHourly, 
            Address, 
            Email, 
            HomePhone,
            MobilePhone, 
            EmpStDate, 
            EmpFinDate) VALUE (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s );''',
                       (empName, DOB, department, salorHourlyID, adrs, email, home,
                        mobile, StDate, FinDate)).InsertOneExecutewithFormatting()

            empID = DB.Querydb("""SELECT idEmployee_TBL FROM Employee_TBL WHERE Name = %s""", (empName, )).fetchAllRecordswithFormatting()

            # disable save and cancel buttons
            self.uie.EmployeeListSaveButt.setDisabled(1)
            self.uie.EmployeeListSaveCancelButt.setDisabled(1)

            # Enable all areas of the form
            self.uie.UpdateEmpRecordBUT.setDisabled(0)
            self.uie.EmployeeListAddButt.setDisabled(0)
            self.uie.EmployeeListDelButt.setDisabled(0)
            self.uie.EmployeeListTable.setDisabled(0)
            self.uie.payrollInformationTab.setDisabled(0)
            self.uie.HolidayTab.setDisabled(0)

            # reload form
            self.queryDB_reloadEmpModule()
            self.IDtoReturnto = empID[0][0]
            self.populateInstantVariablesWithDBData()
            self.populateNameListWidget()

    def cancelAddEmployeeAction(self):
        # disable save and cancel buttons
        self.uie.EmployeeListSaveButt.setDisabled(1)
        self.uie.EmployeeListSaveCancelButt.setDisabled(1)

        # Enable all areas of the form
        self.uie.UpdateEmpRecordBUT.setDisabled(0)
        self.uie.EmployeeListAddButt.setDisabled(0)
        self.uie.EmployeeListDelButt.setDisabled(0)
        self.uie.EmployeeListTable.setDisabled(0)
        self.uie.payrollInformationTab.setDisabled(0)
        self.uie.HolidayTab.setDisabled(0)
        self.queryDB_reloadEmpModule()
        self.selectedEmpVariableUpdate()
        self.populateWidgets_NotNameList()

    def deleteEmployeeAction(self):
        message = QtGui.QMessageBox.question(QtGui.QMessageBox(), 'Warning', "Do you Really Want to Delete {} - This can not be un-done! All Rota data will be lost"
                                             .format(self.currentName), QtGui.QMessageBox.Yes | QtGui.QMessageBox.No,
                                             QtGui.QMessageBox.No)
        if message == QtGui.QMessageBox.Yes:
            DB.Querydb("""DELETE FROM Employee_TBL WHERE idEmployee_TBL = %s""",
                       (self.currentID,)).DeleteOneExecutewithFormatting()
            self.updateNameListVariablewithCurrentDBData()
            if self.listOfEmployees == []:
                self.currentID = None
                self.clearForm()
                self.clearTables()

            else:
                self.currentID = self.listOfEmployees[0][0]
                self.populateWidgets_NotNameList()
                self.populateNameListWidget()
        else:
            pass

    def getIDfromcurrentrow(self):
        try:
            self.IDtoReturnto = None
            row = self.uie.EmployeeListTable.currentRow()
            self.currentID = int(self.uie.EmployeeListTable.item(row, 0).text())
        except StandardError:
            print('Please select an employee from the listOfEmployees')

    def updateEmpDataToDB(self):
        name = self.uie.empNameBox.text()
        DOB = QtCore.QDate.toPyDate(self.uie.empDOBbox.date())
        departmentID = [ID for ID, depType in self.depTable if depType == self.uie.empDepCombo.currentText()][0]
        salorHourlyID = [ID for ID, sal in self.salorHourlyTable if sal == self.uie.empSalCombo.currentText()][0]
        adrs = self.uie.adrsBox.toPlainText()
        email = self.uie.emailBox.text()
        home = self.uie.homeBox.text()
        mobile = self.uie.mobileBox.text()
        StDate = QtCore.QDate.toPyDate(self.uie.empStDateBox.date())

        DB.Querydb('''UPDATE Employee_TBL
                             SET  Name = %s, 
                             DOB = %s, 
                             departmentID = %s, 
                             SalOrHourly = %s, 
                             Address = %s, 
                             Email = %s, 
                             HomePhone = %s, 
                             MobilePhone = %s, 
                             EmpStDate = %s
                             WHERE idEmployee_TBL = %s;''',
                   (name, DOB, departmentID, salorHourlyID,
                    adrs, email, home, mobile,
                    StDate, self.currentID)).InsertOneExecutewithFormatting()

    def setReturntoID(self):
        self.IDtoReturnto = self.currentID

    def populateNameListWidget(self):
        self.emplist = WidgetTools.TableWidgetTools()
        self.emplist.setWidget(self.uie.EmployeeListTable)
        self.emplist.populateTableWidget(self.listOfEmployees, 2, 0)

    def populateDepComboBoxList(self):
        self.depCombo = WidgetTools.comboBoxTools(self.uie.empDepCombo)
        self.depCombo.populateComboBoxList(self.depTable, 1)

    def setDepCombo(self):
        # set selection to employees department
        emp = Employees.employees(self.empTable, self.salTable, self.depTable, self.bonusTable, self.holsTable, self.salorHourlyTable)
        self.depCombo.setComboToSearchedItem(emp.empDepName(self.currentID))

    def populateSalComboBoxList(self):
        self.salCombo = WidgetTools.comboBoxTools(self.uie.empSalCombo)
        self.salCombo.populateComboBoxList(self.salorHourlyTable, 1)

    def setSalCombo(self):
        # set selection to employees department
        emp = Employees.employees(self.empTable, self.salTable, self.depTable, self.bonusTable, self.holsTable, self.salorHourlyTable)
        self.salCombo.setComboToSearchedItem(emp.empSalaryOrHourlyName(self.currentID))

    def calculateAge(self):
        today = datetime.datetime.today()
        dob = datetime.datetime.strptime(str(QtCore.QDate.toPyDate(self.uie.empDOBbox.date())), '%Y-%m-%d')
        age = float((today - dob).days) / 365
        self.uie.empAgeBox.setValue(age)

    def populateSalaryTable(self):
        # populate salarytableWidget
        emp = Employees.employees(self.empTable, self.salTable, self.depTable, self.bonusTable, self.holsTable,
                                  self.salorHourlyTable)

        if emp.empSalaries(self.currentID) is None:
            self.salaryTableWidget = WidgetTools.TableWidgetTools()
            self.salaryTableWidget.setWidget(self.uie.salaryTable)
            self.salaryTableWidget.hideColumn(0)
            self.salaryTableWidget.changeHeaderTitle(1, "Salary")
            self.salaryTableWidget.changeHeaderTitle(2, "Hourly")
            self.salaryTableWidget.changeHeaderTitle(3, "Adjust Date")
            self.salaryTableWidget.setColumnWidth(1, 92)
            self.salaryTableWidget.setColumnWidth(2, 92)
            self.salaryTableWidget.setColumnWidth(3, 110)
        else:
            self.salaryTableWidget = WidgetTools.TableWidgetTools()
            self.salaryTableWidget.setWidget(self.uie.salaryTable)
            self.salaryTableWidget.populateTableWidget_IfDateTimeThenCalElseDspinBox(emp.empSalaries(self.currentID), 4, 0)
            self.salaryTableWidget.changeHeaderTitle(1, "Salary")
            self.salaryTableWidget.changeHeaderTitle(2, "Hourly")
            self.salaryTableWidget.changeHeaderTitle(3, "Adjust Date")
            self.salaryTableWidget.setColumnWidth(1, 92)
            self.salaryTableWidget.setColumnWidth(2, 92)
            self.salaryTableWidget.setColumnWidth(3, 110)

    def addSalary(self):
        DB.Querydb('''INSERT INTO Salary(EmployeeID, PoundsPerHour, Salary, AdjustDate) VALUE (%s, %s, %s, %s);''',
                   (self.currentID, 0, 0, datetime.date.today())).InsertOneExecutewithFormatting()

        # Reload salary table
        self.queryDB_reloadEmpModule()
        self.setReturntoID()
        self.populateInstantVariablesWithDBData()
        self.populateSalaryTable()

    def delSalary(self):
        ID = self.salaryTableWidget.IDfromSelectedRow()
        if ID is None:
            pass
        else:
            message = QtGui.QMessageBox.question(QtGui.QMessageBox(), 'Warning',
                                                 "Do you Really Want to Delete, This can not be un-done!"
                                                 , QtGui.QMessageBox.Yes | QtGui.QMessageBox.No,
                                                 QtGui.QMessageBox.No)
            if message == QtGui.QMessageBox.Yes:
                DB.Querydb("""DELETE FROM Salary WHERE SalaryID = %s""",
                           (ID,)).DeleteOneExecutewithFormatting()
                self.queryDB_reloadEmpModule()
                self.setReturntoID()
                self.populateInstantVariablesWithDBData()
                self.populateSalaryTable()
            else:
                pass

    def updateSalary(self):
        data = self.salaryTableWidget.rowExtractfromWidget()
        empID = self.currentID
        converted = []

        for a in range(len(data)):
            converted.append([empID, data[a][1], data[a][2], data[a][3], data[a][0]])

        DB.Querydb('''UPDATE Salary SET EmployeeID = %s, Salary = %s, PoundsPerHour = %s, AdjustDate = %s WHERE SalaryID = %s''',
                   converted).InsertManyExecutewithFormatting()
        self.queryDB_reloadEmpModule()
        self.updateButtonclicked()

    def populateBonusTable(self):
        # populate bonusTableWidget
        emp = Employees.employees(self.empTable, self.salTable, self.depTable, self.bonusTable, self.holsTable,
                                  self.salorHourlyTable)
        if emp.empBonuses(self.currentID) is None:
            self.bonusTableWidget = WidgetTools.TableWidgetTools()
            self.bonusTableWidget.setWidget(self.uie.bonusTable)
            self.bonusTableWidget.hideColumn(0)
            self.bonusTableWidget.changeHeaderTitle(1, 'Bonus')
            self.bonusTableWidget.changeHeaderTitle(2, 'Period St Date')
            self.bonusTableWidget.changeHeaderTitle(3, 'Pay Date')
            self.bonusTableWidget.setColumnWidth(1, 74)
            self.bonusTableWidget.setColumnWidth(2, 110)
            self.bonusTableWidget.setColumnWidth(3, 110)
        else:
            self.bonusTableWidget = WidgetTools.TableWidgetTools()
            self.bonusTableWidget.setWidget(self.uie.bonusTable)
            self.bonusTableWidget.populateTableWidget_IfDateTimeThenCalElseDspinBox(emp.empBonuses(self.currentID), 4, 0)
            self.bonusTableWidget.changeHeaderTitle(1, 'Bonus')
            self.bonusTableWidget.changeHeaderTitle(2, 'Period St Date')
            self.bonusTableWidget.changeHeaderTitle(3, 'Pay Date')
            self.bonusTableWidget.setColumnWidth(1, 74)
            self.bonusTableWidget.setColumnWidth(2, 110)
            self.bonusTableWidget.setColumnWidth(3, 110)

    def addBonus(self):
        DB.Querydb('''INSERT INTO Bonus(bonus, EmployeeID, bonusPayDate, BonusPeriodStDate) VALUE (%s, %s, %s, %s);''',
                   (0, self.currentID, datetime.date.today(), datetime.date.today())).InsertOneExecutewithFormatting()

        # Reload salary table
        self.queryDB_reloadEmpModule()
        self.setReturntoID()
        self.populateInstantVariablesWithDBData()
        self.populateBonusTable()

    def delBonus(self):
        ID = self.bonusTableWidget.IDfromSelectedRow()
        if ID is None:
            pass
        else:
            message = QtGui.QMessageBox.question(QtGui.QMessageBox(), 'Warning',
                                                 "Do you Really Want to Delete, This can not be un-done!"
                                                 , QtGui.QMessageBox.Yes | QtGui.QMessageBox.No,
                                                 QtGui.QMessageBox.No)
            if message == QtGui.QMessageBox.Yes:
                DB.Querydb("""DELETE FROM Bonus WHERE bonusID = %s""",
                           (ID,)).DeleteOneExecutewithFormatting()
                self.queryDB_reloadEmpModule()
                self.setReturntoID()
                self.populateInstantVariablesWithDBData()
                self.populateBonusTable()
            else:
                pass

    def updateBonus(self):
        data = self.bonusTableWidget.rowExtractfromWidget()
        empID = self.currentID
        converted = []

        for a in range(len(data)):
            converted.append([data[a][1], empID, data[a][2], data[a][3], data[a][0]])

        DB.Querydb('''UPDATE Bonus SET bonus = %s, EmployeeID = %s, BonusPeriodStDate = %s, bonusPayDate = %s  WHERE bonusID = %s''',
                   converted).InsertManyExecutewithFormatting()
        self.queryDB_reloadEmpModule()
        self.updateButtonclicked()

    def populateHolidayTable(self):
        # populate Holiday Entitlement table
        emp = Employees.employees(self.empTable, self.salTable, self.depTable, self.bonusTable, self.holsTable,
                                  self.salorHourlyTable)
        if emp.empHolidayEntitlements(self.currentID) is None:
            self.holsTableWidget = WidgetTools.TableWidgetTools()
            self.holsTableWidget.setWidget(self.uie.holidayEntitlementTable)
            self.holsTableWidget.hideColumn(0)
            self.holsTableWidget.changeHeaderTitle(1, 'Entitlement')
            self.holsTableWidget.changeHeaderTitle(2, 'Adjust Date')
            self.holsTableWidget.setColumnWidth(1, 74)
            self.holsTableWidget.setColumnWidth(2, 110)
        else:
            self.holsTableWidget = WidgetTools.TableWidgetTools()
            self.holsTableWidget.setWidget(self.uie.holidayEntitlementTable)
            self.holsTableWidget.populateTableWidget_IfDateTimeThenCalElseDspinBox(emp.empHolidayEntitlements(self.currentID), 3, 0)
            self.holsTableWidget.changeHeaderTitle(1, 'Entitlement')
            self.holsTableWidget.changeHeaderTitle(2, 'Adjust Date')
            self.holsTableWidget.setColumnWidth(1, 74)
            self.holsTableWidget.setColumnWidth(2, 110)

    def addHolidayEnt(self):
        DB.Querydb('''INSERT INTO HolidayEntitlement(empID, entitledDaysFY, adjustDate) VALUE (%s, %s, %s);''',
                   (self.currentID, 0, datetime.date.today())).InsertOneExecutewithFormatting()

        # Reload salary table
        self.queryDB_reloadEmpModule()
        self.setReturntoID()
        self.populateInstantVariablesWithDBData()
        self.populateHolidayTable()
        self.setReturntoID()

    def delHolidayEnt(self):
        ID = self.holsTableWidget.IDfromSelectedRow()
        if ID is None:
            pass
        else:
            message = QtGui.QMessageBox.question(QtGui.QMessageBox(), 'Warning',
                                                 "Do you Really Want to Delete, This can not be un-done!"
                                                 , QtGui.QMessageBox.Yes | QtGui.QMessageBox.No,
                                                 QtGui.QMessageBox.No)
            if message == QtGui.QMessageBox.Yes:
                DB.Querydb("""DELETE FROM HolidayEntitlement WHERE entitlementID = %s""",
                           (ID,)).DeleteOneExecutewithFormatting()
                self.queryDB_reloadEmpModule()
                self.setReturntoID()
                self.populateInstantVariablesWithDBData()
                self.populateHolidayTable()
            else:
                pass

    def updateHolEntitlement(self):
        data = self.holsTableWidget.rowExtractfromWidget()
        empID = self.currentID
        converted = []

        for a in range(len(data)):
            converted.append([empID, data[a][1], data[a][2], data[a][0]])

        DB.Querydb('''UPDATE HolidayEntitlement SET empID = %s, entitledDaysFY = %s, adjustDate = %s WHERE entitlementID = %s''',
                   converted).InsertManyExecutewithFormatting()
        self.queryDB_reloadEmpModule()
        self.updateButtonclicked()

    def PopulateComboLists(self):
        self.populateDepComboBoxList()
        self.populateSalComboBoxList()

    def clearForm(self):
        self.uie.empNameBox.setText("")
        self.uie.empDOBbox.setDate(QtCore.QDate.fromString('1980-01-01', 'yyyy-M-d'))
        self.uie.empDepCombo.setCurrentIndex(0)
        self.uie.empSalCombo.setCurrentIndex(0)
        self.uie.adrsBox.setText("")
        self.uie.emailBox.setText("")
        self.uie.homeBox.setText("")
        self.uie.mobileBox.setText("")
        self.uie.empStDateBox.setDate(QtCore.QDate.currentDate())
        self.salTable = []
        self.bonusTable = []
        self.holsTable = []
        self.populateSalaryTable()
        self.populateBonusTable()
        self.populateHolidayTable()

    def emitTrigger(self):
        self.trigger.emit()
        self.close()

