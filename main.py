import requests
import redis
import json
import re
import random
import time
import os
from bs4 import BeautifulSoup

    
url = 'https://mp.weixin.qq.com'
header = {
    "HOST": "mp.weixin.qq.com",
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:53.0) Gecko/20100101 Firefox/53.0"
    }
with open("app_msg_list.csv", "w",encoding='utf-8') as file:
    file.write("文章标识符aid,标题title,链接url,时间time\n")
i = 0

with open('cookie.txt', 'r', encoding='utf-8') as f:
    cookie = f.read()
cookies = json.loads(cookie)
def gettoken():
    response = requests.get(url=url, cookies=cookies)
    token = re.findall(r'token=(\d+)', str(response.url))[0]
    return token


def searchforfakeid(accountName):
        query_id = {
            'action': 'search_biz',
            'token': gettoken(),
            'lang': 'zh_CN',
            'f': 'json',
            'ajax': '1',
            'random': random.random(),
            'query': accountName,
            'begin': '0',
            'count': '5',
        }
        search_url = 'https://mp.weixin.qq.com/cgi-bin/searchbiz?'
        search_response = requests.get(search_url, cookies=cookies, headers=header, params=query_id)
        lists = search_response.json().get('list')[0]
        fakeid = lists.get('fakeid')
        if fakeid!='':
            print('找到公众号'+fakeid)
        return fakeid

# 微信公众号的名称就是id，所以此处只返回id
def getpassage(accountName,page):
    query_id_data = {
        'token': gettoken(),
        'lang': 'zh_CN',
        'f': 'json',
        'ajax': '1',
        'random': random.random(),
        'action': 'list_ex',
        'begin': '0',
        'count': '5',
        'query': '',
        'fakeid': searchforfakeid(accountName),
        'type': '9'
    }
    appmsg_url = 'https://mp.weixin.qq.com/cgi-bin/appmsg?'
    appmsg_response = requests.get(appmsg_url, cookies=cookies, headers=header, params=query_id_data)
    max_num = appmsg_response.json().get('app_msg_cnt')
    num = int(int(max_num) / 5)
    if page > num:
        print('页数超出最大值')
        return -1
    query_id_data = {
        'token': gettoken(),
        'lang': 'zh_CN',
        'f': 'json',
        'ajax': '1',
        'random': random.random(),
        'action': 'list_ex',
        'begin': '{}'.format(str(page*5)),
        'count': '5',
        'query': '',
        'fakeid': searchforfakeid(accountName),
        'type': '9'
    }
    print('翻页###################', page)
    query_fakeid_response = requests.get(appmsg_url, cookies=cookies, headers=header, params=query_id_data)
    fakeid_list = query_fakeid_response.json().get('app_msg_list')
    datalist=[]
    for item in fakeid_list:
        print(item.get('link'))
        aid = item['aid']
        title = item['title']
        url = item['link']
        create_time = item['create_time']

        datas={'aid':aid,'title':title,"url":url,"create_time":create_time}
        datalist.append(datas)
        #info = '"{}","{}","{}","{}"'.format(str(item["aid"]), item['title'], item['link'], str(item['create_time']))

    with open(str(accountName) + '_' + str(page) + '.json', 'w', encoding='utf-8') as f:
        json.dump(datalist, f, indent=2, sort_keys=True, ensure_ascii=False)
    time.sleep(2)
    return f
#文章爬取，页数从0开始
'''
def articlespider(accountName):
    query_id_data = {
        'token': gettoken(),
        'lang': 'zh_CN',
        'f': 'json',
        'ajax': '1',
        'random': random.random(),
        'action': 'list_ex',
        'begin': '0',
        'count': '5',
        'query': '',
        'fakeid': searchforfakeid(accountName),
        'type': '9'
    }
    appmsg_url = 'https://mp.weixin.qq.com/cgi-bin/appmsg?'
    appmsg_response = requests.get(appmsg_url, cookies=cookies, headers=header, params=query_id_data)
    max_num = appmsg_response.json().get('app_msg_cnt')
    num = int(int(max_num) / 5)
    begin = 0
    while num + 1 > 0 :
        query_id_data = {
            'token': gettoken(),
            'lang': 'zh_CN',
            'f': 'json',
            'ajax': '1',
            'random': random.random(),
            'action': 'list_ex',
            'begin': '{}'.format(str(begin)),
            'count': '5',
            'query': '',
            'fakeid': searchforfakeid(accountName),
            'type': '9'
        }
        print('翻页###################',begin)
        query_fakeid_response = requests.get(appmsg_url, cookies=cookies, headers=header, params=query_id_data)
        fakeid_list = query_fakeid_response.json().get('app_msg_list')
        for item in fakeid_list:
            print(item.get('link'))
            info = '"{}","{}","{}","{}"'.format(str(item["aid"]), item['title'], item['link'], str(item['create_time']))
            with open("app_msg_list_"+str(accountName)+".csv", "a", encoding='utf-8') as f:
                f.write(info + '\n')

        num -= 1
        begin = int(begin)
        begin += 5
        time.sleep(2)
'''


#以上是一次性爬取所有文章的函数
def getcontent(url, accountname):
    i=0
    title=''
    id=''
    author=str(accountname)
    time=''
    content=''

    while 1:
       if not os.path.exists(str(accountname) + '_' + str(i) + '.json'):
            break
       with open(str(accountname)+'_'+str(i)+'.json','r',encoding='utf-8') as f:
            articlelist=json.load(f)

            for item in articlelist:
                if item['url']==url:
                    title=item['title']
                    id=item['aid']
                    time=item['create_time']
       i=i+1

    headers = {

        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:53.0) Gecko/20100101 Firefox/53.0"
    }
    r = requests.get(str(url),cookies=cookies,headers=headers)
    if r.status_code == 200:
        text = r.text
        soup = BeautifulSoup(text)
        content += soup.find("meta")['content']
        content += soup.get_text(strip=True)
        print(content)
    with open(str(id)+'.json','w',encoding='utf-8') as f:
        articledata={'title':title,'author':author,'time':time,'id':id,'content':content}
        json.dump(articledata, f, indent=2, sort_keys=True, ensure_ascii=False)
        return f

'''
def requestarticle(accountName):
    headers = {

        "User-Agent":  "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:53.0) Gecko/20100101 Firefox/53.0"
    }
    with open("app_msg_list_"+str(accountName)+".csv", "r", encoding="utf-8") as f:
        data = f.readlines()
    n = len(data)
    for i in range(n):
        mes = data[i].strip("\n").split(",")
        if len(mes) != 4:
            continue
        title, url = mes[1:3]
        if i > 0:
            r = requests.get(eval(url), cookies=cookies,headers=headers)
            if r.status_code == 200:
                text = r.text
                soup = BeautifulSoup(text)
                print(soup.get_text(strip=True))
'''




