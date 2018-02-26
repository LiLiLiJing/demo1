#encoding=utf-8
import pymysql
import json
import sys
 
reload(sys)
sys.setdefaultencoding('utf-8')

#kw = "卡尔文森号"
#num = input("Please enter the number of depth: ")

def find(kw):
    db = pymysql.connect("172.18.77.15","root","weiguang123" ,database="knowgraph")
    cursor = db.cursor()
    query = 'SELECT * FROM links WHERE Target ="' + kw + ' "OR Source = "' + kw + '";'
    cursor.execute(query)
    result = cursor.fetchall() 
 
    return result

def find_rela(kw, num):  
    output = []
    whole = list() #searched
    part = list() #waiting for searching
    whole.append(kw)
    part.append(kw)
    i = 1
    while i <= num:
    	temp = list()
    	for word in part:
       	    new_r = find(word)
            output.append(new_r)
            for ele in new_r:
                if ele[1] not in whole:
                    whole.append(ele[1])
                    temp.append(ele[1])
                if ele[2] not in whole:
                    whole.append(ele[2])
                    temp.append(ele[2])
        part = temp
        if len(part) == 0:
           i = num
        i += 1
    final = []
    for tup in output:
    	for sub_tup in tup:
    	    if sub_tup not in final:
    		final.append(sub_tup)
    
    final_str = ""
    for el in final:
	final_str += el[1] + ":" + el[2] + ":" + el[3] + ":" + el[4] + ";;"
 #   print json.dumps(final_str, encoding='UTF-8', ensure_ascii=False)
    return json.dumps(final_str, encoding='UTF-8', ensure_ascii=False)		
#find_rela(kw, num)

def build_rel_info(kw, num):
    db = pymysql.connect("172.18.77.15","root","weiguang123" ,database="knowgraph")
    cursor = db.cursor()
    
    whole = list() #searched
    part = list() #waiting for searching
    whole.append(kw)
    part.append(kw)
    i = 1
    while i <= num:
    	temp = list()
    	for word in part:
       	    new_r = find(word)
            for ele in new_r:
                if ele[1] not in whole:
                    whole.append(ele[1])
                    temp.append(ele[1])
                if ele[2] not in whole:
                    whole.append(ele[2])
                    temp.append(ele[2])
        part = temp
        if len(part) == 0:
           i = num
        i += 1

    rel_info = []
    for name in whole:
    	query = 'SELECT * FROM aircraft_warship WHERE Entity ="' + name + '";'
    	try: 
	    cursor.execute(query)
    	    a_dic = dict()
    	    a_dic['name'] = name
    	    a_dic['info'] = cursor.fetchone()[2]
            rel_info.append(a_dic)
        except:
	    pass
    #print(rel_info)

    return rel_info
#build_rel_info(kw, num)


