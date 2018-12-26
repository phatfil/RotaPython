#!/usr/bin/python
from PyQt4 import QtCore, QtGui
import datetime
import payrollVariablePopUP
import Employees


class rota:
    def __init__(self, shiftsTable):
        self.__shiftsTable = shiftsTable


    def empList(self, fromDate, toDate):
        if self.__shiftsTable == ():
            return []
        else:    # filter duplicate IDs with dict
            empList = {EmployeeID
                      for shiftsID, EmployeeID, Date, StartAM, FinAM, BrkAM, StartPM, FinPM, BrkPM, ConcatShift, TotalHours,
                      shiftTypeAM, shiftTypePM, EmployeeDep, DepAM, DepPM
                      in self.__shiftsTable
                      if fromDate <= Date <= toDate}
            return list(empList)

    def shiftData(self, fromdate, todate):
        if self.__shiftsTable == ():
            return []
        else:
            shifts = [[shiftsID, EmployeeID, Date, StartAM, FinAM, BrkAM, StartPM, FinPM, BrkPM, ConcatShift, TotalHours,
                       shiftTypeAM, EmployeeDep]
                      for shiftsID, EmployeeID, Date, StartAM, FinAM, BrkAM, StartPM, FinPM, BrkPM, ConcatShift, TotalHours,
                      shiftTypeAM, shiftTypePM, EmployeeDep, DepAM, DepPM in self.__shiftsTable if fromdate <= Date <= todate]
            return shifts

    def totalrotaHours(self):
        total = [self.__shiftsTable[a][10] for a in range(len(self.__shiftsTable))]
        return sum(total)

    def shiftTypeReportData(self, fromdate, todate, shiftTypeID):
        shiftTypeData = []
        print('shift table', self.__shiftsTable)
        print('from Date', fromdate)
        print('to Date', todate)
        for a in range(len(self.__shiftsTable)):
            shiftsID = self.__shiftsTable[a][0]
            EmployeeID = self.__shiftsTable[a][1]
            Date = self.__shiftsTable[a][2]
            StartAM = self.__shiftsTable[a][3]
            FinAM = self.__shiftsTable[a][4]
            BrkAM = self.__shiftsTable[a][5]
            StartPM = self.__shiftsTable[a][6]
            FinPM = self.__shiftsTable[a][7]
            BrkPM = self.__shiftsTable[a][8]
            # ConcatShift = self.__shiftsTable[a][9]
            # TotalHours = self.__shiftsTable[a][10]
            shiftTypeAM = self.__shiftsTable[a][11]
            shiftTypePM = self.__shiftsTable[a][12]
            # EmployeeDep = self.__shiftsTable[a][13]
            # DepAM = self.__shiftsTable[a][14]
            # DepPM = self.__shiftsTable[a][15]
            calcAM = ((FinAM - StartAM) - BrkAM)
            calcPM = ((FinPM - StartPM) - BrkPM)
            print('date', Date)
            if fromdate <= Date and todate >= Date:
                if shiftTypeAM == shiftTypeID or shiftTypePM == shiftTypeID:
                    if shiftTypeAM == shiftTypeID:
                        pass
                    else:
                        calcAM = ""
                        shiftTypeAM = ""

                    if shiftTypePM == shiftTypeID:
                        pass
                    else:
                        calcPM = ""
                        shiftTypePM = ""

                    shiftTypeData.append([shiftsID, EmployeeID, Date, calcAM, calcPM, shiftTypeAM, shiftTypePM])


        """shiftTypeData = [[shiftsID, EmployeeID, Date, shiftTypeAM, ((FinAM - StartAM) - BrkAM), shiftTypePM,
                     ((FinPM - StartPM) - BrkPM)]
                    for
                    shiftsID, EmployeeID, Date, StartAM, FinAM, BrkAM, StartPM, FinPM, BrkPM, ConcatShift, TotalHours,
                    shiftTypeAM, shiftTypePM, EmployeeDep, DepAM, DepPM in self.__shiftsTable if
                    fromdate <= Date <= todate and (shiftTypeAM == shiftTypeID or shiftTypePM == shiftTypeID)]
        """
        print('shit type data', shiftTypeData)
        return shiftTypeData

    def empTotalHoursPeriod(self, empID, fromDate, toDate):
        hours = 0
        if fromDate > toDate:
            QtGui.QMessageBox.warning(QtGui.QMessageBox(), 'Error', 'to Date is before from date')
        else:
            days = (toDate - fromDate).days
            for x in range(days):
                hours += self.empTotalHoursDay(empID, (fromDate + datetime.timedelta(days=days)), 'day')
            return hours

    def empTotalHoursDay(self, empID, shiftDate, am_pm_day):
        if self.__shiftsTable == ():
            return []
        else:

            if am_pm_day == "am": # calc am shift totals
                shifts = [[FinAM, StartAM, BrkAM, FinPM, StartPM, BrkPM]
                          for
                          shiftsID, EmployeeID, Date, StartAM, FinAM, BrkAM, StartPM, FinPM, BrkPM, ConcatShift, TotalHours,
                          shiftTypeAM, shiftTypePM, EmployeeDep, DepAM, DepPM in self.__shiftsTable if EmployeeID == empID and shiftDate == Date][0]

                if shifts == []:
                    return 0
                else:
                    total = (shifts[0] - shifts[1]) - shifts[2]
                    return total

            elif am_pm_day == "pm": # calc pm shift totals
                shifts = [[FinAM, StartAM, BrkAM, FinPM, StartPM, BrkPM]
                          for
                          shiftsID, EmployeeID, Date, StartAM, FinAM, BrkAM, StartPM, FinPM, BrkPM, ConcatShift, TotalHours,
                          shiftTypeAM, shiftTypePM, EmployeeDep, DepAM, DepPM in self.__shiftsTable if EmployeeID == empID and shiftDate == Date][0]

                if shifts == []:
                    return 0
                else:
                    total = (shifts[3] - shifts[4]) - shifts[5]
                    return total


            elif am_pm_day == "day":  # calc day totals
                shifts = [TotalHours
                          for
                          shiftsID, EmployeeID, Date, StartAM, FinAM, BrkAM, StartPM, FinPM, BrkPM, ConcatShift, TotalHours,
                          shiftTypeAM, shiftTypePM, EmployeeDep, DepAM, DepPM, holHours, holDays in self.__shiftsTable if
                          EmployeeID == empID and shiftDate == Date]

                if shifts == []:
                    return 0
                else:
                    total = shifts[0]
                    return total

            else:
                print ('enter a correct shift type am pm or day as string')
                pass


