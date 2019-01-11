import MySQLdb
from PyQt4 import QtGui, QtSql


dataBaseType = "QMYSQL"
databaseName = 'mydb'
userName = "phil"
password = "g4ngst3r"
host = '127.0.0.1'

class Querydb():
    def __init__(self, sql, formatting):
        self.host = host
        self.username = userName
        self.password = password
        self.db = databaseName
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
            # print (cursor._last_executed)
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
            # print (cursor._last_executed)
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
            #print (cursor._last_executed)
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
            #print (cursor._last_executed)
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
            #print (cursor._last_executed)
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
            #print (cursor._last_executed)
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
            # print (cursor._last_executed)
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
            # print (cursor._last_executed)
            cursor.close()
        except(MySQLdb.Error, MySQLdb.Warning):
            QtGui.QMessageBox.warning(QtGui.QMessageBox(), 'Error', str(message))
            db.rollback()
            db.close()
            cursor.close()