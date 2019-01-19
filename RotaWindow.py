#!/usr/bin/python2.7
import datetime
import sys
from PyQt4 import QtGui, QtCore
from dateutil.relativedelta import *
from decimal import Decimal
import calendar
import time


import ActualRevWindow
import AddEmployeeWindow
import DB
import EmployeePopUp
import LogMeIn
import Printing
import RotaData
import ShiftPopUp
import WidgetTools
import payrollVariablePopUP
import reporting
from Rotav7 import Ui_MainWindow
from loginwindow import Ui_LoginWindow

import pyximport; pyximport.install()
from Employees import employees


class LoginWindow(QtGui.QDialog):
    def __init__(self):
        super(LoginWindow, self).__init__()
        self.ui2 = Ui_LoginWindow()
        self.ui2.setupUi(self)
        self.ui2.Password.setEchoMode(QtGui.QLineEdit.Password)

        self.ui2.LoginBUT.clicked.connect(self.handleLogin)


    def handleLogin(self):
        textName = str(self.ui2.Username.text())
        textPass = str(self.ui2.Password.text())
        log = LogMeIn.PassPhrase(textName, textPass)._CheckPwd()
        if log is True:
            self.accept()
        else:
            QtGui.QMessageBox.warning(self, 'Error', 'Bad user or password')


class MainWindow(QtGui.QMainWindow):
    def __init__(self, parent=None):
        # Construct and instance of the parent QMainwindow
        super(MainWindow, self).__init__(parent)

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.refreshAndReloadEmpClass()
        self.refreshAndReloadRotaClass()
        self.defineInstantVariables()
        self.queryRevenueTypeDBTable()
        self.queryDepartmentDBTable()
        self.queryShiftTypeDBTable()
        self.rotaTableWidgetFormating()
        self.setupButtonsTriggersAndCombos()

        # Populate data on loading
        self.loadRota()

        # interesintg and worth a play later
        # widget = QtGui.QTextEdit()
        # self.ui.tableWidget.setCellWidget(0, 0, widget.setText("chicken"))

    def defineInstantVariables(self):
        # define instant variables
        # self.dateList = []
        self.fetched = []
        self.results = []
        self.results2 = []
        self.selectedDate = None
        self.predictedCoverTotal = 0
        self.cellrow = 0
        self.cellcoll = 1
        self.scrollbarPosition = 5

    def setupButtonsTriggersAndCombos(self):
        # Set date selector to the Monday of current week
        wk = QtCore.QDate.weekNumber(QtCore.QDate.currentDate())
        self.ui.dateEdit.setDate(datetime.datetime.strptime(str(str(wk[1]) + '-' + str(wk[0])) + '-1', "%Y-%W-%w"))

        # set button Icon
        self.ui.todayBut.setIcon(QtGui.QIcon('dot.png'))
        self.ui.lessWeekBUT.setIcon(QtGui.QIcon('left.png'))
        self.ui.moreWeekBUT.setIcon(QtGui.QIcon('right.png'))

        # populate filter combo drop down
        self.populateDepartmentFilterCombo()

        # Monitor and filter on change of filter category
        self.ui.departmentFilterCombo.currentIndexChanged.connect(self.loadRota)

        # Other button clicks
        self.ui.tableWidget.cellDoubleClicked.connect(self.launchShiftPopUpIfEmployed)
        self.ui.AddEmpBUT.clicked.connect(self.launchaddemployeePopUp)
        self.ui.RemoveEmpBUT.clicked.connect(self.deleteEmployeeFromRota)
        self.ui.delShiftBUT.clicked.connect(self.delShifts)
        self.ui.deleteWeekBUT.clicked.connect(self.delWeek)
        self.ui.tabWidget.currentChanged.connect(self.loadRota)
        self.ui.addRevTypeBUT.clicked.connect(self.addNewRevenueType)
        self.ui.delRevenueTypeBUT.clicked.connect(self.delRevenueType)
        #self.ui.tabWidget.currentChanged.connect(self.wageTabSelected)

        # Week Nav buttons
        self.ui.lessWeekBUT.clicked.connect(self.decreaseDate)
        self.ui.moreWeekBUT.clicked.connect(self.increaseDate)

        # Monitor and reload data on change
        self.ui.dateEdit.dateChanged.connect(self.loadRota)
        self.ui.revenueTypeTable.currentItemChanged.connect(self.updateRevenueTypeToDB)
        #self.ui.predictedCoverTable.currentItemChanged.connect(self.updateCoverForecastToDB2)
        self.ui.predictedCoverTable.currentItemChanged.connect(self.populateCoverTotalsBoxes)
        self.ui.coverUpdateBUT.clicked.connect(self.updateCoverForecastToDB2)
        self.ui.coverUpdateBUT.clicked.connect(self.populateCoverTotalsBoxes)

        # menu item triggers
        self.ui.actionEmployee.triggered.connect(self.launchEmployeeInfoPopUp)
        self.ui.actionPayroll_Variables.triggered.connect(self.launchPayrollVariableUI)
        self.ui.actionPrint_Rota.triggered.connect(self.launchPrint)
        self.ui.actionReporting_Tool.triggered.connect(self.launchReportingTool)
        self.ui.actionBudget_and_Actuals.triggered.connect(self.launchActualRevWindow)

    def coverCalculatorDateRange(self, fromDate, toDate):
        covers = DB.Querydb("""SELECT predCoverAm, predCoverPM from PredictedCovers WHERE predCoverDate BETWEEN %s AND %s """,
                   (fromDate, toDate)).fetchAllRecordswithFormatting()

        totalCovers = 0
        for x in xrange(len(covers)):
            totalCovers += covers[x][0] + covers[x][1]
        return totalCovers

    def generateSelectedMonthDateRange(self):
        date = self.selectedDate

        weekDateList = self.dateList
        #print('week date list', weekDateList)

        # determine if the week is more one month or other
        monthCounter = 0
        for d in xrange(6):
            if weekDateList[0].month == weekDateList[d + 1].month:
                monthCounter += 1
            else:
                pass
        #print('month Counter', monthCounter)

        # if week is more one month, make adjustment
        if monthCounter < 3 :
            date = date + relativedelta(months= 1)
            month = date.month
            year = date.year
        else:
            month = date.month
            year = date.year

        firstOfMonth = datetime.date(year, month, 1)
        endOfWeek = self.selectedDate + datetime.timedelta(days=6)
        daysInMonth = calendar.monthrange(date.year, date.month)[1]
        dateRange = []


        for day in xrange(0, daysInMonth):
            # if monday of selected week is greater than the first of the month add preceding dates to the list
            if self.selectedDate > firstOfMonth + relativedelta(days=day):
                dateRange.append(firstOfMonth + relativedelta(days=day))
            else:
                # add the remaining days if less than end of week
                if (firstOfMonth + relativedelta(days=day)) <= endOfWeek:
                    dateRange.append(firstOfMonth + relativedelta(days=day))
                else:
                    break
        #print ('MTD Range', dateRange)
        #print ('Date', date, 'End of week', endOfWeek, 'days in Month', daysInMonth, 'first of Month', firstOfMonth)
        return dateRange

    def populateCoverTotalsBoxes(self):
        firstOfYearDate = datetime.date(self.selectedDate.year, 1, 1)
        monthRange = self.generateSelectedMonthDateRange()

        self.MTDCoversTotal = self.coverCalculatorDateRange(monthRange[0], monthRange[-1])
        self.YTDcoversTotal = self.coverCalculatorDateRange(firstOfYearDate, monthRange[1])
        weeklyCoverTotal = self.coverCalculatorDateRange(self.dateList[0], self.dateList[-1])

        self.ui.MTDCoversTotalBox.setValue(self.MTDCoversTotal)
        self.ui.YTDCoversTotalBox.setValue(self.YTDcoversTotal)
        self.ui.WeeklyCoversTotal.setValue(weeklyCoverTotal)

        #print ('MTD Covers', self.MTDCoversTotal, 'st date', monthRange[0], ' fin date', monthRange[-1])

    def rotaTableWidgetFormating(self):
        # Rota table widget formating
        header = self.ui.tableWidget.horizontalHeader()
        header.setResizeMode(0, QtGui.QHeaderView.ResizeToContents)
        header.setResizeMode(1, QtGui.QHeaderView.ResizeToContents)
        header.setResizeMode(2, QtGui.QHeaderView.ResizeToContents)
        header.setResizeMode(3, QtGui.QHeaderView.ResizeToContents)
        header.setResizeMode(4, QtGui.QHeaderView.ResizeToContents)
        header.setResizeMode(5, QtGui.QHeaderView.ResizeToContents)
        header.setResizeMode(6, QtGui.QHeaderView.ResizeToContents)
        header.setResizeMode(7, QtGui.QHeaderView.ResizeToContents)
        header.setResizeMode(8, QtGui.QHeaderView.ResizeToContents)
        header.setResizeMode(9, QtGui.QHeaderView.ResizeToContents)
        header.setResizeMode(0, QtGui.QHeaderView.Stretch)
        header.setResizeMode(1, QtGui.QHeaderView.Stretch)
        header.setResizeMode(2, QtGui.QHeaderView.Stretch)
        header.setResizeMode(3, QtGui.QHeaderView.Stretch)
        header.setResizeMode(4, QtGui.QHeaderView.Stretch)
        header.setResizeMode(5, QtGui.QHeaderView.Stretch)
        header.setResizeMode(6, QtGui.QHeaderView.Stretch)
        header.setResizeMode(7, QtGui.QHeaderView.Stretch)
        header.setResizeMode(8, QtGui.QHeaderView.Stretch)
        header.setResizeMode(9, QtGui.QHeaderView.Stretch)


        header1 = self.ui.coverHeaderTable.horizontalHeader()
        header1.setResizeMode(0, QtGui.QHeaderView.Stretch)
        header1.setResizeMode(1, QtGui.QHeaderView.Stretch)
        header1.setResizeMode(2, QtGui.QHeaderView.Stretch)
        header1.setResizeMode(3, QtGui.QHeaderView.Stretch)
        header1.setResizeMode(4, QtGui.QHeaderView.Stretch)
        header1.setResizeMode(5, QtGui.QHeaderView.Stretch)
        header1.setResizeMode(6, QtGui.QHeaderView.Stretch)
        header1.setResizeMode(7, QtGui.QHeaderView.Stretch)
        header1.setResizeMode(8, QtGui.QHeaderView.Stretch)
        header1.setResizeMode(9, QtGui.QHeaderView.Stretch)

        covs = self.ui.predictedCoverTable.horizontalHeader()
        covs.setResizeMode(1, QtGui.QHeaderView.ResizeToContents)
        covs.setResizeMode(2, QtGui.QHeaderView.ResizeToContents)
        covs.setResizeMode(3, QtGui.QHeaderView.ResizeToContents)
        covs.setResizeMode(4, QtGui.QHeaderView.ResizeToContents)
        covs.setResizeMode(5, QtGui.QHeaderView.ResizeToContents)
        covs.setResizeMode(6, QtGui.QHeaderView.ResizeToContents)
        covs.setResizeMode(7, QtGui.QHeaderView.ResizeToContents)
        covs.setResizeMode(8, QtGui.QHeaderView.ResizeToContents)
        covs.setResizeMode(9, QtGui.QHeaderView.ResizeToContents)
        covs.setResizeMode(10, QtGui.QHeaderView.ResizeToContents)
        covs.setResizeMode(11, QtGui.QHeaderView.ResizeToContents)
        covs.setResizeMode(12, QtGui.QHeaderView.ResizeToContents)
        covs.setResizeMode(13, QtGui.QHeaderView.ResizeToContents)
        covs.setResizeMode(14, QtGui.QHeaderView.ResizeToContents)
        self.setGeometry(200, 200, 1255, 500)
        self.ui.tabWidget.setCurrentIndex(0)

    def launchActualRevWindow(self):
        revWindow = ActualRevWindow.ActualRevWindow(self.selectedDate)
        revWindow.exec_()

    def refreshAndReloadRotaClass(self):
        self.shiftsTable = DB.Querydb("""SELECT * FROM shifts""", None).fetchAllRecordswithFormatting()
        self.rotaData = RotaData.rota(self.shiftsTable)

    def refreshAndReloadEmpClass(self):
        self.empTable = DB.Querydb("""SELECT * FROM Employee_TBL""", None).fetchAllRecordswithFormatting()
        self.salTable = DB.Querydb("""SELECT * FROM Salary""", None).fetchAllRecordswithFormatting()
        self.depTable = DB.Querydb("""SELECT * FROM departments""", None).fetchAllRecordswithFormatting()
        self.bonusTable = DB.Querydb("""SELECT * FROM Bonus""", None).fetchAllRecordswithFormatting()
        self.holsTable = DB.Querydb("""SELECT * FROM HolidayEntitlement""", None).fetchAllRecordswithFormatting()
        self.salorHourlyTable = DB.Querydb("""SELECT * FROM salorHourlyTable""", None).fetchAllRecordswithFormatting()
        self.NMWRates = DB.Querydb("""SELECT * FROM nmwRates""", None).fetchAllRecordswithFormatting()
        self.NMWBands = DB.Querydb("""SELECT * FROM nmwBands""", None).fetchAllRecordswithFormatting()
        self.salCalVar =  DB.Querydb("""SELECT * FROM SalaryCalVariables""", None).fetchAllRecordswithFormatting()
        self.emp = employees(self.empTable, self.salTable, self.depTable, self.bonusTable, self.holsTable,
                                       self.salorHourlyTable)

    def launchEmployeeInfoPopUp(self):
        # TODO: think this through, currently + and - 1 year from selected date
        toDate = datetime.date.strftime(self.selectedDate + relativedelta(years=5), '%Y-%m-%d')
        fromDate = datetime.date.strftime(self.selectedDate - relativedelta(years=5), '%Y-%m-%d')

        print (fromDate, toDate)
        empPopUp = EmployeePopUp.EmployeePopUp(fromDate, toDate)
        empPopUp.trigger.connect(self.loadRota)
        empPopUp.exec_()

    def launchShiftPopUpIfEmployed(self):
        # Determine which cell has been selected
        self.cellcoll = self.ui.tableWidget.currentColumn()
        self.cellrow = self.ui.tableWidget.currentRow()

        # Determine return position for scroll bar
        self.scrollbarPosition = self.ui.tableWidget.verticalScrollBar().value()

        # Determine if the shift is within Employee start and finish dates
        shiftDate = self.dateList[int(self.cellcoll) - 1]
        empID = self.results2[self.cellrow][8]

        if self.cellcoll == 0:
            pass
        else:
            if shiftDate < self.emp.empStartDate(empID):
                msgbox = QtGui.QMessageBox()
                msgbox.setWindowTitle("Warning")
                msgbox.setText("{} Doesn't Start until {}".format(self.emp.empName(empID), self.emp.empStartDate(empID)))
                msgbox.exec_()
            elif str(shiftDate) > str(self.emp.empFinishDate(empID)):
                msgbox = QtGui.QMessageBox()
                msgbox.setWindowTitle("Warning")
                msgbox.setText("{} Finished on {}".format(self.emp.empName(empID), self.emp.empFinishDate(empID)))
                msgbox.exec_()
            else:
                # load variable into instance of shift popup window
                self.pop = ShiftPopUp.ShiftPopUp(self.cellcoll, self.cellrow, self.dateList,
                                                 self.results2, self.shiftTypes, self.departments, empID)
                # Show shift pop window
                self.pop.show()
                self.pop.trigger.connect(self.loadRota)

    def launchaddemployeePopUp(self):
        rows = self.ui.tableWidget.rowCount()
        exisitingnames = []
        for row in xrange(0, rows):
            exisitingnames.append(str(self.ui.tableWidget.item(row, 0).text()))

        # launch add employee window
        self.names = AddEmployeeWindow.AddEmployee(self.dateList, exisitingnames)
        self.names.show()
        self.names.trigger.connect(self.addEmployeestoRota)

    def launchPayrollVariableUI(self):
        self.payrollVarPopUp = payrollVariablePopUP.payrollVariablePopUp()
        self.payrollVarPopUp.show()

    def launchReportingTool(self):
        self.reportingTool = reporting.reportWindowui(self.shiftsTable)
        self.reportingTool.importEmpModData(self.empTable, self.salTable, self.depTable, self.bonusTable,
                                            self.holsTable,
                                            self.salorHourlyTable)
        self.reportingTool.show()

    def datetoMonday(self, date):
        dateNum = datetime.date.weekday(QtCore.QDate.toPyDate(date))
        if dateNum == 0:
            return date
        else:
            pydate = QtCore.QDate.toPyDate(date)
            adjustDate = pydate - datetime.timedelta(days=dateNum)
            return QtCore.QDate(adjustDate)

    def loadRota(self):
        # Populate data with selected date data
        # convert date entry to py date
        self.selectedDate = QtCore.QDate.toPyDate(self.datetoMonday(self.ui.dateEdit.date()))
        # Refresh emp module data
        self.refreshAndReloadEmpClass()
        # Refresh rotadata Class
        self.refreshAndReloadRotaClass()
        # populate the table column headers with dates
        self.setColumnDateLabels()
        # Query DB.shifts
        self.queryShiftTable()
        # Convert data in nested lists
        self.convertDBdata()
        # write convert data into table
        self.populateRotaTableWidget()
        # populate the cover forecast data
        self.populatePredictiveCoverTable()
        # populate the Revenue type table
        self.populateRevenueTypeTable()
        # calculate and populate predicted revenue
        self.predictedRevenueTotalAction()
        # Calculate and populate predicted average spend total
        self.predictedAvgSpendTotal()
        # calculate and populate predicted cover totals
        self.PopulateRotaCoversTotals()
        # Populate the cover totals boxes
        self.populateCoverTotalsBoxes()
        #self.ui.tabWidget.close()
        #self.ui.tabWidget.show()
        # if wage tab is selected, calculate the wage information
        if self.ui.tabWidget.currentIndex() == 1:
            splash_pix = QtGui.QPixmap('splash.png')
            splash = QtGui.QSplashScreen(splash_pix, QtCore.Qt.WindowStaysOnTopHint)
            splash.setMask(splash_pix.mask())
            splash.show()
            app.processEvents()

            self.populateWeeklyWageInformation()
            self.populateMonthToDateWageInformation()

            splash.finish(self.ui.wageTab)
        else:
            pass

        self.repositionViewAfterUpdate()

    def repositionViewAfterUpdate(self):
        slider = self.ui.tableWidget.verticalScrollBar()
        slider.setValue(self.scrollbarPosition)
        self.ui.tableWidget.setCurrentCell(self.cellrow, self.cellcoll)

    def increaseDate(self):
        self.ui.dateEdit.setDate(QtCore.QDate.addDays(self.ui.dateEdit.date(), 7))
        self.loadRota()

    def decreaseDate(self):
        self.ui.dateEdit.setDate(QtCore.QDate.addDays(self.ui.dateEdit.date(), -7))
        self.loadRota()

    def setColumnDateLabels(self):
        # self.CalcAndPopPredictedCoverTotals()

        # Set column headers to relevant dates
        blank = self.ui.coverHeaderTable.horizontalHeaderItem(0)
        blank.setText("")
        mondaydate = self.ui.coverHeaderTable.horizontalHeaderItem(1)
        mondaydate.setText(datetime.date.strftime(self.selectedDate, "%a %d %B"))
        tuedaydate = self.ui.coverHeaderTable.horizontalHeaderItem(2)
        tuedaydate.setText(datetime.date.strftime(self.selectedDate + datetime.timedelta(days=1), "%a %d %B"))
        wednesdaydate = self.ui.coverHeaderTable.horizontalHeaderItem(3)
        wednesdaydate.setText(datetime.date.strftime(self.selectedDate + datetime.timedelta(days=2), "%a %d %B"))
        thursdaydate = self.ui.coverHeaderTable.horizontalHeaderItem(4)
        thursdaydate.setText(datetime.date.strftime(self.selectedDate + datetime.timedelta(days=3), "%a %d %B"))
        fridaydate = self.ui.coverHeaderTable.horizontalHeaderItem(5)
        fridaydate.setText(datetime.date.strftime(self.selectedDate + datetime.timedelta(days=4), "%a %d %B"))
        satdaydate = self.ui.coverHeaderTable.horizontalHeaderItem(6)
        satdaydate.setText(datetime.date.strftime(self.selectedDate + datetime.timedelta(days=5), "%a %d %B"))
        sundaydate = self.ui.coverHeaderTable.horizontalHeaderItem(7)
        sundaydate.setText(datetime.date.strftime(self.selectedDate + datetime.timedelta(days=6), "%a %d %B"))

    def queryShiftTable(self):

        # Get shift data from DB
        d = self.selectedDate
        d2 = self.selectedDate + datetime.timedelta(days=6)
        # Reset the date listOfEmployees
        self.dateList = []
        # Write a listOfEmployees of days within the week starting with selected date
        NumDays = 7
        for x in xrange(0, NumDays):
            self.dateList.append(d + datetime.timedelta(days=x))

        self.fetched = DB.Querydb("""
        SELECT EmployeeID, Employee_TBL.Name, `Date`, ConcatShift, 
        TotalHours, StartAM, FinAM, BrkAM, StartPM, FinPM, BrkPM, Employee_TBL.SalOrHourly, 
        TotalHours, EmpStDate, EmpFinDate, departments.department, shiftTypeAM, shiftTypePM, departments.departmentID,
        DepAM, DepPM
        FROM`shifts`
        INNER JOIN `Employee_TBL`
        ON shifts.EmployeeID = idEmployee_TBL
        INNER JOIN `departments`
        ON Employee_TBL.departmentID = departments.departmentID
        WHERE Date BETWEEN %s AND %s
        """, (str(d), str(d2))).fetchAllRecordswithFormatting()

    def convertDBdata(self):
        # Convert data into format to be written to table widget
        # filter the duplicates names from the results with a set and filter for selection in filter combo box
        if self.ui.departmentFilterCombo.currentText() == 'All Staff':
            self.names = set(self.fetched[x][1] for x in xrange(len(self.fetched)))
        elif self.ui.departmentFilterCombo.currentText() == 'Kitchen & FOH':
            self.names = set(self.fetched[x][1] for x in xrange(len(self.fetched)) if self.fetched[x][15]
                             != 'Admin')
        else:
            self.names = set(self.fetched[x][1] for x in xrange(len(self.fetched)) if self.fetched[x][15]
                             == self.ui.departmentFilterCombo.currentText())

        # Reset results listOfEmployees
        self.results2 = []

        # create a listOfEmployees for each name with blanks
        for a in xrange(len(self.names)):
            self.results2.append(["", [], [], [], [], [], [], [], int(), "", "", int()])
        for count, name in enumerate(self.names):  # iterate through names
            self.results2[count][0] = name  # append name to new listOfEmployees
            for i in xrange(len(self.fetched)):  # iterate through records fetched
                if self.fetched[i][1] == name:  # if name is found
                    self.results2[count][8] = self.fetched[i][0]  # append the employee ID
                    self.results2[count][9] = self.fetched[i][13]  # append the employee St Date
                    self.results2[count][10] = self.fetched[i][14]  # append the employee Fin Date
                    self.results2[count][11] = self.fetched[i][18] # append the employee department
                    for cols, date in enumerate(self.dateList):  # iterate through dates
                        if self.fetched[i][2] == date:  # if date is found
                            self.results2[count][cols + 1] = [self.convertDecToTime(self.fetched[i][5]), # append times
                                                              self.convertDecToTime(self.fetched[i][6]), # append times
                                                              self.fetched[i][16],  # append shift type ie work, hol etc
                                                              self.convertDecToTime(self.fetched[i][8]), # append times
                                                              self.convertDecToTime(self.fetched[i][9]), # append times
                                                              self.fetched[i][17],  # append shift type ie work, hol etc
                                                              self.fetched[i][19],  # append employee role AM
                                                              self.fetched[i][20],  # append employee role PM
                                                                ]
        # sort the listOfEmployees by department
        sort = sorted(self.results2, key=lambda department: department[11])
        self.results2 = sort

    def convertDecToTime(self, time):
        hours = int(time)
        mins = (time * 60) % 60
        return "%02d:%02d" % (hours, mins)

    def convertDBdata2(self):

        # Convert data into format to be written to table widget
        # filter the duplicates names from the results with a set and filter for selction in filter combo box
        if self.ui.departmentFilterCombo.currentText() == 'All Staff':
            self.names = set(self.fetched[x][1] for x in xrange(len(self.fetched)))
        elif self.ui.departmentFilterCombo.currentText() == 'Kitchen & FOH':
            self.names = set(self.fetched[x][1] for x in xrange(len(self.fetched)) if self.fetched[x][15]
                             != 'Admin')
        else:
            self.names = set(self.fetched[x][1] for x in xrange(len(self.fetched)) if self.fetched[x][15]
                        == self.ui.departmentFilterCombo.currentText())

        # Reset results listOfEmployees
        self.results = []

        # create a listOfEmployees for each name with blanks
        for a in xrange(len(self.names)):
            self.results.append(["", "", "", "", "", "", "", "", int(), "", ""])
        for count, x in enumerate(self.names):  # iterate through names
            self.results[count][0] = x  # append name to new listOfEmployees
            for i in xrange(len(self.fetched)):  # iterate through records fetched
                if self.fetched[i][1] == x:  # if name is found
                    self.results[count][8] = self.fetched[i][0] # append the employee ID
                    self.results[count][9] = self.fetched[i][13] # append the employee St Date
                    self.results[count][10] = self.fetched[i][14]  # append the employee Fin Date
                    for cols, date in enumerate(self.dateList):  # iterate through dates
                        if self.fetched[i][2] == date:  # if date is found
                            self.results[count][cols + 1] = self.fetched[i][3]  # append concat times

    def populateRotaTableWidget(self):
        pop = WidgetTools.TableWidgetTools()
        pop.setWidget(self.ui.tableWidget)
        pop.populateRotaTableWidgetHTML(self.results2, 8, None, self.shiftTypes, self.departments)

    def addEmployeestoRota(self):
        # insert selected names from add employee window to database
        b = [[int(self.names.SelectionList[a][1]), str(self.selectedDate), 0, 0, 0, 0, 0, 0, "", 0,
              self.names.SelectionList[a][2], self.names.SelectionList[a][2], self.names.SelectionList[a][2]]
             for a in xrange(len(self.names.SelectionList))]
        DB.Querydb('''INSERT INTO shifts (EmployeeID, Date, StartAM, FinAM, BrkAM, StartPM, FinPM, BrkPM, 
                                                    ConcatShift, TotalHours, EmployeeDep, DepAM, DepPM) 
                        VALUE (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s );''', b).InsertManyExecutewithFormatting()
        self.loadRota()

    def deleteEmployeeFromRota(self):
        # Remove employee and shifts from current week
        fetched = self.results2
        row = self.ui.tableWidget.currentRow()
        date = self.dateList
        message = QtGui.QMessageBox.question(QtGui.QMessageBox(), 'Message', "Do you Really Want to Delete {}"
                                             .format(fetched[row][0]), QtGui.QMessageBox.Yes | QtGui.QMessageBox.No,
                                             QtGui.QMessageBox.No)
        if message == QtGui.QMessageBox.Yes:
                DB.Querydb('''DELETE FROM shifts WHERE shifts.EmployeeID = %s AND shifts.`Date` BETWEEN %s AND %s;''',
                           (fetched[row][8], str(date[0]), str(date[6]))).DeleteOneExecutewithFormatting()
                self.loadRota()
        else:
            print('Done')

    def populatePredictiveCoverTable(self):
        # Extract from DB and
        # populate the Cover Forecast table

        self.ui.monDateLBL.setText(str(self.dateList[0]))
        self.ui.tueDateLBL.setText(str(self.dateList[1]))
        self.ui.wedDateLBL.setText(str(self.dateList[2]))
        self.ui.thurDateLBL.setText(str(self.dateList[3]))
        self.ui.friDateLBL.setText(str(self.dateList[4]))
        self.ui.satDateLBL.setText(str(self.dateList[5]))
        self.ui.sunDateLBL.setText(str(self.dateList[6]))


        # Clear Table
        self.ui.predictedCoverTable.clearContents()

        self.predcov = DB.Querydb('''SELECT * FROM PredictedCovers Where predCoverDate BETWEEN %s AND %s''',
                                  (self.dateList[0], self.dateList[6])).fetchAllRecordswithFormatting()

        # reset table widget
        self.ui.predictedCoverTable.setRowCount(0)

        # populate the rev types into the first col
        for row in xrange(0, len(self.revenueTypes)):
            self.ui.predictedCoverTable.insertRow(row)
            record = (self.revenueTypes[row][0], self.revenueTypes[row][1])
            newitem = QtGui.QTableWidgetItem(str(record[1]))
            self.ui.predictedCoverTable.setItem(row, 0, newitem)

            # populate am and pm shifts
            for rec in xrange(0, len(self.predcov)): # iterate through predicted covers
                if self.predcov[rec][4] == record[0]: # match the revenue type to the row
                    for d in xrange(1, len(self.dateList) + 1): #iterate through selected dates
                        if self.predcov[rec][1] == self.dateList[d - 1]: # match the date to the column
                            AM = QtGui.QTableWidgetItem(str(self.predcov[rec][2])) # fetch am data
                            PM = QtGui.QTableWidgetItem(str(self.predcov[rec][3])) # fetch PM data
                            self.ui.predictedCoverTable.setItem(row, (d * 2) - 1, AM) # write AM data
                            self.ui.predictedCoverTable.setItem(row, d * 2, PM) # write PM data

        self.ui.predictedCoverTable.resizeRowsToContents()

    def updateCoverForecastToDB2(self):
        dbExtract = self.coversdata

        row = self.ui.predictedCoverTable.rowCount()
        col = self.ui.predictedCoverTable.columnCount()

        tableExtract = []

        for x in range(row):
            tableExtract.append([])
            for y in range(col):
                if self.ui.predictedCoverTable.item(x, y) is None:
                    tableExtract[x].append(0)
                elif y == 0:
                    text = self.ui.predictedCoverTable.item(x, y).text()
                    tableExtract[x].append(str(text))
                else:
                    returnedTuple = self.ui.predictedCoverTable.item(x, y).text().toInt()
                    tableExtract[x].append(returnedTuple[0])


        revenueTypes = self.revenueTypes
        dateRange = self.dateList

        #print ('table Extract', tableExtract)
        #print ('revenue types', revenueTypes)
        #print ('covers data', dbExtract)
        #print ('date List', dateRange)

        convertedTableExtract = []

        for revType in xrange(len(tableExtract)):
            revTypeID = [revID for revID, revName, DryAM, DryPM, WetAM, WetPM in revenueTypes if revName == tableExtract[revType][0]]
            counter1 = 1
            counter2 = 2
            for date in xrange(len(dateRange)):
                convertedTableExtract.append(
                    [dateRange[date], tableExtract[revType][date + counter1], tableExtract[revType][date + counter2], revTypeID[0],
                     dateRange[date], tableExtract[revType][date + counter1], tableExtract[revType][date + counter2], revTypeID[0]])
                counter1 += 1
                counter2 += 1

        #print ('converted table extract', convertedTableExtract)


        DB.Querydb(''' INSERT INTO PredictedCovers (predCoverDate, predCoverAM, predCoverPM, revenueTypeID)
                                       VALUE (%s, %s, %s, %s) ON DUPLICATE KEY UPDATE predCoverDate = %s, 
                                       predCoverAM = %s, predCoverPM = %s, revenueTypeID = %s;''',
                   convertedTableExtract).InsertManyExecutewithFormatting()

        # calculate and populate predicted revenue
        self.predictedRevenueTotalAction()

        # calculate and populate predicted cover totals
        self.PopulateRotaCoversTotals()

        # Calculate and populate predicted average spend total
        self.predictedAvgSpendTotal()

    def populateRevenueTypeTable(self):
        self.queryRevenueTypeDBTable()
        pop = WidgetTools.TableWidgetTools()
        pop.setWidget(self.ui.revenueTypeTable)
        pop.populateTableWidget(self.revenueTypes, 6, 0)
        self.ui.revenueTypeTable.setHorizontalHeaderLabels(["", "Rev Type", "SPH AM", "SPH PM", "SCPH AM", "SCPH PM"])

    def updateRevenueTypeToDB(self):
        self.queryRevenueTypeDBTable()
        update = WidgetTools.TableWidgetTools()
        update.setWidget(self.ui.revenueTypeTable)
        DB.Querydb("""UPDATE RevenueTypes
                    SET revenueType = %s, amDryAvgSpend = %s, pmDryAvgSpend = %s, amWetAvgSpend = %s, pmWetAvgSpend = %s
                    WHERE RevenueTypeID = %s;""", update.extraWidgetDataToList(True)).InsertManyExecutewithFormatting()
        self.populatePredictiveCoverTable()

    def addNewRevenueType(self):
        DB.Querydb('''INSERT INTO RevenueTypes(revenueType) VALUE (%s);''',("",)).InsertOneExecutewithFormatting()
        self.populateRevenueTypeTable()

    def delRevenueType(self):
        widget = WidgetTools.TableWidgetTools()
        widget.setWidget(self.ui.revenueTypeTable)
        revTypeID = widget.IDfromSelectedRow()

        message = QtGui.QMessageBox.question(QtGui.QMessageBox(), 'Message', "Do you Really Want to Delete this Revenue "
                                                                             "Type. All associated data will be lost"
                                             , QtGui.QMessageBox.Yes | QtGui.QMessageBox.No,
                                             QtGui.QMessageBox.No)

        if message == QtGui.QMessageBox.Yes:
            DB.Querydb("""DELETE FROM RevenueTypes WHERE revenueTypeID = %s""",
                       (int(revTypeID),)).DeleteOneExecutewithFormatting_ErrorMessage("Please Select Revenue Type")
            self.populateRevenueTypeTable()
            self.populatePredictiveCoverTable()
        else:
            pass

    def predictedRevenueTotalAction(self):
        # Calculate the revenue totals for all the cover types from Avg spend * covers
        predictedRevenueTotal = Decimal()
        coversdata = self.queryPredictedCoverDBTable(self.dateList[0], self.dateList[6])

        avgSpendData = self.queryRevenueTypeDBTable()

        for x in xrange(len(coversdata)): # iterate through extracted pred cover data
            for y in xrange(len(avgSpendData)): # iterate through avg spend data
                if str(avgSpendData[y][0]) == str(coversdata[x][4]):
                    predictedRevenueTotal += ((coversdata[x][2] * avgSpendData[y][2]) +
                                                   (coversdata[x][3] * avgSpendData[y][3]) +
                                                   (coversdata[x][2] * avgSpendData[y][4]) +
                                                   (coversdata[x][3] * avgSpendData[y][5]))
        self.ui.predRevBox.setValue(predictedRevenueTotal)
        return predictedRevenueTotal

    def calculateCoverTotals(self):
        # Calculate the am and pm cover total summaries
        coversdata = self.queryPredictedCoverDBTable(self.dateList[0], self.dateList[6])
        predictedCoverTotal = sum([am + pm for (ID, date, am, pm, rev) in coversdata])
        return predictedCoverTotal

    def PopulateRotaCoversTotals(self):
        coversdata = self.queryPredictedCoverDBTable(self.dateList[0], self.dateList[6])
        predictedCoverTotal = sum([am + pm for (ID, date, am, pm, rev) in coversdata])

        monamcov = str(sum([am for (ID, date, am, pm, rev) in coversdata if date == self.dateList[0]]))
        monpmcov = str(sum([pm for (ID, date, am, pm, rev) in coversdata if date == self.dateList[0]]))
        tueamcov = str(sum([am for (ID, date, am, pm, rev) in coversdata if date == self.dateList[1]]))
        tuepmcov = str(sum([pm for (ID, date, am, pm, rev) in coversdata if date == self.dateList[1]]))
        wedamcov = str(sum([am for (ID, date, am, pm, rev) in coversdata if date == self.dateList[2]]))
        wedpmcov = str(sum([pm for (ID, date, am, pm, rev) in coversdata if date == self.dateList[2]]))
        thuramcov = str(sum([am for (ID, date, am, pm, rev) in coversdata if date == self.dateList[3]]))
        thurpmcov = str(sum([pm for (ID, date, am, pm, rev) in coversdata if date == self.dateList[3]]))
        friamcov = str(sum([am for (ID, date, am, pm, rev) in coversdata if date == self.dateList[4]]))
        fripmcov = str(sum([pm for (ID, date, am, pm, rev) in coversdata if date == self.dateList[4]]))
        satamcov = str(sum([am for (ID, date, am, pm, rev) in coversdata if date == self.dateList[5]]))
        satpmcov = str(sum([pm for (ID, date, am, pm, rev) in coversdata if date == self.dateList[5]]))
        sunamcov = str(sum([am for (ID, date, am, pm, rev) in coversdata if date == self.dateList[6]]))
        sunpmcov = str(sum([pm for (ID, date, am, pm, rev) in coversdata if date == self.dateList[6]]))

        # set cover headers
        coverLabel = self.ui.tableWidget.horizontalHeaderItem(0)
        coverLabel.setText('Cover Total =  {}'.format(predictedCoverTotal))
        monCovLabel = self.ui.tableWidget.horizontalHeaderItem(1)
        monCovLabel.setText('{}         |          {}'.format(monamcov, monpmcov))
        tueCovLabel = self.ui.tableWidget.horizontalHeaderItem(2)
        tueCovLabel.setText('{}         |          {}'.format(tueamcov, tuepmcov))
        wedCovLabel = self.ui.tableWidget.horizontalHeaderItem(3)
        wedCovLabel.setText('{}         |          {}'.format(wedamcov, wedpmcov))
        thurCovLabel = self.ui.tableWidget.horizontalHeaderItem(4)
        thurCovLabel.setText('{}         |          {}'.format(thuramcov, thurpmcov))
        friCovLabel = self.ui.tableWidget.horizontalHeaderItem(5)
        friCovLabel.setText('{}         |          {}'.format(friamcov, fripmcov))
        satCovLabel = self.ui.tableWidget.horizontalHeaderItem(6)
        satCovLabel.setText('{}         |          {}'.format(satamcov, satpmcov))
        sunCovLabel = self.ui.tableWidget.horizontalHeaderItem(7)
        sunCovLabel.setText('{}         |          {}'.format(sunamcov, sunpmcov))

    def predictedAvgSpendTotal(self):
        predictedRevenueTotal = self.predictedRevenueTotalAction()
        predictedCoverTotal = self.calculateCoverTotals()

        # Calculate the average spend for the week and populate the box, if no predicted revenue return 0
        if predictedCoverTotal != 0:
            self.ui.predAvgSpendBox.setValue(predictedRevenueTotal / predictedCoverTotal)
        else:
            self.ui.predAvgSpendBox.setValue(0)
    """
    def calculateQualifyingSickPeriodsInDateRange(self, dateRange):
        empList = self.emp.salCalcEmpList(str(dateRange[0]), str(dateRange[-1]))
        QDsickTotals = {}
        firstDate = []

        # Iterate through emps
        for emp in xrange(len(empList)):
            counter = 0
            # create key for each emp in list key:[QDs, first Date]
            QDsickTotals[empList[emp][0]] = [0, None]

            # TODO: build in mechanism to join PIWs
            # iterate through dates in range
            for date in xrange(len(dateRange)):
                # is the date a QD
                if self.emp.empIsDateAContractedDay(empList[emp][0], dateRange[date]) is True:
                    # if shift type empty, pass
                    if self.rotaData.empAMPMshiftTypeAtdate(empList[emp][0], dateRange[date]) == []:
                        counter = 0
                    else:
                        # if either am or pm shift is sick and the then count
                        if self.rotaData.empAMPMshiftTypeAtdate(empList[emp][0], dateRange[date])[0][0] == 3 \
                                or self.rotaData.empAMPMshiftTypeAtdate(empList[emp][0], dateRange[date])[0][1] == 3:
                            counter +=1

                            # if the first date append first date to list
                            if counter == 1:
                                firstDate.append(dateRange[date])
                            else:
                                pass

                            # if 4th sick day in a row add a QD to the corresponding key in dict
                            if counter > 3:
                                QDsickTotals[empList[emp][0]][0] += 1
                                QDsickTotals[empList[emp][0]][1] = firstDate
                            else:
                                pass

                        else:
                            counter = 0
                else:
                    pass

        #print ('sick Totals - RotaWindow.CQSPIDR', QDsickTotals)
        #print ('First Date - RotaWindow.CQSPIDR', firstDate)

        # convert Qualifying sick totals into money and return results
        results = self.sickPayEntitlementCalc(dateRange, QDsickTotals)
        return results

    def sickPayEntitlementCalc(self, dateRange, QDEmpDict):
        for key, value in list(QDEmpDict.items()):
            if value[0] == 0:
                pass
            else:
                empID = key

                payrollVariables = payrollVariablePopUP.payrollVariablePopUp()
                dayRate = payrollVariables.sickPayDayRate(dateRange[-1])
                QDs = QDEmpDict.get(empID)[0]
                empDaysPerWeek = self.emp.empContractedDaysofWork(empID)[1]
                lowerEarningsLimit = payrollVariables.SSPLowerEarningsLimit(dateRange[-1])

                # Calculate End of relative period ie the last pay day before first day of sickness
                firstQualifyingDate = QDEmpDict.get(empID)[1][0]
                EoRP_previousMonth = firstQualifyingDate + relativedelta(months=-1)
                EoRP_last_friday = max(
                    week[calendar.FRIDAY] for week in
                    calendar.monthcalendar(EoRP_previousMonth.year, EoRP_previousMonth.month))
                EoRP = datetime.date(EoRP_previousMonth.year, EoRP_previousMonth.month, EoRP_last_friday)

                # Calculate the Start of the relative period being no less than 8 weeks before EoRP
                EoRPLess8Weeks = EoRP + relativedelta(weeks=-8)
                SoRP_previousMonth = EoRPLess8Weeks + relativedelta(months=-1)
                SoRP_last_friday = max(
                    week[calendar.FRIDAY] for week in
                    calendar.monthcalendar(SoRP_previousMonth.year, SoRP_previousMonth.month))
                SoRP = datetime.date(SoRP_previousMonth.year, SoRP_previousMonth.month, SoRP_last_friday)

                report = reporting.reportWindowui(self.shiftsTable)
                report.importEmpModData(self.empTable, self.salTable, self.depTable, self.bonusTable, self.holsTable, self.salorHourlyTable)
                report = report.employeePayReport(SoRP, EoRP)

                salary = report[empID][2]
                daysEmployeed = self.emp.empDaysemployedWithinDateRange(empID, SoRP, EoRP)
                avgWeekPay = ( salary / daysEmployeed) * 7

                #print('salary - RW.SPEC', salary)
                #print('Days Employed -RW.SPEC', daysEmployeed)
                #print('Avg Week Pay -RW.SPEC', avgWeekPay)
                #print('Lower Earnings Limit - RW.SPEC', lowerEarningsLimit)
                #print('emp Days Per week - RW.SPEC', empDaysPerWeek)
                #print('QDs - RW.SPEC', QDs)
                #print('Total Sick Pay - RW.SPEC', ((dayRate * 7) / empDaysPerWeek) * QDs)

                # If average weekly wage over 8 week period is less than average Earnings limit, pass, otherwise
                # calculate day rate according to number of days worked in week and * by qualifying days
                # update relevant key in dictionary
                if avgWeekPay > lowerEarningsLimit:
                    QDEmpDict[empID][0] = ((dayRate * 7) / empDaysPerWeek) * QDs

                else:
                    pass
        #print ('QD employee Dictionary - RW.SPEC', QDEmpDict)
        total = 0
        salariedTotal = 0
        hourlyTotal = 0

        for key, value in list(QDEmpDict.items()):
            total += value[0]
            if self.emp.empSalaryOrHourlyID(key) == 0:
                salariedTotal += value[0]

            else:
                hourlyTotal += value[0]

        return [QDEmpDict, total, salariedTotal, hourlyTotal]

    def dateRangeListGenerator(self, startDate, endDate):
            days = (endDate - startDate).days
            dateRange = []
            for D in xrange(days + 1):
                dateRange.append(startDate + relativedelta(days=D))
            return dateRange


    def calculateWageCostForDateRange(self, dateRange):
        dates = dateRange
        sickPayEmpDict = self.calculateQualifyingSickPeriodsInDateRange(dates)
        SalariedTotal = sickPayEmpDict[2]
        hourlyWageCost = sickPayEmpDict[3]
        nicCostTotal = 0
        bonusCost = 0
        pensionCostTotal = 0
        nicCostHourly = 0
        nicCostSalaried = 0
        pensionCostHourly = 0
        pensionCostSalaried = 0
        SSPSalaried = sickPayEmpDict[2]
        SSPHourly = sickPayEmpDict[3]

        payVar = payrollVariablePopUP.payrollVariablePopUp()

        msg = QtGui.QMessageBox()

        # calc salaried and Hourly + NIC cost for the period
        for x in xrange(len(dates)):

            # define the nic variables
            threshold = payVar.nicThreshold(dates[x])
            age = payVar.nicMinAge(dates[x])
            rate = payVar.nicRate(dates[x])
            pensionPercent = payVar.pensionPecentage(dates[x])

            print ( threshold, age, rate, pensionPercent)
            if threshold is None or age is None or rate is None or pensionPercent is None:
                msg.setText("Payroll Variable are not complete for this date range. Please update now")
                msg.exec_()
            else:
                # TODO: define list of employees by department, to remove Admin from CALC
                # define employees in date range
                empList = self.emp.salCalcEmpList(str(dates[x]), str(dates[x]))

                for y in xrange(len(empList)):
                    empID = empList[y][0]
                    shiftDate = dates[x]
                    shiftType = self.rotaData.empAMPMshiftTypeAtdate(empID, shiftDate)
                    SalariedShiftCost = self.emp.empShiftSalaryCost_ExcludingSickDays(shiftDate, shiftType, empID)
                    SalariedNicShiftCost = self.emp.empNicCostByShiftSalary(empID, shiftDate, threshold, age, rate)
                    shiftBonusCost = self.emp.empShiftBonusCost(shiftDate, empID)
                    HourlyTotalHours = self.rotaData.empTotalHoursDay(empID, shiftDate, 'day')
                    HourlyHourlyCost = self.emp.empShiftHourlyPay(shiftDate, empID)
                    HourlyNicShiftCost = self.emp.empNicCostByShiftHourly(empID, shiftDate, threshold, age, rate)
                    pensionCostHourly = self.emp.empHourlyPensionShiftCalc(empID, shiftDate, threshold, age, rate, pensionPercent)
                    pensionCostSalaried = self.emp.empSalaryPensionShiftCalc(empID, shiftDate, threshold, age, rate, pensionPercent)
                    SalariedTotal += SalariedShiftCost
                    nicCostTotal += (SalariedNicShiftCost + HourlyNicShiftCost)
                    nicCostHourly += HourlyNicShiftCost
                    nicCostSalaried += SalariedNicShiftCost
                    bonusCost += shiftBonusCost
                    try:
                        hourlyWageCost += (HourlyTotalHours * HourlyHourlyCost)
                    except StandardError:
                        print ('No employees')
                    pensionCostTotal += (pensionCostHourly + pensionCostSalaried)

                    pensionCostHourly += pensionCostHourly
                    pensionCostSalaried += pensionCostSalaried

            return [SalariedTotal + SSPSalaried, hourlyWageCost + SSPHourly, nicCostTotal, bonusCost, pensionCostTotal,
                    nicCostHourly, nicCostSalaried, pensionCostHourly, pensionCostSalaried, SSPSalaried, SSPHourly]
    """

    def populateWeeklyWageInformation(self):
        # generate a list of dates within the selected week
        NumDays = 7
        dateRange = []
        for x in xrange(0, NumDays):
            dateRange.append(self.selectedDate + datetime.timedelta(days=x))

        #Calculate the wage costs for the selected date range
        self.wageReport  = reporting.reportWindowui(self.shiftsTable)
        self.wageReport.importEmpModData(self.empTable, self.salTable, self.depTable, self.bonusTable,
                                            self.holsTable,
                                            self.salorHourlyTable)

        wageData = self.wageReport.calcWageCostforDateRange(dateRange[0], dateRange[-1], 0)

        totalHourlyWages = wageData[3]
        totalSalaryWages = wageData[4]
        totalNetWages = wageData[5]
        totalNIC = wageData[6]
        totalBonus = wageData[7]
        totalPension = wageData[8]
        totalGrossSalary = wageData[9]
        totalSSP = wageData[10]

        self.ui.predWageBox.setValue(totalGrossSalary)
        self.ui.predBonusBox.setValue(totalBonus)
        self.ui.predNICBox.setValue(totalNIC)
        self.ui.predPensionBox.setValue(totalPension)
        self.ui.predHourlyBox.setValue(totalHourlyWages)
        self.ui.predSalariedBox.setValue(totalSalaryWages)
        self.ui.predSSPBox.setValue(totalSSP)

        # update wage %
        predictedRevenueTotal = self.predictedRevenueTotalAction()
        if predictedRevenueTotal == 0:
            self.ui.predWagePercBox.setValue(0)
        else:
            wageCostPercentage = (totalGrossSalary / predictedRevenueTotal) * 100
            self.ui.predWagePercBox.setValue(wageCostPercentage)

    def populateMonthToDateWageInformation(self):
        dateRange = self.generateSelectedMonthDateRange()
        # Calculate the wage costs for the selected date range

        wageData = self.wageReport.calcWageCostforDateRange(dateRange[0], dateRange[-1], 0)

        totalGrossSalary = wageData[9]

        # update wage box
        self.ui.mtdWageBox.setValue(totalGrossSalary)

        # populate wage percentage and mtd Rev
        revWindow = ActualRevWindow.ActualRevWindow(self.selectedDate)

        revenueTotal = revWindow.calculateMTDTotalRev(dateRange[0], dateRange[-1])


        self.ui.mtdRevBox.setValue(revenueTotal)
        try:
            wageCostPercentage = (totalGrossSalary / revenueTotal) * 100
            self.ui.mtdWagePercBox.setValue(wageCostPercentage)
            self.ui.mtdAvgSpendBox.setValue(revenueTotal / self.MTDCoversTotal)
        except ZeroDivisionError:
            self.ui.mtdWagePercBox.setValue(0)


    def populateDepartmentFilterCombo(self):
        combo = self.ui.departmentFilterCombo
        combo.insertItem(0, "All Staff")
        combo.insertItem(1, "Kitchen & FOH","1")
        for a in xrange(len(self.departments)):
            combo.addItem(self.departments[a][1])

    def queryPredictedCoverDBTable(self, fromDate, toDate):
        data = DB.Querydb("""SELECT * FROM PredictedCovers WHERE predCoverDate BETWEEN %s AND %s""",
                   (fromDate, toDate)).fetchAllRecordswithFormatting()
        return data

    def queryRevenueTypeDBTable(self):
        self.revenueTypes = DB.Querydb("""SELECT * from RevenueTypes""", None).fetchAllRecordswithFormatting()
        return self.revenueTypes

    def queryDepartmentDBTable(self):
        self.departments = DB.Querydb("""SELECT * FROM departments""", None).fetchAllRecordswithFormatting()

    def queryShiftTypeDBTable(self):
        self.shiftTypes = DB.Querydb("""SELECT * FROM shiftTypes""", None).fetchAllRecordswithFormatting()

    def delWeek(self):
        message = QtGui.QMessageBox.question(QtGui.QMessageBox(), 'Message', "Do you Really Want to Delete the week? This Can NOT be undone!",
                                             QtGui.QMessageBox.Yes | QtGui.QMessageBox.No, QtGui.QMessageBox.No)
        if message == QtGui.QMessageBox.Yes:
            DB.Querydb("""DELETE FROM `shifts` WHERE `Date` BETWEEN %s AND %s""",
                       (self.dateList[0], self.dateList[6])).DeleteOneExecutewithFormatting()
        self.loadRota()

    def delShifts(self):
        indexSelection = []
        shiftsToDelete = []
        for item in self.ui.tableWidget.selectedIndexes():
            indexSelection.append([item.row(), item.column()])

        # Create a tuple of ID name and date for each cell selected
        for shift in xrange(len(indexSelection)):
            self.rotaDelName = str(self.ui.tableWidget.item(indexSelection[shift][0], 0).text())
            date = str(self.dateList[indexSelection[shift][1]-1])

            # Find the ID from fetched employee info
            ID = [self.fetched[x][0] for x in xrange(len(self.fetched)) if self.fetched[x][1] in self.rotaDelName][0]

            # append cell for deleting info to one listOfEmployees for passing to SQL query
            shiftsToDelete.append([int(ID), str(date), indexSelection[shift][0], indexSelection[shift][1]])

        # if the cell that is selected is a monday update the shift with blank information to prevent the deletion of the
        # employee from the rota
        #print ('Rw.py delShift shifts to delete', shiftsToDelete)
        for a in xrange(len(shiftsToDelete)):
            if datetime.datetime.strptime(shiftsToDelete[a][1], '%Y-%m-%d').weekday() == 0:
                insertblankmonday = ShiftPopUp.ShiftPopUp(shiftsToDelete[a][3], shiftsToDelete[a][2], self.dateList, self.results2, self.shiftTypes, self.departments, shiftsToDelete[a][0])
                insertblankmonday.clearTheshiftAM()
                insertblankmonday.clearTheshiftPM()
                insertblankmonday.updateRecordinDB()

            # if the cell selected is a name cell skip
            elif shiftsToDelete[a][3] == 0:
                pass

            else:
                # if the cell is not a monday delete the shift from the DB
                insertID = shiftsToDelete[a][0]
                insertdate = shiftsToDelete[a][1]
                DB.Querydb("""DELETE FROM `shifts` WHERE `EmployeeID` = %s AND `Date` = %s""", (insertID, insertdate)).DeleteOneExecutewithFormatting()

        # Refresh and move to current cell
        self.cellrow = indexSelection[0][0]
        self.cellcoll = indexSelection[0][1]
        self.loadRota()

    def launchPrint(self):
        p = Printing.Printer()
        header = ["", ]
        for a in xrange(len(self.dateList)):
            st = """
                <p style="LINE-HEIGHT:10px;" align="center">
                <b>{}</b>
                <br>
                <b>AM&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;PM</b>
                """.format(str(datetime.date.strftime(self.dateList[a], "%a %d %b")))
                #</tbody>
                #</table>
                #</body>
            header.append(st)
        p.printTableWidgetText(self.ui.tableWidget, header)


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    # add splash screen when ready and a wait timer
    SplashPix = QtGui.QPixmap('')
    loadingSplash = QtGui.QSplashScreen(SplashPix, QtCore.Qt.WindowStaysOnTopHint)
    loadingSplash.setMask(SplashPix.mask())
    loadingSplash.show()
    app.processEvents()

    # just hack this out
    myapp = MainWindow()
    myapp.show()

    # resize rows for rota widget to include the shift type name
    myapp.ui.tableWidget.resizeRowsToContents()
    loadingSplash.finish(myapp)

    sys.exit(app.exec_())
    # to here, and un-comment bellow



    """login = LoginWindow()
    login.show()"""




    """if login.exec_() == QtGui.QDialog.Accepted:
        myapp = MainWindow()
        myapp.show()
        # resize rows for rota widget to include the shift type name
        myapp.ui.tableWidget.resizeRowsToContents()
        sys.exit(app.exec_())"""
