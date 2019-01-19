from payrollVariableUI import Ui_Dialog
from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import pyqtSignal
import DB
import WidgetTools
import datetime

class payrollVariablePopUp(QtGui.QDialog):
    trigger = pyqtSignal()
    senderBUT = str()
    def __init__(self):
        super(payrollVariablePopUp, self).__init__()

        self.uip = Ui_Dialog()
        self.uip.setupUi(self)

        self.populateTables()
        self.uip.closeBUT.clicked.connect(self.closeWindow)
        self.uip.updateBUT.clicked.connect(self.updateData)
        self.uip.tabWidget.currentChanged.connect(self.updateData)
        self.uip.tabWidget.currentChanged.connect(self.populateTables)
        self.uip.addBUT.clicked.connect(self.addRow)
        self.uip.delBUT.clicked.connect(self.delRow)

    def populateTables(self):
        self.NMWRates = DB.Querydb("""SELECT * FROM nmwRates""", None).fetchAllRecordswithFormatting()
        self.NMWBands = DB.Querydb("""SELECT * FROM nmwBands""", None).fetchAllRecordswithFormatting()
        self.salCalVar = DB.Querydb("""SELECT * FROM SalaryCalVariables""", None).fetchAllRecordswithFormatting()
        #print (self.salCalVar)
        self.ratesTable = WidgetTools.TableWidgetTools()
        self.ratesTable.setWidget(self.uip.ratesNMWTableWidget)
        self.ratesTable.populateTableWidget_Widgets(self.NMWRates, 4, 0, [None, self.nmwBandComboListExtract(), None, 'date'])
        # [['<18', 1], ['18 to 21', 2], ['21 to 25', 3], ['>25', 4]]

        self.bandsTable = WidgetTools.TableWidgetTools()
        self.bandsTable.setWidget(self.uip.bandsNMWTableWidget)
        self.bandsTable.populateTableWidget(self.NMWBands, 4, 0)

        self.salVarTable = WidgetTools.TableWidgetTools()
        self.salVarTable.setWidget(self.uip.pensionNICTableWidget)
        self.salVarTable.populateTableWidget_Widgets(self.salCalVar, 8, 0, [None, 'date', None, 'percentage', None,  'percentage', None, None])

    def nmwBandIDExtract(self, band):
        if self.NMWBands == ():
            return None
        else:
            bID = [id for id, title, age1, age2 in self.NMWBands if band == title][0]
            return bID

    def nmwBandComboListExtract(self):
        if self.NMWBands == ():
            return []
        else:
            titleIDlist = [[str(title), id] for id, title, age1, age2 in self.NMWBands]
            return titleIDlist

    def nicMinAge(self, Sdate):
        if self.NMWRates == ():
            return 0
        else:
            data = [[VariablesDate, minAge] for nicVariablesID, VariablesDate ,minAge,  nicRate, threshold, pensionPercentage, sickPay, SSPLEL
                    in self.salCalVar if Sdate >= VariablesDate]
            if data == []:
                pass
            else:
                result = max(data)
                return result[1]

    def SSPLowerEarningsLimit(self, Sdate):
        if self.NMWRates == ():
            return 0
        else:
            data = [[VariablesDate, SSPLEL] for nicVariablesID, VariablesDate ,minAge,  nicRate, threshold, pensionPercentage, sickPay, SSPLEL
                    in self.salCalVar if Sdate >= VariablesDate]

            if data == []:
                pass
            else:
                result = max(data)
                return result[1]

    def sickPayDayRate(self, Sdate):
        if self.NMWRates == ():
            return 0
        else:
            data = [[VariablesDate, sickPay] for nicVariablesID, VariablesDate ,minAge,  nicRate, threshold, pensionPercentage, sickPay, SSPLEL
                    in self.salCalVar if Sdate >= VariablesDate]

            if data == []:
                pass
            else:
                result = max(data)
                return result[1]

    def nicRate(self, Sdate):
        if self.NMWRates == ():
            return 0
        else:
            data = [[VariablesDate, nicRate] for nicVariablesID, VariablesDate , minAge,  nicRate, threshold, pensionPercentage, sickPay, SSPLEL
                    in self.salCalVar if Sdate >= VariablesDate]

            if data == []:
                pass
            else:
                result = max(data)
                return result[1]

    def nicThreshold(self, Sdate):
        if self.NMWRates == ():
            return 0
        else:
            data = [[VariablesDate, threshold] for nicVariablesID, VariablesDate , minAge,  nicRate, threshold, pensionPercentage, sickPay, SSPLEL
                     in self.salCalVar if Sdate >= VariablesDate]
            if data == []:
                pass
            else:
                result = max(data)
                return result[1]

    def pensionPecentage(self, Sdate):
        if self.NMWRates == ():
            return 0
        else:
            data = [[VariablesDate, pensionPercentage] for nicVariablesID, VariablesDate , minAge, nicRate, threshold, pensionPercentage, sickPay, SSPLEL
                     in self.salCalVar if Sdate >= VariablesDate]
            if data == []:
                pass
            else:
                result = max(data)
                return result[1]

    def closeWindow(self):
        self.close()

    def updateData(self):

        # update rates table
        data = self.ratesTable.rowExtractfromWidget()
        converted = []
        if data is None:
            pass
        else:
            for a in range(len(data)):
                converted.append([self.nmwBandIDExtract(data[a][1]), data[a][2], data[a][3], data[a][0]])

            DB.Querydb(
                '''UPDATE nmwRates SET nmwBandsID = %s, rate = %s, liveDate = %s WHERE nmwRatesID = %s''',
                converted).InsertManyExecutewithFormatting()

        # update bands table
        data = self.bandsTable.rowExtractfromWidget()
        converted = []
        if data is None:
            pass
        else:
            for a in range(len(data)):
                converted.append([data[a][1], data[a][2], data[a][3], data[a][0]])

            DB.Querydb(
                '''UPDATE nmwBands SET nmwTile = %s, fromAge = %s, toAge = %s WHERE nmwBandID = %s''',
                converted).InsertManyExecutewithFormatting()

        # update sal cal variable table
        data = self.salVarTable.rowExtractfromWidget()
        converted = []
        if data is None:
            pass
        else:
            for a in range(len(data)):
                converted.append([data[a][1], (data[a][2]/100), data[a][3], (data[a][4]/100), data[a][5], data[a][0]])
            DB.Querydb(
                '''UPDATE SalaryCalVariables SET minAge = %s, nicRate = %s, threshold = %s, 
                pensionPercentage = %s, VariablesDate = %s WHERE nicVariablesID = %s''',
                converted).InsertManyExecutewithFormatting()

    def addRow(self):
        if self.uip.tabWidget.currentIndex() == 0:
            DB.Querydb('''INSERT INTO SalaryCalVariables(minAge, nicRate, threshold, pensionPercentage, VariablesDate ) 
            VALUE (%s, %s, %s, %s, %s);''',
                       ( 0, 0, 0, 0,  datetime.date.today())).InsertOneExecutewithFormatting()
        elif self.uip.tabWidget.currentIndex() == 1:
            DB.Querydb(
                '''INSERT INTO nmwRates( nmwBandsID, rate, liveDate) 
                VALUE (%s, %s, %s);''',
                (1, 0, datetime.date.today())).InsertOneExecutewithFormatting()
        elif self.uip.tabWidget.currentIndex() == 2:
            DB.Querydb(
                '''INSERT INTO nmwBands(nmwTile, fromAge, toAge) VALUE (%s, %s, %s);''',
                ("", 0, 0)).InsertOneExecutewithFormatting()
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
                    DB.Querydb("""DELETE FROM SalaryCalVariables WHERE  nicVariablesID = %s""",
                               (ID,)).DeleteOneExecutewithFormatting()
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
                    DB.Querydb("""DELETE FROM nmwRates WHERE  nmwRatesID = %s""",
                               (ID,)).DeleteOneExecutewithFormatting()
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
                    DB.Querydb("""DELETE FROM nmwBands WHERE  nmwBandID = %s""",
                               (ID,)).DeleteOneExecutewithFormatting()
                    self.populateTables()
                else:
                    pass
        else:
            pass