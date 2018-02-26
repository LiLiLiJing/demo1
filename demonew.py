# Sample.py
# -*- coding: utf-8 -*-
#encoding=utf-8
import sys
import os
import json
import webbrowser
import random
import string
import mysql.connector
import time
import shutil
import recover_json
import search
from flask import Flask, render_template, url_for, request, redirect, send_file, jsonify



def questoknowg(a):
    reload(sys)
    sys.setdefaultencoding('utf8')
    conn = mysql.connector.connect(user='root', password="123456", host="localhost", port=3306, database='ontodb',
                                   charset="utf8")  # 连接数据库
    # print '连接成功'
    curs = conn.cursor()
    srtcount = curs.execute("select *from  knowgraph where(实例1=\"%s\" or 实例2=\"%s\")" % (a, a))
    sresult = curs.fetchall()
    # for sretmp in sresult:
    # print str(sretmp).decode('unicode-escape')
    conn.commit()
    curs.close()
    conn.close()
    return sresult


def wresult(selresult,file_name):
    noredata = []
    for sretmp in selresult:
        noredata.append(sretmp[1])
        noredata.append(sretmp[2])
    noredata = list(set(noredata))
    # for sretmp1 in noredata:
    # print sretmp1
    logopath = "images/s.png"
    listsdict = []
    listsdict1 = []
    for sretmp1 in noredata:
        dictmp = {}
        dictmp["name"] = sretmp1
        dictmp["logo"] = logopath
        listsdict.append(dictmp)
    # for sretmp11 in listsdict:
    # print listsdict
    for sretmp11 in selresult:
        dictmp1 = {}
        dictmp1["source"] = sretmp11[1]
        dictmp1["target"] = sretmp11[2]
        dictmp1["relation"] = sretmp11[3]
        listsdict1.append(dictmp1)
    # print listsdict1
    dicnode = {}
    dicnode["nodes"] = listsdict
    dicnode["links"] = listsdict1
    # print dicnode
    #file_name = 'static/js/data/data123.json'  # 通过扩展名指纹文件存储的数据为json格式
    with open(file_name, 'w') as file_object:
        json.dump(dicnode, file_object, ensure_ascii=False, indent=4)


app = Flask(__name__)

@app.route('/')
def login():
    return render_template('index.html')


@app.route('/result', methods=['POST'])
def redirect_to_new_url():
    content = request.form['content']
    return redirect(url_for('result', content = content))

@app.route('/result2')
def aaa():
    return render_template('images.html')

@app.route('/result2?<page>', methods=['GET','POST'])
def img(page):
    return render_template('images.html')


@app.route('/result1?<fileName>', methods=['GET'])
def qqq(fileName):
    print  fileName
    return redirect(url_for('result', content=fileName))

@app.route('/result/<content>/search', methods =['POST','GET'])
def sss(content):
    result = search.search(str(content))
    return result

@app.route('/result/<content>/temp', methods = ['POST','GET'])
def js(content):
    data = recover_json.find(str(content)) 
    json_data = recover_json.recover_json(str(content), data)
    return json_data

@app.route('/result/<content>', methods = ['POST', 'GET'])
def result(content):
    #shutil.rmtree('static/js/data')
    #os.mkdir('static/js/data')
    #selresult=questoknowg(content)
    #file_name = 'static/js/data/%s.json'% ''.join(random.sample(string.ascii_letters + string.digits, 16))
    #wresult(selresult,file_name)
    path1 = "../result/" + content + "/temp"
    return render_template("detail1.html", path = path1)



if __name__ == '__main__':
    app.run("0.0.0.0",50001)
    app.debug = True

