from PyQt4 import QtCore, QtGui
from calendar import monthrange
from dateutil.relativedelta import *
from decimal import Decimal

import MySQLdb
import calendar
import datetime
from bcrypt import hashpw, gensalt

from DBData import *


class Rota:
    def __init__(self):

        self.emp = employees()
        self.reloadDBdata()

    def reloadDBdata(self):
        self.predCoverDB = PredictedCovers()
        self.shiftDB = Shifts()
        self.ratesDB = NMWRates()
        self.bandsDB = NMWBands()
        self.salCalVarDB = SalaryCalcVariables()
        self.revenueTypesDB = RevenueTypes()
        self.dailyActuals = DailyActuals()

    def calculateMTDTotalRev(self, firstDate, lastDate):
        data = self.dailyActuals.dailyActualsByDateRange(firstDate, lastDate)

        amTotal = 0
        pmTotal = 0
        MTDTotal = 0

        #print('data', data)
        for day in range(len(data)):
            # if actual rev is 0 then use predicitive figure (if it exists)
            if data[day][1] + data[day][2] == 0:
                predRevTotal = self.predictedRevenueTotalDateRange(data[day][0], data[day][0])
                amTotal += predRevTotal[1]
                pmTotal += predRevTotal[2]
                MTDTotal += predRevTotal[1] + predRevTotal[2]
            else:
                #print(data[day][1], data[day][2])
                amTotal += data[day][1]
                pmTotal += data[day][2]
                MTDTotal += data[day][1] + data[day][2]

        print ('MTD Total', MTDTotal)
        return MTDTotal

    def predictedRevenueTotalDateRange(self, fromDate, toDate):
        # Calculate the revenue totals for all the cover types from Avg spend * covers
        predictedRevenueTotal = Decimal()
        amTotal = Decimal()
        pmTotal = Decimal()
        coversdata = self.predCoverDB.predCoverDateRange(fromDate, toDate)
        avgSpendData = self.revenueTypesDB.select_All()

        for x in range(len(coversdata)): # iterate through extracted pred cover data
            for y in range(len(avgSpendData)): # iterate through avg spend data
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

        print ('predicted rev totals, amtotal, pm totals', [predictedRevenueTotal, amTotal, pmTotal])
        return [predictedRevenueTotal, amTotal, pmTotal]

    def updateActualRevtoDB(self, formatedData):
        Querydb(''' INSERT INTO DailyActuals (actualsDate, amRevenue, pmRevenue)
                                       VALUE (%s, %s, %s) ON DUPLICATE KEY UPDATE amRevenue = %s, pmRevenue = %s;''',
                formatedData).InsertManyExecutewithFormatting()

    def generateFirstOfMonthDate(self, date):
        adjustDate = QtCore.QDate(datetime.date(date.year(), date.month(), 1))
        return adjustDate

    def generateDaysInMonth(self, date):
        dateSelected = self.generateFirstOfMonthDate(date)
        daysInMonth = (dateSelected.toPyDate() + relativedelta(months=+1) - dateSelected.toPyDate()).days
        return daysInMonth

    def deleteSalCalcRow(self, ID):
        Querydb("""DELETE FROM SalaryCalVariables WHERE  nicVariablesID = %s""",
                (ID,)).DeleteOneExecutewithFormatting()

    def deleteNMWRatesRow(self, ID):
        Querydb("""DELETE FROM nmwRates WHERE  nmwRatesID = %s""",
                (ID,)).DeleteOneExecutewithFormatting()

    def deleteNMWBandsRow(self, ID):
        Querydb("""DELETE FROM nmwBands WHERE  nmwBandID = %s""",
                (ID,)).DeleteOneExecutewithFormatting()

    def addSalCalVarRow_blank(self):
        Querydb('''INSERT INTO SalaryCalVariables(minAge, nicRate, threshold, pensionPercentage, VariablesDate ) 
                    VALUE (%s, %s, %s, %s, %s);''',
                (0, 0, 0, 0, datetime.date.today())).InsertOneExecutewithFormatting()

    def addNMWBandsRow_blank(self):
        Querydb(
            '''INSERT INTO nmwBands(nmwTile, fromAge, toAge) VALUE (%s, %s, %s);''',
            ("", 0, 0)).InsertOneExecutewithFormatting()

    def addNMWRatesRow_blank(self):
        Querydb(
            '''INSERT INTO nmwRates( nmwBandsID, rate, liveDate) 
            VALUE (%s, %s, %s);''',
            (1, 0, datetime.date.today())).InsertOneExecutewithFormatting()

    def updateRevenueTypesToDB(self, data):
        Querydb("""UPDATE RevenueTypes
                            SET revenueType = %s, amDryAvgSpend = %s, pmDryAvgSpend = %s, amWetAvgSpend = %s, pmWetAvgSpend = %s
                            WHERE RevenueTypeID = %s;""", data).InsertManyExecutewithFormatting()

    def addNewRevenueType_blank(self):
        Querydb('''INSERT INTO RevenueTypes(revenueType) VALUE (%s);''', ("",)).InsertOneExecutewithFormatting()

    def deleteRevenueType(self, revTypeID, error):
        Querydb("""DELETE FROM RevenueTypes WHERE revenueTypeID = %s""",
                (int(revTypeID),)).DeleteOneExecutewithFormatting_ErrorMessage(error)

    def updateRatesTableToDB(self, tableExport):
        converted = []
        data = tableExport
        if data is None:
            pass
        else:
            for a in range(len(data)):
                converted.append([self.bandsDB.nmwBandID(data[a][1]), data[a][2], data[a][3], data[a][0]])

            Querydb(
                '''UPDATE nmwRates SET nmwBandsID = %s, rate = %s, liveDate = %s WHERE nmwRatesID = %s''',
                converted).InsertManyExecutewithFormatting()

    def deleteDateRangefromRota(self, fromDate, toDate):
        Querydb("""DELETE FROM `shifts` WHERE `Date` BETWEEN %s AND %s""",
                (fromDate, toDate)).DeleteOneExecutewithFormatting()

    def updateBandsTableToDB(self, tableExport):
        converted = []
        data = tableExport
        if data is None:
            pass
        else:
            for a in range(len(data)):
                converted.append([data[a][1], data[a][2], data[a][3], data[a][0]])

            Querydb(
                '''UPDATE nmwBands SET nmwTile = %s, fromAge = %s, toAge = %s WHERE nmwBandID = %s''',
                converted).InsertManyExecutewithFormatting()

    def updateSalCalVarTableToDB(self, tableExport):
        converted = []
        data = tableExport
        if data is None:
            pass
        else:
            for a in range(len(data)):
                converted.append(
                    [data[a][1], (data[a][2] / 100), data[a][3], (data[a][4] / 100), data[a][5], data[a][0]])
            Querydb(
                '''UPDATE SalaryCalVariables SET minAge = %s, nicRate = %s, threshold = %s, 
                pensionPercentage = %s, VariablesDate = %s WHERE nicVariablesID = %s''',
                converted).InsertManyExecutewithFormatting()


    def empListWithinDateRange(self, fromDate, toDate):
        shiftsTable = self.shiftDB.select_All()
        if shiftsTable == ():
            return []
        else:    # filter duplicate IDs with dict
            empList = {EmployeeID
                      for shiftsID, EmployeeID, Date, StartAM, FinAM, BrkAM, StartPM, FinPM, BrkPM, ConcatShift, TotalHours,
                      shiftTypeAM, shiftTypePM, EmployeeDep, DepAM, DepPM
                      in shiftsTable
                      if fromDate <= Date <= toDate}
            return list(empList)

    def shiftData(self, fromdate, todate):
        shiftsTable = self.shiftDB.select_All()
        if shiftsTable == ():
            return []
        else:
            shifts = [[shiftsID, EmployeeID, Date, StartAM, FinAM, BrkAM, StartPM, FinPM, BrkPM, ConcatShift, TotalHours,
                       shiftTypeAM, EmployeeDep]
                      for shiftsID, EmployeeID, Date, StartAM, FinAM, BrkAM, StartPM, FinPM, BrkPM, ConcatShift, TotalHours,
                      shiftTypeAM, shiftTypePM, EmployeeDep, DepAM, DepPM in shiftsTable if fromdate <= Date <= todate]
            return shifts

    def totalrotaHours(self):
        shiftsTable = self.shiftDB.select_All()
        total = [shiftsTable[a][10] for a in range(len(shiftsTable))]
        return sum(total)

    def shiftTypeReportData(self, fromDate, toDate, shiftTypeID):
        shiftsTable = self.shiftDB.select_All()
        shiftTypeData = []
        for a in range(len(shiftsTable)):
            shiftsID = shiftsTable[a][0]
            EmployeeID = shiftsTable[a][1]
            Date = shiftsTable[a][2]
            StartAM = shiftsTable[a][3]
            FinAM = shiftsTable[a][4]
            BrkAM = shiftsTable[a][5]
            StartPM = shiftsTable[a][6]
            FinPM = shiftsTable[a][7]
            BrkPM = shiftsTable[a][8]
            # ConcatShift = shiftsTable[a][9]
            # TotalHours = shiftsTable[a][10]
            shiftTypeAM = shiftsTable[a][11]
            shiftTypePM = shiftsTable[a][12]
            # EmployeeDep =shiftsTable[a][13]
            # DepAM = shiftsTable[a][14]
            # DepPM = shiftsTable[a][15]
            calcAM = ((FinAM - StartAM) - BrkAM)
            calcPM = ((FinPM - StartPM) - BrkPM)

            if fromDate <= Date and toDate >= Date:
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

        return shiftTypeData

    def empTotalHoursPeriod(self, empID, fromDate, toDate):
        hours = 0
        if fromDate > toDate:
            msgBox = QtGui.QMessageBox()
            msgBox.warning(QtGui.QMessageBox(), 'Error', 'to Date is before from date')
        else:
            days = (toDate - fromDate).days
            for x in range(days):
                hours += self.empTotalHoursDay(empID, (fromDate + relativedelta(days=days)), 'day')
            return hours

    def empTotalHoursDay(self, empID, shiftDate, am_pm_day):
        shiftsTable = self.shiftDB.select_All()
        if shiftsTable == ():
            return []
        else:

            if am_pm_day == "am": # calc am shift totals
                shifts = [[FinAM, StartAM, BrkAM, FinPM, StartPM, BrkPM]
                          for
                          shiftsID, EmployeeID, Date, StartAM, FinAM, BrkAM, StartPM, FinPM, BrkPM, ConcatShift, TotalHours,
                          shiftTypeAM, shiftTypePM, EmployeeDep, DepAM, DepPM in shiftsTable if EmployeeID == empID and shiftDate == Date][0]

                if shifts == []:
                    return 0
                else:
                    total = (shifts[0] - shifts[1]) - shifts[2]
                    return total

            elif am_pm_day == "pm": # calc pm shift totals
                shifts = [[FinAM, StartAM, BrkAM, FinPM, StartPM, BrkPM]
                          for
                          shiftsID, EmployeeID, Date, StartAM, FinAM, BrkAM, StartPM, FinPM, BrkPM, ConcatShift, TotalHours,
                          shiftTypeAM, shiftTypePM, EmployeeDep, DepAM, DepPM in shiftsTable if EmployeeID == empID and shiftDate == Date][0]

                if shifts == []:
                    return 0
                else:
                    total = (shifts[3] - shifts[4]) - shifts[5]
                    return total


            elif am_pm_day == "day":  # calc day totals
                shifts = [TotalHours
                          for
                          shiftsID, EmployeeID, Date, StartAM, FinAM, BrkAM, StartPM, FinPM, BrkPM, ConcatShift, TotalHours,
                          shiftTypeAM, shiftTypePM, EmployeeDep, DepAM, DepPM, holHours, holDays in shiftsTable if
                          EmployeeID == empID and shiftDate == Date]

                if shifts == []:
                    return 0
                else:
                    total = shifts[0]
                    return total

            else:
                print ('enter a correct shift type am pm or day as string')
                pass


    def empAMPMshiftTypeAtdate(self, empID, shiftDate):
        shiftsTable = self.shiftDB.select_All()
        if shiftDate is datetime.date:
            print ('Date for RotaData.empAMPMshiftTypeAtDate must datetime.date')
        shifts = [(shiftTypeAM, shiftTypePM) for
                  shiftsID, EmployeeID, Date, StartAM, FinAM, BrkAM, StartPM, FinPM, BrkPM, ConcatShift, TotalHours,
                  shiftTypeAM, shiftTypePM, EmployeeDep, DepAM, DepPM, holHours, holDays in shiftsTable if
                  EmployeeID == empID and shiftDate == Date]
        return shifts


    def calculateQualifyingSickPeriodsInDateRange(self, dateRange):
        empList = self.emp.salCalcEmpList(str(dateRange[0]), str(dateRange[-1]))
        QDEmpDict = {}
        firstDate = []

        # Iterate through emps
        for emp in range(len(empList)):
            counter = 0
            # create key for each emp in list key:[QDs, first Date]
            QDEmpDict[empList[emp][0]] = [0, None]

            # TODO: build in mechanism to join PIWs
            # iterate through dates in range
            for date in range(len(dateRange)):
                # is the date a QD
                if self.emp.empIsDateAContractedDay(empList[emp][0], dateRange[date]) is True:
                    # if shift type empty, pass
                    if self.empAMPMshiftTypeAtdate(empList[emp][0], dateRange[date]) == []:
                        counter = 0
                    else:
                        # if either am or pm shift is sick and the then count
                        if self.empAMPMshiftTypeAtdate(empList[emp][0], dateRange[date])[0][0] == 3 \
                                or self.empAMPMshiftTypeAtdate(empList[emp][0], dateRange[date])[0][1] == 3:
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
                dayRate = self.ratesDB.sickPayDayRate(dateRange[-1])
                QDs = QDEmpDict.get(empID)[0]
                empDaysPerWeek = self.emp.empContractedDaysofWork(empID)[1]
                lowerEarningsLimit = self.ratesDB.SSPLowerEarningsLimit(dateRange[-1])

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
        SSPdata = self.calculateQualifyingSickPeriodsInDateRange(self.generateDateRangeList(fromDate, toDate))
        SSPdata = SSPdata[0]
        return SSPdata

    def calcWageCostforDateRange(self, fromDate, toDate, SSP_on_off):
        print ('calc wage cost for date range dates', fromDate, toDate)
        SSPCheck = SSP_on_off
        dateList = self.generateDateRangeList(fromDate, toDate)
        empList = self.emp.salCalcEmpList(str(fromDate), str(toDate))
        reportTable = []
        self.reportTableINT = []

        if SSPCheck == 0:
            SSPdata = self.calcSSPCostforDateRange(fromDate, toDate)
        else:
            SSPdata = []

        for emp in range(len(empList)):
            empTotalSalary = 0
            empTotalHourly = 0
            nicCost = 0
            pensionCost = 0
            netSalary = 0
            shiftBonusCost = 0

            if SSPCheck == 0:
                SSP = SSPdata[empList[emp][0]][0]
            else:
                SSP = 0

            for date in range(len(dateList)):
                # define the nic variables
                threshold = self.ratesDB.nicThreshold(dateList[date])
                age = self.ratesDB.nicMinAge(dateList[date])
                rate = self.ratesDB.nicRate(dateList[date])
                pensionPercent = self.ratesDB.pensionPecentage(dateList[date])
                empID = empList[emp][0]
                shiftDate = dateList[date]
                shiftType = self.empAMPMshiftTypeAtdate(empID, shiftDate)
                SalariedShiftCost = self.emp.empShiftSalaryCost_ExcludingSickDays(shiftDate, shiftType, empID)
                SalariedNicShiftCost = self.emp.empNicCostByShiftSalary(empID, shiftDate, threshold, age, rate)
                shiftBonusCost = self.emp.empShiftBonusCost(shiftDate, empID)
                HourlyTotalHours = self.empTotalHoursDay(empID, shiftDate, 'day')
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

            self.reportTableINT.append([empList[emp][0], empList[emp][1], nicCost, pensionCost, netSalary, empTotalSalary,
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

        for rec in range(len(self.reportTableINT)):
            empID = self.reportTableINT[rec][0]
            empTotalSalary = self.reportTableINT[rec][5]
            empTotalHourly = self.reportTableINT[rec][6]
            empNetSalary = self.reportTableINT[rec][4]
            empNICTotal = self.reportTableINT[rec][2]
            empBonusTotal = self.reportTableINT[rec][7]
            empPensionTotal = self.reportTableINT[rec][3]
            empSSPtotal = self.reportTableINT[rec][8]

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
        print ('totalHourlyWages, totalSalaryWages, totalNetWages, totalNIC,totalBonus, totalPension, totalGrossSalary, totalSSP')
        print(totalHourlyWages, totalSalaryWages, totalNetWages, totalNIC,
                totalBonus, totalPension, totalGrossSalary, totalSSP)
        return [results, reportTable, self.reportTableINT, totalHourlyWages, totalSalaryWages, totalNetWages, totalNIC,
                totalBonus, totalPension, totalGrossSalary, totalSSP]

    def deleteEmpFromRota(self, empID, dateList):
        Querydb('''DELETE FROM shifts WHERE shifts.EmployeeID = %s AND shifts.`Date` BETWEEN %s AND %s;''',
                (empID, str(dateList[0]), str(dateList[6]))).DeleteOneExecutewithFormatting()

    def addEmpToRota(self, selectionList, selectedDate):
        insertShift = [[int(selectionList[a][1]), str(selectedDate), 0, 0, 0, 0, 0, 0, "", 0,
                        selectionList[a][2], selectionList[a][2], selectionList[a][2]]
                       for a in range(len(selectionList))]
        Querydb('''INSERT INTO shifts (EmployeeID, Date, StartAM, FinAM, BrkAM, StartPM, FinPM, BrkPM, 
                                                            ConcatShift, TotalHours, EmployeeDep, DepAM, DepPM) 
                                VALUE (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s );''',
                insertShift).InsertManyExecutewithFormatting()

    def convertDBdata(self, selectedDep, dateList):
        # Convert data into format to be written to table widget
        # filter the duplicates names from the results with a set and filter for selection in filter combo box
        shiftData = self.queryShiftTable(dateList[0])


        if selectedDep == 'All Staff':
            names = set(shiftData[x][1] for x in range(len(shiftData)))
        elif selectedDep == 'Kitchen & FOH':
            names = set(shiftData[x][1] for x in range(len(shiftData)) if shiftData[x][15]
                             != 'Admin')
        else:
            names = set(shiftData[x][1] for x in range(len(shiftData)) if shiftData[x][15]
                             == selectedDep)

        # Reset results listOfEmployees
        results = []

        # create a listOfEmployees for each name with blanks
        for a in range(len(names)):
            results.append(["", [], [], [], [], [], [], [], int(), "", "", int()])
        for count, name in enumerate(names):  # iterate through names
            results[count][0] = name  # append name to new listOfEmployees
            for i in range(len(shiftData)):  # iterate through records fetched
                if shiftData[i][1] == name:  # if name is found
                    results[count][8] = shiftData[i][0]  # append the employee ID
                    results[count][9] = shiftData[i][13]  # append the employee St Date
                    results[count][10] = shiftData[i][14]  # append the employee Fin Date
                    results[count][11] = shiftData[i][18]  # append the employee department
                    for cols, date in enumerate(dateList):  # iterate through dates
                        if shiftData[i][2] == date:  # if date is found
                            results[count][cols + 1] = [self.convertDecToTime(shiftData[i][5]),  # append times
                                                             self.convertDecToTime(shiftData[i][6]),  # append times
                                                             shiftData[i][16],  # append shift type ie work, hol etc
                                                             self.convertDecToTime(shiftData[i][8]),  # append times
                                                             self.convertDecToTime(shiftData[i][9]),  # append times
                                                             shiftData[i][17],  # append shift type ie work, hol etc
                                                             shiftData[i][19],  # append employee role AM
                                                             shiftData[i][20],  # append employee role PM
                                                             ]
        # sort the listOfEmployees by department
        sort = sorted(results, key=lambda department: department[11])
        results = sort

        return results

    def calculatePredictedCoversTotal(self, fromDate, toDate):
        # Calculate the am and pm cover total summaries
        self.predCoverDB = PredictedCovers()
        coversdata = self.predCoverDB.predCoverDateRange(fromDate, toDate)
        predictedCoverTotal = sum([am + pm for (ID, date, am, pm, rev) in coversdata])

        return predictedCoverTotal

    def calculatePredictedRevenueTotal(self, fromDate, toDate):
        # Calculate the revenue totals for all the cover types from Avg spend * covers
        predictedRevenueTotal = Decimal()
        self.predCoverDB = PredictedCovers()
        coversdata = self.predCoverDB.predCoverDateRange(fromDate, toDate)

        revTypeDB = RevenueTypes()
        avgSpendData = revTypeDB.select_All()

        for x in range(len(coversdata)):  # iterate through extracted pred cover data
            for y in range(len(avgSpendData)):  # iterate through avg spend data
                if str(avgSpendData[y][0]) == str(coversdata[x][4]):
                    predictedRevenueTotal += ((coversdata[x][2] * avgSpendData[y][2]) +
                                              (coversdata[x][3] * avgSpendData[y][3]) +
                                              (coversdata[x][2] * avgSpendData[y][4]) +
                                              (coversdata[x][3] * avgSpendData[y][5]))
        return predictedRevenueTotal

    def generateWkDateList(self, selectedDate):
        dateList = self.generateDateRangeList(selectedDate, selectedDate + relativedelta(days=6))
        return dateList

    def generateSelectedMonthDateRange(self, selectedDate, wkDateList):
        date = selectedDate

        weekDateList = wkDateList
        # print('week date list', weekDateList)

        # determine if the week is more one month or other
        monthCounter = 0
        for d in range(6):
            if weekDateList[0].month == weekDateList[d + 1].month:
                monthCounter += 1
            else:
                pass
        # print('month Counter', monthCounter)

        # if week is more one month, make adjustment
        if monthCounter < 3:
            date = date + relativedelta(months=1)
            month = date.month
            year = date.year
        else:
            month = date.month
            year = date.year

        firstOfMonth = datetime.date(year, month, 1)
        endOfWeek = date + datetime.timedelta(days=6)
        daysInMonth = calendar.monthrange(date.year, date.month)[1]
        dateRange = []

        for day in range(0, daysInMonth):
            # if monday of selected week is greater than the first of the month add preceding dates to the list
            if date > firstOfMonth + relativedelta(days=day):
                dateRange.append(firstOfMonth + relativedelta(days=day))
            else:
                # add the remaining days if less than end of week
                if (firstOfMonth + relativedelta(days=day)) <= endOfWeek:
                    dateRange.append(firstOfMonth + relativedelta(days=day))
                else:
                    break
        # print ('MTD Range', dateRange)
        # print ('Date', date, 'End of week', endOfWeek, 'days in Month', daysInMonth, 'first of Month', firstOfMonth)
        return dateRange

    def generateDateRangeList(self, fromDate, toDate):
        self.dateList = []
        days = (toDate - fromDate).days
        for days in range(days + 1):
            self.dateList.append(fromDate + relativedelta(days=days))
        return self.dateList

    def queryShiftTable(self, selectedDate):
        # Get shift data from DB
        d = selectedDate
        d2 = selectedDate + relativedelta(days=6)

        fetched = Querydb("""
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
        return fetched

    def convertDecToTime(self, time):
        hours = int(time)
        mins = (time * 60) % 60
        return "%02d:%02d" % (hours, mins)

    def datetoMonday(self, date):
        dateNum = datetime.date.weekday(QtCore.QDate.toPyDate(date))
        if dateNum == 0:
            return date
        else:
            pydate = QtCore.QDate.toPyDate(date)
            adjustDate = pydate - datetime.timedelta(days=dateNum)
            return QtCore.QDate(adjustDate)

    def refreshAndReloadEmpClass(self):
        self.emp = employees()
        return self.emp

class Querydb():
    def __init__(self, sql, formatting):
        self.host = '127.0.0.1'
        self.username = "phil"
        self.password = "g4ngst3r"
        self.db = 'mydb'
        self.sql = sql
        self.formating = formatting


    def fetchAllRecordswithFormatting(self):
        # fetch many records with listOfEmployees comprehension and an additional and optional formatting variable
        db = MySQLdb.connect(self.host, self.username, self.password, self.db)
        cursor = db.cursor()
        try:
            cursor.execute(self.sql, self.formating)
            fetched = cursor.fetchall()
            db.close()
            print (cursor._last_executed)
            cursor.close()
            return fetched
        except(MySQLdb.Error, MySQLdb.Warning) as e:
            QtGui.QMessageBox.warning(QtGui.QMessageBox(), 'Error', str(e))
            db.rollback()
            db.close()
            cursor.close()

    def executeManyfetchAllRecordswithFormatting(self):
        # fetch many records with listOfEmployees comprehension and an additional and optional formatting variable
        db = MySQLdb.connect(self.host, self.username, self.password, self.db)
        cursor = db.cursor()
        try:
            cursor.executemany(self.sql, self.formating)
            fetched = cursor.fetchall()
            db.close()
            print (cursor._last_executed)
            cursor.close()
            return fetched
        except(MySQLdb.Error, MySQLdb.Warning) as e:
            QtGui.QMessageBox.warning(QtGui.QMessageBox(), 'Error', str(e))
            db.rollback()
            db.close()
            cursor.close()

    def InsertManyExecutewithFormatting(self):
        # insert many records with listOfEmployees comprehension and an additional and optional formatting variable
        db = MySQLdb.connect(self.host, self.username, self.password, self.db)
        cursor = db.cursor()
        try:
            cursor.executemany(self.sql, self.formating)
            db.commit()
            db.close()
            print (cursor._last_executed)
            cursor.close()
        except(MySQLdb.Error, MySQLdb.Warning) as e:
            QtGui.QMessageBox.warning(QtGui.QMessageBox(), 'Error', str(e))
            db.rollback()
            db.close()
            cursor.close()

    def InsertOneExecutewithFormatting(self):
        # insert one records with listOfEmployees comprehension and an additional and optional formatting variable
        db = MySQLdb.connect(self.host, self.username, self.password, self.db)
        cursor = db.cursor()
        try:
            cursor.execute(self.sql, self.formating)
            db.commit()
            db.close()
            print (cursor._last_executed)
            cursor.close()
        except(MySQLdb.Error, MySQLdb.Warning) as e:
            QtGui.QMessageBox.warning(QtGui.QMessageBox(), 'Error', str(e))
            db.rollback()
            db.close()
            cursor.close()

    def DeleteOneExecutewithFormatting(self):
        # Delete one records with listOfEmployees comprehension and an additional and optional formatting variable
        db = MySQLdb.connect(self.host, self.username, self.password, self.db)
        cursor = db.cursor()
        try:
            cursor.execute(self.sql, self.formating)
            db.commit()
            db.close()
            print (cursor._last_executed)
            cursor.close()
        except(MySQLdb.Error, MySQLdb.Warning) as e:
            QtGui.QMessageBox.warning(QtGui.QMessageBox(), 'Error', str(e))
            db.rollback()
            db.close()
            cursor.close()

    def DeleteOneExecutewithFormatting_ErrorMessage(self, message):
        # Delete one records with listOfEmployees comprehension and an additional and optional formatting variable
        db = MySQLdb.connect(self.host, self.username, self.password, self.db)
        cursor = db.cursor()
        try:
            cursor.execute(self.sql, self.formating)
            db.commit()
            db.close()
            print (cursor._last_executed)
            cursor.close()
        except(MySQLdb.Error, MySQLdb.Warning):
            QtGui.QMessageBox.warning(QtGui.QMessageBox(), 'Error', str(message))
            db.rollback()
            db.close()
            cursor.close()

    def DeleteManyExecutewithFormatting(self):
        # Delete many records with listOfEmployees comprehension and an additional and optional formatting variable
        db = MySQLdb.connect(self.host, self.username, self.password, self.db)
        cursor = db.cursor()
        try:
            cursor.execute(self.sql, self.formating)
            db.commit()
            db.close()
            print (cursor._last_executed)
            cursor.close()
        except(MySQLdb.Error, MySQLdb.Warning) as e:
            QtGui.QMessageBox.warning(QtGui.QMessageBox(), 'Error', str(e))
            db.rollback()
            db.close()
            cursor.close()

    def DeleteManyExecutewithFormatting_ErrorMessage(self, message):
        # Delete many records with listOfEmployees comprehension and an additional and optional formatting variable
        db = MySQLdb.connect(self.host, self.username, self.password, self.db)
        cursor = db.cursor()
        try:
            cursor.execute(self.sql, self.formating)
            db.commit()
            db.close()
            print (cursor._last_executed)
            cursor.close()
        except(MySQLdb.Error, MySQLdb.Warning):
            QtGui.QMessageBox.warning(QtGui.QMessageBox(), 'Error', str(message))
            db.rollback()
            db.close()
            cursor.close()

class PassPhrase:
    def __init__(self, uname, PwdAttempt):
        self.uname = uname
        self.HashPhrase = ()
        self.PwdAttempt = PwdAttempt
        self.uaccess = int()
        self.accessdb()

    def accessdb(self):
        try:
            db = MySQLdb.connect("localhost", "hash", "ad3rl24Ab9", "hash")
            cursor = db.cursor()

            cursor.execute('''
                    SELECT hashphrase, uaccesslevel 
                    FROM hash
                    WHERE uname = %s
                    ''' , [self.uname])


            fetched = cursor.fetchall()


            self.HashPhrase = fetched[0][0]
            self.uaccess = fetched[0][1]
            db.close()
            cursor.close()
            self._CheckPwd()


        except(MySQLdb.Warning, MySQLdb.Error) as e:
            print ('Unable to access credentials, check connection')
            print (e)

    def _CheckPwd(self):
        if hashpw(self.PwdAttempt, self.HashPhrase) == self.HashPhrase:
            #print "Well Done!"
            return True
        else:
            print ("Incorrect Password or Username")

class ConvertHashPhrase:
    def __init__(self, uname, pwd, pwd2):
        self.uname = uname
        self.pwd = pwd
        self.pwd2 = pwd2
        self.hashed = ""

    def hash(self):
        if self.pwd == self.pwd2:
            self.hashed = hashpw(self.pwd, gensalt())
            print (self.hashed)

        else:
            print("passwords didn't match, please try again")

class salary:
    def __init__(self, employeeID, shiftDate_DateTime):
        # Salary, pension and NIC calculation
        self.shiftDate = shiftDate_DateTime
        self.salTable = Querydb("""SELECT SalaryID, EmployeeID, PoundsPerHour, Salary, AdjustDate, 
                                    Employee_TBL.EmpStDate, Employee_TBL.EmpFinDate 
                                    FROM Salary 
                                    INNER JOIN `Employee_TBL` 
                                    ON Salary.EmployeeID = idEmployee_TBL 
                                    ORDER BY EmployeeID, AdjustDate ASC""", None).fetchAllRecordswithFormatting()
        self.empTable = Querydb("""SELECT * FROM Employee_TBL""", None).fetchAllRecordswithFormatting()
        self.bonusTable = Querydb("""SELECT * FROM Bonus WHERE %s BETWEEN BonusPeriodStDate AND bonusPayDate""", (self.shiftDate,)).fetchAllRecordswithFormatting()
        self.salaryCalVariables = Querydb("""SELECT * FROM SalaryCalVariables ORDER BY VariablesDate ASC""", None).fetchAllRecordswithFormatting()
        self.employeeID = employeeID
        self.employee = [DOB for (empID, name, DOB, depID, salOrHourly, adrs, email, home, mobile, empSt, empFin, contractedDays)
                         in self.empTable if empID == self.employeeID]

        # filter bonusTableWidget data according against shift date, periodStDate and PayDate, append for summing
        self.bonusdata = []
        for ID, bonus, empID, bonusPayDate, bonusPeriodStDate in self.bonusTable:
            if empID == self.employeeID:
                if self.shiftDate <= bonusPayDate:
                    if self.shiftDate >= bonusPeriodStDate:
                        self.bonusdata.append([bonus, (bonusPayDate - bonusPeriodStDate).days])
                    else:
                        pass
                else:
                    pass
            else:
                pass

        self.variables = max([[VDate, minAge, nicRate, threshold, penPerc] for (ID, minAge, nicRate, threshold, penPerc, VDate)
                          in self.salaryCalVariables if self.shiftDate >= VDate])

        # filter salary data, if leaving date is not filled in assume still employed, otherwise compare with shift date
        self.salarydata = [None, 0]
        for salid2, empid2, pph2, sal2, AdjustD2, EmpStDate2, EmpFinDate2 in self.salTable:
            if empid2 == self.employeeID:
                if AdjustD2 <= self.shiftDate:
                    if self.shiftDate is None:
                        self.salarydata = [AdjustD2, sal2]
                    elif self.shiftDate <= EmpFinDate2:
                        self.salarydata = [AdjustD2, sal2]
                    else:
                        pass
                else:
                    pass
            else:
                pass
        # self.salarydata = max([[AdjustD, sal] for (salid, empid, pph, sal, AdjustD, EmpStDate, EmpFinDate) in self.salTable
        # if empid == self.employeeID and AdjustD <= self.shiftDate])

    def dailySalariedWageCalc(self):
        return (self.salaryAtShiftDate() / 365) + self.dailyBonusAtShiftDate() + self.salariedEmpNicDailyCalc() + self.pensionCalcDaily()

    def nicMinAge(self):
        return self.variables[1]

    def nicRate(self):
        return self.variables[2]

    def nicThreshold(self):
        return self.variables[3]

    def penPercentage(self):
        return self.variables[4]

    def salaryAtShiftDate(self):
        return self.salarydata[1]

    def pensionCalcDaily(self):
        return (((self.salaryAtShiftDate() / 12) + self.salariedEmpNicMonthlyCalc()) * self.penPercentage()) * 12 / 365

    def salariedEmpNicDailyCalc(self):
        if self.ageAtShiftDate() < self.nicMinAge():
            return 0
        else:
            if (((self.salaryAtShiftDate()/12) + self.dailyBonusAtShiftDate()) - self.nicThreshold()) > 0:
                return (((self.salaryAtShiftDate()/12) + self.dailyBonusAtShiftDate() -
                         self.nicThreshold()) * self.nicRate()) * 12 / 365
            else:
                return 0

    def salariedEmpNicMonthlyCalc(self):
        if self.ageAtShiftDate() < self.nicMinAge():
            return 0
        else:
            if (((self.salaryAtShiftDate()/12) + self.dailyBonusAtShiftDate()) - self.nicThreshold()) > 0:
                return ((self.salaryAtShiftDate()/12) + self.dailyBonusAtShiftDate() - self.nicThreshold()) * self.nicRate()
            else:
                return 0

    def dailyBonusAtShiftDate(self):
        self.dailybonustotals = 0
        if self.bonusdata == []:
            return 0
        else:
            for x in range(len(self.bonusdata)):
                self.dailybonustotals += self.bonusdata[x][0] / self.bonusdata[x][1]

        return self.dailybonustotals

    def ageAtShiftDate(self):
        ageAtShiftDate = float((self.shiftDate - self.employee[0]).days) / 365
        return ageAtShiftDate

    def age(self):
        age = float((datetime.date.today() - self.employee[0]).days) / 365
        return age


class employees:
    def __init__(self):
        empDB = EmployeeTbl()
        self.__empTable = empDB.select_All()

        salDB = Salary()
        self.__salTable = salDB.select_All()

        depDB = Departments()
        self.__depTable = depDB.select_All()

        bonusDB = Bonus()
        self.__bonusTable = bonusDB.select_All()

        holsDB = HolidayEntitlements()
        self.__holsTable = holsDB.select_All()

        salOrHourly = SalaryOrHourly()
        self.__salorHourlyTable = salOrHourly.select_All()

    def empSalaryPensionShiftCalc(self, empID, shiftDate, nicThresholdatShiftDate, nicMinAgeAtShiftDate, nicRateAtShiftDate, pensionPercentageAtShiftDate):
        """
        TODO: need to add the min / max threshold for pension calc into the payroll variable GUI
        TODO: Needs to include: Salary, overtime, holiday pay, sick pay, bonuses, maternity pay
        TODO: add payroll Min age into payroll variables
        """
        minThreshold = 6032
        maxThreshold = 46350
        empSalaryCostAtShift = self.empShiftSalaryCost_Deduction(shiftDate, empID, minThreshold)
        empSalaryCostAtShift += self.empShiftBonusCost(shiftDate, empID)

        if empSalaryCostAtShift == 0 and pensionPercentageAtShiftDate == 0:
            print ('no data to return')
        else:
            if self.empAge(empID, shiftDate) >= 22:
                return empSalaryCostAtShift * pensionPercentageAtShiftDate
            else:
                return 0

    def empHourlyPensionShiftCalc(self, empID, shiftDate, nicThresholdatShiftDate, nicMinAgeAtShiftDate, nicRateAtShiftDate, pensionPercentageAtShiftDate):
        """
        TODO: need to add the min Max threshold for pension calc into the payroll variable GUI
        TODO: Needs to include: Salary, overtime, holiday pay, sick pay, bonuses, maternity pay
        TODO: add payroll Min age into payroll variables
        """
        minThreshold = 6032
        maxThreshold = 46350
        empHoulryCostAtShift = self.empShiftHourlyPay(shiftDate, empID)
        empHoulryCostAtShift += self.empShiftBonusCost(shiftDate, empID)

        if empHoulryCostAtShift == 0 and pensionPercentageAtShiftDate == 0:
            print('no data to return')
        else:
            if self.empAge(empID, shiftDate) >= 22:
                return empHoulryCostAtShift * pensionPercentageAtShiftDate
            else:
                return 0

    def empNicCostByShiftSalary(self, empID, shiftDate, nicThresholdatShiftDate, nicMinAgeAtShiftDate, nicRateAtShiftDate):
        #TODO: Build a mechanism to reduce to 2 percent if earnings are over 892 per week

        salAtShift = self.empSalaryAtShiftDate(shiftDate, empID)
        bonusAtShift = self.empShiftBonusCost(shiftDate, empID)
        upperSecondaryThreshold = 3750
        USTupperAge = 20

        # This might be slightly incorrect but I can't be arsed to work it out......
        # shiftDate = shiftDate - relativedelta(months=-1)

        if self.empAge(empID, shiftDate) < nicMinAgeAtShiftDate:
            return 0

        # if employee is under the UST threshold age limit then deduct the UST from the salary to calc NIC
        elif self.empAge(empID, shiftDate) < USTupperAge + 1:
            if ((salAtShift + bonusAtShift) / 12) - upperSecondaryThreshold > 0:
                calc = (salAtShift + bonusAtShift) / 12
                calc -= upperSecondaryThreshold
                calc *= nicRateAtShiftDate
                calc *= 12
                calc /= self.empContractedAnualDays()
                return calc
            else:
                return 0
        else:
            if ((salAtShift + bonusAtShift / 12) - nicThresholdatShiftDate) > 0:
                calc = (salAtShift + bonusAtShift) / 12
                calc -= nicThresholdatShiftDate
                calc *= nicRateAtShiftDate
                #calc *= 12
                calc /= self.daysInMonth(shiftDate)
                return calc

            else:
                return 0

    def empNicCostByShiftHourly(self, empID, shiftDate, nicThresholdatShiftDate, nicMinAgeAtShiftDate, nicRateAtShiftDate):
        # Calculate the NIC cost of hourly members of staff by using the previous 30 days wage and NIC totals

        daysInMonthBefore = monthrange(shiftDate.year, shiftDate.month)[1]
        previousMonthsWageCost = 0
        for a in range(daysInMonthBefore):
            total = self.empShiftHourlyPay(shiftDate - datetime.timedelta(days=a), empID) \
                    + self.empShiftBonusCost(shiftDate - datetime.timedelta(days=a), empID)
            previousMonthsWageCost += total
        if self.empAge(empID, shiftDate) < nicMinAgeAtShiftDate:
            return 0
        else:
            if ((previousMonthsWageCost) - nicThresholdatShiftDate) > 0:
                return ((previousMonthsWageCost - nicThresholdatShiftDate) * nicRateAtShiftDate) * 12 / 365
            else:
                return 0

    def empSalaryAtShiftDate(self, shiftDate, empID):
        salary = []
        if self.empSalaryOrHourlyID(empID) == 0:  # if emp has salary then process, if hourly skip
            salary = [[adjustDate, pph, sal] for salID, ID, pph, sal, adjustDate in self.__salTable if
                      empID == ID and shiftDate >= adjustDate]
        else:
            return 0

        if salary == []:
            return 0
        else:
            return max(salary)[2]

    def empShiftSalaryCost_Deduction(self, shiftDate, empID, annual_deduction):
        salary = []
        deduct = annual_deduction
        daysInMonth = self.daysInMonth(shiftDate)
        if self.empSalaryOrHourlyID(empID) == 0:  # if emp has salary then process, if hourly skip
            salary = [[adjustDate, pph, sal] for salID, ID, pph, sal, adjustDate in self.__salTable if
                      empID == ID and shiftDate >= adjustDate]
        else:
            pass

        if salary == []:
            return 0
        else:
            if max(salary)[2] == 0:
                deduct = 0
            return (max(salary)[2] - deduct) / 12 / daysInMonth
            # self.empContractedAnualDays()

    def daysInMonth(self, monthDate):
        month = monthDate.month
        year = monthDate.year
        daysInMonth = monthrange(year, month)[1]

        return daysInMonth

    def empShiftSalaryCost_ExcludingSickDays(self, shiftDate, shiftType, empID):
        #TODO: need to work out a mechanism that deals with different working paterns ie. 3 days per week not 5
        #TODO: finish the shift type controls ie Work vs Holiday vs MAT PAY
        #TODO: Build in a department function ie if 0 is selected count all, if 1 is selected count all ex ADMIN
        salary = []
        daysInMonth = self.daysInMonth(shiftDate)
        if self.empSalaryOrHourlyID(empID) == 0:    # if emp has salary then process, if hourly skip
            salary = [[adjustDate, pph, sal] for salID, ID, pph, sal, adjustDate in self.__salTable if
                      empID == ID and shiftDate >= adjustDate]

        else:
            pass

        if salary == []:
            return 0

        elif shiftType == []:
            return max(salary)[2] / 12 / daysInMonth
        else:
            standardShift = max(salary)[2] / 12 / daysInMonth / 2 # self.empContractedAnualDays()
            daySum = 0
            shiftType = shiftType[0]


            if shiftType[0] == 0 : # blank
                daySum += standardShift
            elif shiftType[0] == 1: # Work
                daySum += standardShift
            elif shiftType[0] == 2: # Holiday
                daySum += standardShift # if allowance has been used at this date then 0 else standard week
            elif shiftType[0] == 3: # Sick
                daySum += 0
            elif shiftType[0] == 4: # On-Call
                daySum += standardShift
            elif shiftType[0] == 5: # Unavailable
                daySum += standardShift
            elif shiftType[0] == 6: # Over-Time
                daySum += standardShift
            elif shiftType[0] == 7: # MAT - PAT
                daySum += standardShift
            else:
                print('ERROR - unknown / missing shift Type in emp.empShiftSalaryCost calculation' )


            if shiftType[1] == 0 : # blank
                daySum += standardShift
            elif shiftType[1] == 1: # Work
                daySum += standardShift
            elif shiftType[1] == 2: # Holiday
                daySum += standardShift # if allowance has been used at this date then 0 else standard week
            elif shiftType[1] == 3: # Sick
                daySum += 0
            elif shiftType[1] == 4: # On-Call
                daySum += standardShift
            elif shiftType[1] == 5: # Unavailable
                daySum += standardShift
            elif shiftType[1] == 6: # Over-Time
                daySum += standardShift
            elif shiftType[1] == 7: # MAT - PAT
                daySum += standardShift
            else:
                print('ERROR - unknown / missing shift Type in emp.empShiftSalaryCost calculation' )

            return daySum

    def empShiftHourlyPay(self, shiftDate, empID):
        hourly = []
        if self.empSalaryOrHourlyID(empID) == 1:     # is the emp on hourly
            hourly = [[adjustDate, pph, sal] for salID, ID, pph, sal, adjustDate in self.__salTable if
                      empID == ID and shiftDate >= adjustDate]
        else:
            pass

        if hourly == []:
            return 0
        else:
            return max(hourly)[1]

    def empShiftBonusCost(self, shiftDate, empID):
        # Calculate the bonus to be allocated to specified shift date. Bonus total devided by the number of days between
        # start and pay date

        bonusSum = 0
        bonus = [[BonusPeriodStDate, (bonus / (bonusPayDate - BonusPeriodStDate).days)] for
                 bonusID, bonus, EmployeeID, BonusPeriodStDate, bonusPayDate in self.__bonusTable if
                 empID == EmployeeID and BonusPeriodStDate <= shiftDate < bonusPayDate]
        if bonus == []:
            return 0
        else:
            for a in range(len(bonus)):
                bonusSum += bonus[a][1]

        return bonusSum

    #FIXME: NEED TO ADD THE FUNCTIONALITY FOR THIS!!!!!!!
    def empContractedAnualDays(self):
        return 52*7


    def empBonuses(self, empID):
        if self.__bonusTable is ():
            return None
        else:
            data = [[bonusID, bonus, periodStDate, payDate] for bonusID, bonus, ID, periodStDate, payDate in self.__bonusTable if ID == empID]
            return data

    def empHolidayEntitlements(self, empID):
        if self.__holsTable is ():
            return None
        else:
            data = [[holsID, entitlement, adjustDate] for holsID, ID, entitlement, adjustDate in
                    self.__holsTable if ID == empID]
            return data

    def empHolidayEntitlementAtDate(self, empID, date):
        if self.__holsTable is ():
            return None
        else:
            data = [[adjustDate, entitlement] for holsID, ID, entitlement, adjustDate in
                    self.__holsTable if ID == empID and adjustDate <= date]
            #print ('holiday entitlement at Date', max(data)[1])
            return max(data)[1]

    def empSalaries(self, empID):
        if self.__salTable is ():
            return None
        else:
            data = [[salID, sal, PPH, adjustDate] for salID, ID, PPH, sal, adjustDate in self.__salTable if ID == empID]
            return data

    def empContractedDaysofWork(self, empID):
        if self.__empTable is ():
            return None
        else:
            data = [(QDm, QDt, QDw, QDth, QDf, QDs, QDsu) for
                    ID, name, DOB, Dep, sal, adr, email, Hphone, Mphone, empSD, empFD, empCAD, QDm, QDt, QDw, QDth, QDf, QDs, QDsu
                    in self.__empTable if ID == empID][0]
            daysperweek = sum(data)
            return [data, daysperweek]

    def empIsDayAContractedDay(self, empID, dayNum0_6):
        if self.__empTable is ():
            return None
        else:
            data = [(QDm, QDt, QDw, QDth, QDf, QDs, QDsu) for
                    ID, name, DOB, Dep, sal, adr, email, Hphone, Mphone, empSD, empFD, empCAD, QDm, QDt, QDw, QDth, QDf, QDs, QDsu
                    in self.__empTable if ID == empID][0]
            if data[dayNum0_6] is 1:
                return True
            else:
                return False

    def empIsDateAContractedDay(self, empID, date):
        if self.__empTable is ():
            return None
        else:
            data = [(QDm, QDt, QDw, QDth, QDf, QDs, QDsu) for
                    ID, name, DOB, Dep, sal, adr, email, Hphone, Mphone, empSD, empFD, empCAD, QDm, QDt, QDw, QDth, QDf, QDs, QDsu
                    in self.__empTable if ID == empID][0]

            if data[date.weekday()] is 1:
                return True
            else:
                return False

    def empRecord(self, empID):
        if self.__empTable is ():
            return None
        else:
            data = [(ID, name, DOB, Dep, sal, adr, email, Hphone, Mphone, empSD, empFD) for
                     ID, name, DOB, Dep, sal, adr, email, Hphone, Mphone, empSD, empFD, empCAD, QDm, QDt, QDw, QDth, QDf,
                     QDs, QDsu in self.__empTable if
                     ID == empID][0]
            return data

    def empName(self, empID):
        if self.__empTable is ():
            return ""
        else:
            data = [name for ID, name, DOB, Dep, sal, adr, email, Hphone, Mphone, empSD, empFD, empCAD, QDm, QDt, QDw, QDth,
                             QDf, QDs, QDsu in self.__empTable if
                     ID == empID]

            if data == []:
                print ('No Employee Data for Range ')
                return ""
            else:
                return data[0]


    def empDOB(self, empID):
        if self.__empTable is ():
            return QtCore.QDate.fromString('1980-01-01', 'yyyy-M-d')
        else:
            data = [DOB for ID, name, DOB, Dep, sal, adr, email, Hphone, Mphone, empSD, empFD, empCAD, QDm, QDt, QDw, QDth,
                         QDf, QDs, QDsu in self.__empTable if ID == empID]

            if data == []:
                return QtCore.QDate.fromString('1980-01-01', 'yyyy-M-d')
            else:
                return data[0]

    def empID(self, empName):
        if self.__empTable is ():
            return None
        else:
            data = [ID for ID, name, DOB, Dep, sal, adr, email, Hphone, Mphone, empSD, empFD, empCAD, QDm, QDt, QDw, QDth,
                           QDf, QDs, QDsu in self.__empTable if
                     name == empName]
            if data == []:
                return None
            else:
                return data[0]

    def empDepID(self, empID):
        if self.__empTable is ():
            return None
        else:
            data = [DepID for ID, name, DOB, DepID, salID, adr, email, Hphone, Mphone, empSD, empFD, empCAD, QDm, QDt,
                              QDw, QDth, QDf, QDs, QDsu in self.__empTable if
                    ID == empID]
            if data == []:
                return None
            else:
                return data[0]


    def empDepName(self, empID):
        if self.__empTable is ():
            return ""
        else:
            empData = [DepID for ID, name, DOB, DepID, salID, adr, email, Hphone, Mphone, empSD, empFD, empCAD, QDm,
                                 QDt, QDw, QDth, QDf, QDs, QDsu in self.__empTable if
                    ID == empID][0]
            data = [depType for ID, depType in self.__depTable if ID == empData][0]
            return data

    def empSalaryOrHourlyID(self, empID):
        if self.__empTable is ():
            return None
        else:
            data = [salID for ID, name, DOB, DepID, salID, adr, email, Hphone, Mphone, empSD, empFD, empCAD, QDm, QDt,
                              QDw, QDth, QDf, QDs, QDsu in self.__empTable if
                     ID == empID]
            if data == []:
                return None
            else:
                return data[0]


    def empSalaryOrHourlyName(self, empID):
        if self.__empTable is ():
            return None
        else:
            empData = [salID for ID, name, DOB, DepID, salID, adr, email, Hphone, Mphone, empSD, empFD, empCAD, QDm,
                                 QDt, QDw, QDth, QDf, QDs, QDsu in self.__empTable if
                       ID == empID][0]
            data = [sal for ID, sal in self.__salorHourlyTable if ID == empData][0]
            return data

    def empAdrs(self, empID):
        if self.__empTable is ():
            return ""
        else:
            data = [adr for ID, name, DOB, Dep, sal, adr, email, Hphone, Mphone, empSD, empFD, empCAD, QDm, QDt, QDw, QDth,
                            QDf, QDs, QDsu in self.__empTable if
                     ID == empID]
            if data == []:
                return ""
            else:
                return data[0]


    def empEmail(self, empID):
        if self.__empTable is ():
            return ""
        else:
            data = [email for ID, name, DOB, Dep, sal, adr, email, Hphone, Mphone, empSD, empFD, empCAD, QDm, QDt,
                              QDw, QDth, QDf, QDs, QDsu in self.__empTable if
                     ID == empID]
            if data == []:
                return ""
            else:
                return data[0]

    def empHphone(self, empID):
        if self.__empTable is ():
            return ""
        else:
            data = [Hphone for ID, name, DOB, Dep, sal, adr, email, Hphone, Mphone, empSD, empFD, empCAD, QDm, QDt,
                               QDw, QDth, QDf, QDs, QDsu in self.__empTable if
                     ID == empID]
            if data == []:
                return ""
            else:
                return data[0]

    def empMphone(self, empID):
        if self.__empTable is ():
            return ""
        else:
            data = [Mphone for ID, name, DOB, Dep, sal, adr, email, Hphone, Mphone, empSD, empFD, empCAD, QDm, QDt,
                               QDw, QDth, QDf, QDs, QDsu in self.__empTable if
                     ID == empID]
            if data == []:
                return ""
            else:
                return data[0]

    def empStartDate(self, empID):
        if self.__empTable is ():
            return datetime.date.today()
        else:
            data = [empSD for ID, name, DOB, Dep, sal, adr, email, Hphone, Mphone, empSD, empFD, empCAD, QDm, QDt,
                              QDw, QDth, QDf, QDs, QDsu in self.__empTable if
                      ID == empID]
            if data == []:
                return datetime.date.today()
            else:
                return data[0]

    def empFinishDate(self, empID):
        if self.__empTable is ():
            return datetime.date.today()
        else:
            data = [empFD for ID, name, DOB, Dep, sal, adr, email, Hphone, Mphone, empSD, empFD, empCAD, QDm, QDt,
                              QDw, QDth, QDf, QDs, QDsu in self.__empTable if
                      ID == empID]
            if data == []:
                return datetime.date.today()
            else:
                return data[0]

    def empAge(self, empID, todayDate):
        if self.__empTable is ():
            return 0
        else:
            data = [DOB for ID, name, DOB, Dep, sal, adr, email, Hphone, Mphone, empSD, empFD, empCAD, QDm, QDt,
                            QDw, QDth, QDf, QDs, QDsu in self.__empTable if
                    ID == empID][0]
            today = todayDate
            dob = datetime.datetime.strptime(str(data), '%Y-%m-%d').date()

            age = float((today - dob).days) / 365

            return age


    def NameListEmpList(self, fromDate, toDate, ):
        # Return a listOfEmployees of employees with start dates and finish dates between two dates
        if self.__empTable is ():
            return []
        else:
            emplist = []
            for a in range(len(self.__empTable)):
                if self.__empTable[a][9] >= datetime.datetime.strptime(fromDate, '%Y-%m-%d').date() and \
                        self.__empTable[a][9] <= datetime.datetime.strptime(toDate, '%Y-%m-%d').date():
                    if self.__empTable[a][10] is None:
                        emplist.append([self.__empTable[a][0], self.__empTable[a][1]])
                    else:
                        if self.__empTable[a][10] >= datetime.datetime.strptime(toDate, '%Y-%m-%d').date():
                            pass
                        else:
                            emplist.append([self.__empTable[a][0], self.__empTable[a][1]])
                else:
                    pass
            return emplist

    def salCalcEmpList(self, fromDate, toDate):
        # Return a listOfEmployees of employees that are employeed at the point, between two dates
        if self.__empTable is ():
            return []
        else:
            emplist = []
            for a in range(len(self.__empTable)):
                #TODO: Add an if statement that determines the department to allow the wage calc to exclude Admin
                if self.__empTable[a][9] <= datetime.datetime.strptime(fromDate, '%Y-%m-%d').date() and \
                        datetime.datetime.strptime(toDate, '%Y-%m-%d').date() >= self.__empTable[a][9]:
                    if self.__empTable[a][10] is None:
                        emplist.append([self.__empTable[a][0], self.__empTable[a][1]])
                    else:
                        if self.__empTable[a][10] >= datetime.datetime.strptime(toDate, '%Y-%m-%d').date():
                            pass
                        else:
                            emplist.append([self.__empTable[a][0], self.__empTable[a][1]])
                else:
                    pass
            return emplist

    def isEmpCurrentlyEmployed(self, empID, eDate):
        if self.empFinishDate(empID) is None:
            if self.empStartDate(empID) <= eDate:
                return True
            else:
                return False
        else:
            if self.empStartDate(empID) <= eDate >= self.empFinishDate(empID):
                return True
            else:
                return  False


    def empDaysemployedWithinDateRange(self, empID, startDate, endDate):
        days = (endDate - startDate).days
        dateRange = []
        for D in xrange(days+1):
            if self.empStartDate(empID) <= startDate + relativedelta(days=D):
                dateRange.append(startDate + relativedelta(days=D))
            else:
                pass
        return len(dateRange)