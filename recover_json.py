#encoding=utf-8
import pymysql
import json
import sys
import form_links;
 
reload(sys)
sys.setdefaultencoding('utf-8')


def find(lookup):
    db = pymysql.connect("172.18.77.15","root","weiguang123" ,database="knowgraph")
    cursor = db.cursor()
    #lookup = input("Please enter the entity that you are looking for: ")
    query = 'SELECT * FROM aircraft_warship WHERE Entity ="' + lookup +'";'
    cursor.execute(query)
    return cursor.fetchall() 


#lookup = "卡尔文森号"
#data = find(lookup)

def recover_json(lookup, data):
    if len(data)==0:
    	return ('Sorry, there is no result found in our database.')    

    files = data[0][1]
    value = data[0][2]
    images = data[0][3]
    rel = data[0][4]
    #num = input("Please enter the number of depth: ")
    num = 100    

    links = form_links.find_rela(lookup, num)
    rel_info = form_links.build_rel_info(lookup, num)
        
    j_dict = dict()

    files_list = []
    files = files.split(";;")
    for j in range(len(files)-1):
        d1 = dict()
        d1['content'] = files[j]
        files_list.append(d1)
        
    value_list = []
    value = value.split(";;")
    for k in range(len(value)-1):
        d2 = dict()
        d2['content'] = value[k]

        value_list.append(d2)

    images_list = []
    images = images.split(";;")
    for l in range(len(images)-1):
        d3 = dict()
        d3['path'] = images[l]
        images[l] = images[l].split('/')
        d3['name'] = images[l][-1]
        images_list.append(d3)   

    rel_list = []
    rel = rel.split(";;")
    for m in range(len(rel)-1):
        rel[m] = rel[m].split(":")
        d4 = dict()
        d4['name'] = rel[m][0]
        d4['path'] = rel[m][1]
        #d4['name'] = rel[m]
	#d4['path'] = '../static/img/' + rel[m] + '.jpg'
	rel_list.append(d4)
    

    links_list = []
    links = links.split(";;")
    for n in range(len(links)-1):
	links[n] = links[n].split(":")    
	d5 = dict()
        d5['source'] = links[n][0]
        d5['target'] = links[n][1]
        d5['type'] = links[n][3]
        d5['rela'] = links[n][2]
        links_list.append(d5)
 

    j_dict['files'] = files_list
    j_dict['value'] = value_list
    j_dict['images'] = images_list
    j_dict['rel'] = rel_list
    j_dict['links'] = links_list
    j_dict['rel_info'] = rel_info
            
    js = json.dumps(j_dict , ensure_ascii=False)
    
#    print(js)
    return js

#recover_json(lookup, data)

