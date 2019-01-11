from PyQt4 import QtGui, QtCore
from reportWindow import Ui_reportingWindow
import RotaData
import WidgetTools
import DB
import datetime
import Employees
import payrollVariablePopUP
from dateutil.relativedelta import *

class reportWindowui(QtGui.QDialog):

    def __init__(self, shiftdata, parent=None):
        super(reportWindowui, self).__init__(parent)

        self.ui = Ui_reportingWindow()
        self.ui.setupUi(self)
        self.shiftdata = shiftdata
        self.setSlots()
        self.populateReportCombo()
        #self.calendar()

        # set the widget for population
        self.reportWidget = WidgetTools.TableWidgetTools()
        self.reportWidget.setWidget(self.ui.reportTableWidget)

        self.firstClick = []

        # set the date pickers to todays date
        self.ui.fromDateEdit.setDate(datetime.date.today())
        self.ui.toDateEdit.setDate(datetime.date.today())

    def calendar(self):
        self.cal = WidgetTools.calendarWidget()
        self.ui.verticalLayout.insertLayout(9, self.cal.calendarWidget)

    def fetchDates(self):
        # fetch to and from dates from date edits
        self.toDate = QtCore.QDate(self.ui.toDateEdit.date()).toPyDate()
        self.fromDate = QtCore.QDate(self.ui.fromDateEdit.date()).toPyDate()

    def setSlots(self):
        self.ui.runReportBut.clicked.connect(self.fetchDates)
        self.ui.runReportBut.clicked.connect(self.whichReport)

    def populateReportCombo(self):
        items = ['Employee Holiday Shifts', 'Holiday Totals', 'Employee Sickness shifts', 'Employee Pay']
        combo = self.ui.selectReportCombo
        for a in range(len(items)):
            combo.insertItem(a, items[a])

    def whichReport(self):
        if self.ui.selectReportCombo.currentIndex() == 0:
            self.holidayReportData()
        elif self.ui.selectReportCombo.currentIndex() == 1:
            self.holidayTotals()
        elif self.ui.selectReportCombo.currentIndex() == 2:
            print('salary report')
        elif self.ui.selectReportCombo.currentIndex() == 3:
            self.employeePayReport()

    def importEmpModData(self, empTable, salTable, depTable, bonusTable, holTable, salorHourlyTable):
        self.empTable = empTable
        self.salTable = salTable
        self.depTable = depTable
        self.bonusTable = bonusTable
        self.holTable = holTable
        self.salorHourlyTable = salorHourlyTable

        # load emp module with data
        self.emp = Employees.employees(self.empTable, self.salTable, self.depTable, self.bonusTable, self.holTable,
                                  self.salorHourlyTable)

    def dateListGenerator(self):
        self.dateList = []
        days = (self.toDate - self.fromDate).days
        for days in xrange(days+1):
            self.dateList.append(self.fromDate + relativedelta(days=+days))

    def employeePayReport(self):

        #TODO: already called in module bellow.
        self.shiftsTable = DB.Querydb("""SELECT * FROM shifts""", None).fetchAllRecordswithFormatting()
        self.rotaData = RotaData.rota(self.shiftsTable)

        empList = self.emp.salCalcEmpList(str(self.fromDate), str(self.toDate))
        reportTable = []
        payVar = payrollVariablePopUP.payrollVariablePopUp()

        self.dateListGenerator()
        for emp in xrange(len(empList)):
            empTotalSalary = 0
            empTotalHourly = 0
            nicCost = 0
            pensionCost = 0
            netSalary = 0

            for date in xrange(len(self.dateList)):
                # define the nic variables
                threshold = payVar.nicThreshold(self.dateList[date])
                age = payVar.nicMinAge(self.dateList[date])
                rate = payVar.nicRate(self.dateList[date])
                pensionPercent = payVar.pensionPecentage(self.dateList[date])

                empID = empList[emp][0]
                shiftDate = self.dateList[date]
                shiftType = self.rotaData.empAMPMshiftTypeAtdate(empID, shiftDate)
                SalariedShiftCost = self.emp.empShiftSalaryCost(shiftDate, shiftType, empID)
                SalariedNicShiftCost = self.emp.empNicCostByShiftSalary(empID, shiftDate, threshold, age, rate)
                shiftBonusCost = self.emp.empShiftBonusCost(shiftDate, empID)
                HourlyTotalHours = self.rotaData.empTotalHoursDay(empID, shiftDate, 'day')
                HourlyHourlyCost = self.emp.empShiftHourlyPay(shiftDate, empID)
                HourlyNicShiftCost = self.emp.empNicCostByShiftHourly(empID, shiftDate, threshold, age, rate)
                pensionCostHourly = self.emp.empHourlyPensionShiftCalc(empID, shiftDate, threshold, age, rate,
                                                                       pensionPercent)
                pensionCostSalaried = self.emp.empSalaryPensionShiftCalc(empID, shiftDate, threshold, age, rate,
                                                                         pensionPercent)

                nicCost += SalariedNicShiftCost + HourlyNicShiftCost
                pensionCost += pensionCostSalaried + pensionCostHourly
                netSalary += SalariedShiftCost + (HourlyTotalHours * HourlyHourlyCost)
                empTotalSalary += SalariedShiftCost + SalariedNicShiftCost + shiftBonusCost + pensionCostSalaried
                empTotalHourly += (HourlyTotalHours * HourlyHourlyCost) + HourlyNicShiftCost + pensionCostHourly

            reportTable.append(
                [empList[emp][0], empList[emp][1], '{0:.2f}'.format(nicCost), '{0:.2f}'.format(pensionCost),
                 '{0:.2f}'.format(netSalary), '{0:.2f}'.format(empTotalSalary), '{0:.2f}'.format(empTotalHourly)])

        table = WidgetTools.TableWidgetTools()
        table.setWidget(self.ui.reportTableWidget)
        table.populateTableWidget(reportTable, 7, 0)

        headerList = ['EmpID', 'Employee Name', 'NIC', 'Pension', 'Net Salary', 'Gross Salaried Pay', 'Gross Hourly Pay']
        self.ui.reportTableWidget.setHorizontalHeaderLabels(headerList)

        header = self.ui.reportTableWidget.horizontalHeader()
        header.setResizeMode(0, QtGui.QHeaderView.ResizeToContents)
        header.setResizeMode(1, QtGui.QHeaderView.ResizeToContents)
        header.setResizeMode(2, QtGui.QHeaderView.ResizeToContents)
        header.setResizeMode(3, QtGui.QHeaderView.ResizeToContents)
        header.setResizeMode(4, QtGui.QHeaderView.ResizeToContents)
        header.setResizeMode(5, QtGui.QHeaderView.ResizeToContents)
        header.setResizeMode(6, QtGui.QHeaderView.ResizeToContents)

    def holidayData(self):
        # filter shift data for only those days including holiday shifts
        D = RotaData.rota(self.shiftdata)
        self.holidayShiftData = D.shiftTypeReportData(self.fromDate, self.toDate, 2)

    def holidayReportData(self):
        self.holidayData()
        # define column header titles
        headerList = ['Shift ID', 'Employee', 'Date', 'AM Hours', 'PM Hours']

        # iterate through shifts and replace the  empID with a name
        for data in range(len(self.holidayShiftData)):
            empID = self.holidayShiftData[data][1]
            self.holidayShiftData[data][1] = self.emp.empName(empID)

        # populate the data to the table
        self.reportWidget.populateTableWidget(self.holidayShiftData, 5, 0)

        # populate the column header titles
        self.ui.reportTableWidget.setHorizontalHeaderLabels(headerList)
        # print ('hol shift data', holidayShiftData)

    def holidayTotals(self):
        self.holidayData()
        processedData = {}

        # iterate through shifts and add the name instead of the empID
        # add all names within data to dictionary
        for data in range(len(self.holidayShiftData)):
            empID = self.holidayShiftData[data][1]
            self.holidayShiftData[data][1] = self.emp.empName(empID)
            empName = self.holidayShiftData[data][1]

            # create dictionary values day | shift | hours | entitlement | remaining
            processedData['{}'.format(empName)] = [0, 0, 0, ]
            # print('hours', D.empTotalHoursPeriod(holidayShiftData[data][1], fromDate, toDate))

        # iterate through data and count the number of holidays and add to the relevant name key in dict
        for data1 in range(len(self.holidayShiftData)):
            empName = self.holidayShiftData[data1][1]
            dayCol = 0
            shiftcol = 1
            hourscol = 2
            # insert emp name into dictionary
            processedData['{}'.format(empName)][dayCol] += 1

            # if AM shift is a holiday, count and add the hours up, add to the dict
            print ('data1', self.holidayShiftData)
            if self.holidayShiftData[data1][5] == 2:
                processedData['{}'.format(empName)][shiftcol] += 1
                processedData['{}'.format(empName)][hourscol] += self.holidayShiftData[data1][3]

            # if PM shift is a holiday, count and add the hours up add to the dictionary
            if self.holidayShiftData[data1][6] == 2:
                processedData['{}'.format(empName)][shiftcol] += 1
                processedData['{}'.format(empName)][hourscol] += self.holidayShiftData[data1][4]

        # Convert the dictionary into list
        reportData = []
        for name, value in processedData.items():
            empEntitlement = self.emp.empHolidayEntitlementAtDate(self.emp.empID(name), QtCore.QDate(self.ui.fromDateEdit.date()).toPyDate())
            days = value[0]
            shifts = value[1]
            hours = value[2]
            reportData.append([name, days, shifts, hours, empEntitlement])

        print ('report data', reportData)

        # populate the converted list to the table
        self.reportWidget.populateTableWidget(reportData, 5, None)

        # define column header titles
        headerList = ['Employee', 'Days', 'Shifts', 'Hours', 'Remaining']

        # populate the column header titles
        self.ui.reportTableWidget.setHorizontalHeaderLabels(headerList)

        print ('processed data', processedData)





