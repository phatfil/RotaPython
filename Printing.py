from PyQt4 import QtCore, QtGui, QtWebKit
import WidgetTools
import subprocess
from jinja2 import Template


class Printer(QtGui.QTableWidget):
    def __init__(self, parent=None):
        super(Printer, self).__init__(parent)


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

