#encoding=utf-8
import pymysql
from webscrap import main
import requests
import sys

reload(sys)
sys.setdefaultencoding('utf8')


def data_to_mysql():
    db = pymysql.connect("172.18.77.15","root","weiguang123" ,database="knowgraph")
    cursor = db.cursor()
    l = main()
    valid = []
    for elm in l:
        if type(elm) == tuple:
            valid.append(elm)
    for tup in valid:
        
        try:
            pic= requests.get(tup[1], timeout=30)
            string = 'static/img/'+ tup[0] + '.jpg'
            fp = open(string,'wb')
            fp.write(pic.content)
            fp.close()
        except:
            pass
        
        #image
        if tup[0]!="":
            image = '../static/img/'+ str(tup[0]) + '.jpg'
	    image += ";;"
        else:
            image = ""
        
        #files
        files =""
        if len(tup[2])!=0:
            for string in tup[2]:
                files += string
                files += ";;"
        if len(tup[3])!=0:
            for string_ in tup[3]:
                files += string_
                files += ";;"
        new_files = ""
        if files != "":
	    for let in files:
                if let =="'":
		    letter = "*"
	    	new_files += let
	        
        #value
        value = ""
        if len(tup[4])!=0:
            for s in tup[4]:
                value += s
                value += ";;"
	new_value = ""
        for letter in value:
            if letter == "'":
		letter = "*"
            new_value += letter

        query = "replace into aircraft_warship values('" + str(tup[0]) + "','"+ new_files + "','" + new_value + "','" + image + "','" + "NULL" + "','" + "NULL" +"');"
#        query = 'insert into know_graph values("' + str(tup[0]) + '","' + files + '","' + value + '","' + image + '","' + 'NULL' + '","' + 'NULL' + '");'
        query = query.encode('utf-8')
	cursor.execute(query)
    db.commit()
    db.close()
    return
        
data_to_mysql()       
        
        
    

