import datetime
import calendar
from dateutil.relativedelta import *
import Employees

startDate = datetime.date(2019,1,1)
endDate = datetime.date(2019,1,10)
d3 = "2019-10-14"
d4 = {1: [5, 1], 2: [10, 2]}

a = 0
for key , value in list(d4.items()):
    a += d4[key][0]
print (a)