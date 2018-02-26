#eoncoding=utf-8

import pymysql

def search(content):
    db = pymysql.connect("172.18.77.15", "root", "weiguang123", database = "knowgraph")
    cursor = db.cursor()
    query = 'SELECT Entity FROM aircraft_warship WHERE Entity like "%' + content + '%";'
    cursor.execute(query)
    all_ = cursor.fetchall()
    result = ""
    for elem in all_:
        if len(elem)!=0:
	    result += elem[0]
	    result += "@"
    db.commit()
    db.close()
    return result

