# 2017.08.08
#
# Get keywords 
# count and list
#

import sqlite3


file_url = '..\\0. raw_data\\'
db_name = 'tpe_faq.db'
db_keywords = {}

# Create table
conn = sqlite3.connect(file_url + db_name)
c = conn.cursor()

sql_cmd = 'SELECT keyword FROM faqs'
c.execute(sql_cmd)

for row in c.fetchall() :
    for k_items in list(row) :
        if k_items != None :
            for k_item in k_items.split(',') :
                if k_item in db_keywords.keys() :
                    db_keywords[k_item] = db_keywords[k_item] + 1
                else :
                    db_keywords[k_item] = 1


db_kw = 'tpe_keywords.csv'
db_f = open(file_url + db_kw, 'w', encoding ='UTF-8')
db_f.write('Keywords, Counts' + '\n\r')
for w in sorted(db_keywords, key=db_keywords.get, reverse=True):
    db_f.write(w + ', ' + str(db_keywords[w]) + '\n\r')

db_f.close()
conn.commit()
conn.close()