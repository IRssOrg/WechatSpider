import requests
from fastapi import FastAPI
import json
import re
import random
import time
import os
from bs4 import BeautifulSoup

wechatCreeper = FastAPI()
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


@wechatCreeper.get('/api/search/author/{username}')
def searchforfakeid(username):
        query_id = {
            'action': 'search_biz',
            'token': gettoken(),
            'lang': 'zh_CN',
            'f': 'json',
            'ajax': '1',
            'random': random.random(),
            'query': username,
            'begin': '0',
            'count': '5',
        }
        search_url = 'https://mp.weixin.qq.com/cgi-bin/searchbiz?'
        search_response = requests.get(search_url, cookies=cookies, headers=header, params=query_id)
        lists = search_response.json().get('list')[0]
        fakeid = lists.get('fakeid')
        if fakeid!='':
            print('找到公众号'+fakeid)
        return{'username': username,'id':fakeid}



@wechatCreeper.get('/api/passages/{username}/{page}')
def getpassage(username,page):
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
        'fakeid': searchforfakeid(username).get('id'),
        'type': '9'
    }
    appmsg_url = 'https://mp.weixin.qq.com/cgi-bin/appmsg?'
    appmsg_response = requests.get(appmsg_url, cookies=cookies, headers=header, params=query_id_data)
    print(appmsg_response.json())
    max_num = appmsg_response.json().get('app_msg_cnt')
    num = int(int(max_num) / 5)
    if int(page) > num:
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
        'fakeid': searchforfakeid(username).get('id'),
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

        datas={'id': username+'/' + aid, 'title': title, "url":url,"time":create_time,"time_stamp":create_time}
        datalist.append(datas)
        #info = '"{}","{}","{}","{}"'.format(str(item["aid"]), item['title'], item['link'], str(item['create_time']))

    with open(str(username) + '_' + str(page) + '.json', 'w', encoding='utf-8') as f:
        json.dump(datalist, f, indent=2, sort_keys=True, ensure_ascii=False)
    return {'ret': datalist}

#文章爬取，页数从0开始


@wechatCreeper.get('/api/passage/{username}/{id}')
#以上是一次性爬取所有文章的函数
def getcontent(id, username):
    i=0
    title=''
    id=''
    author=str(username)
    time=''
    content=''
    url=''

    while 1:
       if not os.path.exists(str(username) + '_' + str(i) + '.json'):
            break
       with open(str(username)+'_'+str(i)+'.json','r',encoding='utf-8') as f:
            articlelist=json.load(f)

            for item in articlelist:
                if item['id']==item['id']:
                    title=item['title']
                    url=item['url']
                    time=item['time']
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

    return {'ret': articledata}



