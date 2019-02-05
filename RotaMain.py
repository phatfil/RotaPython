#!/usr/bin/python2.7

import sys
from PyQt4 import QtGui

# import pyximport; pyximport.install()
from GUIs import MainWindow

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)

    # just hack this out
    myapp = MainWindow()
    myapp.show()

    # resize rows for rota widget to include the shift type name
    myapp.ui.tableWidget.resizeRowsToContents()

    sys.exit(app.exec_())
    # to here, and un-comment bellow



    """login = LoginWindow()
    login.show()"""




    """if login.exec_() == QtGui.QDialog.Accepted:
        myapp = MainWindow()
        myapp.show()
        # resize rows for rota widget to include the shift type name
        myapp.ui.tableWidget.resizeRowsToContents()
        sys.exit(app.exec_())"""
