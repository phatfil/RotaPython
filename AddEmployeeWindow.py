from PyQt4 import QtGui
from AddEmployeeUI import Ui_AddEmpDialog
import DB
from PyQt4.QtCore import QObject, pyqtSignal


class AddEmployee(QtGui.QDialog):
    trigger = pyqtSignal()
    def __init__(self, datelistDV3, exisitingnames):
        self.lastDate = str(datelistDV3[6])
        self.exisitingnames = exisitingnames

        super(AddEmployee, self).__init__()
        self.uip = Ui_AddEmpDialog()
        self.uip.setupUi(self)
        self.SelectionList = []
        self.namesandID = []
        self.PopulateEmployeesList()
        self.uip.AddEmpBUT.clicked.connect(self.whichCellsHaveIselected)
        self.uip.AddEmpBUT.clicked.connect(self.emitTrigger)


    def PopulateEmployeesList(self):
        # populate the add employee window with Employees that have started before current date
        Employees = DB.Querydb("SELECT idEmployee_TBL, Name, departmentID FROM Employee_TBL WHERE EmpStDate <= %s",
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

        for a in range(len(nameList)):
            for b in range(len(self.namesandID)):
                if self.namesandID[b][0] == nameList[a]:
                    self.SelectionList.append([self.namesandID[b][0], self.namesandID[b][1], self.namesandID[b][2]])

    def emitTrigger(self):
        self.trigger.emit()
        self.close()
