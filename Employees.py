#!/usr/bin/python
import cProfile
import datetime
import calendar
from PyQt4 import QtCore, QtGui
from calendar import monthrange
import payrollVariablePopUP
import RotaData
import DB
from dateutil.relativedelta import *




class employees:
    def __init__(self, empTable, salTable, departmentsTable, bonusTable, holsTable, salorHourlyTable):
        self.__empTable = empTable
        self.__salTable = salTable
        self.__depTable = departmentsTable
        self.__bonusTable = bonusTable
        self.__holsTable = holsTable
        self.__salorHourlyTable = salorHourlyTable

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