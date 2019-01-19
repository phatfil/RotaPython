from PyQt4 import QtGui, QtCore
from dateutil.relativedelta import *
import datetime
import WidgetTools
from actualRevUI import Ui_ActRevWindow
import DB
from decimal import Decimal

class ActualRevWindow(QtGui.QDialog):
    def __init__(self, rotaDate):
        super(ActualRevWindow, self).__init__()
        QtGui.QWidget.__init__(self)
        self.ui = Ui_ActRevWindow()
        self.ui.setupUi(self)

        self.table = self.ui.revTable
        self.rotaDate = rotaDate

        self.ui.dateEditBox.dateChanged.connect(self.dateCalc)
        self.ui.dateEditBox.dateChanged.connect(self.tableConfig)
        self.ui.dateEditBox.dateChanged.connect(self.loadData)
        #self.ui.dateEditBox.dateChanged.connect(self.populateMonthTotalRev)
        self.ui.buttonBox.accepted.connect(self.updateData)

        self.ui.dateEditBox.setDate(self.datetoFirst(QtCore.QDate(self.rotaDate)))
        self.loadData()

    def datetoFirst(self, date):
        adjustDate = QtCore.QDate(datetime.date(date.year(), date.month(), 1))
        return adjustDate

    def dateCalc(self):
        self.dateSelected = self.datetoFirst(self.ui.dateEditBox.date())
        self.daysInMonth = (self.dateSelected.toPyDate() + relativedelta(months=+1) - self.dateSelected.toPyDate()).days

    def tableConfig(self):
        self.table.setRowCount(2)
        self.table.setColumnCount(self.daysInMonth)
        self.tableHeaders()

    def tableHeaders(self):
        for day in range(self.daysInMonth):
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
        tableData = WidgetTools.TableWidgetTools()
        tableData.setWidget(self.table)
        self.revTableData = tableData.extraWidgetDataToList(False)
        formatedData = []
        # build a list of date, am rev and pm rev to be updated / inserted to DB
        for day in range(len(self.revTableData[0])):
            formatedData.append(
                [self.dateSelected.toPyDate() + datetime.timedelta(days=day), 0 if self.revTableData[0][day] == "" else self.revTableData[0][day],
                 0 if self.revTableData[1][day] == "" else self.revTableData[1][day], 0 if self.revTableData[0][day] == "" else self.revTableData[0][day],
                 0 if self.revTableData[1][day] == "" else self.revTableData[1][day]])

        DB.Querydb(''' INSERT INTO DailyActuals (actualsDate, amRevenue, pmRevenue)
                               VALUE (%s, %s, %s) ON DUPLICATE KEY UPDATE amRevenue = %s, pmRevenue = %s;''',
                   formatedData).InsertManyExecutewithFormatting()


    def loadData(self):
        firstOfMonth = datetime.date(self.dateSelected.year(), self.dateSelected.month(), 1)
        lastofMonth = datetime.date(self.dateSelected.year(), self.dateSelected.month(), self.daysInMonth)
        self.data = DB.Querydb('''SELECT * FROM DailyActuals Where actualsDate BETWEEN %s AND %s''',
                   (firstOfMonth, lastofMonth)).fetchAllRecordswithFormatting()

        try:
            for col in range(self.daysInMonth):
                record = self.data[col]
                for row in range(2):
                    newitem = QtGui.QTableWidgetItem(str(record[row+1]))
                    self.table.setItem(row, col, newitem)
        except StandardError:
            self.table.clearContents()

    def calculateMTDTotalRev(self, StartDate, LastDate):
        firstDate = StartDate
        lastDate = LastDate

        data = DB.Querydb('''SELECT * FROM DailyActuals Where actualsDate BETWEEN %s AND %s''',
                               (firstDate, lastDate)).fetchAllRecordswithFormatting()
        amTotal = 0
        pmTotal = 0
        self.MTDTotal = 0

        #print('data', data)
        for day in range(len(data)):
            # if actual rev is 0 then use predicitive figure (if it exists)
            if data[day][1] + data[day][2] == 0:
                predRevTotal = self.predictedRevenueTotalDateRange(data[day][0], data[day][0])
                amTotal += predRevTotal[1]
                pmTotal += predRevTotal[2]
                self.MTDTotal += predRevTotal[1] + predRevTotal[2]
            else:
                #print(data[day][1], data[day][2])
                amTotal += data[day][1]
                pmTotal += data[day][2]
                self.MTDTotal += data[day][1] + data[day][2]


        return self.MTDTotal

    def predictedRevenueTotalDateRange(self, fromDate, toDate):
        # Calculate the revenue totals for all the cover types from Avg spend * covers
        predictedRevenueTotal = Decimal()
        amTotal = Decimal()
        pmTotal = Decimal()
        coversdata = self.queryPredictedCoverDBTable(fromDate, toDate)

        avgSpendData = self.queryRevenueTypeDBTable()

        for x in xrange(len(coversdata)): # iterate through extracted pred cover data
            for y in xrange(len(avgSpendData)): # iterate through avg spend data
                if str(avgSpendData[y][0]) == str(coversdata[x][4]):
                    predictedRevenueTotal += ((coversdata[x][2] * avgSpendData[y][2]) +
                                              (coversdata[x][3] * avgSpendData[y][3]) +
                                              (coversdata[x][2] * avgSpendData[y][4]) +
                                              (coversdata[x][3] * avgSpendData[y][5]))

                    amTotal +=((coversdata[x][2] * avgSpendData[y][2]) +
                               (coversdata[x][2] * avgSpendData[y][4]))


                    pmTotal += ((coversdata[x][3] * avgSpendData[y][3]) +
                                (coversdata[x][3] * avgSpendData[y][5]))
                else:
                    pass

        return [predictedRevenueTotal, amTotal, pmTotal]


    def queryPredictedCoverDBTable(self, fromDate, toDate):
        data = DB.Querydb("""SELECT * FROM PredictedCovers WHERE predCoverDate BETWEEN %s AND %s""",
                   (fromDate, toDate)).fetchAllRecordswithFormatting()
        return data

    def queryRevenueTypeDBTable(self):
        revenueTypes = DB.Querydb("""SELECT * from RevenueTypes""", None).fetchAllRecordswithFormatting()

        return revenueTypes




