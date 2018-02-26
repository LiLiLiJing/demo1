#encoding=utf-8
import pymysql
import sys

reload(sys)
sys.setdefaultencoding('utf8')

def build_data():
    db = pymysql.connect("172.18.77.15","root","weiguang123" ,database="knowgraph")
    cursor = db.cursor()
    query = "SELECT DISTINCT Target from links;"
    #query = query.encode('utf-8')
    cursor.execute(query)
    all_list = []
    all_list = list(cursor.fetchall())
    #print(all_list)
    query = "SELECT DISTINCT Source from links;"
    #query = query.encode('utf-8')
    cursor.execute(query)
    for e in cursor.fetchall():
	if e not in all_list:
            all_list.append(e)
    for element in all_list:
	try: 
	    query = "insert into know_graph values('" + str(element[0]).encode('utf-8') + "', 'This;;is;;in;;files;;', 'This;;is;;value;;', '../static/img/17.png;;..static/img/18/png;;', 'a: ../static/img/111.png;;', 'F18:F14:resolved:lalala;;');"
	    query = query.encode('utf-8')
	    cursor.execute(query)
	except:
	    pass    


    
    db.commit()
    db.close()

build_data()

