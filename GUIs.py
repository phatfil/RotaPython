import csv
import threading
import time

import pyximport;
from PyQt4.QtCore import pyqtSignal

import WidgetTools
from Core import *
from DBData import *
from QtUis.AddEmployeeWindowUI import Ui_AddEmpDialog
from QtUis.EmployeeinfoEntry import Ui_Employee
from QtUis.Rotav7 import Ui_MainWindow
from QtUis.ShiftPopUpWindow import Ui_ShiftPopUpWindow
from QtUis.TimePad import Ui_Dialog
from QtUis.actualRevWindowUI import Ui_ActRevWindow
from QtUis.loginwindow import Ui_LoginWindow
from QtUis.payrollVariableUI import Ui_Dialog
from QtUis.reportWindow import Ui_reportingWindow

pyximport.install()


class MainWindow(QtGui.QMainWindow):
    finished = QtCore.pyqtSignal()

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.Rota = Rota()
        self.emp = self.Rota.emp


        # load shift and department classes
        self.shiftTypesDB = ShiftTypes()
        self.departmentsDB = Departments()

        self.rotaTableWidgetFormating()
        self.setupButtonsTriggersAndCombos()

        self.scrollbarPosition = 5

        # Populate data on loading
        self.loadRota()



    def selectedDate(self, addDays):
        if addDays == 0:
            return QtCore.QDate.toPyDate(self.Rota.datetoMonday(self.ui.dateEdit.date()))
        else:
            return QtCore.QDate.toPyDate(self.Rota.datetoMonday(self.ui.dateEdit.date())+relativedelta(days=addDays))

    def setupButtonsTriggersAndCombos(self):
        # Set date selector to the Monday of current week
        Qdate = QtCore.QDate()

        wk = QtCore.QDate.weekNumber(Qdate.currentDate())
        self.ui.dateEdit.setDate(datetime.datetime.strptime(str(str(wk[1]) + '-' + str(wk[0])) + '-1', "%Y-%W-%w"))

        # set button Icon
        self.ui.todayBut.setIcon(QtGui.QIcon(':/images/dot.png'))
        self.ui.lessWeekBUT.setIcon(QtGui.QIcon(':/images/left.png'))
        self.ui.moreWeekBUT.setIcon(QtGui.QIcon(':/images/right.png'))

        # populate filter combo drop down
        self.populateDepartmentFilterCombo()

        # Monitor and filter on change of filter category
        self.ui.departmentFilterCombo.currentIndexChanged.connect(self.loadRota)

        # Other button clicks
        self.ui.tableWidget.cellDoubleClicked.connect(self.launchShiftWindow)
        self.ui.AddEmpBUT.clicked.connect(self.launchAddEmployeeWindow)
        self.ui.RemoveEmpBUT.clicked.connect(self.deleteEmployeeFromRota)
        self.ui.delShiftBUT.clicked.connect(self.delShifts)
        self.ui.deleteWeekBUT.clicked.connect(self.delWeek)
        self.ui.tabWidget.currentChanged.connect(self.loadRota)
        self.ui.addRevTypeBUT.clicked.connect(self.addNewRevenueType)
        self.ui.delRevenueTypeBUT.clicked.connect(self.delRevenueType)
        # self.ui.tabWidget.currentChanged.connect(self.wageTabSelected)

        # Week Nav buttons
        self.ui.lessWeekBUT.clicked.connect(self.decreaseDate)
        self.ui.moreWeekBUT.clicked.connect(self.increaseDate)

        # Monitor and reload data on change
        self.ui.dateEdit.dateChanged.connect(self.loadRota)
        self.ui.revenueTypeTable.currentItemChanged.connect(self.updateRevenueTypeToDB)
        # self.ui.predictedCoverTable.currentItemChanged.connect(self.updateCoverForecastToDB2)
        self.ui.predictedCoverTable.currentItemChanged.connect(self.populateCoverTotalsBoxes)
        self.ui.coverUpdateBUT.clicked.connect(self.updateCoverForecastToDB2)
        self.ui.coverUpdateBUT.clicked.connect(self.populateCoverTotalsBoxes)

        # menu item triggers
        self.ui.actionEmployee.triggered.connect(self.launchEmployeeInformationWindow)
        self.ui.actionPayroll_Variables.triggered.connect(self.launchPayrollVariableWindow)
        self.ui.actionPrint_Rota.triggered.connect(self.launchPrint)
        self.ui.actionReporting_Tool.triggered.connect(self.launchReportingToolWindow)
        self.ui.actionBudget_and_Actuals.triggered.connect(self.launchActualRevWindow)

    def populateCoverTotalsBoxes(self):
        selectedDate = self.selectedDate(0)
        firstOfYearDate = datetime.date(selectedDate.year, 1, 1)
        wkDateList = self.Rota.generateWkDateList(selectedDate)
        monthRange = self.Rota.generateSelectedMonthDateRange(selectedDate, wkDateList)

        MTDCoversTotal = self.Rota.calculatePredictedCoversTotal(monthRange[0], monthRange[-1])
        YTDcoversTotal = self.Rota.calculatePredictedCoversTotal(firstOfYearDate, monthRange[1])
        weeklyCoverTotal = self.Rota.calculatePredictedCoversTotal(wkDateList[0], wkDateList[-1])

        self.ui.MTDCoversTotalBox.setValue(MTDCoversTotal)
        self.ui.YTDCoversTotalBox.setValue(YTDcoversTotal)
        self.ui.WeeklyCoversTotal.setValue(weeklyCoverTotal)

        # print ('MTD Covers', self.MTDCoversTotal, 'st date', monthRange[0], ' fin date', monthRange[-1])

    def rotaTableWidgetFormating(self):
        # Rota table widget formating
        header = self.ui.tableWidget.horizontalHeader()
        for x in range(9):
            header.setResizeMode(x, QtGui.QHeaderView.ResizeToContents)
            header.setResizeMode(x, QtGui.QHeaderView.Stretch)

        header1 = self.ui.coverHeaderTable.horizontalHeader()
        for x in range(9):
            header1.setResizeMode(x, QtGui.QHeaderView.Stretch)


        covs = self.ui.predictedCoverTable.horizontalHeader()
        for x in range(1, 14):
            covs.setResizeMode(x, QtGui.QHeaderView.ResizeToContents)

        self.setGeometry(200, 200, 1255, 500)
        self.ui.tabWidget.setCurrentIndex(0)

    def launchActualRevWindow(self):
        selectedDate = self.selectedDate(0)
        revWindow = ActualRevWindow(selectedDate)
        revWindow.exec_()

    def launchEmployeeInformationWindow(self):
        # TODO: think this through, currently + and - 5 year from selected date
        selectedDate = self.selectedDate(0)
        toDate = datetime.date.strftime(selectedDate + relativedelta(years=5), '%Y-%m-%d')
        fromDate = datetime.date.strftime(selectedDate - relativedelta(years=5), '%Y-%m-%d')

        print (fromDate, toDate)
        empPopUp = EmployeeInformationWindow(fromDate, toDate)
        empPopUp.trigger.connect(self.loadRota)
        empPopUp.exec_()

    def rotaRowCount(self):
        rows = self.ui.tableWidget.rowCount()
        return rows

    def rotaWhichColSelected(self):
        selectedColl = self.ui.tableWidget.currentColumn()
        return selectedColl

    def rotaWhichRowSelected(self):
        selectedRow = self.ui.tableWidget.currentRow()
        return selectedRow

    def verticalScrollBarPosition(self):
        scrollbarPosition = self.ui.tableWidget.verticalScrollBar().value()
        return scrollbarPosition

    def launchShiftWindow(self):
        # Determine which cell has been selected
        cellcoll = self.rotaWhichColSelected()
        cellrow = self.rotaWhichRowSelected()

        # Determine return position for scroll bar
        self.scrollbarPosition = self.ui.tableWidget.verticalScrollBar().value()

        # Determine if the shift is within Employee start and finish dates
        selectedDate = self.selectedDate(0)
        wkDateList = self.Rota.generateWkDateList(selectedDate)
        shiftDate = wkDateList[int(cellcoll) - 1]

        selectedDepartment = self.whichDepartmentFilterIsSelected()

        #TODO: Make sure this is the best way to do this
        results = self.Rota.convertDBdata(selectedDepartment, wkDateList)

        empID = results[cellrow][8]

        if cellcoll == 0:
            pass
        else:
            if shiftDate < self.emp.empStartDate(empID):
                msgbox = QtGui.QMessageBox()
                msgbox.setWindowTitle("Warning")
                msgbox.setText(
                    "{} Doesn't Start until {}".format(self.emp.empName(empID), self.emp.empStartDate(empID)))
                msgbox.exec_()
            elif str(shiftDate) > str(self.emp.empFinishDate(empID)):
                msgbox = QtGui.QMessageBox()
                msgbox.setWindowTitle("Warning")
                msgbox.setText("{} Finished on {}".format(self.emp.empName(empID), self.emp.empFinishDate(empID)))
                msgbox.exec_()
            else:
                # load variable into instance of shift popup window
                pop = ShiftWindow(cellcoll, cellrow, wkDateList,
                                  results, self.shiftTypesDB.select_All(), self.departmentsDB.select_All(), empID)
                # Show shift pop window
                pop.show()
                pop.trigger.connect(self.loadRota)

    def launchAddEmployeeWindow(self):
        rows = self.ui.tableWidget.rowCount()
        dateList = self.Rota.generateWkDateList(self.selectedDate(0))
        exisitingNames = []
        for row in range(0, rows):
            exisitingNames.append(str(self.ui.tableWidget.item(row, 0).text()))

        # launch add employee window
        names = AddEmployeeWindow(dateList, exisitingNames)
        names.show()
        names.trigger.connect(self.addEmployeestoRota)

    def launchPayrollVariableWindow(self):
        self.payrollVarPopUp = payrollVariableWindow()
        self.payrollVarPopUp.show()

    def launchReportingToolWindow(self):
        self.reportingTool = reportWindow()
        self.reportingTool.show()

    @QtCore.pyqtSlot(int)
    def loadRota(self):
        self.Rota.refreshAndReloadEmpClass()
        self.setColumnDateLabels()
        self.populateRotaTableWidget()
        self.populatePredictiveCoverTableWidget()
        self.populateRevenueTypeTable()
        self.populatePredictedRevenueTotal()
        self.populateAvgSpendTotal()
        self.PopulateRotaCoversTotals()
        self.populateCoverTotalsBoxes()

        # if wage tab is selected, calculate the wage information
        if self.ui.tabWidget.currentIndex() == 1:
            splash_pix = QtGui.QPixmap('')#:/images/splash.png
            splash = QtGui.QSplashScreen(splash_pix, QtCore.Qt.WindowStaysOnTopHint)
            # splash.setMask(splash_pix.mask())
            splash.show()

            loop = QtCore.QEventLoop()
            self.finished.connect(loop.quit)
            threading.Thread(target=self.populateWeeklyWageInformation).start()
            threading.Thread(target=self.populateMonthToDateWageInformation).start()
            loop.exec_()

            splash.finish(self.ui.wageTab)
            # splash.close()
        else:
            pass

        self.repositionViewAfterUpdate()

    def repositionViewAfterUpdate(self):
        cellrow = self.rotaWhichRowSelected()
        cellcol = self.rotaWhichColSelected()

        slider = self.ui.tableWidget.verticalScrollBar()
        slider.setValue(self.scrollbarPosition)
        self.ui.tableWidget.setCurrentCell(cellrow, cellcol)

    def increaseDate(self):
        self.ui.dateEdit.setDate(QtCore.QDate.addDays(self.ui.dateEdit.date(), 7))
        self.loadRota()

    def decreaseDate(self):
        self.ui.dateEdit.setDate(QtCore.QDate.addDays(self.ui.dateEdit.date(), -7))
        self.loadRota()

    def setColumnDateLabels(self):
        selectedDate = self.selectedDate(0)
        # Set column headers to relevant dates

        blank = self.ui.coverHeaderTable.horizontalHeaderItem(0)
        blank.setText("")
        mondaydate = self.ui.coverHeaderTable.horizontalHeaderItem(1)
        mondaydate.setText(datetime.date.strftime(selectedDate, "%a %d %B"))
        tuedaydate = self.ui.coverHeaderTable.horizontalHeaderItem(2)
        tuedaydate.setText(datetime.date.strftime(selectedDate + relativedelta(days=1), "%a %d %B"))
        wednesdaydate = self.ui.coverHeaderTable.horizontalHeaderItem(3)
        wednesdaydate.setText(datetime.date.strftime(selectedDate + relativedelta(days=2), "%a %d %B"))
        thursdaydate = self.ui.coverHeaderTable.horizontalHeaderItem(4)
        thursdaydate.setText(datetime.date.strftime(selectedDate + relativedelta(days=3), "%a %d %B"))
        fridaydate = self.ui.coverHeaderTable.horizontalHeaderItem(5)
        fridaydate.setText(datetime.date.strftime(selectedDate + relativedelta(days=4), "%a %d %B"))
        satdaydate = self.ui.coverHeaderTable.horizontalHeaderItem(6)
        satdaydate.setText(datetime.date.strftime(selectedDate + relativedelta(days=5), "%a %d %B"))
        sundaydate = self.ui.coverHeaderTable.horizontalHeaderItem(7)
        sundaydate.setText(datetime.date.strftime(selectedDate + relativedelta(days=6), "%a %d %B"))

    def populateRotaTableWidget(self):
        selectedDepartment = self.whichDepartmentFilterIsSelected()
        dateList = self.Rota.generateWkDateList(self.selectedDate(0))
        results = self.Rota.convertDBdata(selectedDepartment, dateList)
        pop = WidgetTools.TableWidgetTools()
        pop.setWidget(self.ui.tableWidget)
        pop.populateRotaTableWidgetHTML(results, 8, None, self.shiftTypesDB.select_All(), self.departmentsDB.select_All())

    def namesCurrentlyOnRota(self):
        rows = self.rotaRowCount()
        exisitingNames = []
        for row in range(0, rows):
            exisitingNames.append(str(self.ui.tableWidget.item(row, 0).text()))
        return exisitingNames

    def addEmployeestoRota(self):
        # insert selected names from add employee window to database
        dateList = self.Rota.generateWkDateList(self.selectedDate(0))
        exisitingNames = self.namesCurrentlyOnRota()
        empNames = AddEmployeeWindow(dateList, exisitingNames)
        selectionList = empNames.whichCellsHaveIselected()
        selectedDate = self.selectedDate(0)
        self.Rota.addEmpToRota(selectionList, selectedDate)
        self.loadRota()

    def deleteEmployeeFromRota(self):
        # Remove employee and shifts from current week
        selectedDepartment = self.whichDepartmentFilterIsSelected()
        row = self.rotaWhichRowSelected()
        dateList = self.Rota.generateWkDateList(self.selectedDate(0))
        shiftData = self.Rota.convertDBdata(selectedDepartment, dateList)
        empName = shiftData[row][0]
        empID = shiftData[row][8]

        message = QtGui.QMessageBox.question(QtGui.QMessageBox(), 'Message', "Do you Really Want to Delete {}"
                                             .format(empName), QtGui.QMessageBox.Yes | QtGui.QMessageBox.No,
                                             QtGui.QMessageBox.No)
        if message == QtGui.QMessageBox.Yes:
            self.Rota.deleteEmpFromRota(empID, dateList)
            self.loadRota()
        else:
            print('Done')

    def whichDepartmentFilterIsSelected(self):
        depSelected = self.ui.departmentFilterCombo.currentText()
        return depSelected

    def populatePredictiveCoverTableWidget(self):
        # Extract from DB and
        # populate the Cover Forecast table
        dateList = self.Rota.generateWkDateList(self.selectedDate(0))

        self.ui.monDateLBL.setText(str(dateList[0]))
        self.ui.tueDateLBL.setText(str(dateList[1]))
        self.ui.wedDateLBL.setText(str(dateList[2]))
        self.ui.thurDateLBL.setText(str(dateList[3]))
        self.ui.friDateLBL.setText(str(dateList[4]))
        self.ui.satDateLBL.setText(str(dateList[5]))
        self.ui.sunDateLBL.setText(str(dateList[6]))

        # Clear Table
        self.ui.predictedCoverTable.clearContents()

        predCoverDB =  PredictedCovers()
        predcov = predCoverDB.predCoverDateRange(dateList[0], dateList[6])

        revTypesDB = RevenueTypes()
        revenueTypes =  revTypesDB.select_All()

        # reset table widget
        self.ui.predictedCoverTable.setRowCount(0)

        # populate the rev types into the first col
        for row in range(0, len(revenueTypes)):
            self.ui.predictedCoverTable.insertRow(row)
            record = (revenueTypes[row][0], revenueTypes[row][1])
            newitem = QtGui.QTableWidgetItem(str(record[1]))
            self.ui.predictedCoverTable.setItem(row, 0, newitem)

            # populate am and pm shifts
            for rec in range(0, len(predcov)):  # iterate through predicted covers
                if predcov[rec][4] == record[0]:  # match the revenue type to the row
                    for d in range(1, len(dateList) + 1):  # iterate through selected dates
                        if predcov[rec][1] == dateList[d - 1]:  # match the date to the column
                            AM = QtGui.QTableWidgetItem(str(predcov[rec][2]))  # fetch am data
                            PM = QtGui.QTableWidgetItem(str(predcov[rec][3]))  # fetch PM data
                            self.ui.predictedCoverTable.setItem(row, (d * 2) - 1, AM)  # write AM data
                            self.ui.predictedCoverTable.setItem(row, d * 2, PM)  # write PM data

        self.ui.predictedCoverTable.resizeRowsToContents()

    def updateCoverForecastToDB2(self):
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

        convertedTableExtract = []

        for revType in range(len(tableExtract)):
            revTypeID = [revID for revID, revName, DryAM, DryPM, WetAM, WetPM in revenueTypes if
                         revName == tableExtract[revType][0]]
            counter1 = 1
            counter2 = 2
            for date in range(len(dateRange)):
                convertedTableExtract.append(
                    [dateRange[date], tableExtract[revType][date + counter1], tableExtract[revType][date + counter2],
                     revTypeID[0],
                     dateRange[date], tableExtract[revType][date + counter1], tableExtract[revType][date + counter2],
                     revTypeID[0]])
                counter1 += 1
                counter2 += 1

        Querydb(''' INSERT INTO PredictedCovers (predCoverDate, predCoverAM, predCoverPM, revenueTypeID)
                                       VALUE (%s, %s, %s, %s) ON DUPLICATE KEY UPDATE predCoverDate = %s, 
                                       predCoverAM = %s, predCoverPM = %s, revenueTypeID = %s;''',
                         convertedTableExtract).InsertManyExecutewithFormatting()

        # calculate and populate predicted revenue
        self.populatePredictedRevenueTotal()

        # calculate and populate predicted cover totals
        self.PopulateRotaCoversTotals()

        # Calculate and populate predicted average spend total
        self.populateAvgSpendTotal()

    def loadRevenueTypesDB(self):
        self.revenueTypeDB = RevenueTypes()
        revenueTypes = self.revenueTypeDB.select_All()
        return revenueTypes

    def populateRevenueTypeTable(self):
        revenueTypes = self.loadRevenueTypesDB()
        pop = WidgetTools.TableWidgetTools()
        pop.setWidget(self.ui.revenueTypeTable)
        pop.populateTableWidget(revenueTypes, 6, 0)
        self.ui.revenueTypeTable.setHorizontalHeaderLabels(["", "Rev Type", "SPH AM", "SPH PM", "SCPH AM", "SCPH PM"])

    def updateRevenueTypeToDB(self):
        update = WidgetTools.TableWidgetTools()
        update.setWidget(self.ui.revenueTypeTable)
        data = update.extraWidgetDataToList(True)
        self.Rota.updateRevenueTypesToDB(data)
        self.populatePredictiveCoverTableWidget()

    def addNewRevenueType(self):
        self.Rota.addNewRevenueType_blank()
        self.populateRevenueTypeTable()

    def delRevenueType(self):
        widget = WidgetTools.TableWidgetTools()
        widget.setWidget(self.ui.revenueTypeTable)
        revTypeID = widget.IDfromSelectedRow()

        message = QtGui.QMessageBox.question(QtGui.QMessageBox(), 'Message',
                                             "Do you Really Want to Delete this Revenue "
                                             "Type. All associated data will be lost"
                                             , QtGui.QMessageBox.Yes | QtGui.QMessageBox.No,
                                             QtGui.QMessageBox.No)

        if message == QtGui.QMessageBox.Yes:
            error = "Please Select Revenue Type"
            self.Rota.deleteRevenueType(revTypeID, error)
            self.populateRevenueTypeTable()
            self.populatePredictiveCoverTableWidget()
        else:
            pass

    def populatePredictedRevenueTotal(self):
        dateList = self.Rota.generateWkDateList(self.selectedDate(0))
        predictedRevenueTotal = self.Rota.calculatePredictedRevenueTotal(dateList[0], dateList[6])
        self.ui.predRevBox.setValue(predictedRevenueTotal)

    def PopulateRotaCoversTotals(self):
        predCoverDB = self.Rota.predCoverDB
        dateList = self.Rota.generateWkDateList(self.selectedDate(0))
        coversdata = predCoverDB.predCoverDateRange(dateList[0], dateList[6])
        predictedCoverTotal = sum([am + pm for (ID, date, am, pm, rev) in coversdata])

        monamcov = str(sum([am for (ID, date, am, pm, rev) in coversdata if date == dateList[0]]))
        monpmcov = str(sum([pm for (ID, date, am, pm, rev) in coversdata if date == dateList[0]]))
        tueamcov = str(sum([am for (ID, date, am, pm, rev) in coversdata if date == dateList[1]]))
        tuepmcov = str(sum([pm for (ID, date, am, pm, rev) in coversdata if date == dateList[1]]))
        wedamcov = str(sum([am for (ID, date, am, pm, rev) in coversdata if date == dateList[2]]))
        wedpmcov = str(sum([pm for (ID, date, am, pm, rev) in coversdata if date == dateList[2]]))
        thuramcov = str(sum([am for (ID, date, am, pm, rev) in coversdata if date == dateList[3]]))
        thurpmcov = str(sum([pm for (ID, date, am, pm, rev) in coversdata if date == dateList[3]]))
        friamcov = str(sum([am for (ID, date, am, pm, rev) in coversdata if date == dateList[4]]))
        fripmcov = str(sum([pm for (ID, date, am, pm, rev) in coversdata if date == dateList[4]]))
        satamcov = str(sum([am for (ID, date, am, pm, rev) in coversdata if date == dateList[5]]))
        satpmcov = str(sum([pm for (ID, date, am, pm, rev) in coversdata if date == dateList[5]]))
        sunamcov = str(sum([am for (ID, date, am, pm, rev) in coversdata if date == dateList[6]]))
        sunpmcov = str(sum([pm for (ID, date, am, pm, rev) in coversdata if date == dateList[6]]))

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

    def populateAvgSpendTotal(self):
        dateList = self.Rota.generateWkDateList(self.selectedDate(0))
        fromDate = dateList[0]
        toDate = dateList[6]
        predictedRevenueTotal = self.Rota.calculatePredictedRevenueTotal(fromDate, toDate)
        predictedCoverTotal = self.Rota.calculatePredictedCoversTotal(fromDate, toDate)

        # Calculate the average spend for the week and populate the box, if no predicted revenue return 0
        if predictedCoverTotal != 0:
            self.ui.predAvgSpendBox.setValue(predictedRevenueTotal / predictedCoverTotal)
        else:
            self.ui.predAvgSpendBox.setValue(0)

    def populateWeeklyWageInformation(self):
        dateList = self.Rota.generateWkDateList(self.selectedDate(0))
        fromDate = dateList[0]
        toDate = dateList[-1]

        # Calculate the wage costs for the selected date range
        wageData = self.Rota.calcWageCostforDateRange(fromDate, toDate, 0)

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
        predictedRevenueTotal = self.Rota.calculatePredictedRevenueTotal(fromDate, toDate)
        if predictedRevenueTotal == 0:
            self.ui.predWagePercBox.setValue(0)
        else:
            wageCostPercentage = (totalGrossSalary / predictedRevenueTotal) * 100
            self.ui.predWagePercBox.setValue(wageCostPercentage)

        # call finished signal in threading loop of LoadRota
        self.finished.emit()

    def populateMonthToDateWageInformation(self):
        wkDateList = self.Rota.generateWkDateList(self.selectedDate(0))
        # generate list MTD dates
        dateRange = self.Rota.generateSelectedMonthDateRange(self.selectedDate(0), wkDateList)
        wageData = self.Rota.calcWageCostforDateRange(dateRange[0], dateRange[-1], 0)
        totalGrossSalary = wageData[9]

        # update wage box
        self.ui.mtdWageBox.setValue(totalGrossSalary)

        # populate wage percentage and mtd Rev
        revenueTotal = self.Rota.calculateMTDTotalRev(dateRange[0], dateRange[-1])

        self.ui.mtdRevBox.setValue(revenueTotal)
        try:
            wageCostPercentage = (totalGrossSalary / revenueTotal) * 100
            self.ui.mtdWagePercBox.setValue(wageCostPercentage)
            self.ui.mtdAvgSpendBox.setValue(revenueTotal / self.Rota.calculatePredictedCoversTotal(dateRange[0], dateRange[-1]))
        except ZeroDivisionError:
            self.ui.mtdWagePercBox.setValue(0)

        # call finished signal in threading loop of LoadRota
        self.finished.emit()

    def populateDepartmentFilterCombo(self):
        combo = self.ui.departmentFilterCombo
        combo.insertItem(0, "All Staff")
        combo.insertItem(1, "Kitchen & FOH", "1")
        departments = self.departmentsDB.select_All()
        for a in range(len(departments)):
            combo.addItem(departments[a][1])

    def delWeek(self):
        dateList = self.Rota.generateWkDateList(self.selectedDate(0))
        message = QtGui.QMessageBox.question(QtGui.QMessageBox(), 'Message',
                                             "Do you Really Want to Delete the week? This Can NOT be undone!",
                                             QtGui.QMessageBox.Yes | QtGui.QMessageBox.No, QtGui.QMessageBox.No)
        if message == QtGui.QMessageBox.Yes:
            self.Rota.deleteDateRangefromRota(dateList[0], dateList[-1])
        self.loadRota()

    def delShifts(self):
        indexSelection = []
        shiftsToDelete = []
        for item in self.ui.tableWidget.selectedIndexes():
            indexSelection.append([item.row(), item.column()])

        # Create a tuple of ID name and date for each cell selected
        for shift in range(len(indexSelection)):
            self.rotaDelName = str(self.ui.tableWidget.item(indexSelection[shift][0], 0).text())
            date = str(self.dateList[indexSelection[shift][1] - 1])

            # Find the ID from fetched employee info
            ID = [self.fetched[x][0] for x in range(len(self.fetched)) if self.fetched[x][1] in self.rotaDelName][0]

            # append cell for deleting info to one listOfEmployees for passing to SQL query
            shiftsToDelete.append([int(ID), str(date), indexSelection[shift][0], indexSelection[shift][1]])

        # if the cell that is selected is a monday update the shift with blank information to prevent the deletion of the
        # employee from the rota
        # print ('Rw.py delShift shifts to delete', shiftsToDelete)
        for a in range(len(shiftsToDelete)):
            if datetime.datetime.strptime(shiftsToDelete[a][1], '%Y-%m-%d').weekday() == 0:
                insertblankmonday = ShiftWindow(shiftsToDelete[a][3], shiftsToDelete[a][2], self.dateList,
                                                self.results, self.shiftTypes, self.departments,
                                                shiftsToDelete[a][0])
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
                Querydb("""DELETE FROM `shifts` WHERE `EmployeeID` = %s AND `Date` = %s""",
                                 (insertID, insertdate)).DeleteOneExecutewithFormatting()

        # Refresh and move to current cell
        self.cellrow = indexSelection[0][0]
        self.cellcoll = indexSelection[0][1]
        self.loadRota()

    def launchPrint(self):
        p = PrintingWindow.Printer()
        header = ["", ]
        for a in range(len(self.dateList)):
            st = """
                <p style="LINE-HEIGHT:10px;" align="center">
                <b>{}</b>
                <br>
                <b>AM&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;PM</b>
                """.format(str(datetime.date.strftime(self.dateList[a], "%a %d %b")))
            # </tbody>
            # </table>
            # </body>
            header.append(st)
        p.printTableWidgetText(self.ui.tableWidget, header)


class ShiftWindow(QtGui.QDialog, QtGui.QLabel):
    trigger = pyqtSignal()
    senderBUT = str()
    def __init__(self, cellcol, cellrow, dateList, results, shiftTypes, departments, empID):
        super(ShiftWindow, self).__init__()

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
        ShiftWindow.populatesVariablesfromMain(self)

        # 2 Query DB and populate class variables
        ShiftWindow.queryShiftandEmployeeTbl(self)

        # 2.1 Query Emp Class Tables
        self.queryEmpClassTables()

        # 2.2 define emp class
        self.emp = employees()

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
            ShiftWindow.buttonDectoTimeConvertion(self)

            # 7 Set buttons to relevant times
            ShiftWindow.writeTimetoButton(self)

            # 8 Concatenate the fetched times
            ShiftWindow.concatenateShiftEngine(self)

            # 9 Calculate Total Hours
            ShiftWindow.calculateHours(self)

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
            data = Querydb('''
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
        self.empTable = Querydb("""SELECT * FROM Employee_TBL""", None).fetchAllRecordswithFormatting()
        self.salTable = Querydb("""SELECT * FROM Salary""", None).fetchAllRecordswithFormatting()
        self.depTable = Querydb("""SELECT * FROM departments""", None).fetchAllRecordswithFormatting()
        self.bonusTable = Querydb("""SELECT * FROM Bonus""", None).fetchAllRecordswithFormatting()
        self.holsTable = Querydb("""SELECT * FROM HolidayEntitlement""", None).fetchAllRecordswithFormatting()
        self.salorHourlyTable = Querydb("""SELECT * FROM salorHourlyTable""", None).fetchAllRecordswithFormatting()

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

        ShiftWindow.buttonDectoTimeConvertion(self)
        ShiftWindow.writeTimetoButton(self)
        ShiftWindow.concatenateShiftEngine(self)
        ShiftWindow.calculateHours(self)

    def clearTheshiftPM(self):
        self.StPM = int()
        self.FinPM = int()
        self.BrkPM = int()
        self.uip.PmShiftTypeCombo.setCurrentIndex(0)

        ShiftWindow.buttonDectoTimeConvertion(self)
        ShiftWindow.writeTimetoButton(self)
        ShiftWindow.concatenateShiftEngine(self)
        ShiftWindow.calculateHours(self)

    def retrieveAutoShiftTimes(self):
        auto = Querydb("SELECT * FROM AutoShiftTimes", None).fetchAllRecordswithFormatting()
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

        self.fetched = Querydb('''
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
        self.pad = TimePadWindow.TimePadPopUp(self.StAM, self.FinAM, self.BrkAM, self.StPM, self.FinPM, self.BrkPM)
        self.pad.show()
        self.pad.uip.setBut.clicked.connect(self.timePadSetBUTClicked)

    def timePadSetBUTClicked(self):
        # use Button clicked sender information to assign info to relevant variable from Time pad
        if str(self.senderBUT[0:-3]) == "StAM":
            self.StAM = TimePadWindow.TimePadPopUp.a
        elif str(self.senderBUT[0:-3]) == "FinAM":
            self.FinAM = TimePadWindow.TimePadPopUp.a
        elif str(self.senderBUT[0:-3]) == "BrkAM":
            self.BrkAM = TimePadWindow.TimePadPopUp.a
        elif str(self.senderBUT[0:-3]) == "StPM":
            self.StPM = TimePadWindow.TimePadPopUp.a
        elif str(self.senderBUT[0:-3]) == "FinPM":
            self.FinPM = TimePadWindow.TimePadPopUp.a
        elif str(self.senderBUT[0:-3]) == "BrkPM":
            self.BrkPM = TimePadWindow.TimePadPopUp.a

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
        Querydb('''
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
        Querydb('''
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


            Querydb('''UPDATE AutoShiftTimes
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


class TimePadWindow(QtGui.QDialog):
    a = float()  # Total hours counter variable
    #sender = str()

    def __init__(self, StAM, FinAM, BrkAM, StPM, FinPM, BrkPM):
        super(TimePadWindow, self).__init__()
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
        TimePadWindow.a = + 0
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
        self.sender = ShiftWindow.ShiftPopUp.senderBUT
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
            TimePadWindow.a = TimePadWindow.a + 1
        elif self.uip.pushButton1.isChecked() is False:  # If button is unchecked decrease counter by 1
            TimePadWindow.a = TimePadWindow.a - 1
        print(TimePadWindow.a)

    def Button2(self):
        if self.uip.pushButton2.isChecked() is True:
            TimePadWindow.a = TimePadWindow.a + 2
        elif self.uip.pushButton2.isChecked() is False:
            TimePadWindow.a = TimePadWindow.a - 2
        print(TimePadWindow.a)

    def Button3(self):
        if self.uip.pushButton3.isChecked() is True:
            TimePadWindow.a = TimePadWindow.a + 3
        elif self.uip.pushButton3.isChecked() is False:
            TimePadWindow.a = TimePadWindow.a - 3
        print(TimePadWindow.a)

    def Button4(self):
        if self.uip.pushButton4.isChecked() is True:
            TimePadWindow.a = TimePadWindow.a + 4
        elif self.uip.pushButton4.isChecked() is False:
            TimePadWindow.a = TimePadWindow.a - 4
        print(TimePadWindow.a)

    def Button5(self):
        if self.uip.pushButton5.isChecked() is True:
            TimePadWindow.a = TimePadWindow.a + 5
        elif self.uip.pushButton5.isChecked() is False:
            TimePadWindow.a = TimePadWindow.a - 5
        print(TimePadWindow.a)

    def Button6(self):
        if self.uip.pushButton6.isChecked() is True:
            TimePadWindow.a = TimePadWindow.a + 6
        elif self.uip.pushButton6.isChecked() is False:
            TimePadWindow.a = TimePadWindow.a - 6
        print(TimePadWindow.a)

    def Button7(self):
        if self.uip.pushButton7.isChecked() is True:
            TimePadWindow.a = TimePadWindow.a + 7
        elif self.uip.pushButton7.isChecked() is False:
            TimePadWindow.a = TimePadWindow.a - 7
        print(TimePadWindow.a)

    def Button8(self):
        if self.uip.pushButton8.isChecked() is True:
            TimePadWindow.a = TimePadWindow.a + 8
        elif self.uip.pushButton8.isChecked() is False:
            TimePadWindow.a = TimePadWindow.a - 8
        print(TimePadWindow.a)

    def Button9(self):
        if self.uip.pushButton9.isChecked() is True:
            TimePadWindow.a = TimePadWindow.a + 9
        elif self.uip.pushButton9.isChecked() is False:
            TimePadWindow.a = TimePadWindow.a - 9
        print(TimePadWindow.a)

    def Button10(self):
        if self.uip.pushButton10.isChecked() is True:
            TimePadWindow.a = TimePadWindow.a + 10
        elif self.uip.pushButton10.isChecked() is False:
            TimePadWindow.a = TimePadWindow.a - 10
        print(TimePadWindow.a)

    def Button11(self):
        if self.uip.pushButton11.isChecked() is True:
            TimePadWindow.a = TimePadWindow.a + 11
        elif self.uip.pushButton11.isChecked() is False:
            TimePadWindow.a = TimePadWindow.a - 11
        print(TimePadWindow.a)

    def Button12(self):
        if self.uip.pushButton12.isChecked() is True:
            TimePadWindow.a = TimePadWindow.a + 12
        elif self.uip.pushButton12.isChecked() is False:
            TimePadWindow.a = TimePadWindow.a - 12
        print(TimePadWindow.a)

    def Button13(self):
        if self.uip.pushButton13.isChecked() is True:
            TimePadWindow.a = TimePadWindow.a + 13
        elif self.uip.pushButton13.isChecked() is False:
            TimePadWindow.a = TimePadWindow.a - 13
        print(TimePadWindow.a)

    def Button14(self):
        if self.uip.pushButton14.isChecked() is True:
            TimePadWindow.a = TimePadWindow.a + 14
        elif self.uip.pushButton14.isChecked() is False:
            TimePadWindow.a = TimePadWindow.a - 14
        print(TimePadWindow.a)

    def Button15(self):
        if self.uip.pushButton15.isChecked() is True:
            TimePadWindow.a = TimePadWindow.a + 15
        elif self.uip.pushButton15.isChecked() is False:
            TimePadWindow.a = TimePadWindow.a - 15
        print(TimePadWindow.a)

    def Button16(self):
        if self.uip.pushButton16.isChecked() is True:
            TimePadWindow.a = TimePadWindow.a + 16
        elif self.uip.pushButton16.isChecked() is False:
            TimePadWindow.a = TimePadWindow.a - 16
        print(TimePadWindow.a)

    def Button17(self):
        if self.uip.pushButton17.isChecked() is True:
            TimePadWindow.a = TimePadWindow.a + 17
        elif self.uip.pushButton17.isChecked() is False:
            TimePadWindow.a = TimePadWindow.a - 17
        print(TimePadWindow.a)

    def Button18(self):
        if self.uip.pushButton18.isChecked() is True:
            TimePadWindow.a = TimePadWindow.a + 18
        elif self.uip.pushButton18.isChecked() is False:
            TimePadWindow.a = TimePadWindow.a - 18
        print(TimePadWindow.a)

    def Button19(self):
        if self.uip.pushButton19.isChecked() is True:
            TimePadWindow.a = TimePadWindow.a + 19
        elif self.uip.pushButton19.isChecked() is False:
            TimePadWindow.a = TimePadWindow.a - 19
        print(TimePadWindow.a)

    def Button20(self):
        if self.uip.pushButton20.isChecked() is True:
            TimePadWindow.a = TimePadWindow.a + 20
        elif self.uip.pushButton20.isChecked() is False:
            TimePadWindow.a = TimePadWindow.a - 20
        print(TimePadWindow.a)

    def Button21(self):
        if self.uip.pushButton21.isChecked() is True:
            TimePadWindow.a = TimePadWindow.a + 21
        elif self.uip.pushButton21.isChecked() is False:
            TimePadWindow.a = TimePadWindow.a - 21
        print(TimePadWindow.a)

    def Button22(self):
        if self.uip.pushButton22.isChecked() is True:
            TimePadWindow.a = TimePadWindow.a + 22
        elif self.uip.pushButton22.isChecked() is False:
            TimePadWindow.a = TimePadWindow.a - 22
        print(TimePadWindow.a)

    def Button23(self):
        if self.uip.pushButton23.isChecked() is True:
            TimePadWindow.a = TimePadWindow.a + 23
        elif self.uip.pushButton23.isChecked() is False:
            TimePadWindow.a = TimePadWindow.a - 23
        print(TimePadWindow.a)

    def Button24(self):
        if self.uip.pushButton24.isChecked() is True:
            TimePadWindow.a = TimePadWindow.a + 24
        elif self.uip.pushButton24.isChecked() is False:
            TimePadWindow.a = TimePadWindow.a - 24
        print(TimePadWindow.a)

    def Button25(self):
        if self.uip.pushButton25.isChecked() is True:
            TimePadWindow.a = TimePadWindow.a + 25
        elif self.uip.pushButton25.isChecked() is False:
            TimePadWindow.a = TimePadWindow.a - 25
        print(TimePadWindow.a)

    def Button26(self):
        if self.uip.pushButton26.isChecked() is True:
            TimePadWindow.a = TimePadWindow.a + 26
        elif self.uip.pushButton26.isChecked() is False:
            TimePadWindow.a = TimePadWindow.a - 26
        print(TimePadWindow.a)

    def Button0015(self):
        if self.uip.pushButton0015.isChecked() is True:
            TimePadWindow.a = TimePadWindow.a + 0.25
        elif self.uip.pushButton0015.isChecked() is False:
            TimePadWindow.a = TimePadWindow.a - 0.25
        print(TimePadWindow.a)

    def Button0030(self):
        if self.uip.pushButton0030.isChecked() is True:
            TimePadWindow.a = TimePadWindow.a + 0.5
        elif self.uip.pushButton0030.isChecked() is False:
            TimePadWindow.a = TimePadWindow.a - 0.5
        print(TimePadWindow.a)

    def Button0045(self):
        if self.uip.pushButton0045.isChecked() is True:
            TimePadWindow.a = TimePadWindow.a + 0.75
        elif self.uip.pushButton0045.isChecked() is False:
            TimePadWindow.a = TimePadWindow.a - 0.75
        print(TimePadWindow.a)

    def Button0000(self):
        if self.uip.pushButton0000.isChecked() is True:
            TimePadWindow.a = TimePadWindow.a + 0.0
        elif self.uip.pushButton0000.isChecked() is False:
            TimePadWindow.a = TimePadWindow.a - 0.0
        print(TimePadWindow.a)

class reportWindow(QtGui.QDialog):

    def __init__(self, parent=None):
        super(reportWindow, self).__init__(parent)

        self.ui = Ui_reportingWindow()
        self.ui.setupUi(self)

        self.emp = Core.employees()

        self.shiftdata = Querydb("""SELECT * FROM shifts""", None).fetchAllRecordswithFormatting()
        self.setSlots()
        self.populateReportCombo()

        # set the widget for population
        self.reportWidget = WidgetTools.TableWidgetTools()
        self.reportWidget.setWidget(self.ui.reportTableWidget)

        self.firstClick = []

        # set the date pickers to todays date
        self.ui.fromDateEdit.setDate(datetime.date.today())
        self.ui.toDateEdit.setDate(datetime.date.today())

        self.Rota = Core.Rota()


    def fetchDates(self):
        # fetch to and from dates from date edits
        toDate = QtCore.QDate(self.ui.toDateEdit.date()).toPyDate()
        fromDate = QtCore.QDate(self.ui.fromDateEdit.date()).toPyDate()
        return [fromDate, toDate]

    def setSlots(self):
        self.ui.runReportBut.clicked.connect(self.fetchDates)
        self.ui.runReportBut.clicked.connect(self.whichReport)
        self.ui.exportToCSVBUT.clicked.connect(self.exportToCSV)

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
            dates = self.fetchDates()
            self.employeePayReport(dates[0], dates[1])

    def exportToCSV(self):
        table = self.Rota.reportTableINT
        picker = QtGui.QFileDialog()
        location = picker.getSaveFileName(self, 'Save to Folder', '*.csv')
        print (location)
        with open('{}'.format(location), mode='w') as CSVfile:
            fileWriter = csv.writer(CSVfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            fileWriter.writerow(['empID', 'empName', 'nicCost', 'pensionCost', 'netSalary', 'empTotalSalary','empTotalHourly', 'shiftBonusCost', 'SSP'])
            for row in range(len(table)):
                fileWriter.writerow(table[row])
        msg = QtGui.QMessageBox()
        msg.setIcon(QtGui.QMessageBox.Information)
        msg.setText("The report has been exported to a CSV")
        msg.setWindowTitle("File to CSV")
        msg.show()

    def employeePayReport(self, fromDate, toDate):
        reportTable = self.Rota.calcWageCostforDateRange(fromDate, toDate, 0)
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
        self.holidayShiftData = self.Rota.shiftTypeReportData(self.fromDate, self.toDate, 2)

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


class PrintingWindow(QtGui.QTableWidget):
    def __init__(self, parent=None):
        super(PrintingWindow, self).__init__(parent)


    def createDocumnet(self, TableWidget, header):
        document = QtGui.QTextDocument()
        self.header = header
        cursor = QtGui.QTextCursor(document)
        rows = TableWidget.rowCount()
        columns = TableWidget.columnCount()
        table = cursor.insertTable(rows + 1, columns)
        format = table.format()
        format.setHeaderRowCount(1)
        format.setAlignment(QtCore.Qt.AlignHCenter)
        format.setCellPadding(2)
        #format.setCellSpacing(0)
        table.setFormat(format)
        format = cursor.blockCharFormat()
        format.setFontWeight(QtGui.QFont.Condensed)

        for column in range(columns):
            if column == 0:
                coverdata = TableWidget.horizontalHeaderItem(column).text()
                data = """&nbsp;&nbsp;{}&nbsp;&nbsp;""".format(coverdata)
            else:
                coverdata = TableWidget.horizontalHeaderItem(column).text()
                data = """
                        {}
                        <br>
                        &nbsp;&nbsp;
                        <b>{}</b>
                        &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
                        <b>{}</b>
                        &nbsp;&nbsp;
                        </p>
                        """\
                    .format(self.header[column], coverdata.split('|')[0], coverdata.split('|')[1])
            alignment = QtGui.QTextBlockFormat()
            alignment.setAlignment(QtCore.Qt.AlignCenter)
            cursor.setBlockFormat(alignment)
            cursor.insertHtml(data)
            cursor.movePosition(QtGui.QTextCursor.NextCell)

        for row in range(rows):
            for column in range(columns):
                a = WidgetTools.TableWidgetTools()
                a.setWidget(TableWidget)
                formating = QtGui.QTextBlockFormat()
                formating.setAlignment(QtCore.Qt.AlignHCenter)
                cursor.setBlockFormat(formating)
                cursor.insertHtml(a.cellExtractfromWidget(row, column))
                cursor.movePosition(QtGui.QTextCursor.NextCell)
        return document

    def printTableWidgetText(self, TableWidget, header):
        printer = QtGui.QPrinter()
        printer.setOrientation(QtGui.QPrinter.Landscape)
        printer.setPageMargins(3, 3, 3, 3, QtGui.QPrinter.Millimeter)
        self.tableWidget = TableWidget
        doc = self.createDocumnet(self.tableWidget, header)
        dialog = QtGui.QPrintDialog(printer)
        dialog.setModal(True)
        dialog.setWindowTitle("Print Document")


        # dialog.addEnabledOption(QAbstractPrintDialog.PrintSelection)

        if dialog.exec_() == True:
            doc.print_(printer)
            #subprocess.Popen([printer.outputFileName()], shell=True)



class payrollVariableWindow(QtGui.QDialog):
    trigger = pyqtSignal()
    senderBUT = str()
    def __init__(self):
        super(payrollVariableWindow, self).__init__()

        self.uip = Ui_Dialog()
        self.uip.setupUi(self)

        self.Rota = Core.Rota()
        self.ratesDB = NMWRates()
        self.bandsDB = NMWBands()
        self.salCalVarDB = SalaryCalcVariables()

        self.populateTables()
        self.uip.closeBUT.clicked.connect(self.closeWindow)
        self.uip.updateBUT.clicked.connect(self.updateData)
        self.uip.tabWidget.currentChanged.connect(self.updateData)
        self.uip.tabWidget.currentChanged.connect(self.populateTables)
        self.uip.addBUT.clicked.connect(self.addRow)
        self.uip.delBUT.clicked.connect(self.delRow)



    def populateTables(self):

        NMWratesData = self.ratesDB.select_All()
        NMWBandsData = self.bandsDB.select_All()
        salCalVarData = self.salCalVarDB.select_All()

        self.ratesTable = WidgetTools.TableWidgetTools()
        self.ratesTable.setWidget(self.uip.ratesNMWTableWidget)
        self.ratesTable.populateTableWidget_Widgets(NMWratesData, 4, 0, [None, self.nmwBandComboListExtract(), None, 'date'])

        self.bandsTable = WidgetTools.TableWidgetTools()
        self.bandsTable.setWidget(self.uip.bandsNMWTableWidget)
        self.bandsTable.populateTableWidget(NMWBandsData, 4, 0)

        self.salVarTable = WidgetTools.TableWidgetTools()
        self.salVarTable.setWidget(self.uip.pensionNICTableWidget)
        self.salVarTable.populateTableWidget_Widgets(salCalVarData, 8, 0, [None, 'date', None, 'percentage', None,  'percentage', None, None])


    def closeWindow(self):
        self.close()

    def updateData(self):

        # update rates table
        tableExport = self.ratesTable.rowExtractfromWidget()
        self.Rota.updateRatesTableToDB(tableExport)

        # update bands table
        tableExport = self.bandsTable.rowExtractfromWidget()
        self.Rota.updateBandsTableToDB(tableExport)

        # update sal cal variable table
        tableExport = self.salVarTable.rowExtractfromWidget()
        self.Rota.updateSalCalVarTableToDB(tableExport)

    def addRow(self):
        if self.uip.tabWidget.currentIndex() == 0:
            self.Rota.addSalCalVarRow_blank()
        elif self.uip.tabWidget.currentIndex() == 1:
            self.Rota.addNMWRatesRow_blank()
        elif self.uip.tabWidget.currentIndex() == 2:
            self.Rota.addNMWBandsRow_blank()
        else:
            pass

        self.populateTables()

    def delRow(self):

        # delete from sal var table
        if self.uip.tabWidget.currentIndex() == 0:
            ID = self.salVarTable.IDfromSelectedRow()
            if ID is None:
                pass
            else:
                message = QtGui.QMessageBox.question(QtGui.QMessageBox(), 'Warning',
                                                     "Do you Really Want to Delete, This can not be un-done!"
                                                     , QtGui.QMessageBox.Yes | QtGui.QMessageBox.No,
                                                     QtGui.QMessageBox.No)
                if message == QtGui.QMessageBox.Yes:
                    self.Rota.deleteSalCalcRow(ID)
                    self.populateTables()
                else:
                    pass

        # delete row from NMW rates table
        elif self.uip.tabWidget.currentIndex() == 1:
            ID = self.ratesTable.IDfromSelectedRow()
            if ID is None:
                pass
            else:
                message = QtGui.QMessageBox.question(QtGui.QMessageBox(), 'Warning',
                                                     "Do you Really Want to Delete, This can not be un-done!"
                                                     , QtGui.QMessageBox.Yes | QtGui.QMessageBox.No,
                                                     QtGui.QMessageBox.No)
                if message == QtGui.QMessageBox.Yes:
                    self.Rota.deleteNMWRatesRow(ID)
                    self.populateTables()
                else:
                    pass

        # delete from NMW bands table
        elif self.uip.tabWidget.currentIndex() == 2:
            ID = self.bandsTable.IDfromSelectedRow()
            if ID is None:
                pass
            else:
                message = QtGui.QMessageBox.question(QtGui.QMessageBox(), 'Warning',
                                                     "Do you Really Want to Delete, This can not be un-done!"
                                                     , QtGui.QMessageBox.Yes | QtGui.QMessageBox.No,
                                                     QtGui.QMessageBox.No)
                if message == QtGui.QMessageBox.Yes:
                    self.Rota.deleteNMWBandsRow(ID)
                    self.populateTables()
                else:
                    pass
        else:
            pass


class EmployeeInformationWindow(QtGui.QDialog):
    trigger = pyqtSignal()

    def __init__(self, fromDate, toDate, parent=None):
        super(EmployeeInformationWindow, self).__init__(parent)

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

        self.Rota = Core.Rota()
        self.emp = employees()


    def defineTriggers(self):
        # define triggers
        self.uie.EmployeeListTable.currentCellChanged.connect(self.updateEmpDataToDB)
        self.uie.EmployeeListTable.currentCellChanged.connect(self.clearCheckBoxes)
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

    def queryDB_reloadEmpModule(self):
        self.emp = employees()

    def setEmpWorkingDaysInWeek(self):
        self.uie.mondayCB.setChecked(True) \
            if self.emp.empIsDayAContractedDay(self.currentID,0) is True else self.uie.mondayCB.setChecked(False)
        self.uie.tuesdayCB.setChecked(True) \
            if self.emp.empIsDayAContractedDay(self.currentID, 1) is True else self.uie.mondayCB.setChecked(False)
        self.uie.wednesdayCB.setChecked(True) \
            if self.emp.empIsDayAContractedDay(self.currentID, 2) is True else self.uie.mondayCB.setChecked(False)
        self.uie.thursdayCB.setChecked(True) \
            if self.emp.empIsDayAContractedDay(self.currentID, 3) is True else self.uie.mondayCB.setChecked(False)
        self.uie.fridayCB.setChecked(True) \
            if self.emp.empIsDayAContractedDay(self.currentID, 4) is True else self.uie.mondayCB.setChecked(False)
        self.uie.saturdayCB.setChecked(True) \
            if self.emp.empIsDayAContractedDay(self.currentID, 5) is True else self.uie.mondayCB.setChecked(False)
        self.uie.sundayCB.setChecked(True) \
            if self.emp.empIsDayAContractedDay(self.currentID, 6) is True else self.uie.mondayCB.setChecked(False)
        self.uie.contractedDaysPerWeekBOX.setValue(self.emp.empContractedDaysofWork(self.currentID)[1])

    def updateButtonclicked(self):
        self.updateEmpDataToDB()
        self.setReturntoID()
        self.populateInstantVariablesWithDBData()
        self.populateNameListWidget()
        self.populateWidgets_NotNameList()

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
            self.setEmpWorkingDaysInWeek()

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
            Querydb('''INSERT INTO Employee_TBL 
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

            empID = Querydb("""SELECT idEmployee_TBL FROM Employee_TBL WHERE Name = %s""", (empName,)).fetchAllRecordswithFormatting()

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
            Querydb("""DELETE FROM Employee_TBL WHERE idEmployee_TBL = %s""",
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
        mon = 1 if self.uie.mondayCB.isChecked() is True else 0
        tue = 1 if self.uie.tuesdayCB.isChecked() is True else 0
        wed = 1 if self.uie.wednesdayCB.isChecked() is True else 0
        thu = 1 if self.uie.thursdayCB.isChecked() is True else 0
        fri = 1 if self.uie.fridayCB.isChecked() is True else 0
        sat = 1 if self.uie.saturdayCB.isChecked() is True else 0
        sun = 1 if self.uie.sundayCB.isChecked() is True else 0

        Querydb('''UPDATE Employee_TBL
                             SET  Name = %s, 
                             DOB = %s, 
                             departmentID = %s, 
                             SalOrHourly = %s, 
                             Address = %s, 
                             Email = %s, 
                             HomePhone = %s, 
                             MobilePhone = %s, 
                             EmpStDate = %s,
                             QDMon = %s,
                             QDTue = %s,
                             QDWed = %s,
                             QDThu = %s,
                             QDFri = %s,
                             QDSat = %s,
                             QDSun = %s
                             WHERE idEmployee_TBL = %s;''',
                         (name, DOB, departmentID, salorHourlyID,
                    adrs, email, home, mobile,
                    StDate, mon, tue, wed, thu, fri, sat, sun, self.currentID)).InsertOneExecutewithFormatting()

    def setReturntoID(self):
        self.IDtoReturnto = self.currentID

    def populateNameListWidget(self):
        self.emplist = WidgetTools.TableWidgetTools()
        self.emplist.setWidget(self.uie.EmployeeListTable)
        self.emplist.populateTableWidget(self.listOfEmployees, 2, 0)

    def populateDepComboBoxList(self):
        self.depTable = Departments()
        departments = self.depTable.select_All()
        self.depCombo = WidgetTools.comboBoxTools(self.uie.empDepCombo)
        self.depCombo.populateComboBoxList(departments, 1)

    def setDepCombo(self):
        self.depCombo.setComboToSearchedItem(self.emp.empDepName(self.currentID))

    def populateSalComboBoxList(self):
        salOrHourlyDB = SalaryOrHourly()
        salOrHourly = salOrHourlyDB.select_All()
        self.salCombo = WidgetTools.comboBoxTools(self.uie.empSalCombo)
        self.salCombo.populateComboBoxList(salOrHourly, 1)

    def setSalCombo(self):
        # set selection to employees department
        self.salCombo.setComboToSearchedItem(self.emp.empSalaryOrHourlyName(self.currentID))

    def calculateAge(self):
        today = datetime.datetime.today()
        dob = datetime.datetime.strptime(str(QtCore.QDate.toPyDate(self.uie.empDOBbox.date())), '%Y-%m-%d')
        age = float((today - dob).days) / 365
        self.uie.empAgeBox.setValue(age)

    def populateSalaryTable(self):
        # populate salarytableWidget
        emp = employees()

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
        Querydb('''INSERT INTO Salary(EmployeeID, PoundsPerHour, Salary, AdjustDate) VALUE (%s, %s, %s, %s);''',
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
                Querydb("""DELETE FROM Salary WHERE SalaryID = %s""",
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

        Querydb('''UPDATE Salary SET EmployeeID = %s, Salary = %s, PoundsPerHour = %s, AdjustDate = %s WHERE SalaryID = %s''',
                         converted).InsertManyExecutewithFormatting()
        self.queryDB_reloadEmpModule()
        self.updateButtonclicked()

    def populateBonusTable(self):
        # populate bonusTableWidget
        emp = employees()
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
        Querydb('''INSERT INTO Bonus(bonus, EmployeeID, bonusPayDate, BonusPeriodStDate) VALUE (%s, %s, %s, %s);''',
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
                Querydb("""DELETE FROM Bonus WHERE bonusID = %s""",
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

        Querydb('''UPDATE Bonus SET bonus = %s, EmployeeID = %s, BonusPeriodStDate = %s, bonusPayDate = %s  WHERE bonusID = %s''',
                         converted).InsertManyExecutewithFormatting()
        self.queryDB_reloadEmpModule()
        self.updateButtonclicked()

    def populateHolidayTable(self):
        # populate Holiday Entitlement table
        emp = employees()
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
        Querydb('''INSERT INTO HolidayEntitlement(empID, entitledDaysFY, adjustDate) VALUE (%s, %s, %s);''',
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
                Querydb("""DELETE FROM HolidayEntitlement WHERE entitlementID = %s""",
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

        Querydb('''UPDATE HolidayEntitlement SET empID = %s, entitledDaysFY = %s, adjustDate = %s WHERE entitlementID = %s''',
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
        self.clearCheckBoxes()

    def clearCheckBoxes(self):
        self.uie.mondayCB.setChecked(False)
        self.uie.tuesdayCB.setChecked(False)
        self.uie.wednesdayCB.setChecked(False)
        self.uie.thursdayCB.setChecked(False)
        self.uie.fridayCB.setChecked(False)
        self.uie.saturdayCB.setChecked(False)
        self.uie.sundayCB.setChecked(False)

    def emitTrigger(self):
        self.trigger.emit()
        self.close()



class AddEmployeeWindow(QtGui.QDialog):
    trigger = pyqtSignal()
    def __init__(self, datelistDV3, exisitingnames):
        self.lastDate = str(datelistDV3[6])
        self.exisitingnames = exisitingnames

        super(AddEmployeeWindow, self).__init__()
        self.uip = Ui_AddEmpDialog()
        self.uip.setupUi(self)
        self.namesandID = []
        self.PopulateEmployeesList()
        self.uip.AddEmpBUT.clicked.connect(self.whichCellsHaveIselected)
        self.uip.AddEmpBUT.clicked.connect(self.emitTrigger)


    def PopulateEmployeesList(self):
        # populate the add employee window with Employees that have started before current date
        Employees = Querydb("SELECT idEmployee_TBL, Name, departmentID FROM Employee_TBL WHERE EmpStDate <= %s",
                                     (self.lastDate,)).fetchAllRecordswithFormatting()
        # remove the already entered names from the add employee listOfEmployees
        self.namesandID = [[Employees[x][1], Employees[x][0], Employees[x][2]]
                           for x in range(0, len(Employees)) if Employees[x][1] not in self.exisitingnames]

        # add items to listOfEmployees
        for row in range(0, len(self.namesandID)):
            item = QtGui.QListWidgetItem(self.namesandID[row][0])
            self.uip.EmpList.addItem(item)

    def whichCellsHaveIselected(self):
        nameList = [str(x.text()) for x in self.uip.EmpList.selectedItems()]
        selectionList = []
        for a in range(len(nameList)):
            for b in range(len(self.namesandID)):
                if self.namesandID[b][0] == nameList[a]:
                    selectionList.append([self.namesandID[b][0], self.namesandID[b][1], self.namesandID[b][2]])

        return selectionList
    def emitTrigger(self):
        self.trigger.emit()
        self.close()

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
        log = PassPhrase(textName, textPass)._CheckPwd()
        if log is True:
            self.accept()
        else:
            QtGui.QMessageBox.warning(self, 'Error', 'Bad user or password')

class ActualRevWindow(QtGui.QDialog):
    def __init__(self, rotaDate):
        super(ActualRevWindow, self).__init__()
        QtGui.QWidget.__init__(self)
        self.ui = Ui_ActRevWindow()
        self.ui.setupUi(self)

        self.table = self.ui.revTable
        self.rotaDate = rotaDate
        self.Rota = Rota()

        #self.ui.dateEditBox.dateChanged.connect(self.Rota.generateDaysInMonth(self.rotaDate))
        self.ui.dateEditBox.dateChanged.connect(self.tableConfig)
        self.ui.dateEditBox.dateChanged.connect(self.loadData)
        self.ui.buttonBox.accepted.connect(self.updateData)

        self.ui.dateEditBox.setDate(self.Rota.generateFirstOfMonthDate(QtCore.QDate(self.rotaDate)))
        self.loadData()


    def tableConfig(self):
        daysInMonth = self.Rota.generateDaysInMonth(self.rotaDate)
        self.table.setRowCount(2)
        self.table.setColumnCount(daysInMonth)
        self.tableHeaders()

    def tableHeaders(self):
        daysInMonth = self.Rota.generateDaysInMonth(self.rotaDate)
        for day in range(daysInMonth):
            if day == 0 or day == 20 or day == 30:
                postfix = "st"

            elif day == 1 or day == 21:
                postfix = "nd"

            elif day == 2 or day == 22:
                postfix = "rd"

            else:
                postfix = "th"

            self.table.setHorizontalHeaderItem(day, QtGui.QTableWidgetItem("{} {}".format(day + 1, postfix)))
            self.table.setVerticalHeaderItem(0, QtGui.QTableWidgetItem("AM"))
            self.table.setVerticalHeaderItem(1, QtGui.QTableWidgetItem("PM"))

    def updateData(self):
        dateSelected = self.rotaDate
        tableData = WidgetTools.TableWidgetTools()
        tableData.setWidget(self.table)
        revTableData = tableData.extraWidgetDataToList(False)
        formatedData = []
        # build a list of date, am rev and pm rev to be updated / inserted to DB
        for day in range(len(revTableData[0])):
            formatedData.append(
                [dateSelected.toPyDate() + relativedelta(days=day), 0 if revTableData[0][day] == "" else revTableData[0][day],
                 0 if revTableData[1][day] == "" else revTableData[1][day], 0 if revTableData[0][day] == "" else revTableData[0][day],
                 0 if revTableData[1][day] == "" else revTableData[1][day]])

        self.Rota.updateActualRevtoDB(formatedData)


    def loadData(self):
        dateSelected = self.rotaDate
        daysInMonth = self.Rota.generateDaysInMonth(dateSelected)
        firstOfMonth = datetime.date(dateSelected.year(), dateSelected.month(), 1)
        lastofMonth = datetime.date(dateSelected.year(), dateSelected.month(), daysInMonth)
        DailyActualsDB = DailyActuals()
        data = DailyActualsDB.dailyActualsByDateRange(firstOfMonth, lastofMonth)

        try:
            for col in range(daysInMonth):
                record = data[col]
                for row in range(2):
                    newitem = QtGui.QTableWidgetItem(str(record[row+1]))
                    self.table.setItem(row, col, newitem)
        except StandardError:
            self.table.clearContents()




