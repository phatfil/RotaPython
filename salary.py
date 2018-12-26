import DB
import datetime
import decimal


class salary:
    def __init__(self, employeeID, shiftDate_DateTime):
        # Salary, pension and NIC calculation
        self.shiftDate = shiftDate_DateTime
        self.salTable = DB.Querydb("""SELECT SalaryID, EmployeeID, PoundsPerHour, Salary, AdjustDate, 
                                    Employee_TBL.EmpStDate, Employee_TBL.EmpFinDate 
                                    FROM Salary 
                                    INNER JOIN `Employee_TBL` 
                                    ON Salary.EmployeeID = idEmployee_TBL 
                                    ORDER BY EmployeeID, AdjustDate ASC""", None).fetchAllRecordswithFormatting()
        self.empTable = DB.Querydb("""SELECT * FROM Employee_TBL""", None).fetchAllRecordswithFormatting()
        self.bonusTable = DB.Querydb("""SELECT * FROM Bonus WHERE %s BETWEEN BonusPeriodStDate AND bonusPayDate""", (self.shiftDate,) ).fetchAllRecordswithFormatting()
        self.salaryCalVariables = DB.Querydb("""SELECT * FROM SalaryCalVariables ORDER BY VariablesDate ASC""", None).fetchAllRecordswithFormatting()
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




