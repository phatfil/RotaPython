import Core

class DailyActuals:
    def __init__(self):
        self.data = Core.Querydb('SELECT * FROM DailyActuals', None).fetchAllRecordswithFormatting()

    def select_All(self):
        return self.data

    def dailyActualsByDateRange(self, fromDate, toDate):
        data = Core.Querydb('''SELECT * FROM DailyActuals Where actualsDate BETWEEN %s AND %s''',
                (fromDate, toDate)).fetchAllRecordswithFormatting()
        print('daily actuals by Date Range', data)
        return data

    def actualsDate(self, ref, col_To_Ref):
        if self.data is ():
            print ('no data in Daily Actuals table')
            return None
        else:
            data = [col[0] for col in self.data if ref == col[col_To_Ref]]
            if data == []:
                return ""
            else:
                return data

    def amRevenue(self, ref, col_To_Ref):
        if self.data is ():
            print ('no data in Daily Actuals table')
            return None
        else:
            data = [col[1] for col in self.data if ref == col[col_To_Ref]]
            if data == []:
                return ""
            else:
                return data

    def pmRevenue(self, ref, col_To_Ref):
        if self.data is ():
            print ('no data in Daily Actuals table')
            return None
        else:
            data = [col[2] for col in self.data if ref == col[col_To_Ref]]
            if data == []:
                return ""
            else:
                return data


class Departments:
    def __init__(self):
        self.data = Core.Querydb('SELECT * FROM departments', None).fetchAllRecordswithFormatting()

    def select_All(self):
        return self.data

    def departmentID(self, ref, col_To_Ref):
        if self.data is ():
            print ('no data in departments table')
            return None
        else:
            data = [col[0] for col in self.data if ref == col[col_To_Ref]]
            if data == []:
                return ""
            else:
                return data

    def department(self, ref, col_To_Ref):
        if self.data is ():
            print ('no data in departments table')
            return None
        else:
            data = [col[1] for col in self.data if ref == col[col_To_Ref]]
            if data == []:
                return ""
            else:
                return data



class HolidayEntitlements:
    def __init__(self):
        self.data = Core.Querydb('SELECT * FROM HolidayEntitlement', None).fetchAllRecordswithFormatting()

    def select_All(self):
        return self.data

    def entitlementID(self, ref, col_To_Ref):
        if self.data is ():
            print ('no data in entitlementID table')
            return None
        else:
            data = [col[0] for col in self.data if ref == col[col_To_Ref]]
            if data == []:
                return ""
            else:
                return data

    def empID(self, ref, col_To_Ref):
        if self.data is ():
            print ('no data in entitlementID table')
            return None
        else:
            data = [col[1] for col in self.data if ref == col[col_To_Ref]]
            if data == []:
                return ""
            else:
                return data

    def entitledDaysFY(self, ref, col_To_Ref):
        if self.data is ():
            print ('no data in entitlementID table')
            return None
        else:
            data = [col[2] for col in self.data if ref == col[col_To_Ref]]
            if data == []:
                return ""
            else:
                return data

    def adjustDate(self, ref, col_To_Ref):
        if self.data is ():
            print ('no data in entitlementID table')
            return None
        else:
            data = [col[3] for col in self.data if ref == col[col_To_Ref]]
            if data == []:
                return ""
            else:
                return data


class MonthlyBudgets:
    def __init__(self):
        self.data = Core.Querydb('SELECT * FROM MonthlyBudgets', None).fetchAllRecordswithFormatting()

    def select_All(self):
        return self.data

    def MonthBudgetID(self, ref, col_To_Ref):
        if self.data is ():
            print ('no data in Monthly Budget table')
            return None
        else:
            data = [col[0] for col in self.data if ref == col[col_To_Ref]]
            if data == []:
                return ""
            else:
                return data

    def budgetYear(self, ref, col_To_Ref):
        if self.data is ():
            print ('no data in Monthly Budget table')
            return None
        else:
            data = [col[1] for col in self.data if ref == col[col_To_Ref]]
            if data == []:
                return ""
            else:
                return data

    def janBudget(self, ref, col_To_Ref):
        if self.data is ():
            print ('no data in Monthly Budget table')
            return None
        else:
            data = [col[2] for col in self.data if ref == col[col_To_Ref]]
            if data == []:
                return ""
            else:
                return data

    def febBudget(self, ref, col_To_Ref):
        if self.data is ():
            print ('no data in Monthly Budget table')
            return None
        else:
            data = [col[3] for col in self.data if ref == col[col_To_Ref]]
            if data == []:
                return ""
            else:
                return data

    def marBudget(self, ref, col_To_Ref):
        if self.data is ():
            print ('no data in Monthly Budget table')
            return None
        else:
            data = [col[4] for col in self.data if ref == col[col_To_Ref]]
            if data == []:
                return ""
            else:
                return data

    def aprBudget(self, ref, col_To_Ref):
        if self.data is ():
            print ('no data in Monthly Budget table')
            return None
        else:
            data = [col[5] for col in self.data if ref == col[col_To_Ref]]
            if data == []:
                return ""
            else:
                return data

    def mayBudget(self, ref, col_To_Ref):
        if self.data is ():
            print ('no data in Monthly Budget table')
            return None
        else:
            data = [col[6] for col in self.data if ref == col[col_To_Ref]]
            if data == []:
                return ""
            else:
                return data

    def junBudgets(self, ref, col_To_Ref):
        if self.data is ():
            print ('no data in Monthly Budget table')
            return None
        else:
            data = [col[7] for col in self.data if ref == col[col_To_Ref]]
            if data == []:
                return ""
            else:
                return data

    def julBudget(self, ref, col_To_Ref):
        if self.data is ():
            print ('no data in Monthly Budget table')
            return None
        else:
            data = [col[8] for col in self.data if ref == col[col_To_Ref]]
            if data == []:
                return ""
            else:
                return data

    def augBudget(self, ref, col_To_Ref):
        if self.data is ():
            print ('no data in Monthly Budget table')
            return None
        else:
            data = [col[9] for col in self.data if ref == col[col_To_Ref]]
            if data == []:
                return ""
            else:
                return data

    def septBudget(self, ref, col_To_Ref):
        if self.data is ():
            print ('no data in Monthly Budget table')
            return None
        else:
            data = [col[10] for col in self.data if ref == col[col_To_Ref]]
            if data == []:
                return ""
            else:
                return data

    def octbudget(self, ref, col_To_Ref):
        if self.data is ():
            print ('no data in Monthly Budget table')
            return None
        else:
            data = [col[11] for col in self.data if ref == col[col_To_Ref]]
            if data == []:
                return ""
            else:
                return data

    def novBudget(self, ref, col_To_Ref):
        if self.data is ():
            print ('no data in Monthly Budget table')
            return None
        else:
            data = [col[12] for col in self.data if ref == col[col_To_Ref]]
            if data == []:
                return ""
            else:
                return data

    def decBudget(self, ref, col_To_Ref):
        if self.data is ():
            print ('no data in Monthly Budget table')
            return None
        else:
            data = [col[13] for col in self.data if ref == col[col_To_Ref]]
            if data == []:
                return ""
            else:
                return data



class EmployeeTbl:
    def __init__(self):
        self.data = Core.Core.Querydb('SELECT * FROM Employee_TBL', None).fetchAllRecordswithFormatting()
        #self.data = self.data

    def select_All(self):
        return self.data

    def IdEmployee_TBL(self, ref, col_To_Ref):
        if self.data is ():
            print ('no data in Employee table')
            return None
        else:
            data = [col[0] for col in self.data if ref == col[col_To_Ref]]
            if data == []:
                return ""
            else:
                return data

    def Name(self, ref, col_To_Ref):
        if self.data is ():
            print ('no data in Employee table')
            return None
        else:
            data = [col[1] for col in self.data if ref == col[col_To_Ref]]
            if data == []:
                return ""
            else:
                return data

    def DOB(self, ref, col_To_Ref):
        if self.data is ():
            print ('no data in Employee table')
            return None
        else:
            data = [col[2] for col in self.data if ref == col[col_To_Ref]]
            if data == []:
                return ""
            else:
                return data

    def departmentID(self, ref, col_To_Ref):
        if self.data is ():
            print ('no data in Employee table')
            return None
        else:
            data = [col[3] for col in self.data if ref == col[col_To_Ref]]
            if data == []:
                return ""
            else:
                return data

    def SalOrHourly(self, ref, col_To_Ref):
        if self.data is ():
            print ('no data in Employee table')
            return None
        else:
            data = [col[4] for col in self.data if ref == col[col_To_Ref]]
            if data == []:
                return ""
            else:
                return data

    def Address(self, ref, col_To_Ref):
        if self.data is ():
            print ('no data in Employee table')
            return None
        else:
            data = [col[5] for col in self.data if ref == col[col_To_Ref]]
            if data == []:
                return ""
            else:
                return data

    def Email(self, ref, col_To_Ref):
        if self.data is ():
            print ('no data in Employee table')
            return None
        else:
            data = [col[6] for col in self.data if ref == col[col_To_Ref]]
            if data == []:
                return ""
            else:
                return data

    def HomePhone(self, ref, col_To_Ref):
        if self.data is ():
            print ('no data in Employee table')
            return None
        else:
            data = [col[7] for col in self.data if ref == col[col_To_Ref]]
            if data == []:
                return ""
            else:
                return data

    def MobilePhone(self, ref, col_To_Ref):
        if self.data is ():
            print ('no data in Employee table')
            return None
        else:
            data = [col[8] for col in self.data if ref == col[col_To_Ref]]
            if data == []:
                return ""
            else:
                return data

    def EmpStDate(self, ref, col_To_Ref):
        if self.data is ():
            print ('no data in Employee table')
            return None
        else:
            data = [col[9] for col in self.data if ref == col[col_To_Ref]]
            if data == []:
                return ""
            else:
                return data

    def EmpFinDate(self, ref, col_To_Ref):
        if self.data is ():
            print ('no data in Employee table')
            return None
        else:
            data = [col[10] for col in self.data if ref == col[col_To_Ref]]
            if data == []:
                return ""
            else:
                return data

    def contractedAnnualDays(self, ref, col_To_Ref):
        if self.data is ():
            print ('no data in Employee table')
            return None
        else:
            data = [col[11] for col in self.data if ref == col[col_To_Ref]]
            if data == []:
                return ""
            else:
                return data

    def QDMon(self, ref, col_To_Ref):
        if self.data is ():
            print ('no data in Employee table')
            return None
        else:
            data = [col[12] for col in self.data if ref == col[col_To_Ref]]
            if data == []:
                return ""
            else:
                return data

    def QDTue(self, ref, col_To_Ref):
        if self.data is ():
            print ('no data in Employee table')
            return None
        else:
            data = [col[13] for col in self.data if ref == col[col_To_Ref]]
            if data == []:
                return ""
            else:
                return data

    def QDWed(self, ref, col_To_Ref):
        if self.data is ():
            print ('no data in Employee table')
            return None
        else:
            data = [col[14] for col in self.data if ref == col[col_To_Ref]]
            if data == []:
                return ""
            else:
                return data

    def QDThu(self, ref, col_To_Ref):
        if self.data is ():
            print ('no data in Employee table')
            return None
        else:
            data = [col[15] for col in self.data if ref == col[col_To_Ref]]
            if data == []:
                return ""
            else:
                return data

    def QDFri(self, ref, col_To_Ref):
        if self.data is ():
            print ('no data in Employee table')
            return None
        else:
            data = [col[16] for col in self.data if ref == col[col_To_Ref]]
            if data == []:
                return ""
            else:
                return data

    def QDSat(self, ref, col_To_Ref):
        if self.data is ():
            print ('no data in Employee table')
            return None
        else:
            data = [col[17] for col in self.data if ref == col[col_To_Ref]]
            if data == []:
                return ""
            else:
                return data

    def QDSun(self, ref, col_To_Ref):
        if self.data is ():
            print ('no data in Employee table')
            return None
        else:
            data = [col[18] for col in self.data if ref == col[col_To_Ref]]
            if data == []:
                return ""
            else:
                return data


class NMWBands:
    def __init__(self):
        self.data = Core.Querydb('SELECT * FROM nmwBands', None).fetchAllRecordswithFormatting()

    def select_All(self):
        return self.data

    def nmwBandComboListExtract(self):
        if NMWBands == ():
            return []
        else:
            titleIDlist = [[str(title), id] for id, title, age1, age2 in self.data]
            return titleIDlist

    def nmwBandID(self, band):
        if self.data is ():
            print ('no data in NMWBands table')
            return None
        else:
            data = [col[0] for col in self.data if col[1] == band]
            if data == []:
                return ""
            else:
                return data

    def nmwTile(self, ref, col_To_Ref):
        if self.data is ():
            print ('no data in NMWBands table')
            return None
        else:
            data = [col[1] for col in self.data if ref == col[col_To_Ref]]
            if data == []:
                return ""
            else:
                return data

    def fromAge(self, ref, col_To_Ref):
        if self.data is ():
            print ('no data in NMWBands table')
            return None
        else:
            data = [col[2] for col in self.data if ref == col[col_To_Ref]]
            if data == []:
                return ""
            else:
                return data

    def toAge(self, ref, col_To_Ref):
        if self.data is ():
            print ('no data in NMWBands table')
            return None
        else:
            data = [col[3] for col in self.data if ref == col[col_To_Ref]]
            if data == []:
                return ""
            else:
                return data



class NMWRates:
    def __init__(self):
        self.data = Core.Querydb('SELECT * FROM nmwRates', None).fetchAllRecordswithFormatting()
        self.salCalVar = Core.Querydb('SELECT * FROM SalaryCalVariables', None).fetchAllRecordswithFormatting()

    def select_All(self):
        return self.data

    def nicMinAge(self, Sdate):
        if self.data == ():
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
        if self.data == ():
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
        if self.data == ():
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
        if self.data == ():
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
        if self.data == ():
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
        if self.data == ():
            return 0
        else:
            data = [[VariablesDate, pensionPercentage] for nicVariablesID, VariablesDate , minAge, nicRate, threshold, pensionPercentage, sickPay, SSPLEL
                     in self.salCalVar if Sdate >= VariablesDate]
            if data == []:
                pass
            else:
                result = max(data)
                return result[1]

    def nmwRatesID(self, ref, col_To_Ref):
        if self.data is ():
            print ('no data in NMWRates table')
            return None
        else:
            data = [col[0] for col in self.data if ref == col[col_To_Ref]]
            if data == []:
                return ""
            else:
                return data

    def nmwBandsID(self, ref, col_To_Ref):
        if self.data is ():
            print ('no data in NMWRates table')
            return None
        else:
            data = [col[1] for col in self.data if ref == col[col_To_Ref]]
            if data == []:
                return ""
            else:
                return data

    def rate(self, ref, col_To_Ref):
        if self.data is ():
            print ('no data in NMWRates table')
            return None
        else:
            data = [col[2] for col in self.data if ref == col[col_To_Ref]]
            if data == []:
                return ""
            else:
                return data

    def liveDate(self, ref, col_To_Ref):
        if self.data is ():
            print ('no data in NMWRates table')
            return None
        else:
            data = [col[3] for col in self.data if ref == col[col_To_Ref]]
            if data == []:
                return ""
            else:
                return data


class PredictedCovers:
    def __init__(self):
        self.data = Core.Querydb('SELECT * FROM PredictedCovers', None).fetchAllRecordswithFormatting()

    def select_All(self):
        return self.data

    def predCoverDateRange(self, fromDate, toDate):
        if self.data is ():
            print ('no data in Predicted Cover table')
            return None
        else:
            data = [[col[0],col[1],col[2],col[3],col[4]] for col in self.data if fromDate <= col[1] <= toDate]
            if data == []:
                return ""
            else:
                return data

    def predCoverID(self, ref, col_To_Ref):
        if self.data is ():
            print ('no data in Predicted Cover table')
            return None
        else:
            data = [col[0] for col in self.data if ref == col[col_To_Ref]]
            if data == []:
                return ""
            else:
                return data

    def predCoverDate(self, ref, col_To_Ref):
        if self.data is ():
            print ('no data in Predicted Cover table')
            return None
        else:
            data = [col[1] for col in self.data if ref == col[col_To_Ref]]
            if data == []:
                return ""
            else:
                return data

    def predCoverAM(self, ref, col_To_Ref):
        if self.data is ():
            print ('no data in Predicted Cover table')
            return None
        else:
            data = [col[2] for col in self.data if ref == col[col_To_Ref]]
            if data == []:
                return ""
            else:
                return data

    def predCoverPM(self, ref, col_To_Ref):
        if self.data is ():
            print ('no data in Predicted Cover table')
            return None
        else:
            data = [col[3] for col in self.data if ref == col[col_To_Ref]]
            if data == []:
                return ""
            else:
                return data

    def revenueTypeID(self, ref, col_To_Ref):
        if self.data is ():
            print ('no data in Predicted Cover table')
            return None
        else:
            data = [col[4] for col in self.data if ref == col[col_To_Ref]]
            if data == []:
                return ""
            else:
                return data



class RevenueTypes:
    def __init__(self):
        self.data = Core.Querydb('SELECT * FROM RevenueTypes', None).fetchAllRecordswithFormatting()

    def select_All(self):
        return self.data

    def RevenueTypeID(self, ref, col_To_Ref):
        if self.data is ():
            print ('no data in Revenue Types table')
            return None
        else:
            data = [col[0] for col in self.data if ref == col[col_To_Ref]]
            if data == []:
                return ""
            else:
                return data

    def revenueType(self, ref, col_To_Ref):
        if self.data is ():
            print ('no data in Revenue Types table')
            return None
        else:
            data = [col[1] for col in self.data if ref == col[col_To_Ref]]
            if data == []:
                return ""
            else:
                return data

    def amDryAvgSpend(self, ref, col_To_Ref):
        if self.data is ():
            print ('no data in Revenue Types table')
            return None
        else:
            data = [col[2] for col in self.data if ref == col[col_To_Ref]]
            if data == []:
                return ""
            else:
                return data

    def pmDryAvgSpend(self, ref, col_To_Ref):
        if self.data is ():
            print ('no data in Revenue Types table')
            return None
        else:
            data = [col[3] for col in self.data if ref == col[col_To_Ref]]
            if data == []:
                return ""
            else:
                return data

    def amWetAvgSpend(self, ref, col_To_Ref):
        if self.data is ():
            print ('no data in Revenue Types table')
            return None
        else:
            data = [col[4] for col in self.data if ref == col[col_To_Ref]]
            if data == []:
                return ""
            else:
                return data

    def pmWetAvgSpend(self, ref, col_To_Ref):
        if self.data is ():
            print ('no data in Revenue Types table')
            return None
        else:
            data = [col[5] for col in self.data if ref == col[col_To_Ref]]
            if data == []:
                return ""
            else:
                return data





class Salary:
    def __init__(self):
        self.data = Core.Querydb('SELECT * FROM Salary', None).fetchAllRecordswithFormatting()

    def select_All(self):
        return self.data

    def SalaryID(self, ref, col_To_Ref):
        if self.data is ():
            print ('no data in Salary table')
            return None
        else:
            data = [col[0] for col in self.data if ref == col[col_To_Ref]]
            if data == []:
                return ""
            else:
                return data

    def EmployeeID(self, ref, col_To_Ref):
        if self.data is ():
            print ('no data in Salary table')
            return None
        else:
            data = [col[1] for col in self.data if ref == col[col_To_Ref]]
            if data == []:
                return ""
            else:
                return data

    def PoundsPerHour(self, ref, col_To_Ref):
        if self.data is ():
            print ('no data in Salary table')
            return None
        else:
            data = [col[2] for col in self.data if ref == col[col_To_Ref]]
            if data == []:
                return ""
            else:
                return data

    def Salary(self, ref, col_To_Ref):
        if self.data is ():
            print ('no data in Salary table')
            return None
        else:
            data = [col[3] for col in self.data if ref == col[col_To_Ref]]
            if data == []:
                return ""
            else:
                return data

    def AdjustDate(self, ref, col_To_Ref):
        if self.data is ():
            print ('no data in Salary table')
            return None
        else:
            data = [col[4] for col in self.data if ref == col[col_To_Ref]]
            if data == []:
                return ""
            else:
                return data



class SalaryOrHourly:
    def __init__(self):
        self.data = Core.Querydb('SELECT * FROM salorHourlyTable', None).fetchAllRecordswithFormatting()

    def select_All(self):
        return self.data

    def salorHourlyID(self, ref, col_To_Ref):
        if self.data is ():
            print ('no data in SalaryorHourly table')
            return None
        else:
            data = [col[0] for col in self.data if ref == col[col_To_Ref]]
            if data == []:
                return ""
            else:
                return data

    def SalorHourly(self, ref, col_To_Ref):
        if self.data is ():
            print ('no data in SalaryorHourly table')
            return None
        else:
            data = [col[1] for col in self.data if ref == col[col_To_Ref]]
            if data == []:
                return ""
            else:
                return data



class SalaryCalcVariables:
    def __init__(self):
        self.data = Core.Querydb('SELECT * FROM SalaryCalVariables', None).fetchAllRecordswithFormatting()

    def select_All(self):
        return self.data

    def nicVariablesID(self, ref, col_To_Ref):
        if self.data is ():
            print ('no data in SalaryCalVariables table')
            return None
        else:
            data = [col[0] for col in self.data if ref == col[col_To_Ref]]
            if data == []:
                return ""
            else:
                return data

    def VariablesDate(self, ref, col_To_Ref):
        if self.data is ():
            print ('no data in SalaryCalVariables table')
            return None
        else:
            data = [col[1] for col in self.data if ref == col[col_To_Ref]]
            if data == []:
                return ""
            else:
                return data

    def minAge(self, ref, col_To_Ref):
        if self.data is ():
            print ('no data in SalaryCalVariables table')
            return None
        else:
            data = [col[2] for col in self.data if ref == col[col_To_Ref]]
            if data == []:
                return ""
            else:
                return data

    def nicRate(self, ref, col_To_Ref):
        if self.data is ():
            print ('no data in SalaryCalVariables table')
            return None
        else:
            data = [col[3] for col in self.data if ref == col[col_To_Ref]]
            if data == []:
                return ""
            else:
                return data

    def threshold(self, ref, col_To_Ref):
        if self.data is ():
            print ('no data in SalaryCalVariables table')
            return None
        else:
            data = [col[4] for col in self.data if ref == col[col_To_Ref]]
            if data == []:
                return ""
            else:
                return data

    def pensionPercentage(self, ref, col_To_Ref):
        if self.data is ():
            print ('no data in SalaryCalVariables table')
            return None
        else:
            data = [col[5] for col in self.data if ref == col[col_To_Ref]]
            if data == []:
                return ""
            else:
                return data

    def sickPayDayRate(self, ref, col_To_Ref):
        if self.data is ():
            print ('no data in SalaryCalVariables table')
            return None
        else:
            data = [col[6] for col in self.data if ref == col[col_To_Ref]]
            if data == []:
                return ""
            else:
                return data

    def SSPLowerEarningsLimit(self, ref, col_To_Ref):
        if self.data is ():
            print ('no data in SalaryCalVariables table')
            return None
        else:
            data = [col[7] for col in self.data if ref == col[col_To_Ref]]
            if data == []:
                return ""
            else:
                return data



class Shifts:
    def __init__(self):
        self.data = Core.Querydb('SELECT * FROM shifts', None).fetchAllRecordswithFormatting()

    def select_All(self):
        return self.data

    def shiftsID(self, ref, col_To_Ref):
        if self.data is ():
            print ('no data in Shifts table')
            return None
        else:
            data = [col[0] for col in self.data if ref == col[col_To_Ref]]
            if data == []:
                return ""
            else:
                return data

    def EmployeeID(self, ref, col_To_Ref):
        if self.data is ():
            print ('no data in Shifts table')
            return None
        else:
            data = [col[1] for col in self.data if ref == col[col_To_Ref]]
            if data == []:
                return ""
            else:
                return data

    def Date(self, ref, col_To_Ref):
        if self.data is ():
            print ('no data in Shifts table')
            return None
        else:
            data = [col[2] for col in self.data if ref == col[col_To_Ref]]
            if data == []:
                return ""
            else:
                return data

    def StartAM(self, ref, col_To_Ref):
        if self.data is ():
            print ('no data in Shifts table')
            return None
        else:
            data = [col[3] for col in self.data if ref == col[col_To_Ref]]
            if data == []:
                return ""
            else:
                return data

    def FinAM(self, ref, col_To_Ref):
        if self.data is ():
            print ('no data in Shifts table')
            return None
        else:
            data = [col[4] for col in self.data if ref == col[col_To_Ref]]
            if data == []:
                return ""
            else:
                return data

    def BrkAM(self, ref, col_To_Ref):
        if self.data is ():
            print ('no data in Shifts table')
            return None
        else:
            data = [col[5] for col in self.data if ref == col[col_To_Ref]]
            if data == []:
                return ""
            else:
                return data

    def StartPM(self, ref, col_To_Ref):
        if self.data is ():
            print ('no data in Shifts table')
            return None
        else:
            data = [col[6] for col in self.data if ref == col[col_To_Ref]]
            if data == []:
                return ""
            else:
                return data

    def FinPM(self, ref, col_To_Ref):
        if self.data is ():
            print ('no data in Shifts table')
            return None
        else:
            data = [col[7] for col in self.data if ref == col[col_To_Ref]]
            if data == []:
                return ""
            else:
                return data

    def BrkPM(self, ref, col_To_Ref):
        if self.data is ():
            print ('no data in Shifts table')
            return None
        else:
            data = [col[8] for col in self.data if ref == col[col_To_Ref]]
            if data == []:
                return ""
            else:
                return data

    def ConcatShift(self, ref, col_To_Ref):
        if self.data is ():
            print ('no data in Shifts table')
            return None
        else:
            data = [col[9] for col in self.data if ref == col[col_To_Ref]]
            if data == []:
                return ""
            else:
                return data

    def TotalHours(self, ref, col_To_Ref):
        if self.data is ():
            print ('no data in Shifts table')
            return None
        else:
            data = [col[10] for col in self.data if ref == col[col_To_Ref]]
            if data == []:
                return ""
            else:
                return data

    def shiftTypeAM(self, ref, col_To_Ref):
        if self.data is ():
            print ('no data in Shifts table')
            return None
        else:
            data = [col[11] for col in self.data if ref == col[col_To_Ref]]
            if data == []:
                return ""
            else:
                return data

    def shiftTypePM(self, ref, col_To_Ref):
        if self.data is ():
            print ('no data in Shifts table')
            return None
        else:
            data = [col[12] for col in self.data if ref == col[col_To_Ref]]
            if data == []:
                return ""
            else:
                return data

    def EmployeeDep(self, ref, col_To_Ref):
        if self.data is ():
            print ('no data in Shifts table')
            return None
        else:
            data = [col[13] for col in self.data if ref == col[col_To_Ref]]
            if data == []:
                return ""
            else:
                return data

    def DepAM(self, ref, col_To_Ref):
        if self.data is ():
            print ('no data in Shifts table')
            return None
        else:
            data = [col[14] for col in self.data if ref == col[col_To_Ref]]
            if data == []:
                return ""
            else:
                return data

    def DepPM(self, ref, col_To_Ref):
        if self.data is ():
            print ('no data in Shifts table')
            return None
        else:
            data = [col[15] for col in self.data if ref == col[col_To_Ref]]
            if data == []:
                return ""
            else:
                return data

    def HolidayHours(self, ref, col_To_Ref):
        if self.data is ():
            print ('no data in Shifts table')
            return None
        else:
            data = [col[16] for col in self.data if ref == col[col_To_Ref]]
            if data == []:
                return ""
            else:
                return data

    def HolidayDays(self, ref, col_To_Ref):
        if self.data is ():
            print ('no data in Shifts table')
            return None
        else:
            data = [col[17] for col in self.data if ref == col[col_To_Ref]]
            if data == []:
                return ""
            else:
                return data



class ShiftTypes:
    def __init__(self):
        self.data = Core.Querydb('SELECT * FROM shiftTypes', None).fetchAllRecordswithFormatting()

    def select_All(self):
        return self.data

    def shiftTypesID(self, ref, col_To_Ref):
        if self.data is ():
            print ('no data in Shift Types table')
            return None
        else:
            data = [col[0] for col in self.data if ref == col[col_To_Ref]]
            if data == []:
                return ""
            else:
                return data

    def shiftType(self, ref, col_To_Ref):
        if self.data is ():
            print ('no data in Shift Types table')
            return None
        else:
            data = [col[1] for col in self.data if ref == col[col_To_Ref]]
            if data == []:
                return ""
            else:
                return data



class Bonus:
    def __init__(self):
        self.data = Core.Querydb('SELECT * FROM Bonus', None).fetchAllRecordswithFormatting()

    def select_All(self):
        return self.data

    def BonusID(self, ref, col_To_Ref):
        if self.data is ():
            print ('no data in Bonus table')
            return None
        else:
            data = [col[0] for col in self.data if ref == col[col_To_Ref]]
            if data == []:
                return ""
            else:
                return data

    def Bonus(self, ref, col_To_Ref):
        if self.data is ():
            print ('no data in Bonus table')
            return None
        else:
            data = [col[1] for col in self.data if ref == col[col_To_Ref]]
            if data == []:
                return ""
            else:
                return data

    def EmployeeID(self, ref, col_To_Ref):
        if self.data is ():
            print ('no data in Bonus table')
            return None
        else:
            data = [col[2] for col in self.data if ref == col[col_To_Ref]]
            if data == []:
                return ""
            else:
                return data

    def BonusPeriodStDate(self, ref, col_To_Ref):
        if self.data is ():
            print ('no data in Bonus table')
            return None
        else:
            data = [col[3] for col in self.data if ref == col[col_To_Ref]]
            if data == []:
                return ""
            else:
                return data

    def BonusPayDate(self, ref, col_To_Ref):
        if self.data is ():
            print ('no data in Bonus table')
            return None
        else:
            data = [col[4] for col in self.data if ref == col[col_To_Ref]]
            if data == []:
                return ""
            else:
                return data

class AutoShifts:
    def __init__(self):
        self.data = Core.Querydb('SELECT * FROM AutoShiftTimes', None).fetchAllRecordswithFormatting()

    def select_All(self):
        return self.data

    def AutoShiftTimesID(self, ref, col_To_Ref):
        if self.data is ():
            print ('no data in AutoShifts table')
            return None
        else:
            data = [col[0] for col in self.data if ref == col[col_To_Ref]]
            if data == []:
                return ""
            else:
                return data

    def ButtonReference(self,  ref, col_To_Ref):
        if self.data is ():
            print ('no data in AutoShifts table')
            return None
        else:
            data = [col[1] for col in self.data if ref == col[col_To_Ref]]
            if data == []:
                return ""
            else:
                return data

    def ConcatShift(self,  ref, col_To_Ref):
        if self.data is ():
            print ('no data in AutoShifts table')
            return None
        else:
            data = [col[2] for col in self.data if ref == col[col_To_Ref]]
            if data == []:
                return ""
            else:
                return data

    def StAM(self,  ref, col_To_Ref):
        if self.data is ():
            print ('no data in AutoShifts table')
            return None
        else:
            data = [col[3] for col in self.data if ref == col[col_To_Ref]]
            if data == []:
                return ""
            else:
                return data

    def FinAM(self,  ref, col_To_Ref):
        if self.data is ():
            print ('no data in AutoShifts table')
            return None
        else:
            data = [col[4] for col in self.data if ref == col[col_To_Ref]]
            if data == []:
                return ""
            else:
                return data

    def BrkAM(self,  ref, col_To_Ref):
        if self.data is ():
            print ('no data in AutoShifts table')
            return None
        else:
            data = [col[5] for col in self.data if ref == col[col_To_Ref]]
            if data == []:
                return ""
            else:
                return data

    def StPM(self,  ref, col_To_Ref):
        if self.data is ():
            print ('no data in AutoShifts table')
            return None
        else:
            data = [col[6] for col in self.data if ref == col[col_To_Ref]]
            if data == []:
                return ""
            else:
                return data

    def FinPM(self,  ref, col_To_Ref):
        if self.data is ():
            print ('no data in AutoShifts table')
            return None
        else:
            data = [col[7] for col in self.data if ref == col[col_To_Ref]]
            if data == []:
                return ""
            else:
                return data

    def BrkPM(self,  ref, col_To_Ref):
        if self.data is ():
            print ('no data in AutoShifts table')
            return None
        else:
            data = [col[8] for col in self.data if ref == col[col_To_Ref]]
            if data == []:
                return ""
            else:
                return data

    def AMShiftType(self,  ref, col_To_Ref):
        if self.data is ():
            print ('no data in AutoShifts table')
            return None
        else:
            data = [col[9] for col in self.data if ref == col[col_To_Ref]]
            if data == []:
                return ""
            else:
                return data

    def PMShiftType(self, ref, col_To_Ref):
        if self.data is ():
            print ('no data in AutoShifts table')
            return None
        else:
            data = [col[10] for col in self.data if ref == col[col_To_Ref]]
            if data == []:
                return ""
            else:
                return data