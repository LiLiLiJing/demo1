#encoding=utf-8
import pymysql
import sys
import collections


reload(sys)
sys.setdefaultencoding('utf-8')

def find_relation():

    db = pymysql.connect("172.18.77.15","root","weiguang123" ,database="knowgraph")
    cursor = db.cursor()

    query = 'SELECT * FROM aircraft_warship;'
    cursor.execute(query)
    all_ = cursor.fetchall()
    for data in all_:
        #query = 'SELECT * FROM know_graph WHERE Entity ="' + lookup +'";'
        #cursor.execute(query)
        #data = cursor.fetchone() 
        entity = data[0]
        value = data[2]
        value = value.split(";;")
        d = dict()
       
        try: 
            for v in value:
                if len(v)!=0:
                    query = 'SELECT * FROM aircraft_warship WHERE Value like "%' + v +'%";'
                    cursor.execute(query)
                    temp = cursor.fetchall()
                    for t in temp:
                        if len(t[0]) != 0:
                	    if t[0] not in d:
                    	        d[t[0]] = 1
                	    else:
                	        d[t[0]] +=1
       
            output = sorted(d.iteritems(), key=lambda d:d[1], reverse = True)
            result = ""
            for e in output[1:16]:
                if len(e[0])!=0:
            	    result += e[0]
		    result += ":"
		    result += "../static/img/" + e[0] + ".jpg"
            	    result += ";;"

            query = 'UPDATE aircraft_warship SET Rel = "' + str(result) + '" where Entity = "' + entity + '";' 
            cursor.execute(query)
        except:
	    pass

    db.commit()
    db.close()
    return 

find_relation()
