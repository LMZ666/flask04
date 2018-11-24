# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import re
import json
import pymysql

# url = "http://www.gx8899.com/weimei/"
# 此处的末尾要加两个反斜杠！！！！！！！！，代表了一个反斜杠
# path = r"C:\Users\舍喔齐誰\Desktop\download\\"
path = r"F:\QianFengStudy\2Third\flask\flask04\app\static\img\goods\\"
def get_html(url):
    headers= {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}
    try:
        r = requests.get(url,headers=headers)
        r.encoding = r.apparent_encoding
        r.raise_for_status()
        print("连接成功！！！！！！！！！！")
        return r.text
    except BaseException as e:
        print("请求错误！！")
        print(e)
        return

def get_url_list(url,list1):
    num = 0
    html = get_html(url)
    pattern = re.compile(r"(?<=_)\d+(?=\.)")
    soup = BeautifulSoup(html,"html.parser")
    a_list = soup("a")
    for a in a_list:
        if re.search("末页",str(a)):
            num = int(re.findall(pattern,str(a))[0])
    for i in range(2,num+1):
        newurl = url+"index_"+str(i)+".html"
        list1.append(newurl)
        print(newurl)
    # print(a)
def download_img(url,db):
    # for url in url_list:
    html = get_html(url)
    soup = BeautifulSoup(html, "html.parser")
    # count = 80
    count = 320
    type = "女装"
    for div in soup("div",id="thelist"):
        div1 = div("div",attrs={"class":"sp_1"})
        for div2 in div1:
            img = "img/goods/"+str(count)+".jpg"
            name = div2('span',attrs={"class":"nr"})[0]("a")[0].string
            org_price = div2("span",attrs={"class":"price_new_c"})[0].string
            price = div2("span",attrs={"class":"price_new_a"})[0].string
            buy_num = div2("span",attrs={"class":"price_new_b"})[1].string
            quan = div2("a",attrs={"class":"f_coupont"})[0]("span")[0].string
            tag_img = div2("img",attrs={"class":"main_icon"})[0]
            if re.search("http",name):
                name="女士秋冬韩版修身羽绒服"

            result = (img,name,org_price,price,buy_num,quan,type)
            # reviewdata_insert(db, result)


            name = str(count)+".jpg"
            count += 1
            img = requests.get("http:"+tag_img['src'])
            with open(path+name,"wb") as fp:
                fp.write(img.content)



# 读取review数据，并写入数据库
# 导入数据库成功，总共4736897条记录
def prem(db):
    cursor = db.cursor()
    cursor.execute("SELECT VERSION()")
    data = cursor.fetchone()
    print("Database version : %s " % data)  # 结果表明已经连接成功



def reviewdata_insert(db,result):
    print(len(result))
    inesrt_re = "insert into goods (img,name,org_price,price,buy_num,quan,type) values (%s,%s,%s,%s,%s,%s,%s)"
    cursor = db.cursor()
    cursor.execute(inesrt_re, result)
    db.commit()


if __name__ == "__main__":  # 起到一个初始化或者调用函数的作用
    db = pymysql.connect("localhost", "root", "1234", "flask04", charset='utf8')
    cursor = db.cursor()
    prem(db)
    # http://lingquvip.com/index.php?r=y&cid=2
    # http://lingquvip.com/index.php?r=y&cid=2&page=2

    # http://lingquvip.com/index.php?r=y&cid=1
    #http://lingquvip.com/index.php?r=y&cid=1&page=2

    #http://lingquvip.com/index.php?r=y&cid=5
    download_img("http://lingquvip.com/index.php?r=y&cid=5",db)
    # reviewdata_insert(db)
    cursor.close()




# 有一次爬取数据出错，用来改名
# import os
# path = r"F:\QianFengStudy\2Third\flask\flask04\app\static\img\goods\\"
# flienames = os.listdir(path)
# count = 0
# for filename in flienames:
#     try:
#         os.renames(path+filename,path+str(count)+".jpg")
#     except:
#         pass
#     count+=1
