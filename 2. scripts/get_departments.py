# 2017.08.08
#
# Get Office/Departments list
#

import sqlite3

file_url = '..\\0. raw_data\\'
db_name = 'tpe_faq.db'
db_offices = {}

# Create table
conn = sqlite3.connect(file_url + db_name)
c = conn.cursor()

sql_cmd = 'SELECT DeptName, COUNT(DeptName) FROM faqs GROUP BY DeptName ORDER BY COUNT(DeptName) DESC'
c.execute(sql_cmd)


db_dept = 'tpe_departments.csv'
db_f = open(file_url + db_dept, 'w', encoding ='UTF-8')
db_f.write('Department, Counts' + '\n\r')
for row in c.fetchall() :
    d_item = list(row)
    db_f.write(d_item[0] + ', ' + str(d_item[1]) + '\n\r')

db_f.close()
conn.commit()
conn.close()