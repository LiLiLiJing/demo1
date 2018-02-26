
# coding: utf-8

# In[18]:

import requests
from bs4 import BeautifulSoup

f = open('/Users/fengsiqi/Desktop/warship.txt', 'w')
def find_urls(categ, page):
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36', "Host": "weapon.huanqiu.com", "Connection": "keep-alive", "Accept-Ecoding": "gzip, deflate", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8"}
    url_list = []
    i=0
    while True:
        i+=1
        categ_url = "http://weapon.huanqiu.com/weaponlist/" + categ + "/list_0_0_0_0_" + str(i)
        response = requests.get(categ_url, headers=headers)
        if response.status_code == 200:
            results_page = BeautifulSoup(response.content, 'lxml')
            links = results_page.find_all('span',class_='pic')
            for l in links:
                url_list.append(l.find('a').get('href'))
        if i == page:
            break
    return url_list

def main():
    categ = "warship"
    page = 100
    new_list = []
    while True:
        lis = find_urls(categ, page)
        for l in lis:
            if l not in new_list:
                new_list.append(l)
        if len(new_list) == 1192:
            break
    print(len(new_list))
    result = ""
    for i in new_list:
        result += i
        result += '@@'
        
    f.write(result)
    f.close()
    return 

main()




# In[28]:


import requests
from bs4 import BeautifulSoup
import sys
import time
import pymysql
import re


headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36', "Host": "weapon.huanqiu.com", "Connection": "keep-alive", "Accept-Ecoding": "gzip, deflate", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8"}



def web_scrap (url):
    url1 = "http://weapon.huanqiu.com" + url
    response = requests.get(url1, headers=headers)
        
    if response.status_code == 200:
        results_page = BeautifulSoup(response.content, 'lxml')
        
        #get image
        try:
            img = results_page.find('div', class_='maxPic')
            img_link = img.find('img').get('src')
            name = img.find('span', class_ = 'name').get_text()
            name = re.sub("[\s+\.\!\/_,$%^*(+\"\']+|[+——！，。？、~@#￥%……&*（）]+", "",name)
            

        except:
            try:
                img = results_page.find('div', class_='dataInfo')
                img_link = img.find('img').get('src')
                name = img.find('li').get_text()[3:]
                name = re.sub("[\s+\.\!\/_,$%^*(）（+\"\']+|[+——！，。？、~@#￥%……&*（）]+", "",name)
                

            except:
                img_link = ""
                name = ""

        #get description
        try:
            des = results_page.find('div', class_='intron').find_all('p')
            description = []
            for p in des:
                description.append(p.get_text())
            if description == []:
                para = des.find_all('div')
                for p in para:
                    description.append(p.get_text())
        except:
            description = []

        #get information
        try:
            info = results_page.find('div', class_='info')
            titles = info.find_all('h3', class_ = 'title_')
            title_list = []
            for t in titles:
                title_list.append(t.get_text())
            cont_list = []
            contents = info.find_all('div', class_='textInfo')
            for element in contents:
                cont_list.append(element.get_text())
           
            information = list() 
            for i in range(len(title_list)):
                information.append(title_list[i])
                information.append(cont_list[i])
        except:
            information = []
        
        
        #get data info on the side
        try:
            datainfo = results_page.find('div', class_='dataInfo').find_all('li')
            data_list = []
            for el in datainfo:
                data_list.append(el.get_text())
        except:
            data_list = []
        
        if len(name) <= 8:
            return (name, img_link, description, information, data_list)
        else:
            return ""

    else:
        return ("Fail")



def main():
    file_obj = open("warship.txt", 'r')
    output = []
    try:
        result = file_obj.read()
    finally:
        file_obj.close()
    result = result.split("@@")
    
    for element in result[:len(result)-1]:
        tup = web_scrap(element)
        output.append(tup)
    return output


def data_to_mysql():
    db = pymysql.connect("172.18.77.15","root","weiguang123" ,database="knowgraph")
    cursor = db.cursor()
    l = main()
    valid = []
    for elm in l:
        if type(elm)==tuple:
            valid.append(elm)
    for tup in valid:  
        try:
            pic= requests.get(tup[1])
            #string = 'static/img/'+ tup[0] + '.jpg'
            string = 'img_folder/' + tup[0]+'.jpg'

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
        try:
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
        except:
            pass
        
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
        try:
            cursor.execute(query)
        except:
            print("wrong")
    db.commit()
    db.close()
    
    return
        
data_to_mysql()       





