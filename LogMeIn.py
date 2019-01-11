from bcrypt import hashpw, gensalt
import MySQLdb


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

