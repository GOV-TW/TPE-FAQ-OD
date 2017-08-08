# 2017.08.08
# json to sqlite
# FAQ file : 市政網站整合平台之常見問答V2_m.json
#   {
#    "Icuitem": "214224457",
#    "Title": "對國民年金被保險人所得未達一定標準資格核定公文有疑義，該怎麼辦?",
#    "Url": "http://www.gov.taipei/ct.asp?xItem=214224457&ctNode=72231&mp=100001",
#    "PostDate": "2017-08-08 00:00:00",
#    "TcgCateId": "805306999,805307031",
#    "LastModifyDate": "2017-08-08 12:31:00",
#    "LastModifyName": "system",
#    "DeptName": "臺北市政府社會局社會救助科",
#    "Content": "可於上班時間電話洽詢「戶籍所在地區公所」承辦人，對該核定公文如仍不服，請檢具申請書及相關證明文件重新提出申請，或自公文送達之次日起30日內，採行政救濟途徑。",
#    "FctuPublic": "Y",
#    "start_date": "2017-08-08 00:00:00",
#    "end_date": "2035-12-31 00:00:00",
#    "keyword": "國民年金,QA",
#    "file": null
#  },
# 
# TODO : url encoding ?
#

import json
import sqlite3 


file_url = '..\\0. raw_data\\'
file_name = '市政網站整合平台之常見問答V2_m.json'
db_name = 'tpe_faq.db'

# Create table
conn = sqlite3.connect(file_url + db_name)
c = conn.cursor()
sql_cmd = 'DROP TABLE faqs'
c.execute(sql_cmd)
sql_cmd = '''CREATE TABLE faqs 
           (Icuitem text, Title text, Url text, 
            PostDate date, TcgCateId text, LastModifyDate date,
            LastModifyName text, DeptName text, 
            Content text, 
            FctuPublic boolean,
            start_date date, end_date date, 
            keyword text, file text)
            
          '''
c.execute(sql_cmd)

file_json = json.load(open(file_url+file_name, encoding='utf-8'))
file_items = iter(file_json)

for i in range(len(file_json)):
    columns = list(next(file_items).values())
    # keywords -refactoring with ','
    if columns[12] != None :
        columns[12]= columns[12].replace(' ', ',')
        columns[12]= columns[12].replace('、', ',')
        columns[12]= columns[12].replace('，', ',')
        columns[12] = columns[12].replace(',,', ',')
        if columns[12].endswith(',') :
            columns[12] = columns[12][:-1]
        
    # attached files - change to tuples
    # columns[13] = file attachement
    if columns[13] != None :
        column = list(columns[13].values())
        columns[13] = ''
        
        # refactoring attachement list
        if type(column[0]) is list :
            column = list(column[0])
            
            for i in range(0, len(column)):
                columns[13] = columns[13] + '(\'' + column[i]['attributes']['descr'] + '\', \'' + column[i]['$value'].replace('tcwww', 'www') + '\')'
                if i != len(column) :
                    columns[13] = columns[13] + ', '
        else : 
            columns[13] =  '(\'' + str(column[0]['attributes']['descr']) + '\', \'' + column[0]['$value'].replace('tcwww', 'www') + '\')'

        columns[13] = str(columns[13])
        
    # change data to tuple and insert to DB
    columns = tuple(columns)        
    c.execute('INSERT INTO faqs VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?) ', columns)

conn.commit()
conn.close()