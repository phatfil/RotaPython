
from PyQt4 import QtGui, QtSql, QtCore
import datetime
import calendar


class calendarWidget(QtGui.QWidget):
    # Not finished yet
    def __init__(self, parent = None):
        super(calendarWidget, self).__init__(parent)

        self.firstCellClick = []
        self.secondCellClick = []

        self.tableWidget = QtGui.QTableWidget()
        self.tableWidget.setFixedHeight(207)
        self.tableWidget.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.today = datetime.date.today()

        self.tableWidget.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)

        self.monthBut = QtGui.QComboBox()
        self.monthBut.addItems(['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])
        self.monthBut.setFixedWidth(60)
        self.monthBut.setCurrentIndex(self.today.month - 1)

        self.yearBut = QtGui.QDoubleSpinBox()
        self.yearBut.setDecimals(0)
        self.yearBut.setMaximum(2999)
        self.yearBut.setMinimum(1985)
        self.yearBut.setValue(self.today.year)

        self.todayBut = QtGui.QPushButton()
        self.todayBut.setFlat(1)
        self.todayBut.setFixedWidth(20)
        self.todayBut.setIcon(QtGui.QIcon('dot.png'))

        self.backYear = QtGui.QPushButton()
        self.backYear.setFlat(1)
        self.backYear.setFixedWidth(20)
        self.backYear.setIcon(QtGui.QIcon('Lleft.png'))

        self.backMonth = QtGui.QPushButton()
        self.backMonth.setFlat(1)
        self.backMonth.setFixedWidth(20)
        self.backMonth.setIcon(QtGui.QIcon('left.png'))

        self.forwardMonth = QtGui.QPushButton()
        self.forwardMonth.setFlat(1)
        self.forwardMonth.setFixedWidth(20)
        self.forwardMonth.setIcon(QtGui.QIcon('right.png'))

        self.forwardYear = QtGui.QPushButton()
        self.forwardYear.setFlat(1)
        self.forwardYear.setFixedWidth(20)
        self.forwardYear.setIcon(QtGui.QIcon('Rright.png'))

        self.calendarWidget = QtGui.QGridLayout()
        self.calendarWidget.addWidget(self.backYear, 0, 0)
        self.calendarWidget.addWidget(self.backMonth, 0, 1)
        self.calendarWidget.addWidget(self.todayBut, 0, 2)
        self.calendarWidget.addWidget(self.forwardMonth, 0, 3)
        self.calendarWidget.addWidget(self.forwardYear, 0, 4)
        self.calendarWidget.addWidget(self.monthBut, 0, 5, 1, 2)
        self.calendarWidget.addWidget(self.yearBut, 0, 6)
        self.calendarWidget.addWidget(self.tableWidget, 1, 0, 1, 7)

        self.tableWidget.setColumnCount(7)

        self.tableWidget.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.tableWidget.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)

        vHeadear = self.tableWidget.verticalHeader()
        vHeadear.setVisible(False)

        header = self.tableWidget.horizontalHeader()
        header.setResizeMode(0, QtGui.QHeaderView.Stretch)
        header.setResizeMode(1, QtGui.QHeaderView.Stretch)
        header.setResizeMode(2, QtGui.QHeaderView.Stretch)
        header.setResizeMode(3, QtGui.QHeaderView.Stretch)
        header.setResizeMode(4, QtGui.QHeaderView.Stretch)
        header.setResizeMode(5, QtGui.QHeaderView.Stretch)
        header.setResizeMode(6, QtGui.QHeaderView.Stretch)


        headerList =['Mon', 'Tue', 'Wed', 'Thur', 'Fri', 'Sat', 'Sun']
        self.tableWidget.setHorizontalHeaderLabels(headerList)
        self.updateDate()
        self.populateCalendar()

        # set all slots
        self.tableWidget.cellClicked.connect(self.cellClick)
        self.tableWidget.cellClicked.connect(self.cellSelection)
        self.yearBut.valueChanged.connect(self.updateDate)
        self.monthBut.currentIndexChanged.connect(self.updateDate)
        self.forwardMonth.clicked.connect(self.monthForward)
        self.forwardYear.clicked.connect(self.yearForward)
        self.backYear.clicked.connect(self.yearBackwards)
        self.backMonth.clicked.connect(self.monthBackwards)
        self.todayBut.clicked.connect(self.moveToday)

    def moveToday(self):
        month = datetime.datetime.today().month
        year = datetime.datetime.today().year
        self.monthBut.setCurrentIndex(month -1)
        self.yearBut.setValue(year)

    def yearForward(self):
        currentYear = self.yearBut.value()
        self.yearBut.setValue(currentYear + 1)

    def monthForward(self):
        if self.monthBut.currentIndex() == 11:
            self.monthBut.setCurrentIndex(0)
            year = self.yearBut.value()
            self.yearBut.setValue(year + 1)
        else:
            currentMonth = self.monthBut.currentIndex()
            self.monthBut.setCurrentIndex(currentMonth + 1)

    def yearBackwards(self):
        currentYear = self.yearBut.value()
        self.yearBut.setValue(currentYear - 1)

    def monthBackwards(self):
        if self.monthBut.currentIndex() == 0:
            self.monthBut.setCurrentIndex(11)
            year = self.yearBut.value()
            self.yearBut.setValue(year - 1)
        else:
            currentMonth = self.monthBut.currentIndex()
            self.monthBut.setCurrentIndex(currentMonth - 1)

    def updateDate(self):
        self.monthList = [['Jan', 1], ['Feb', 2], ['Mar', 3], ['Apr', 4], ['May', 5], ['Jun', 6],
                     ['Jul', 7], ['Aug', 8], ['Sep', 9], ['Oct', 10], ['Nov', 11], ['Dec', 12]]
        self.month = [num for month, num in self.monthList if self.monthBut.currentText() == month][0]
        self.year = int(self.yearBut.value())
        self.populateCalendar()

    def populateCalendar(self):
        self.tableWidget.setRowCount(0)

        self.calWeeks = [[], [], [], [], [], []]

        row = 0
        firstWeekNum = datetime.date(self.year, self.month, 1).strftime("%W")

        for week in range(0, 6):
            weekNumFormat = '{}-{}'.format(self.year, int(firstWeekNum) + week)
            for day in ['-1', '-2', '-3', '-4', '-5', '-6', '-0']:
                dateInfo = datetime.datetime.strptime(weekNumFormat + '{}'.format(day), '%Y-%W-%w').date()
                dayDate = dateInfo.day
                dayData = ""
                dayData2 = ""
                self.calWeeks[row].append([dayDate, dateInfo, dayData, dayData2])
            row += 1
        print (self.calWeeks)

        for row in range(len(self.calWeeks)):
            self.tableWidget.insertRow(row)
            record = self.calWeeks[row]
            for column in range(0, len(record)):
                newitem = QtGui.QTableWidgetItem(str(record[column][0]))
                self.tableWidget.setItem(row, column, newitem)

    def cellClick(self):
        if QtGui.QApplication.keyboardModifiers() != QtCore.Qt.ShiftModifier:
            self.firstCellClick = [self.tableWidget.currentItem().row(), self.tableWidget.currentIndex().column()]
            self.firstDateSelected = self.calWeeks[self.firstCellClick[0]][self.firstCellClick[1]]
            self.selectedMonth = self.monthBut.currentIndex()
            self.secondCellClick = []

        if QtGui.QApplication.keyboardModifiers() == QtCore.Qt.ShiftModifier:
            if self.monthBut.currentIndex() == self.monthBut.currentIndex():
                self.secondCellClick = [self.tableWidget.currentItem().row(), self.tableWidget.currentIndex().column()]
                self.secondDateSelected = self.calWeeks[self.secondCellClick[0]][self.secondCellClick[1]]
            else:
                pass

    def rangeCalc(self, firstCell, lastCell):
        fcrow = firstCell[0]
        fccol = firstCell[1]
        scrow = lastCell[0]
        sccol = lastCell[1]

        days = (((scrow+1)-(fcrow+1))*7)-(fccol+1)+(sccol+2)
        print (days)

        cellRange = [[fcrow, fccol]]

        for a in range(1, days):
            if fccol == 6:
                fccol = 0
                fcrow += 1
                cellRange.append([fcrow, fccol])
            else:
                fccol += 1
                cellRange.append([fcrow, fccol])

        print (cellRange)
        return cellRange

    def cellSelection(self):

        # if a single click is made, continue as normal
        if self.secondCellClick == []:
            print ('clicked data', self.calWeeks[self.firstCellClick[0]][self.firstCellClick[1]])
            return self.firstCellClick

        # if the 1st click is before the 2nd click
        elif ((self.firstCellClick[0] * 7) + self.firstCellClick[1]) < ((self.secondCellClick[0] * 7) + self.secondCellClick[1]):
            self.tableWidget.setSelectionMode(QtGui.QAbstractItemView.MultiSelection)
            cellrange = self.rangeCalc(self.firstCellClick, self.secondCellClick)

            # cycle through the calculated cells in range and set selected
            for cell in range(len(cellrange)):
                index = self.tableWidget.item(cellrange[cell][0], cellrange[cell][1])
                self.tableWidget.setItemSelected(index, 1)
                self.tableWidget.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)

        # if 1st click is after 2nd click, reverse the order
        else:
            self.tableWidget.setSelectionMode(QtGui.QAbstractItemView.MultiSelection)
            cellrange = self.rangeCalc(self.secondCellClick, self.firstCellClick)

            # cycle through the calculated cells in range and set selected
            for cell in range(len(cellrange)):
                index = self.tableWidget.item(cellrange[cell][0], cellrange[cell][1])
                self.tableWidget.setItemSelected(index, 1)
                self.tableWidget.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)


class TableWidgetTools(QtGui.QTableWidget):
    def __init__(self, parent=None):
        super(TableWidgetTools, self).__init__(parent)

    def setWidget(self, widget):
        self.__widget = widget

    def populateRotaTableWidgetHTML(self, data, colCount, hideCol, shiftTypeData, departmentList):
        self.__colCount = colCount
        self.__hideCol = hideCol
        self.__data = data
        self.__shiftTypeData = shiftTypeData
        self.__departmentList = departmentList

        self.__widget.setRowCount(0)
        self.__widget.setColumnCount(self.__colCount)
        if self.__hideCol is None:
            pass
        else:
            self.__widget.hideColumn(self.__hideCol)

        for row in range(len(self.__data)):
            self.__widget.insertRow(row)
            record = self.__data[row]
            newitem = QtGui.QTableWidgetItem(str(record[0]))
            newitem.setTextAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)

            # insert the Names in the first column
            self.__widget.setItem(row, 0, newitem)
            for column in range(1, 8):

                if record[column] == []:
                    bwidget = QtGui.QWidget()
                    widget = QtGui.QLabel()
                    layout = QtGui.QHBoxLayout(bwidget)
                    layout.addWidget(widget)
                    layout.setAlignment(QtCore.Qt.AlignHCenter)
                    layout.setContentsMargins(0, 0, 0, 0)
                    bwidget.setLayout(layout)



                    #widget.setAlignment(QtCore.Qt.AlignVCenter)
                    widget.setText("""
                        <table>
                        <tbody>
                        <td></td>
                        </tr>
                        </tbody>
                        </table>
                        """)

                else:
                    AmStartTime = str(record[column][0])
                    AmFinishTime = str(record[column][1])
                    PmStartTime = str(record[column][3])
                    PmFinishTime = str(record[column][4])

                    # set the colour of text depending on AM shift type
                    if record[column][2] == 0:
                        color1 = 'light grey'
                    elif record[column][2] == 1:
                        color1 = 'black'
                    elif record[column][2] == 2:
                        color1 = 'green'
                    elif record[column][2] == 3:
                        color1 = 'orange'
                    elif record[column][2] == 4:
                        color1 = 'yellow'
                    elif record[column][2] == 5:
                        color1 = 'blue'
                    elif record[column][2] == 6:
                        color1 = 'red'
                    else:
                        color1 = 'black'

                    # set the colour of text depending on PM shift type
                    if record[column][5] == 0:
                        color2 = 'light grey'
                    elif record[column][5] == 1:
                        color2 = 'black'
                    elif record[column][5] == 2:
                        color2 = 'green'
                    elif record[column][5] == 3:
                        color2 = 'orange'
                    elif record[column][5] == 4:
                        color2 = 'yellow'
                    elif record[column][5] == 5:
                        color2 = 'blue'
                    elif record[column][5] == 6:
                        color2 = 'red'
                    else:
                        color2 = 'black'

                    # define shift type and department types to be written
                    AMshiftName = [name for ID, name in self.__shiftTypeData if ID == record[column][2]]
                    PMshiftName = [name for ID, name in self.__shiftTypeData if ID == record[column][5]]
                    DepTypeAM = [depType for (ID, depType) in self.__departmentList if ID == record[column][6]]
                    DepTypePM = [depType for (ID, depType) in self.__departmentList if ID == record[column][7]]

                    if record[column][6] == record[11]:
                        DepAMColour = 'grey'
                    else:
                        DepAMColour = 'blue'

                    if record[column][7] == record[11]:
                        DepPMColour = 'grey'
                    else:
                        DepPMColour = 'blue'

                    seperator = "|"

                    # if there are no am shifts then remove from input
                    if AmStartTime == '00:00' and AmFinishTime == '00:00':
                        AmStartTime = ""
                        AmFinishTime = '&nbsp;' * 20
                        DepTypeAM = ['&nbsp;' * 20]
                        AMshiftName = ['&nbsp;' * 20]
                    else:
                        pass

                    # if there are no pm shifts remove from input
                    if PmStartTime == '00:00' and PmFinishTime == '00:00':
                        PmStartTime = ""
                        PmFinishTime = ""
                        DepTypePM = [""]
                        PMshiftName = [""]
                    else:
                        pass

                    # if there are no am or pm shifts remove the seperator from the input
                    if PmStartTime == "" and PmFinishTime == "" and AmStartTime == "" and AmFinishTime == '&nbsp;' * 20:
                        seperator = ""
                    else:
                        pass

                    bwidget = QtGui.QWidget()
                    widget = QtGui.QLabel()
                    layout = QtGui.QHBoxLayout(bwidget)
                    layout.addWidget(widget)
                    layout.setAlignment(QtCore.Qt.AlignHCenter)
                    layout.setContentsMargins(0, 4, 0, 4)
                    bwidget.setLayout(layout)
                    widget.setText(
                        """
                        <body>
                        <table>
                        <tbody>
                        <td width = "60" style="LINE-HEIGHT:10px;" align="center"><font size = "2" color="{}">{}</font></td>
                        <td width = "5" style="LINE-HEIGHT:10px;"></td>
                        <td width = "60" style="LINE-HEIGHT:10px;" align="center"><font size = "2" color="{}">{}</font></td>
                        <tr>
                        <td width = "60" style="LINE-HEIGHT:10px;" align="center"><font size = "2" color="{}">{}-{}&nbsp;</font></td>
                        <td width = "5" style="LINE-HEIGHT:10px;"  >{}</td>
                        <td width = "60" style="LINE-HEIGHT:10px;" align="center"><font size = "2" color="{}">{}-{}</font></td>
                        </tr>
                        <tr>
                        <td width = "60" style="LINE-HEIGHT:10px;" align="center"><font  size = "2" color="{}">{}</font></td>
                        <td width = "5" style="LINE-HEIGHT:10px;"></td>
                        <td width = "60" style="LINE-HEIGHT:10px;" align="center"><font  size = "2" color="{}">{}</font></td>
                        </tr>
                        </tbody>
                        </table>
                        </body>
                        """.format(DepAMColour, DepTypeAM[0], DepPMColour, DepTypePM[0], color1, AmStartTime,
                                   AmFinishTime, seperator, color2, PmStartTime,
                                   PmFinishTime, color1, AMshiftName[0], color2, PMshiftName[0]))
                self.__widget.setCellWidget(row, column, bwidget)
        self.__widget.resizeRowsToContents()
        # <font color="{}">{}</font>

    def populateTableWidget(self, data, colCount, hideCol):
        self.__colCount = colCount
        self.__hideCol = hideCol
        self.__data = data

        self.__widget.setRowCount(0)
        self.__widget.setColumnCount(self.__colCount)
        if self.__hideCol is None:
            pass
        else:
            self.__widget.hideColumn(self.__hideCol)
        # print (self.__data)
        for row in range(len(self.__data)):
            self.__widget.insertRow(row)
            record = self.__data[row]
            for column in range(0, len(record)):
                newitem = QtGui.QTableWidgetItem(str(record[column]))
                self.__widget.setItem(row, column, newitem)

        self.__widget.resizeRowsToContents()

    def populateTableWidget_Widgets(self, data, colCount, hideCol, ColwidgetList):
        self.__colCount = colCount
        self.__hideCol = hideCol
        self.__data = data
        self.__colWidgetList = ColwidgetList


        self.__widget.setRowCount(0)
        self.__widget.setColumnCount(self.__colCount)
        if self.__hideCol is None:
            pass
        else:
            self.__widget.hideColumn(self.__hideCol)

        for row in range(len(self.__data)):
            self.__widget.insertRow(row)
            record = self.__data[row]
            for column in range(0, len(record)):
                if self.__colWidgetList[column] == None:
                    newitem = QtGui.QTableWidgetItem(str(record[column]))
                    self.__widget.setItem(row, column, newitem)
                elif self.__colWidgetList[column] == 'date':
                    newitem = QtCore.QDate(record[column])
                    Dwidget = dateEdit()
                    Dwidget.setDate(newitem)
                    Dwidget.setCalendarPopup(1)
                    self.__widget.setCellWidget(row, column, Dwidget)

                elif self.__colWidgetList[column] == 'percentage':
                    newitem = record[column]
                    Dwidget = QtGui.QDoubleSpinBox()
                    Dwidget.setDecimals(2)
                    Dwidget.setMaximum(100000)
                    Dwidget.setSuffix('%')
                    Dwidget.setValue(newitem*100)                                 # remember to /100 on the entry into the DB
                    Dwidget.setButtonSymbols(QtGui.QAbstractSpinBox.NoButtons)
                    self.__widget.setCellWidget(row, column, Dwidget)

                # in the col widget List enter , [[item1, ID1] , [item2, ID2], [item3, ID3], etc]]
                elif isinstance(self.__colWidgetList[column], list):
                    Items = []
                    for a in range(len(self.__colWidgetList[column])):               # extract the item names from the listOfEmployees of lists
                        Items.append(self.__colWidgetList[column][a][0])

                    newitem = [itemName for itemName, ID in self.__colWidgetList[column] if ID == record[column]][0]   # find the item name linked to ID
                    Dwidget = QtGui.QComboBox()
                    Dwidget.addItems(Items)
                    index = Dwidget.findText(newitem)
                    Dwidget.setCurrentIndex(index)
                    self.__widget.setCellWidget(row, column, Dwidget)
                else:
                    newitem = QtGui.QTableWidgetItem(str(record[column]))
                    self.__widget.setItem(row, column, newitem)
        self.__widget.resizeRowsToContents()

    def populateTableWidget_IfDateTimeThenCalElseDspinBox(self, data, colCount, hideCol):
        self.__colCount = colCount
        self.__hideCol = hideCol
        self.__data = data


        self.__widget.setRowCount(0)
        self.__widget.setColumnCount(self.__colCount)
        if self.__hideCol is None:
            pass
        else:
            self.__widget.hideColumn(self.__hideCol)

        for row in range(len(self.__data)):
            self.__widget.insertRow(row)
            record = self.__data[row]
            for column in range(0, len(record)):
                    if isinstance(record[column], datetime.date):
                        newitem = QtCore.QDate(record[column])
                        Dwidget = dateEdit()
                        Dwidget.setDate(newitem)
                        Dwidget.setCalendarPopup(1)
                        self.__widget.setCellWidget(row, column, Dwidget)
                    elif record[column] is float:
                        newitem = record[column]
                        Dwidget = QtGui.QDoubleSpinBox()
                        Dwidget.setDecimals(2)
                        Dwidget.setMaximum(100000)
                        Dwidget.setButtonSymbols(QtGui.QAbstractSpinBox.NoButtons)
                        Dwidget.setValue(newitem)
                        self.__widget.setCellWidget(row, column, Dwidget)
                    else:
                        newitem = QtGui.QTableWidgetItem(str(record[column]))
                        self.__widget.setItem(row, column, newitem)


        self.__widget.resizeRowsToContents()

    def populateTableWidgetTextColour(self, data, data_ref1, colCount, hideCol):
        self.__colCount = colCount
        self.__hideCol = hideCol
        self.__data = data

        self.__widget.setRowCount(0)
        self.__widget.setColumnCount(self.__colCount)
        if self.__hideCol is None:
            pass
        else:
            self.__widget.hideColumn(self.__hideCol)

        for row in range(len(self.__data)):
            self.__widget.insertRow(row)
            record = self.__data[row]
            for column in range(0, len(record)):
                newitem = QtGui.QTableWidgetItem(str(record[column]))
                # newitem.setTextColor(QtGui.QColor(100, 119, 0))
                self.__widget.setItem(row, column, newitem)

                # paint cell background colour
                if self.__widget.item(row, column) is None:
                    pass
                else:
                    self.__widget.item(row, column).setTextColor(QtGui.QColor(50, 100, 150))

        self.__widget.resizeRowsToContents()

    def populateColumnHeaders(self, headerList):
        self.__widget.setHorizontalHeaderLabels(headerList)

    def setColumnWidth(self, col, width):
        self.__widget.setColumnWidth(col, width)

    def extractWidgetDataToListForceInt(self):
        row = self.__widget.rowCount()
        col = self.__widget.columnCount()
        data = []
        for x in range(row):
            data.append([])
            for y in range(col):
                if self.__widget.item(x, y) is None:
                    data[x].append(0)
                else:
                    returnedTuple = self.__widget.item(x, y).text().toInt()
                    data[x].append(returnedTuple[0])
        return data

    def extraWidgetDataToList(self, IDtoEnd_T_F):
        self.__IDmove = IDtoEnd_T_F
        row = self.__widget.rowCount()
        col = self.__widget.columnCount()
        data = []
        if self.__IDmove:
            IDtoEndColAdjust = 1
        else:
            IDtoEndColAdjust = 0

        for x in range(row):
            data.append([])
            for y in range(IDtoEndColAdjust, col):
                if self.__widget.item(x, y) is None:
                    data[x].append("")
                else:
                    data[x].append(str(self.__widget.item(x, y).text()))

        if self.__IDmove:
            for x in range(row):
                if self.__widget.item(x, 0) is None:
                    data[x].append("")
                else:
                    data[x].append(str(self.__widget.item(x, 0).text()))
            else:
                pass
        return data

    def changeHeaderTitle(self, colNumber, text):
        # didn't work until the columns where created in QT first including the column to be hidden. Need to look into
        header = self.__widget.horizontalHeaderItem(colNumber)
        header.setText(text)

    def hideColumn(self, col):
        self.__widget.hideColumn(col)

    def resizeColumntoContent(self, col):
        self.__widget.resizeColumnToContents(col)

    def setItemDelegateForColumn(self, col, delegate):
        self.__widget.setItemDelegateForColumn(col, delegate)

    def insertRow(self, row):
        self.__widget.insertRow(row)

    def IDfromSelectedRow(self):
        try:
            row = self.__widget.currentRow()
            ID = self.__widget.item(row, 0).text()
            return ID
        except StandardError:
            QtGui.QMessageBox.warning(QtGui.QMessageBox(), 'Warning', "'Please select an item from the listOfEmployees'")

    def cellWidget(self, p_int, p_int_1):
        self.__widget.cellWidget(p_int, p_int_1)

    def cellExtractfromWidget(self, rowNum, colNum):
        if isinstance(self.__widget.cellWidget(rowNum, colNum),
                      QtGui.QDateEdit):  # checks to see if cell contains dateEdit widget
            a = self.__widget.cellWidget(rowNum, colNum)
            return a.date().toPyDate()

        elif isinstance(self.__widget.cellWidget(rowNum, colNum),
                        QtGui.QDoubleSpinBox):  # checks to see if cell contains spin box widget
            a = self.__widget.cellWidget(rowNum, colNum)
            return a.value()

        elif isinstance(self.__widget.cellWidget(rowNum, colNum),
                        QtGui.QComboBox):  # checks to see if cell contains spin box widget
            a = self.__widget.cellWidget(rowNum, colNum)
            return a.currentText()

        elif isinstance(self.__widget.cellWidget(rowNum, colNum),
                        QtGui.QLabel):  # checks to see if cell contains spin box widget
            a = self.__widget.cellWidget(rowNum, colNum)
            return a.text()

        elif isinstance(self.__widget.cellWidget(rowNum, colNum),
                        QtGui.QWidget):  # checks to see if cell contains a QWidget ie a QHBoxLayout container
            myWidget = self.__widget.cellWidget(rowNum, colNum).layout() # access the QHboxLayout
            return myWidget.itemAt(0).widget().text()   # extract the text from the Qlabel at position 0

        else:
            try:
                a = self.__widget.item(rowNum, colNum)  # if cell isn't a dateEdit Widget extract cell item
                return a.text()  # convert to float and append to relevant listOfEmployees

            except ValueError:
                a = self.__widget.item(rowNum, colNum)  # if cell doesn't convert to float
                return a.text() # write as text

    def rowExtractfromWidget(self):
        columns = self.__widget.columnCount()
        row = self.__widget.rowCount()
        data = []
        for rowNum in range(row): # iterate through tablewidget rows
            data.append([]) # add a new listOfEmployees
            for colNum in range(columns):

                if isinstance(self.__widget.cellWidget(rowNum, colNum),  QtGui.QDateEdit):      # checks to see if cell contains dateEdit widget
                    a = self.__widget.cellWidget(rowNum, colNum)
                    data[rowNum].append(a.date().toPyDate())

                elif isinstance(self.__widget.cellWidget(rowNum, colNum),  QtGui.QDoubleSpinBox):   # checks to see if cell contains spin box widget
                    a = self.__widget.cellWidget(rowNum, colNum)
                    data[rowNum].append(a.value())
                elif isinstance(self.__widget.cellWidget(rowNum, colNum),  QtGui.QComboBox):   # checks to see if cell contains spin box widget
                    a = self.__widget.cellWidget(rowNum, colNum)
                    data[rowNum].append(a.currentText())
                else:
                    try:
                        a = self.__widget.item(rowNum, colNum) # if cell isn't a dateEdit Widget extract cell item
                        data[rowNum].append(float(a.text())) # convert to float and append to relevant listOfEmployees
                    except ValueError:
                        a = self.__widget.item(rowNum, colNum)  # if cell doesn't convert to float
                        data[rowNum].append(a.text())  # write as text

        return data

    def selectRow(self, p_int):
        self.__widget.selectRow(p_int)

    def findIDforItems(self, search_string, ID_col):
        a = self.__widget.findItems(search_string, QtCore.Qt.MatchExactly)
        return self.__widget.item(a[0].row(), ID_col).text()

class dateEdit(QtGui.QDateEdit):
    def __init__(self, parent=None):
        super(dateEdit, self).__init__(parent)

class comboBox(QtGui.QComboBox):
    def __init__(self, parent=None):
        super(comboBox, self).__init__(parent)

class comboBoxTools(QtGui.QComboBox):
    def __init__(self, widget):
        super(comboBoxTools, self).__init__()
        self.__widget = widget

    def populateComboBoxList(self, data, dataColIndex):
        list = self.__widget
        for a in range(len(data)):
            list.addItem(data[a][dataColIndex])

    def setComboToSearchedItem(self, item):
        index = self.__widget.findText(item)
        self.__widget.setCurrentIndex(index)


