import json
import requests
import time
import random
import yaml
from selenium import webdriver
import re

AccountName=""
input(AccountName)
with open("wechat.yaml", "r") as file:
    file_data = file.read()
config = yaml.safe_load(file_data)

headers = {
    "Cookie": config['cookie'],
    "User-Agent": config['user_agent']
}
url = 'https://mp.weixin.qq.com'
url_Search = "https://mp.weixin.qq.com/cgi-bin/searchbiz?"
url_Article = "https://mp.weixin.qq.com/cgi-bin/appmsg"

def getToken():
    resp = requests.get(url, headers=headers)
    print(len(str(resp.url)))
    print(resp.url)
    token = re.findall(r'token=(\d+)', str(resp.url))[0]
    return token
def searchAccount(AccountName):
    paramsSearch = {
        'action': 'search_biz',
        'begin': '0',
        'count': '5',
        'query': AccountName,
        'token': getToken(),
        'lang': 'zh_CN',

        'f': 'json',
        'ajax': '1'
    }
    fakeid='null'
    search_resp = requests.get(url_Search, headers=headers, params=paramsSearch, verify=False)
    if (search_resp.json() == 0):
        print("未找到此公众号，请检查公众号名称是否正确")
    else: print("成功找到公众号")

    lists = search_resp.json()
    print(lists)
    if 'fakeid' in lists:
        fakeid = lists['fakeid']

    else:
        print('未找到公众号fakeid')
    return fakeid

def requestArticle(AccountName):
    begin = "0"
    params = {
        "action": "list_ex",
        "begin": begin,
        "count": "5",
        "fakeid": str(searchAccount(AccountName)),
        "type": "9",
        "token": config['token'],
        "lang": "zh_CN",
        "f": "json",
        "ajax": "1"
    }
    i=0
    while True:
        begin = i * 5
        params["begin"] = str(begin)
        # 随机暂停几秒，避免过快的请求导致过快的被查到
        time.sleep(random.randint(1, 10))
        resp = requests.get(url_Article, headers=headers, params=params, verify=False)
        # 微信流量控制, 退出
        if resp.json()['base_resp']['ret'] == 200013:
            print("frequencey control, stop at {}".format(str(begin)))
            time.sleep(3600)
            continue

        # 如果返回的内容中为空则结束
        if len(resp.json()['app_msg_list']) == 0:
            print("all ariticle parsed")
            break

        msg = resp.json()
        if "app_msg_list" in msg:
            for item in msg["app_msg_list"]:
                info = '"{}","{}","{}","{}"'.format(str(item["aid"]), item['title'], item['link'],
                                                    str(item['create_time']))
                with open("app_msg_list.csv", "a", encoding='utf-8') as f:
                    f.write(info + '\n')
            print(f"第{i}页爬取成功\n")
            print("\n".join(info.split(",")))
            print("\n\n---------------------------------------------------------------------------------\n")
        i += 1


requestArticle("武汉大学")


