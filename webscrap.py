#encoding=utf-8
import requests
from bs4 import BeautifulSoup
import sys
import time

reload(sys)
sys.setdefaultencoding('utf-8')

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36', "Host": "weapon.huanqiu.com", "Connection": "keep-alive", "Accept-Ecoding": "gzip, deflate", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8"}
session = requests.Session()
session.keep_alive = False

def web_scrap (url):
    url1 = "http://weapon.huanqiu.com" + url
    #response = requests.get(url1, headers=headers)
    response = session.get(url1, headers = headers)    
    if response.status_code == 200:
        results_page = BeautifulSoup(response.content, 'lxml')
        #get image
        try:
            img = results_page.find('div', class_='maxPic')
            img_link = img.find('img').get('src')
            name = img.find('span', class_ = 'name').get_text()
        except:
            try:
                img = results_page.find('div', class_='dataInfo')
                img_link = img.find('img').get('src')
                name = img.find('li').get_text()[3:]
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
        
        return (name, img_link, description, information, data_list)

    else:
        return ("Fail")



def find_urls(categ, page):
    url_list = []
    i=0
    while True:
        i+=1
        categ_url = "http://weapon.huanqiu.com/weaponlist/" + categ + "/list_0_0_0_0_" + str(i)
        #response = requests.get(categ_url, headers=headers)
        response = session.get(cat_url, headers=headers)
        if response.status_code == 200:
            results_page = BeautifulSoup(response.content, 'lxml')
            links = results_page.find_all('span',class_='pic')
            for l in links:       
                url_list.append(l.find('a').get('href'))
        if i == page-20:
            break
    return url_list


def urls_in_categ(home):
    if home == "飞行器":
        categ = 'aircraft'
        num = 1330
        page = 111
    elif home == "舰船舰艇":
        categ = 'warship'
        num = 1192
        page = 100
    elif home == "枪械与单兵":
        categ = 'guns'
        num = 966
        page = 81
    elif home == "坦克装甲车辆":
        categ = 'tank'
        num = 547
        page = 46
    elif home == "火炮":
        categ = 'artillery'
        num = 540
        page = 45
    elif home == "导弹武器":
        categ = 'missile'
        num = 458
        page = 39
    elif home == "太空装备":
        categ = 'spaceship'
        num = 366
        page = 31
    elif home == "爆炸物":
        categ = 'explosive'
        num = 459
        page = 39
    else:
        print("sorry, keyword not found")
    
    new_list = []
    while True:
        lis = find_urls(categ, page)
        for l in lis:
            if l not in new_list:
                new_list.append(l)
        if len(new_list) == num:
            break
    return new_list

def main():
    #home = input("Please enter a key word: ")
    #home = "飞行器"
    output = []
    #result = urls_in_categ(home)
    file_obj = open('aircraft.txt')
    try:
        result = file_obj.read()
    finally:
        file_obj.close()
    result = result.split("@@")
    
    for element in result[:len(result)-1]:
        tup = web_scrap(element)
        output.append(tup)
    return output

