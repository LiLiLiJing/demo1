import pymysql
import json
import io
import sys
 
reload(sys)
sys.setdefaultencoding('utf-8')

def read_json(filename):
    db = pymysql.connect("172.18.77.15","root","weiguang123" ,database="knowgraph")
    cursor = db.cursor()
    f = io.open(filename, encoding='utf-8')
    data = json.load(f)
    links = data['links']

    for n in range(len(links)):
        source = str(links[n]['source'])
        target = str(links[n]['target'])
        types = str(links[n]['type'])
        rela = str(links[n]['rela'])
        query = "insert into links (Source, Target, Rela, Type) values('"+source+"','"+target+"','"+rela+"','"+types+"');"
        cursor.execute(query)
    db.commit()
    db.close()

    return 
    

fname = input("Please enter the file path: :")
read_json(fname)


