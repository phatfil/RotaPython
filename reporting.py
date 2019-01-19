from PyQt4 import QtGui, QtCore
from reportWindow import Ui_reportingWindow
import RotaWindow
import RotaData
import WidgetTools
import DB
import datetime
import Employees
import payrollVariablePopUP
from dateutil.relativedelta import *
import calendar

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

        self.shiftsTable = DB.Querydb("""SELECT * FROM shifts""", None).fetchAllRecordswithFormatting()
        self.rotaData = RotaData.rota(self.shiftsTable)

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
            self.employeePayReport(self.fromDate, self.toDate)

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

    def dateRangeListGenerator(self, fromDate, toDate):
        self.dateList = []
        days = (toDate - fromDate).days
        for days in xrange(days + 1):
            self.dateList.append(fromDate + relativedelta(days=days))
        return self.dateList

    def calculateQualifyingSickPeriodsInDateRange(self, dateRange):
        #print ('date Range CQSPDR', dateRange)
        empList = self.emp.salCalcEmpList(str(dateRange[0]), str(dateRange[-1]))
        #print ('emlist CQSPDR', empList)
        QDEmpDict = {}
        firstDate = []

        # Iterate through emps
        for emp in xrange(len(empList)):
            counter = 0
            # create key for each emp in list key:[QDs, first Date]
            QDEmpDict[empList[emp][0]] = [0, None]

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
                                QDEmpDict[empList[emp][0]][0] += 1
                                QDEmpDict[empList[emp][0]][1] = firstDate
                            else:
                                pass

                        else:
                            counter = 0
                else:
                    pass


        # convert Qualifying sick totals into money and return results
        results = self.sickPayEntitlementCalc(dateRange, QDEmpDict)
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
                # run wage calc with no SSP calc to prevent loop
                report = self.calcWageCostforDateRange(SoRP, EoRP,1)[0]
                salary = report[empID][2]
                daysEmployeed = self.emp.empDaysemployedWithinDateRange(empID, SoRP, EoRP)
                avgWeekPay = ( salary / daysEmployeed) * 7


                # If average weekly wage over 8 week period is less than average Earnings limit, pass, otherwise
                # calculate day rate according to number of days worked in week and * by qualifying days
                # update relevant key in dictionary
                if avgWeekPay > lowerEarningsLimit:
                    QDEmpDict[empID][0] = ((dayRate * 7) / empDaysPerWeek) * QDs

                else:
                    pass
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

    def calcSSPCostforDateRange(self, fromDate, toDate):
        SSPdata = self.calculateQualifyingSickPeriodsInDateRange(self.dateRangeListGenerator(fromDate, toDate))
        SSPdata = SSPdata[0]
        return SSPdata

    def calcWageCostforDateRange(self, fromDate, toDate, SSP_on_off):
        SSPCheck = SSP_on_off
        dateList = self.dateRangeListGenerator(fromDate, toDate)
        empList = self.emp.salCalcEmpList(str(fromDate), str(toDate))
        reportTable = []
        reportTableINT = []
        payVar = payrollVariablePopUP.payrollVariablePopUp()

        if SSPCheck == 0:
            SSPdata = self.calcSSPCostforDateRange(fromDate, toDate)
        else:
            SSPdata = []

        for emp in xrange(len(empList)):
            empTotalSalary = 0
            empTotalHourly = 0
            nicCost = 0
            pensionCost = 0
            netSalary = 0

            if SSPCheck == 0:
                SSP = SSPdata[empList[emp][0]][0]
            else:
                SSP = 0

            for date in xrange(len(dateList)):
                # define the nic variables
                threshold = payVar.nicThreshold(dateList[date])
                age = payVar.nicMinAge(dateList[date])
                rate = payVar.nicRate(dateList[date])
                pensionPercent = payVar.pensionPecentage(dateList[date])
                empID = empList[emp][0]
                shiftDate = dateList[date]
                shiftType = self.rotaData.empAMPMshiftTypeAtdate(empID, shiftDate)
                SalariedShiftCost = self.emp.empShiftSalaryCost_ExcludingSickDays(shiftDate, shiftType, empID)
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

                if self.emp.empSalaryOrHourlyID(empID) == 0:
                    empTotalSalary += SalariedShiftCost + SalariedNicShiftCost + shiftBonusCost + pensionCostSalaried + SSP
                    empTotalHourly += (HourlyTotalHours * HourlyHourlyCost) + HourlyNicShiftCost + pensionCostHourly
                else:
                    empTotalSalary += SalariedShiftCost + SalariedNicShiftCost + shiftBonusCost + pensionCostSalaried
                    empTotalHourly += (
                                                  HourlyTotalHours * HourlyHourlyCost) + HourlyNicShiftCost + pensionCostHourly + SSP

            reportTable.append(
                [empList[emp][0], empList[emp][1], '{0:.2f}'.format(nicCost), '{0:.2f}'.format(pensionCost),
                 '{0:.2f}'.format(SSP), '{0:.2f}'.format(netSalary), '{0:.2f}'.format(empTotalSalary),
                 '{0:.2f}'.format(empTotalHourly)])

            reportTableINT.append([empList[emp][0], empList[emp][1], nicCost, pensionCost, netSalary, empTotalSalary,
                                   empTotalHourly, shiftBonusCost, SSP])

        # produce a table of salary info for each employee for SSP calc
        results = {}
        totalHourlyWages = 0
        totalSalaryWages = 0
        totalNetWages = 0
        totalNIC = 0
        totalBonus = 0
        totalPension = 0
        totalGrossSalary = 0
        totalSSP = 0

        for rec in xrange(len(reportTableINT)):
            empID = reportTable[rec][0]
            empTotalSalary = reportTableINT[rec][5]
            empTotalHourly = reportTableINT[rec][6]
            empNetSalary = reportTableINT[rec][4]
            empNICTotal = reportTableINT[rec][2]
            empBonusTotal = reportTableINT[rec][7]
            empPensionTotal = reportTableINT[rec][3]
            empSSPtotal = reportTableINT[rec][8]

            results[empID] = [empTotalSalary, empTotalHourly, empNetSalary]

            # produce totals
            totalHourlyWages += empTotalHourly
            totalSalaryWages += empTotalSalary
            totalNetWages += empNetSalary
            totalNIC += empNICTotal
            totalBonus += empBonusTotal
            totalPension += empPensionTotal
            totalGrossSalary += (empTotalHourly + empTotalSalary)
            totalSSP += empSSPtotal



        return [results, reportTable, reportTableINT, totalHourlyWages, totalSalaryWages, totalNetWages, totalNIC,
                totalBonus, totalPension, totalGrossSalary, totalSSP]

    def employeePayReport(self, fromDate, toDate):
        reportTable = self.calcWageCostforDateRange(fromDate, toDate, 0)
        table = WidgetTools.TableWidgetTools()
        table.setWidget(self.ui.reportTableWidget)
        table.populateTableWidget(reportTable[1], 8, 0)

        headerList = ['EmpID', 'Employee Name', 'NIC', 'Pension', 'SSP', 'Net Salary', 'Gross Salaried Pay', 'Gross Hourly Pay']
        self.ui.reportTableWidget.setHorizontalHeaderLabels(headerList)

        header = self.ui.reportTableWidget.horizontalHeader()
        header.setResizeMode(0, QtGui.QHeaderView.ResizeToContents)
        header.setResizeMode(1, QtGui.QHeaderView.ResizeToContents)
        header.setResizeMode(2, QtGui.QHeaderView.ResizeToContents)
        header.setResizeMode(3, QtGui.QHeaderView.ResizeToContents)
        header.setResizeMode(4, QtGui.QHeaderView.ResizeToContents)
        header.setResizeMode(5, QtGui.QHeaderView.ResizeToContents)
        header.setResizeMode(6, QtGui.QHeaderView.ResizeToContents)
        header.setResizeMode(7, QtGui.QHeaderView.ResizeToContents)

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
            #print ('data1', self.holidayShiftData)
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

        #print ('report data', reportData)

        # populate the converted list to the table
        self.reportWidget.populateTableWidget(reportData, 5, None)

        # define column header titles
        headerList = ['Employee', 'Days', 'Shifts', 'Hours', 'Remaining']

        # populate the column header titles
        self.ui.reportTableWidget.setHorizontalHeaderLabels(headerList)

        #print ('processed data', processedData)





