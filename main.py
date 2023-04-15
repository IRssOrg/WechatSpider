import requests
import redis
import json
import re
import random
import time
class passage:
    title=''
    id=''
    author=''
    time=''
    content=''
    
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
        return fakeid

def articlespider(accoutName):
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
        'fakeid': searchforfakeid(accoutName),
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
            'fakeid': searchforfakeid(accoutName),
            'type': '9'
        }
        print('翻页###################',begin)
        query_fakeid_response = requests.get(appmsg_url, cookies=cookies, headers=header, params=query_id_data)
        fakeid_list = query_fakeid_response.json().get('app_msg_list')
        for item in fakeid_list:
            print(item.get('link'))
            info = '"{}","{}","{}","{}"'.format(str(item["aid"]), item['title'], item['link'], str(item['create_time']))
            with open("app_msg_list.csv", "a", encoding='utf-8') as f:
                f.write(info + '\n')

        num -= 1
        begin = int(begin)
        begin+=5
        time.sleep(2)

articlespider('武汉大学')




