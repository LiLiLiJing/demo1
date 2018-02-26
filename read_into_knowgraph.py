import pymysql
import json
import io
import sys
 
reload(sys)
sys.setdefaultencoding('utf-8')

def read_json(filename):
    f = io.open(filename, encoding='utf-8')
    data = json.load(f)
    files = data['files']
    value = data['value']
    images = []
    for i in range(len(data['images'])):
        images.append(data['images'][i]['path'])
    rel = data['rel']
    links = data['links']

    num = ""
    for c in filename:
        if c.isdigit():
            num+=c
    entity = ""
    if num == "11":
        entity = str(files[0]['content'][0:2])
        entity += str(files[0]['content'][3:6])
    elif num == "22":
        entity = str(files[0]['content'][0:4])
        entity += str(files[0]['content'][5])
    elif num == "33":
        entity = str(files[0]['content'][0:3])
        entity += str(files[1]['content'][13:18])

    files_con = ""
    for j in range(len(files)):
        files_con += str(files[j]['content'])
        files_con += ';;'
    
    value_con = ""
    for k in range(len(value)):
        value_con += str(value[k]['content'])
        value_con += ';;'

    images_con = ""
    for m in range(len(images)):
        images_con += str(images[m])
        images_con += ';;'

    rel_con = ""
    for n in range(len(rel)):
        rel_con += str(rel[n]['name'])
        rel_con += ':'
        rel_con += str(rel[n]['path'])
        rel_con += ';;'

    links_con = ""
    for n in range(len(links)):
        links_con += str(links[n]['source'])
        links_con += ':'
        links_con += str(links[n]['target'])
        links_con += ':'
        links_con += str(links[n]['type'])
        links_con += ':'
        links_con += str(links[n]['rela'])
        links_con += ';;'

    return (entity, files_con, value_con, images_con, rel_con, links_con)
    

fname = input("Please enter the file path: :")
#fname = "static/data4.json"
#read_json(fname)
col1, col2, col3, col4, col5, col6 = read_json(fname)
db = pymysql.connect("172.18.77.15","root","weiguang123" ,database="knowgraph")
cursor = db.cursor()
query = "insert into know_graph values('" + col1 + "','"+ col2 + "','" + col3 + "','" + col4 + "','" + col5 + "','" + col6 +"')"
cursor.execute(query)
db.commit()
db.close()


